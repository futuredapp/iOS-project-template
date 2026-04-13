# Concurrency — Swift 6 default MainActor isolation

Projects seeded from this template enable **default `MainActor` isolation**. Every type, function, and extension without an explicit isolation annotation becomes `MainActor`-isolated.

## What becomes MainActor automatically

- All SwiftUI `View` structs, `@Observable` ComponentModels, Coordinators.
- Helpers, utilities, and extensions declared at file scope without `nonisolated`.

This is usually what you want. UI code runs on the main thread; forgetting `@MainActor` on a view model is no longer possible.

## What must be `nonisolated`

Any value type that:
- Is stored in `DataCache` (which is `@Observable @MainActor` but whose `Model: Equatable & Sendable` generic parameter must work nonisolated for cross-context equality/hash).
- Participates in `Equatable` comparisons reached from nonisolated code.
- Is `Sendable`-returned across isolation boundaries (network layer, background work, tests).

Concretely, **mark these `nonisolated`**:
- `DataCacheModel` — required.
- Top-level model types referenced by `DataCacheModel` (e.g. `Exhibit`, `UserProfile`).
- `CacheProjection` conformers and their `Data` structs.
- `StateInfoConfig`, `ComponentState`, `ItemState`, `ArrayState`, `MockableArray`, `Mockable` requirements.

```swift
nonisolated struct DataCacheModel: Equatable, Sendable {
    var exampleItem: ExampleItem?
}

nonisolated struct ExampleItem: Equatable, Sendable, Identifiable {
    let id: String
    var title: String
}
```

## Extension gotcha

Nested types **inside an extension** do not inherit the extended type's isolation. In Swift 6 default-MainActor mode they pick up `MainActor`, which breaks equality on a `nonisolated` outer type:

```swift
// BROKEN — extension adds a MainActor-isolated nested type
nonisolated struct DataCacheModel: Equatable, Sendable {
    var exampleItem: ExampleItem?
}
extension DataCacheModel {
    struct ExampleItem: Equatable, Sendable, Identifiable { ... } // MainActor
}
```

Fix: declare the nested type inside the struct body (it inherits `nonisolated`), or move it to file scope with an explicit `nonisolated` annotation.

## Sendable closures

`async` closures stored inside model/state types (e.g. `StateInfoConfig.Action.action`) must be `@Sendable`:

```swift
struct Action: Equatable {
    let title: String
    let action: @Sendable () async -> Void
}
```

## Do not

- Do not add `@MainActor` to models, views, or coordinators. It's already the default. Redundant annotations create noise and occasionally conflict with protocol requirements.
- Do not sprinkle `Task { @MainActor in ... }` — you're already on MainActor. Use a plain `Task` and only `nonisolated` out when you need to escape.
- Do not mark UI helper views (e.g. `StateInfoView`, `ComponentStateView`) as `nonisolated`. They live on MainActor.
