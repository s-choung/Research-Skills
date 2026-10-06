"""SKKU official brand colors for scientific plots.

Source: SKKU UI color system (Pantone/CMYK/RGB from brand guide).
Usage:
    from skku_colors import SKKU, skku_palette
    colors = skku_palette()  # ordered list for categorical series
"""

SKKU = {
    # 파란색 — 리더십, 신뢰, 지성, 책임 (Pantone 541C)
    "navy": "#072B61",       # R7 G43 B97
    # 연두색 — 다시 시작되는 역사 (Pantone 367C)
    "lime": "#8DC63F",       # R141 G198 B63
    # 주황색 — 창조, 역동, 혁신 (Pantone 1585C)
    "orange": "#FF6C0F",     # R255 G108 B15
    # 진녹색 — 소통, 공유, 협력 (Pantone 3435C)
    "green": "#124633",      # R18 G70 B51
}

# neutral companion (not official; for de-emphasized series)
SKKU_NEUTRAL = "#C7C4B5"


def skku_palette():
    """Categorical order: navy, orange, lime, green, neutral."""
    return [SKKU["navy"], SKKU["orange"], SKKU["lime"], SKKU["green"],
            SKKU_NEUTRAL]
