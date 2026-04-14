# General Swift rules

## Immutability

Prefer `let` over `var`. Mutable state must be justified. Use value types (struct/enum) by default; reach for `class` only when you need reference semantics, identity, or `@Observable`.

## Error handling

Use `throw`ing functions and `try`/`catch`. Do not encode errors as optional return values — `nil` means "absent", not "failed".

## Implicit returns & force operations

- Single-expression functions/properties omit the `return` keyword (SwiftLint enforces `implicit_return`).
- Never use `try!`, `as!`, or `!` (force unwrap) in production code. `fatalError(_:)` is acceptable only for truly unreachable states with a descriptive message.

## View modifier order

Order modifiers consistently: **UI → Navigation/Presentation → Action/Data**.

```swift
// Correct
Text("Hello, World!")
    .foregroundStyle(.blue)
    .padding()
    .navigationTitle("Greeting")
    .task { await viewModel.load() }
```

Screen-level views additionally apply `.background(...)` first, then navigation, then events.

## Access control on structs with custom init

When a struct has a custom `init`, all stored properties not accessed externally must be `private`. The init is the public API.

```swift
struct MyCard<Content: View>: View {
    private let title: String
    @ViewBuilder private let content: () -> Content

    init(title: String, @ViewBuilder content: @escaping () -> Content) {
        self.title = title
        self.content = content
    }
}
```

## Safe URL construction

For compile-time constant URLs (API base URLs, deep-link schemes, known endpoints), use a `URL(staticString:)` extension instead of force-unwrapping:

```swift
extension URL {
    init(staticString: StaticString) {
        guard let url = URL(string: "\(staticString)") else {
            fatalError("Invalid static URL: \(staticString)")
        }
        self = url
    }
}

// Usage
let termsURL = URL(staticString: "https://example.com/terms")
```

This avoids `URL(string:)!` with a swiftlint disable comment while still failing loudly in development if the string is malformed.

## DateFormatter — reuse, do not recreate

`DateFormatter` creation is expensive. Never create one inside a `body` or a function called on every render. Define formatters as `static let` on an extension or a dedicated type:

```swift
extension DateFormatter {
    static let eventDate: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter
    }()
}

// Usage
Text(DateFormatter.eventDate.string(from: event.date))
```

For simple, non-reused formatting, `.formatted()` on `Date` is acceptable — it is internally cached by the system.

## Tap-target hit areas

Empty whitespace inside a `Button` or gesture container is not tappable. Apply `.contentShape(.rect)`:

```swift
Button(action: onTap) {
    HStack {
        Text("Label")
        Spacer()
    }
    .contentShape(.rect)
}
```
