---
name: frontend-design
description: Build web pages, components, landing pages, dashboards, or UI layouts. Use when asked to "build a page", "create a component", "design a landing page", "make a dashboard", or any frontend/UI implementation task.
model: inherit
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Scope

Use this skill for a component, a page, or a dashboard inside an existing visual language. For a whole site, generate the design system first (tokens, type scale, colour roles, component shapes) and hand that to the build as the source of truth; this skill steers strongly enough that site-wide generation converges on one house look. When a design system already exists, follow it and treat the guidance below as tie-breakers rather than as direction.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Load them via Google Fonts CDN (`<link>` or `@import`): specify exact weights and styles (e.g., `Instrument Serif:ital,wght@0,400;1,400` not just the family name). Pair a distinctive display font with a refined body font. Avoid generic fonts like Arial, Inter, Roboto, and system fonts.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Specify exact hex values: don't default to pure black (#000), pure white (#fff), or standard Tailwind palette stops.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.
- **Content**: Use realistic, contextual placeholder content that matches the domain: not "Lorem ipsum" or generic "Welcome to our app" copy. The content should feel like it belongs in a real product.

## Avoiding distributional convergence

LLMs naturally gravitate toward the average of their training data. Fight this actively:
- Before choosing fonts, colors, or layout, mentally discard the first idea, it's likely the statistical mode.
- Rotate between light/dark themes, serif/sans-serif typography, warm/cool palettes, dense/spacious layouts across generations.
- Avoid "safe" choices that recur across AI-generated designs: Space Grotesk, Tailwind indigo/purple gradients, centered hero + 3-column grid, rounded-xl cards with shadows.
- When in doubt, pick something you haven't used in the last 5 designs.

NEVER use generic AI-generated aesthetics: overused font families (Inter, Roboto, Space Grotesk, system fonts), cliched color schemes (purple gradients on white), predictable layouts (centered hero → feature grid → footer), or cookie-cutter component patterns.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Working from reference designs

When the user provides a screenshot, Figma link, or design reference:

1. **Extract constraints only**, identify the color palette (exact hex values) and typography (font families, weights, sizes) from the reference
2. **Build original layout**, do NOT replicate the reference layout pixel-for-pixel. Use the extracted colors and fonts as constraints, but create an original spatial composition
3. **Check references/**, if past designs exist in the `references/` directory alongside this skill, use them to understand the user's preferred aesthetic and maintain consistency

This approach ensures brand consistency (same colors/fonts) while avoiding derivative layouts.

## Gotchas

Things this skill must NEVER do:

- **Never use generic AI-generated aesthetics.** No purple/indigo gradients on white, no centered-hero → 3-column feature grid → footer, no cookie-cutter rounded-xl cards with shadows.
- **Never use overused fonts.** Avoid Inter, Roboto, Space Grotesk, Arial, and system fonts. Pair a distinctive display font with a refined body font, loaded via Google Fonts with exact weights/styles.
- **Never default to pure black (#000) or pure white (#fff)**, or to standard Tailwind palette stops. Specify exact hex values committed to a cohesive theme.
- **Never settle for the first idea.** It is the statistical mode: discard it before choosing fonts, colors, or layout. Don't repeat a choice used in the last 5 designs.
- **Never default backgrounds to flat solid colors.** Add atmosphere and depth (gradient meshes, noise, texture, layered transparency, shadows).
- **Never use "Lorem ipsum" or generic copy.** Use realistic, domain-specific placeholder content.
- **Never replicate a reference design pixel-for-pixel.** Extract only colors and typography as constraints; build an original layout.
- **Never mismatch complexity to the vision.** Maximalist designs need elaborate code; minimalist designs need restraint and precision: not under- or over-built output.