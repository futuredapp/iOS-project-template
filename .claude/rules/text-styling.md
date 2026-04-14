---
paths:
  - "**/*View*.swift"
  - "**/*Component*.swift"
  - "**/*UI*.swift"
  - "**/UI/**/*.swift"
  - "**/TextStyle*"
  - "**/Theme/**/*.swift"
  - "**/DesignSystem/**/*.swift"
---
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
- Apply via `.textStyle(_:foregroundColor:)`; never call `.font(.system(size:))` in a view.

```swift
// Correct
Text("Welcome")
    .textStyle(.title1(.semibold))

// Wrong — raw font
Text("Welcome")
    .font(.system(size: 28, weight: .semibold))
    .lineSpacing(6)
```

## Supporting Dynamic Type

`TextStyle` handles Dynamic Type scaling internally. Do not override with fixed `.font(.custom:size:)` unless the design explicitly calls for a non-scaling label (in which case document why).

Sheets with dynamic content should measure their height and use `.presentationDetents([.height(measuredHeight)])` so the sheet grows with the user's text size.
