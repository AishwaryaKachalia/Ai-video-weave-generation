#!/usr/bin/env python3
"""Replace garbled can labels in a generated frame with the real Layer Zero label art.

Detects can bodies by their navy colour + cream/gold lettering, warps the label from
products/layer-zero/can.png onto each one, matches the local lighting, and keeps
fingers/hands in front. Run on the RAW frame, then run film_post.py on the result.

Usage: python3 scripts/fix_cans.py in.png out.png [--debug debug.png]
"""
import argparse
import math

import cv2
import numpy as np

ART = "products/layer-zero/can.png"
# body region of the can art (below the lid shoulder, above the base rim)
ART_BODY = (4, 118, 476, 1222)  # x0, y0, x1, y1


def load_art():
    art = cv2.imread(ART, cv2.IMREAD_UNCHANGED)
    if art.shape[2] == 4:
        art = art[:, :, :3]
    x0, y0, x1, y1 = ART_BODY
    return art[y0:y1, x0:x1].copy()


def _evaluate(c, img_shape, cream, gold, min_area, debug=False):
    h, w = img_shape[:2]
    area = cv2.contourArea(c)
    if area < min_area:
        return None
    rect = cv2.minAreaRect(c)
    (cx, cy), (rw, rh), ang = rect
    long_, short_ = max(rw, rh), min(rw, rh)
    if short_ < 14 or not (1.35 <= long_ / short_ <= 3.6):
        return None
    if area / (rw * rh) < 0.5:
        return None
    box = cv2.boxPoints(rect)
    m = np.zeros((h, w), np.uint8)
    cv2.fillConvexPoly(m, box.astype(np.int32), 255)
    cream_frac = cv2.countNonZero(cv2.bitwise_and(cream, m)) / (rw * rh)
    gold_px = cv2.bitwise_and(gold, m)
    if cream_frac < 0.07 or cv2.countNonZero(gold_px) < 12:
        return None
    sil = np.zeros((h, w), np.uint8)
    cv2.drawContours(sil, [c], -1, 255, cv2.FILLED)
    return box, gold_px, sil


def detect_cans(img, debug=False):
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    navy = cv2.inRange(hsv, (98, 70, 30), (130, 255, 200))
    k = max(5, int(w * 0.004) | 1)
    navy = cv2.morphologyEx(navy, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (k, k)))
    navy = cv2.morphologyEx(navy, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    cnts, _ = cv2.findContours(navy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cream = cv2.inRange(hsv, (0, 0, 165), (40, 90, 255))
    gold = cv2.inRange(hsv, (12, 150, 130), (30, 255, 255))
    min_area = 0.00035 * w * h
    cans = []
    for c in cnts:
        if cv2.contourArea(c) < min_area:
            continue
        r = _evaluate(c, img.shape, cream, gold, min_area)
        if r:
            cans.append(r)
            continue
        # merged with neighbours? erode progressively to split, then grow back
        blob = np.zeros((h, w), np.uint8)
        cv2.drawContours(blob, [c], -1, 255, cv2.FILLED)
        for ks in (7, 11, 15, 21, 27):
            ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ks, ks))
            er = cv2.erode(blob, ker)
            sub, _ = cv2.findContours(er, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            found = []
            for sc in sub:
                grown = np.zeros((h, w), np.uint8)
                cv2.drawContours(grown, [sc], -1, 255, cv2.FILLED)
                grown = cv2.dilate(grown, ker)
                grown = cv2.bitwise_and(grown, blob)
                gc, _ = cv2.findContours(grown, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for g in gc:
                    rr = _evaluate(g, img.shape, cream, gold, min_area)
                    if rr:
                        found.append(rr)
            if found:
                cans.extend(found)
                break
        elif_debug = debug and not r
    return cans


def order_box(box, gold_px):
    """Return TL, TR, BR, BL so that 'top' is the lid end (gold mass sits at the bottom)."""
    c = box.mean(axis=0)
    d = [np.linalg.norm(box[(i + 1) % 4] - box[i]) for i in range(4)]
    # long edges are the two sides; find the long axis direction
    if d[0] + d[2] >= d[1] + d[3]:
        axis = box[1] - box[0]
    else:
        axis = box[2] - box[1]
    axis = axis / np.linalg.norm(axis)
    ys, xs = np.nonzero(gold_px)
    gold_c = np.array([xs.mean(), ys.mean()])
    if np.dot(gold_c - c, axis) < 0:
        axis = -axis  # axis now points from top (lid) to bottom (gold)
    perp = np.array([-axis[1], axis[0]])
    # project corners
    proj = [(np.dot(p - c, axis), np.dot(p - c, perp), p) for p in box]
    # image y points down: with axis pointing down, perp=(-ay, ax) points LEFT, so sort descending for left-first
    top = sorted([t for t in proj if t[0] < 0], key=lambda t: -t[1])
    bot = sorted([t for t in proj if t[0] >= 0], key=lambda t: -t[1])
    tl, tr = top[0][2], top[1][2]
    bl, br = bot[0][2], bot[1][2]
    return np.array([tl, tr, br, bl], np.float32)


def lowfreq(arr, mask, sigma):
    m = mask.astype(np.float32)
    num = cv2.GaussianBlur(arr * m, (0, 0), sigma)
    den = cv2.GaussianBlur(m, (0, 0), sigma) + 1e-4
    return num / den


def composite(img, art, quad, sil, strength=1.0):
    h, w = img.shape[:2]
    ah, aw = art.shape[:2]
    src = np.float32([[0, 0], [aw, 0], [aw, ah], [0, ah]])
    M = cv2.getPerspectiveTransform(src, quad)
    warped = cv2.warpPerspective(art, M, (w, h), flags=cv2.INTER_AREA if aw > 200 else cv2.INTER_LINEAR)
    inner = cv2.erode(sil, np.ones((3, 3), np.uint8))

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # skin / fingers in front of the can: orange-ish hue, mid saturation
    skin = cv2.inRange(hsv, (0, 45, 70), (13, 200, 255))
    skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    mask = cv2.bitwise_and(inner, cv2.bitwise_not(skin))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    # match lighting: transfer the low-frequency luminance of the original can onto the art
    lum_o = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    lum_w = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY).astype(np.float32)
    sig = max(3.0, math.sqrt(cv2.countNonZero(mask)) * 0.12)
    lo = lowfreq(lum_o, mask > 0, sig)
    lw = lowfreq(lum_w, mask > 0, sig)
    ratio = np.clip(lo / (lw + 1e-3), 0.45, 1.7)
    ratio = 1.0 + (ratio - 1.0) * strength
    lit = np.clip(warped.astype(np.float32) * ratio[..., None], 0, 255)

    soft = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (0, 0), 1.2)[..., None]
    out = img.astype(np.float32) * (1 - soft) + lit * soft
    return np.clip(out, 0, 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--debug")
    ap.add_argument("--strength", type=float, default=1.0)
    a = ap.parse_args()
    img = cv2.imread(a.src)
    art = load_art()
    cans = detect_cans(img, bool(a.debug))
    out = img.copy()
    dbg = img.copy()
    for box, gold_px, sil in cans:
        quad = order_box(box, gold_px)
        out = composite(out, art, quad, sil, a.strength)
        cv2.polylines(dbg, [quad.astype(np.int32)], True, (0, 255, 0), 3)
        cv2.circle(dbg, tuple(quad[0].astype(int)), 8, (0, 0, 255), -1)  # TL marker
    cv2.imwrite(a.dst, out)
    if a.debug:
        cv2.imwrite(a.debug, dbg)
    print(f"{a.src}: fixed {len(cans)} cans")


if __name__ == "__main__":
    main()
