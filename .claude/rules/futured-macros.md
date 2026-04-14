---
paths:
  - "**/*.swift"
---
# FuturedMacros

`futured-macros` is a package dependency that ships a handful of Swift macros. Use them; do not reinvent their output.

## `@ProxyMembers`

Forwards member access from a wrapper to an inner value type via `@dynamicMemberLookup`. Used primarily on `CacheProjection` types.

Requirements:
- The enclosing type **must** be marked `@dynamicMemberLookup`.
- Apply to a stored property that holds a value type (typically the `Data` struct on a projection).
- Import `ProxyMembers`.

```swift
import ProxyMembers

@dynamicMemberLookup
nonisolated struct ExampleCacheProjection: CacheProjection {
    var state: ComponentState
    @ProxyMembers var data: ExampleData
    // Callers write projection.title, not projection.data.title.
}
```

Do not hand-roll `subscript(dynamicMember:)` — the macro handles it.

## `@EnumIdentable`

Generates `Identifiable` conformance for enums with associated values while preserving those values and producing stable identifiers.

Requirements:
- Apply to the enum declaration.
- Parameter labels containing `id` contribute to the identity (e.g. `case detail(id: String, tab: Int)` identifies by `id`).

```swift
@EnumIdentable
nonisolated enum Destination {
    case detail(id: String)
    case editor(draftId: String, template: Template)
    case settings
}
```

Use for coordinator `Destination` enums, SwiftUI list item enums, and any diffable enum state.

Do not hand-roll an `id` property that maps cases to strings — the macro produces a more precise identity.

## When macros aren't the right tool

- Trivial forwarding of a single property: a plain computed var is clearer than `@ProxyMembers`.
- Identifiable types with one case: just add `Identifiable` conformance manually.

Macros pay off when they delete boilerplate that would otherwise be repeated across many sites.
