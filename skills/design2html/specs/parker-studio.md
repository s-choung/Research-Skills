# parker-studio — Style Reference
> Curated art gallery

**Theme:** light

Parker Studio utilizes a 'scrapbook chic' aesthetic, layering textural and tonal imagery on a white canvas accented by a soft, muted green. Typography is a sophisticated blend of classic serif for display and a custom sans-serif for body text, maintaining a refined visual identity. The overall impression is one of curated elegance, where UI elements are minimal and recede, allowing photographic content to dominate and define the brand narrative.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Canvas White | `#ffffff` | `--color-canvas-white` | Page backgrounds, elevated card surfaces, primary text on dark accents, ghost button borders and text for dark sections |
| Midnight Ink | `#000000` | `--color-midnight-ink` | Primary text, headings, links, form input text, borders, dark ghost button borders and text for light sections. Provides high contrast against light surfaces |
| Sage Green | `#b7e3b6` | `--color-sage-green` | Backgrounds for select sections (e.g., footer), decorative background elements, large blocks of color used to highlight or separate content |
| Subtle Gray | `#a5a5a5` | `--color-subtle-gray` | Muted secondary text, date/category metadata, subtle body text borders. Creates a soft hierarchy without strong contrast |

## Tokens — Typography

### PSTimes — Signature display headlines, conveying an artisan, bespoke quality. Uses a custom serif for distinctiveness. · `--font-pstimes`
- **Substitute:** Times New Roman
- **Weights:** 400
- **Sizes:** 62px
- **Line height:** 0.96
- **OpenType features:** `"ss03", "ss04"`
- **Role:** Signature display headlines, conveying an artisan, bespoke quality. Uses a custom serif for distinctiveness.

### ChaletBook — Primary body text, navigation items, buttons, and some sub-headlines. Its custom nature provides brand personality. · `--font-chaletbook`
- **Substitute:** Arial
- **Weights:** 400
- **Sizes:** 16px, 19px, 43px
- **Line height:** 1.00, 1.10, 1.13, 1.15
- **Letter spacing:** -0.02
- **OpenType features:** `"ss03" on, "ss04"`
- **Role:** Primary body text, navigation items, buttons, and some sub-headlines. Its custom nature provides brand personality.

### Times — Utility serif for specific text elements where a classic, readable aesthetic is desired, likely for small print or meta information. Only 'system' font used. · `--font-times`
- **Substitute:** Times New Roman
- **Weights:** 400
- **Sizes:** 
- **Line height:** 1.20
- **OpenType features:** `"ss03" on, "ss04"`
- **Role:** Utility serif for specific text elements where a classic, readable aesthetic is desired, likely for small print or meta information. Only 'system' font used.

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| body | 16px | 1 | -0.32px | `--text-body` |
| subheading | 19px | 1.15 | -0.38px | `--text-subheading` |
| heading | 43px | 1.1 | -0.86px | `--text-heading` |
| display | 62px | 0.96 | -1.24px | `--text-display` |

## Tokens — Spacing & Shapes

**Base unit:** 4px

**Density:** comfortable

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 8 | 8px | `--spacing-8` |
| 12 | 12px | `--spacing-12` |
| 24 | 24px | `--spacing-24` |
| 56 | 56px | `--spacing-56` |
| 220 | 220px | `--spacing-220` |

### Border Radius

| Element | Value |
|---------|-------|
| cards | 0px |
| inputs | 0px |
| buttons | 0px |

### Layout

- **Section gap:** 56px
- **Card padding:** 19px
- **Element gap:** 21px

## Components

### Header Navigation Link (Light)
**Role:** Navigational element for primary site sections on light backgrounds.

Text in Midnight Ink (#000000), font 'ChaletBook' weight 400. Has a 0px radius, with a border-bottom of 1px solid Midnight Ink (#000000) on hover/active states. Padding of 19px left/right, 0px top/bottom. Spacing: 8px right margin to next item.

### Header Navigation Link (Dark)
**Role:** Navigational element for primary site sections on dark backgrounds.

Text in Canvas White (#ffffff), font 'ChaletBook' weight 400. Has a 0px radius, with a border-bottom of 1px solid Canvas White (#ffffff) on hover/active states. Padding of 19px left/right, 0px top/bottom. Spacing: 8px right margin to next item.

### Ghost Button (Light BG)
**Role:** Minimal call to action, typically used for secondary actions or links.

Transparent background, Midnight Ink (#000000) text and 1px bottom border. Font 'ChaletBook', weight 400, letter-spacing -0.02em. No border-radius. Minimal padding to appear as an underline, specifically 18.5143px left padding.

### Ghost Button (Dark BG)
**Role:** Minimal call to action, typically used for secondary actions or links, for use against dark backgrounds.

Transparent background, Canvas White (#ffffff) text and 1px bottom border. Font 'ChaletBook', weight 400, letter-spacing -0.02em. No border-radius. No padding.

### Input Field
**Role:** Standard form input for text entry.

Transparent background, Midnight Ink (#000000) text and a 1px solid Midnight Ink (#000000) bottom border. Font 'ChaletBook', weight 400, letter-spacing -0.02em. No border-radius or internal padding.

### News Card Detail Link
**Role:** Secondary link for descriptive text beneath news cards.

Text in Subtle Gray (#a5a5a5), font 'ChaletBook' weight 400, size 16px. No explicit background, border, or radius. Appears as a muted textual annotation with 12px top margin for spacing from other content.

## Do's and Don'ts

### Do
- Prioritize Canvas White (#ffffff) as the primary page background.
- Use Sage Green (#b7e3b6) for large background sections or as a distinct atmospheric accent.
- Employ Midnight Ink (#000000) for all primary text, headings, and outlines on light backgrounds.
- For all typographic elements excluding signature display headlines, use 'ChaletBook' font family with a letter-spacing of -0.02em.
- Maintain consistently sharp, 0px border-radii across all UI components, including buttons, cards, and input fields.
- Apply 21px as the standard horizontal and vertical spacing between most non-text elements.
- Ensure interactive elements reveal a 1px bottom border in their respective text color on hover or focus.

### Don't
- Avoid using high-saturation colors; restrict the palette to the defined muted green and achromatic tones.
- Do not introduce rounded corners; all interface elements must retain sharp, 0px corners.
- Refrain from using drop shadows or complex elevation; maintain a flat, layered aesthetic.
- Do not deviate from the defined serif and sans-serif font families or their specified letter spacing values.
- Avoid dense, information-heavy sections; prioritize spacious layouts with ample negative space.
- Do not use separate solid fills for buttons; primary calls to action should be ghost buttons with underlying borders.
- Decline to use system default blue for links; all links must be black and integrate with the defined typography.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 1 | Canvas | `#ffffff` | Primary page background, base layer. |
| 2 | Sectional Accent | `#b7e3b6` | Background for distinct content sections or decorative blocks. |

## Imagery

The site primarily uses photography and graphic treatments that evoke a 'mood board' or 'scrapbook' aesthetic. Imagery, particularly product photography, is often contained within rectangular frames, sometimes at varying sizes and orientations, creating a dynamic, collage-like layout. Treatments range from full-color vibrant shots to more subdued, sometimes monochromatic or duotone, effects where the product often takes center stage against a clean or textural background. Some abstract, gradient-like graphics also appear, adding a soft, ethereal quality. Icons, if present in the UI, appear to be outlined with a moderate stroke weight, aligning with the minimal component style. The imagery serves both decorative and explanatory roles, heavily contributing to the brand's sophisticated but artful atmosphere, dominating visual space over text.

## Layout

The page embraces a full-bleed layout for its initial presentation, allowing varied image compositions to fill the viewport, while later sections shift to a maximum-width contained model. The hero section features a dynamic, asymmetric collage of images that command attention. Content sections primarily exhibit consistent vertical spacing, creating an airy rhythm without explicit dividers, though large Sage Green (#b7e3b6) blocks serve as implicit section breaks. The content arrangement frequently utilizes a text-left/image-right or vice-versa pattern, with sections often arranged in a loose grid. Card grids are used for feature or news sections, showcasing content in distinct visual blocks. The overall density is spacious, emphasizing individual content pieces. Navigation appears as a minimalist sticky top bar with subtle text links.

## Agent Prompt Guide

Quick Color Reference: 
text: #000000
background: #ffffff
border: #000000
accent: #b7e3b6
primary action: no distinct CTA color

Example Component Prompts:
1. Create a header navigation item: text 'Work' in ChaletBook (400, 19px, -0.02em letter-spacing), color Midnight Ink (#000000). On hover, add a 1px bottom border in Midnight Ink (#000000).
2. Create a large display headline: text 'Selected Work' in PSTimes (400, 62px, 0.96 lineHeight), color Midnight Ink (#000000).
3. Create a footer section: use Sage Green (#b7e3b6) as background color. Include general body text in Midnight Ink (#000000) using ChaletBook (400, 16px, -0.02em letter-spacing).
4. Create a news card metadata link: text '09/08/24 • Brand Strategy' in ChaletBook (400, 16px, -0.02em letter-spacing), color Subtle Gray (#a5a5a5), with 12px top margin.

## Similar Brands

- **AIGA** — Showcases strong, artistic imagery with minimal UI, leveraging custom typography and a muted color palette.
- **Pentagram** — Employs an editorial layout style with large, impactful visuals and sophisticated typography, often within white space.
- **Made Thought** — Known for a clean, design-forward aesthetic, balancing high-quality photography with bold, custom typography and often-muted accent colors.
- **The Brand Identity** — Features a 'scrapbook' or editorial layout with varied image sizing and placements, prioritizing visual content over heavy UI elements.

## Quick Start

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-canvas-white: #ffffff;
  --color-midnight-ink: #000000;
  --color-sage-green: #b7e3b6;
  --color-subtle-gray: #a5a5a5;

  /* Typography — Font Families */
  --font-pstimes: 'PSTimes', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-chaletbook: 'ChaletBook', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-times: 'Times', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* Typography — Scale */
  --text-body: 16px;
  --leading-body: 1;
  --tracking-body: -0.32px;
  --text-subheading: 19px;
  --leading-subheading: 1.15;
  --tracking-subheading: -0.38px;
  --text-heading: 43px;
  --leading-heading: 1.1;
  --tracking-heading: -0.86px;
  --text-display: 62px;
  --leading-display: 0.96;
  --tracking-display: -1.24px;

  /* Typography — Weights */
  --font-weight-regular: 400;

  /* Spacing */
  --spacing-unit: 4px;
  --spacing-8: 8px;
  --spacing-12: 12px;
  --spacing-24: 24px;
  --spacing-56: 56px;
  --spacing-220: 220px;

  /* Layout */
  --section-gap: 56px;
  --card-padding: 19px;
  --element-gap: 21px;

  /* Named Radii */
  --radius-cards: 0px;
  --radius-inputs: 0px;
  --radius-buttons: 0px;

  /* Surfaces */
  --surface-canvas: #ffffff;
  --surface-sectional-accent: #b7e3b6;
}
```

### Tailwind v4

```css
@theme {
  /* Colors */
  --color-canvas-white: #ffffff;
  --color-midnight-ink: #000000;
  --color-sage-green: #b7e3b6;
  --color-subtle-gray: #a5a5a5;

  /* Typography */
  --font-pstimes: 'PSTimes', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-chaletbook: 'ChaletBook', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-times: 'Times', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* Typography — Scale */
  --text-body: 16px;
  --leading-body: 1;
  --tracking-body: -0.32px;
  --text-subheading: 19px;
  --leading-subheading: 1.15;
  --tracking-subheading: -0.38px;
  --text-heading: 43px;
  --leading-heading: 1.1;
  --tracking-heading: -0.86px;
  --text-display: 62px;
  --leading-display: 0.96;
  --tracking-display: -1.24px;

  /* Spacing */
  --spacing-8: 8px;
  --spacing-12: 12px;
  --spacing-24: 24px;
  --spacing-56: 56px;
  --spacing-220: 220px;
}
```
