---
name: Fintech Momentum
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daea'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eefe'
  surface-container-high: '#e2e8f8'
  surface-container-highest: '#dce2f3'
  on-surface: '#151c27'
  on-surface-variant: '#594139'
  inverse-surface: '#2a313d'
  inverse-on-surface: '#ebf1ff'
  outline: '#8d7168'
  outline-variant: '#e1bfb5'
  surface-tint: '#ab3500'
  primary: '#ab3500'
  on-primary: '#ffffff'
  primary-container: '#ff6b35'
  on-primary-container: '#5f1900'
  inverse-primary: '#ffb59d'
  secondary: '#515f78'
  on-secondary: '#ffffff'
  secondary-container: '#d2e0fe'
  on-secondary-container: '#55637d'
  tertiary: '#006c49'
  on-tertiary: '#ffffff'
  tertiary-container: '#00af79'
  on-tertiary-container: '#003a25'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbd0'
  primary-fixed-dim: '#ffb59d'
  on-primary-fixed: '#390c00'
  on-primary-fixed-variant: '#832600'
  secondary-fixed: '#d6e3ff'
  secondary-fixed-dim: '#b9c7e4'
  on-secondary-fixed: '#0d1c32'
  on-secondary-fixed-variant: '#39475f'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f9f9ff'
  on-background: '#151c27'
  surface-variant: '#dce2f3'
typography:
  headline-lg:
    fontFamily: DM Sans
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
  headline-lg-mobile:
    fontFamily: DM Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: DM Sans
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 28px
  body-lg:
    fontFamily: DM Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: DM Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: DM Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  button-text:
    fontFamily: DM Sans
    fontSize: 16px
    fontWeight: '700'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  margin-mobile: 16px
  margin-desktop: 32px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style

This design system is engineered for a high-velocity B2B fintech environment. It balances the urgency and energy of business growth with the steadfast reliability required for financial decision-making. The aesthetic is **Corporate / Modern**, characterized by high-contrast typography and a vibrant primary palette that directs user attention toward growth opportunities and recommendations.

The visual language emphasizes clarity and speed. By utilizing a "Mobile-First" philosophy, the design system ensures that complex financial data is digestible on small screens through generous whitespace, clear information hierarchy, and a tactile, card-based interface. The atmosphere is professional and trustworthy, eschewing traditional banking blues in favor of a modern, energetic orange and deep navy pairing.

## Colors

The palette is anchored by **Vivid Orange**, used exclusively for primary actions and key performance indicators. This is countered by **Oxford Navy**, which provides the structural weight and authority needed for headings and navigation elements.

- **Primary (#FF6B35):** The engine of the UI. Used for CTAs, active toggle states, and brand-driven highlights.
- **Secondary (#0A192F):** Used for typography and deep-background elements to establish a premium B2B feel.
- **Surface & Background:** A strict distinction is maintained between the off-white page background (#F8F9FA) and the pure white (#FFFFFF) containers to create natural depth without heavy shadows.
- **Semantic Colors:** Success Green (#10B981) and Error Red (#EF4444) are reserved for transactional feedback and financial trend indicators.

## Typography

This design system utilizes **DM Sans** for its geometric clarity and modern professional tone. The typographic scale is optimized for high legibility in data-dense environments.

- **Headings:** Always set in Bold weight using Oxford Navy to ensure immediate visual anchoring.
- **Body Text:** Use Regular weight. Secondary information and helper text should utilize the Muted Gray to create a clear contrast with primary data.
- **Numbers:** Given the fintech context, numerical data should be clear and unobstructed. When displaying currency or metrics, ensure the weight matches the surrounding context to maintain flow.
- **Line Height:** Tight for headings to maintain impact; generous for body text to improve scanning on mobile devices.

## Layout & Spacing

This design system follows a **Fluid Grid** model with an 8px base unit. 

### Mobile Layout
- **Margins:** 16px lateral margins to maximize screen real estate for data tables and recommendation cards.
- **Structure:** Single column vertical stack for cards. Content should utilize 100% of the available width within margins.

### Desktop/Tablet Layout
- **Margins:** Scales to 32px or center-aligned fixed containers (max-width 1200px) depending on the complexity of the recommendation dashboard.
- **Gutter:** 16px fixed gutter between multi-column cards.

### Spacing Philosophy
Emphasis is placed on vertical "stack" spacing. Elements related to the same data point should use `stack-sm`, while distinct sections or cards use `stack-lg` to prevent visual clutter.

## Elevation & Depth

Visual hierarchy in this design system is achieved through **Ambient Shadows** and tonal layering. 

- **Level 0 (Background):** #F8F9FA. The foundation for all navigation and content.
- **Level 1 (Cards/Inputs):** #FFFFFF. These elements sit on the background with a very soft, diffused shadow (0px 4px 12px rgba(10, 25, 47, 0.05)).
- **Level 2 (Active/Hover):** When an element is interacted with, the shadow deepens (0px 8px 24px rgba(10, 25, 47, 0.10)) to provide tactile feedback.

Avoid heavy black shadows; always tint shadows with the secondary Navy color at very low opacity to maintain a clean, fintech aesthetic.

## Shapes

The shape language is approachable yet structured. All interactive and container elements use a consistent roundedness scale to evoke a friendly, modern "app-like" feel.

- **Standard Elements:** Inputs, small buttons, and tags use a **0.5rem (8px)** radius.
- **Large Containers:** Product recommendation cards and primary action buttons use **0.75rem to 1rem (12px - 16px)** radius to soften the high-contrast color palette.
- **Iconography:** Icons should feature slightly rounded terminals to match the font characteristics of DM Sans.

## Components

### Buttons
- **Primary:** Solid #FF6B35 with white text. 12px corner radius. High-impact for "Apply Now" or "Get Recommended."
- **Secondary:** Outlined with Oxford Navy (#0A192F) and 1.5px border weight. Used for "Learn More" or "Filter."
- **Disabled:** 40% opacity of the respective style with a "not-allowed" cursor on desktop.

### Input Fields
- **Background:** Solid white.
- **Border:** 1px Muted Gray, turning Navy on focus.
- **Prefixes:** Currency inputs must always include a ₹ prefix in a slightly muted weight to differentiate from the user's input.
- **Labels:** Small, uppercase bold labels positioned above the field.

### Recommendation Cards
- **Structure:** White background, 12px rounded corners, subtle shadow.
- **Header:** Contains the product logo and a "Match Score" or "Tag" in the top right.
- **Footer:** Separated by a thin #F1F3F5 divider, containing the primary CTA.

### Chips & Tags
- **Success:** Green background at 10% opacity with solid green text for "Eligible" or "Approved" statuses.
- **Neutral:** Light gray background with navy text for category tags.

### Progress Indicators
- Linear progress bars for application steps, utilizing the Primary Orange to show completion.