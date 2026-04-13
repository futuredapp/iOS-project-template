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
