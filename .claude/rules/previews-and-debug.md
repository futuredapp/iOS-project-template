# Previews and debug code

## `#if DEBUG` wrapping

All preview-only code must be inside `#if DEBUG ... #endif`:

- `#Preview` blocks themselves are stripped by the compiler, but **helper functions, mock factories, and extensions used only by previews are not**.
- Wrap the entire preview section — `#Preview`, supporting private functions, mock convenience inits, and sample data — in a single `#if DEBUG` block at the bottom of the file.

```swift
// MARK: - Production code above

#if DEBUG
private extension ExampleData {
    static let previewSample = ExampleData(title: "Preview", count: 3)
}

#Preview {
    ExampleComponent(model: MockExampleComponentModel())
}
#endif
```

Rules:
- `#if DEBUG` goes around the **entire preview section**, not around each individual item.
- Mock ComponentModel implementations (`MockExampleComponentModel`) that exist solely for previews live inside `#if DEBUG`. The protocol declaration in `architecture.md` already mandates shipping a mock — this rule clarifies it must be debug-only.
- Do not wrap production-visible `Mockable` conformances (used by `CacheProjection.empty(state:)`) in `#if DEBUG` — those are needed at runtime for loading/empty states.
- When in doubt: if removing the code would break a release build, it does not belong in `#if DEBUG`.
