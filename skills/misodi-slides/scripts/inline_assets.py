# -*- coding: utf-8 -*-
"""HTML 안의 __HEADER_BAND__ / __WAVE_BG__ 플레이스홀더를 base64 data URI로 치환.

사용: conda run -n base python inline_assets.py <deck.html>
(제자리 치환. 결과 HTML은 단일 파일로 어디서나 열림)
"""
import sys
import base64
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

def b64(path, mime):
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())

def main(html_path):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    html = html.replace("__HEADER_BAND__", b64(os.path.join(ASSETS, "header_band.png"), "image/png"))
    html = html.replace("__WAVE_BG__", b64(os.path.join(ASSETS, "wave_bg.jpg"), "image/jpeg"))
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("inlined:", html_path)

if __name__ == "__main__":
    main(sys.argv[1])
