---
paths:
  - "**/*.swift"
---
# Design Tokens

## Spacing

Use `CGFloat` extensions for spacing — never inline numeric literals:

```swift
extension CGFloat {
    static let space4: CGFloat = 4
    static let space8: CGFloat = 8
    static let space12: CGFloat = 12
    static let space16: CGFloat = 16
    static let space20: CGFloat = 20
    static let space24: CGFloat = 24
    static let space32: CGFloat = 32
    static let space48: CGFloat = 48
    // ...
}
```

```swift
// Correct
.padding(.space16)
.spacing(.space8)
.frame(height: .space48)
VStack(spacing: .space12) { ... }

// Wrong — magic numbers
.padding(16)
.spacing(8)
```

## Colors

Colors live in `Assets.xcassets/Colors/` organized by category (Primary, Accent, Support, Special). Reference via asset catalog — no hardcoded hex values in Swift.

## Corner Radius, Border Width, Shadows

Define as `CGFloat` extensions or a dedicated tokens file in the design system folder. No inline magic values.

## Typography

All text styling goes through the `TextStyles` enum (see @.claude/rules/text-styling.md). Never call `.font(.system(size:))` directly.
