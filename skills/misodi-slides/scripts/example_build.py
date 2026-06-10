# -*- coding: utf-8 -*-
"""misodi_pptx 사용 예제: templates/deck.html과 1:1 대응하는 4장 샘플 덱.

실행: conda run -n base python example_build.py [출력경로.pptx]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from misodi_pptx import MisodiDeck

out = sys.argv[1] if len(sys.argv) > 1 else "misodi_sample.pptx"
deck = MisodiDeck(out)

# ---- 슬라이드 1: 타이틀 ----
s = deck.add_title_slide(
    kicker="미래소재디스커버리지원+",
    title_runs=[
        ("키워드1", {"xb": True, "size": 31, "color": "8AB1E3"}),
        (" 기반\n", {"xb": True, "size": 31, "color": "FFFFFF"}),
        ("키워드2", {"xb": True, "size": 31, "color": "FFC18C"}),
        (" 핵심소재\n나머지 제목 줄\n마지막 제목 줄", {"xb": True, "size": 31, "color": "FFFFFF"}),
    ],
    date="2026.06.11", leader="연구책임자", leader_name="홍길동",
)
deck.add_fade_animation(s, [sh for sh in s.shapes][1:])  # 배경 제외 전부

# ---- 슬라이드 2: 2단 패널 ----
s = deck.add_content_slide("슬라이드 제목", subtitle="부제목", page=(2, 16))
blocks = []
cont1, chip1 = deck.panel(s, 0.60, 2.96, 15.50, 14.80, color="gray",
                          tab="기존 접근 ( 한계 )", fill_white=False)
blocks += [cont1, chip1]
cont2, chip2 = deck.panel(s, 17.78, 2.96, 15.50, 14.80, color="navy",
                          tab="제안 접근 ( 핵심 )")
blocks += [cont2, chip2]
card = deck.card(s, 1.60, 11.40, 6.35, 4.23)
cap = deck.text(s, 2.10, 15.90, 8.0, 0.9, [
    ("카드 캡션 ", {"size": 14}),
    ("강조", {"xb": True, "size": 14, "color": "0F0F70"}),
])
blocks += [card, cap]
h = deck.text(s, 18.50, 4.25, 8.0, 0.9, [("섹션 소제목", {"xb": True, "size": 18, "color": "0F0F70"})])
body = deck.text(s, 18.50, 5.30, 13.8, 2.0, [
    ("본문 텍스트에 ", {"size": 16}),
    ("오렌지 강조", {"xb": True, "size": 16, "color": "FA901E"}),
    ("와 ", {"size": 16}),
    ("네이비 강조", {"xb": True, "size": 16, "color": "0F0F70"}),
    ("를 섞는다", {"size": 16}),
])
blocks += [h, body]
deck.add_fade_animation(s, blocks)

# ---- 슬라이드 3: 요약 컴포넌트 ----
s = deck.add_content_slide("요약 컴포넌트", page=(3, 16))
g = deck.grad_card(s, 0.90, 3.20, 7.33, 5.24, color="orange")
c1 = deck.chip(s, 1.47, 2.70, 6.30, "그라데이션 카드", color="orange")
p1 = deck.pill(s, 10.58, 3.97, 5.0, "알약 배지")
band = deck.summary_band(s, 13.08, [
    ("핵심 결론", {"xb": True, "size": 18, "color": "0F0F70"}),
    ("을 담는 골드 요약 밴드", {"size": 18}),
])
foot = deck.navy_footer(s, [
    ("강조 단어", {"xb": True, "size": 20, "color": "FA901E"}),
    ("가 들어가는 네이비 푸터 밴드", {"size": 20, "color": "FFFFFF"}),
])
deck.add_fade_animation(s, [g, c1, p1, band, foot])

# ---- 슬라이드 4: 클로징 ----
s = deck.add_closing_slide(sub_runs=[("프로젝트 부제 또는 워드마크", {"size": 12, "color": "FFFFFF"})])
deck.add_fade_animation(s, [sh for sh in s.shapes][1:])

print("saved:", deck.save())
