# Design Tokens

Every Futured iOS project defines its design system as typed Swift tokens. **Never inline magic numbers in feature code** — if a value represents a design decision, it belongs in the design system.

## Spacing

Use the project's `CGFloat` spacing tokens from `Spacing+<Project>.swift` (e.g. `Spacing+SMSTicket.swift`). Semantic names are preferred over size-based ones:

```swift
// Typical semantic schema (project-specific values)
extension CGFloat {
    static let spacingXS: CGFloat = 4
    static let spacingSM: CGFloat = 6
    static let spacingMD: CGFloat = 8
    static let spacingLG: CGFloat = 12
    static let spacingXL: CGFloat = 16
    static let spacing2XL: CGFloat = 20
    static let spacing3XL: CGFloat = 24
    static let spacing4XL: CGFloat = 32
    static let spacing5XL: CGFloat = 40
    // ... up to design system's largest step
}
```

```swift
// Correct
.padding(.spacingXL)
VStack(spacing: .spacingMD) { ... }
.frame(height: .spacing4XL)

// Wrong — magic numbers
.padding(16)
VStack(spacing: 8) { ... }
```

Rules:
- **Semantic names** (`spacingXS`, `spacingLG`, `spacing2XL`) over size-based ones (`space4`, `space16`). The spec can change the underlying value without renaming every call site.
- The exact set of steps and their values comes from the project's design system (Figma / tokens repo). Add missing steps to `Spacing+<Project>.swift` before using them in feature code.
- `Spacing+<Project>.swift` lives under `Resources/DesignSystem/` (or equivalent).

## Colors

Colors live in `Assets.xcassets/Colors/` organized by category (Primary, Accent, Support, Special, Text). Reference via the asset catalog as `Color(.tokenName)` — no hardcoded hex literals, no `Color(white:)`, `Color(red:green:blue:)` in feature code.

If a color doesn't exist in the catalog, ask the designer/user to provide it before using it.

## Corner Radius

Corner radii belong in `CornerRadius+<Project>.swift` as `CGFloat` extensions. Use the same semantic pattern (`cornerRadiusSM`, `cornerRadiusMD`, `cornerRadiusLG`, `cornerRadius2XL`, …). No inline magic values.

## Border Width & Shadows

Define as `CGFloat` / composite extensions in the design system folder alongside corner radii. No inline magic values.

## Typography

All text styling goes through the `TextStyles` enum (see `@.claude/rules/text-styling.md`). Never call `.font(.system(size:))` directly.
