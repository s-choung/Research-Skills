# Ease Health — Style Reference
> calm clinical canvas

**Theme:** light

Ease Health employs a grounded, clinical yet approachable aesthetic, balancing a muted green-blue palette with abundant whitespace. The design emphasizes clarity through distinct surface levels, subtle typography, and a signature deep forest green for primary actions, contrasting with the soft, almost pastel backgrounds. Components are clean and substantial, featuring generous padding and distinctive rounded corners, giving the interface a calm, trustworthy, and organized feel.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Forest Green | `#0f3e17` | `--color-forest-green` | Primary brand color for calls to action, text, and critical icons — grounding the UI with a sense of growth and reliability |
| Cream Canvas | `#fffefc` | `--color-cream-canvas` | Background for page surfaces and pristine component backdrops, providing a clean, bright foundation |
| Mint Glaze | `#b1dbb8` | `--color-mint-glaze` | Soft background for informational cards and sections, introducing a gentle, almost pastel tint to the UI planes |
| Slate Mist | `#b6ced5` | `--color-slate-mist` | Cool, muted background for secondary cards and sections, offering visual separation without overwhelming the primary content |
| Keylime Wash | `#e1f4df` | `--color-keylime-wash` | Lightest green surface, used for subtle card backgrounds or layered elements, providing a hint of color |
| Mint Kiss | `#cfe7d3` | `--color-mint-kiss` | Another very light green surface, subtly differentiating stacked cards or sections |
| Border Grey | `#e5e7eb` | `--color-border-grey` | Default boundary and separator color, used for hairline borders and inactive states, maintaining visual separation with minimal distraction |
| Ink Text | `#222222` | `--color-ink-text` | Primary text color for navigation and core content, providing strong contrast against light backgrounds |
| Dark Charcoal | `#333333` | `--color-dark-charcoal` | Secondary text and link color for less prominent information, like image captions or muted links |

## Tokens — Typography

### Suisseintl — The workhorse sans-serif for most body text, links, buttons, and detailed interface elements. Its refined simplicity supports a clinical tone without feeling sterile. · `--font-suisseintl`
- **Substitute:** Inter
- **Weights:** 300, 400
- **Sizes:** 12px, 14px, 18px, 23px, 28px, 56px
- **Line height:** 1.00, 1.30, 1.50
- **Letter spacing:** -0.0300em
- **Role:** The workhorse sans-serif for most body text, links, buttons, and detailed interface elements. Its refined simplicity supports a clinical tone without feeling sterile.

### Faire Octave — Used exclusively for large, impactful headings. Its light weight (300) for such prominent sizes creates an authoritative yet approachable voice, suggesting wisdom through understatement rather than volume. · `--font-faire-octave`
- **Substitute:** Playfair Display
- **Weights:** 300
- **Sizes:** 40px, 74px
- **Line height:** 1.05, 1.35
- **Letter spacing:** -0.0300em, -0.0100em
- **Role:** Used exclusively for large, impactful headings. Its light weight (300) for such prominent sizes creates an authoritative yet approachable voice, suggesting wisdom through understatement rather than volume.

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| caption | 12px | 1.5 | -0.36px | `--text-caption` |
| body | 14px | 1.5 | -0.42px | `--text-body` |
| body-lg | 18px | 1.5 | -0.54px | `--text-body-lg` |
| subheading | 23px | 1.3 | -0.69px | `--text-subheading` |
| heading-sm | 28px | 1.3 | -0.84px | `--text-heading-sm` |
| heading | 40px | 1.05 | -0.4px | `--text-heading` |
| display | 56px | 1 | -1.68px | `--text-display` |
| display-lg | 74px | 1.05 | -0.74px | `--text-display-lg` |

## Tokens — Spacing & Shapes

**Density:** comfortable

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 7 | 7px | `--spacing-7` |
| 9 | 9px | `--spacing-9` |
| 11 | 11px | `--spacing-11` |
| 14 | 14px | `--spacing-14` |
| 18 | 18px | `--spacing-18` |
| 21 | 21px | `--spacing-21` |
| 28 | 28px | `--spacing-28` |
| 35 | 35px | `--spacing-35` |
| 42 | 42px | `--spacing-42` |
| 49 | 49px | `--spacing-49` |
| 56 | 56px | `--spacing-56` |
| 70 | 70px | `--spacing-70` |
| 76 | 76px | `--spacing-76` |
| 99 | 99px | `--spacing-99` |
| 156 | 156px | `--spacing-156` |

### Border Radius

| Element | Value |
|---------|-------|
| nav | 7px |
| cards | 14px |
| badges | 999px |
| buttons | 14px |

### Layout

- **Section gap:** 42px
- **Card padding:** 42px
- **Element gap:** 21px

## Components

### Primary Action Button (Filled)
**Role:** Main call-to-action button, conveying primary user interaction.

Solid Forest Green background (#0f3e17), Cream Canvas text (#fffefc), 14px rounded corners, with generous 14px vertical and 21px horizontal padding. Delivers a confident and prominent interaction point.

### Large Action Button
**Role:** Prominent full-block call-to-action for key feature sections.

Solid Forest Green background (#0f3e17), Cream Canvas text (#fffefc), 14px radius. Features expansive 42px padding on all sides, drawing significant attention to critical actions.

### Content Card (Mint Glaze)
**Role:** General purpose container for information or features, with a refreshing tint.

Mint Glaze background (#b1dbb8), no box shadow, 14px rounded corners. Offers 42px of internal padding.

### Content Card (Slate Mist)
**Role:** Alternative general purpose container, providing subtle visual distinction.

Slate Mist background (#b6ced5), no box shadow, 14px rounded corners. Offers 42px of internal padding.

### Content Card (Keylime Wash)
**Role:** Lightest card background for sub-sections or layered content.

Keylime Wash background (#e1f4df), no box shadow, 14px rounded corners. Offers 70px of internal padding for a spacious feel.

### Pill Badge
**Role:** Used for categorization or brief status indicators.

Cream Canvas background (#fffefc), Forest Green text (#0f3e17), with maximum border-radius (999px) for a pill shape. Contains 9px vertical and 14px horizontal padding.

## Do's and Don'ts

### Do
- Use Forest Green (#0f3e17) exclusively for primary action buttons and core brand elements to maintain its impact.
- Apply 14px border-radius to all cards and most buttons for a consistent soft, approachable aesthetic.
- Ensure all text content defaults to Suisseintl for readability and consistency, varying only weight and size.
- Utilize Faire Octave at weight 300 for major headlines (40px, 74px) to convey understated authority.
- Employ Cream Canvas (#fffefc) as the primary background for detailed UI elements, balancing against chromatic cards.
- Maintain a comfortable density with 21px for element gaps and 42px for card and section padding.
- Use Border Grey (#e5e7eb) for all neutral borders and dividers to keep the interface light and airy.

### Don't
- Do not introduce new chromatic colors outside of the defined green and blue accents to preserve the muted palette.
- Avoid harsh shadows or strong elevation; surfaces should feel flat and distinct through color changes, not depth.
- Do not use multiple font families for body text or interface elements; Suisseintl serves this purpose exclusively.
- Never use full black (#000000) for text; opt for Ink Text (#222222) or Dark Charcoal (#333333) for softer contrast.
- Do not deviate from the established border-radius values across component types.
- Avoid compacting content; err on the side of generous element and padding values to maintain the comfortable density.
- Do not use generic system fonts when Suisseintl or Faire Octave are available; these are critical for brand identity.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Canvas Background | `#fffefc` | Dominant page background, providing a clean, bright, and almost textured base for all content. |
| 1 | Keylime Wash Card | `#e1f4df` | First layer of elevated content, used for prominent cards or hero sections, offering a subtle green tint. |
| 2 | Mint Glaze Card | `#b1dbb8` | Second layer of elevated content, for detailed information cards or feature blocks, slightly more saturated green. |
| 3 | Slate Mist Card | `#b6ced5` | Third layer of elevated content, providing clear visual separation for distinct blocks, using a cool desaturated blue-gray. |

## Imagery

Imagery is functional and product-focused, featuring clean product screenshots of UI elements and interface cards. These visuals often overlap or are presented as distinct, rounded-corner elements against tinted backgrounds. Text-based icons are minimal. Visuals serve to explain product features rather than create abstract atmosphere, maintaining a high-fidelity, clear display of the software's capabilities.

## Layout

The page uses a maximum-width contained layout, centering content within a white canvas. The hero section features a split layout: a bold green content block on the left with a large headline, contrasted by a light blue canvas on the right presenting stacked product visuals. Sections below alternate between full-width content blocks and contained layouts, often with alternating two-column layouts (text left, image right, or vice-versa). Vertical rhythm is established through generous and consistent section gaps, giving content ample breathing room. The navigation is a sticky top bar with a primary 'Book a Demo' button.

## Agent Prompt Guide

Quick Color Reference:
text: #222222
background: #fffefc
border: #e5e7eb
accent: #b1dbb8
primary action: #0f3e17 (filled action)

Example Component Prompts:
1. Create a Primary Action Button: #0f3e17 background, #fffefc text, 9999px radius, compact pill padding. Use this filled treatment for the main CTA.
2. Design a feature card: Mint Glaze background (#b1dbb8), 14px radius, 42px padding. Title 'AI-Powered Documentation' using Suisseintl weight 400 at 28px, #0f3e17. Body copy 'Reduce administrative burden…' using Suisseintl weight 300 at 18px, #333333. Includes a small checked icon (Forest Green, 0f3e17).
3. Generate a testimonial section: Cream Canvas background (#fffefc). Headline 'What healthcare providers say' using Faire Octave weight 300 at 40px, #0f3e17, letter-spacing -0.4px. Display a Pill Badge 'Broad clinical support', Cream Canvas background (#fffefc), Forest Green text (#0f3e17).

## Similar Brands

- **Alinea** — Shares a similar muted pastel color palette with one dominant deep action color, spacious layouts, and rounded card styles.
- **Elation Health** — Employs a clean, health-tech aesthetic with a focus on clear UI design, abundant whitespace, and subtle use of color for functional elements.
- **Klang.ai** — Uses a single, grounding brand color for primary actions and headlines against a light, neutral background, with clean typography.
- **Notion** — Exhibits a comfortable density with generous spacing and distinct, subtly colored surface levels for content organization, though with a different palette.

## Quick Start

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-forest-green: #0f3e17;
  --color-cream-canvas: #fffefc;
  --color-mint-glaze: #b1dbb8;
  --color-slate-mist: #b6ced5;
  --color-keylime-wash: #e1f4df;
  --color-mint-kiss: #cfe7d3;
  --color-border-grey: #e5e7eb;
  --color-ink-text: #222222;
  --color-dark-charcoal: #333333;

  /* Typography — Font Families */
  --font-suisseintl: 'Suisseintl', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-faire-octave: 'Faire Octave', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1.5;
  --tracking-caption: -0.36px;
  --text-body: 14px;
  --leading-body: 1.5;
  --tracking-body: -0.42px;
  --text-body-lg: 18px;
  --leading-body-lg: 1.5;
  --tracking-body-lg: -0.54px;
  --text-subheading: 23px;
  --leading-subheading: 1.3;
  --tracking-subheading: -0.69px;
  --text-heading-sm: 28px;
  --leading-heading-sm: 1.3;
  --tracking-heading-sm: -0.84px;
  --text-heading: 40px;
  --leading-heading: 1.05;
  --tracking-heading: -0.4px;
  --text-display: 56px;
  --leading-display: 1;
  --tracking-display: -1.68px;
  --text-display-lg: 74px;
  --leading-display-lg: 1.05;
  --tracking-display-lg: -0.74px;

  /* Typography — Weights */
  --font-weight-light: 300;
  --font-weight-regular: 400;

  /* Spacing */
  --spacing-4: 4px;
  --spacing-7: 7px;
  --spacing-9: 9px;
  --spacing-11: 11px;
  --spacing-14: 14px;
  --spacing-18: 18px;
  --spacing-21: 21px;
  --spacing-28: 28px;
  --spacing-35: 35px;
  --spacing-42: 42px;
  --spacing-49: 49px;
  --spacing-56: 56px;
  --spacing-70: 70px;
  --spacing-76: 76px;
  --spacing-99: 99px;
  --spacing-156: 156px;

  /* Layout */
  --section-gap: 42px;
  --card-padding: 42px;
  --element-gap: 21px;

  /* Border Radius */
  --radius-lg: 7.04px;
  --radius-xl: 14.08px;
  --radius-full: 999px;

  /* Named Radii */
  --radius-nav: 7px;
  --radius-cards: 14px;
  --radius-badges: 999px;
  --radius-buttons: 14px;

  /* Surfaces */
  --surface-canvas-background: #fffefc;
  --surface-keylime-wash-card: #e1f4df;
  --surface-mint-glaze-card: #b1dbb8;
  --surface-slate-mist-card: #b6ced5;
}
```

### Tailwind v4

```css
@theme {
  /* Colors */
  --color-forest-green: #0f3e17;
  --color-cream-canvas: #fffefc;
  --color-mint-glaze: #b1dbb8;
  --color-slate-mist: #b6ced5;
  --color-keylime-wash: #e1f4df;
  --color-mint-kiss: #cfe7d3;
  --color-border-grey: #e5e7eb;
  --color-ink-text: #222222;
  --color-dark-charcoal: #333333;

  /* Typography */
  --font-suisseintl: 'Suisseintl', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-faire-octave: 'Faire Octave', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1.5;
  --tracking-caption: -0.36px;
  --text-body: 14px;
  --leading-body: 1.5;
  --tracking-body: -0.42px;
  --text-body-lg: 18px;
  --leading-body-lg: 1.5;
  --tracking-body-lg: -0.54px;
  --text-subheading: 23px;
  --leading-subheading: 1.3;
  --tracking-subheading: -0.69px;
  --text-heading-sm: 28px;
  --leading-heading-sm: 1.3;
  --tracking-heading-sm: -0.84px;
  --text-heading: 40px;
  --leading-heading: 1.05;
  --tracking-heading: -0.4px;
  --text-display: 56px;
  --leading-display: 1;
  --tracking-display: -1.68px;
  --text-display-lg: 74px;
  --leading-display-lg: 1.05;
  --tracking-display-lg: -0.74px;

  /* Spacing */
  --spacing-4: 4px;
  --spacing-7: 7px;
  --spacing-9: 9px;
  --spacing-11: 11px;
  --spacing-14: 14px;
  --spacing-18: 18px;
  --spacing-21: 21px;
  --spacing-28: 28px;
  --spacing-35: 35px;
  --spacing-42: 42px;
  --spacing-49: 49px;
  --spacing-56: 56px;
  --spacing-70: 70px;
  --spacing-76: 76px;
  --spacing-99: 99px;
  --spacing-156: 156px;

  /* Border Radius */
  --radius-lg: 7.04px;
  --radius-xl: 14.08px;
  --radius-full: 999px;
}
```
