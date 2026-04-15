# Text styling

Every project defines a central `TextStyles` enum that maps to `TextStyle` from `FuturedHelpers`. No raw font sizes, weights, or line heights anywhere else in the codebase.

## Pattern

```swift
import FuturedHelpers
import SwiftUI

public enum TextStyles {
    case caption(Font.Weight = .regular)
    case body
    case title1(Font.Weight = .regular)

    var textStyle: TextStyle {
        switch self {
        case let .caption(weight):
            TextStyle(
                fontType: .system(weight: weight, width: .standard),
                size: 11,
                lineHeight: 14
            )
        case .body:
            TextStyle(
                fontType: .system(weight: .regular, width: .standard),
                size: 17,
                lineHeight: 22
            )
        case let .title1(weight):
            TextStyle(
                fontType: .system(weight: weight, width: .standard),
                size: 28,
                lineHeight: 34,
                letter: .absolute(points: -0.5)
            )
        }
    }
}
```

## Rules

- Case names are semantic (`title1`, `body`, `caption`) — never size-based (`size28`, `font14`).
- Provide a sensible default weight; accept a `Font.Weight` associated value for customization.
- Include line height and letter spacing in the `TextStyle` when the design system specifies them.
- Apply via `.textStyle(_:)` or `.textStyle(_:foregroundStyle:)`; never call `.font(.system(size:))` in a view.
- For `Text`-specific styling (no lineSpacing/textCase/padding), use `.textStyleText(_:)` — needed when composing styled `Text` with `+` operator.

```swift
// Correct
Text("Welcome")
    .textStyle(.title1(.semibold))

// Wrong — raw font
Text("Welcome")
    .font(.system(size: 28, weight: .semibold))
    .lineSpacing(6)
```

## Combining text style with foreground color

When you need both a text style AND a foreground color, use the `textStyle(_:foregroundStyle:)` overload from `FuturedHelpers` — **do not** apply `.textStyle(...)` and `.foregroundStyle(...)` as separate modifiers:

```swift
// Correct — single modifier
Text("Caption")
    .textStyle(.bodySMRegular, foregroundStyle: Color(.textSecondary))

// Wrong — separate modifiers (extra render pass, inconsistent animation)
Text("Caption")
    .textStyle(.bodySMRegular)
    .foregroundStyle(Color(.textSecondary))
```

For `Text`-only composition (e.g. using `+` operator with styled runs), use `.textStyleText(_:foregroundStyle:)` instead.

