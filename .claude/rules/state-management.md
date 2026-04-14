# State management — DataCache, CacheProjection, StateInfoView

Shared data flows from `DataCache<DataCacheModel>` → `CacheProjection` → `ComponentStateView` / `ItemStateView`. This pipeline is how every data-driven scene reads the cache; hand-rolled Combine subscriptions are obsolete in this project.

## DataCache

- One app-wide `DataCache<DataCacheModel>` in `Container`. Coordinators may create private caches for scoped flows.
- `@Observable @MainActor` — reading `dataCache.value` from a SwiftUI view body (or a `@Observable` model's computed property that the view reads) automatically registers observation.
- Mutate only via `update(with:)`, `update(_:with:)`, `populate(_:with:)`.

## CacheProjection

A `CacheProjection` is a value type that derives a scene's data from the cache.

**Why projections exist.** `DataCache` is the single source of truth for shared data. Each screen should derive its current state entirely from the cache — not from ad-hoc local variables. A `CacheProjection` decomposes that derivation into a clear mapping: cache values in, screen state out. This keeps the logic testable, declarative, and contained in one place.

**Why state and mock data are bundled.** The `.empty(state:)` factory pairs a `ComponentState` (`.loading`, `.empty`, `.error`) with `.mock` data. This is intentional: `.redacted(reason: .placeholder)` needs a fully populated view hierarchy to render shimmer placeholders correctly. By binding the loading state to mock data in the projection itself, we guarantee two things: (1) mock data never leaks into the `.ready` state, and (2) the `.ready` state is never shown while data is still loading.

```swift
@dynamicMemberLookup
nonisolated struct ExhibitDetailCacheProjection: CacheProjection {
    typealias ID = String // swiftlint:disable:this type_name

    var state: ComponentState
    @ProxyMembers var data: ExhibitDetailData

    static func empty(state: ComponentState) -> Self {
        Self(state: state, data: .mock)
    }

    static func data(for id: String, from cache: DataCacheModel) -> Self? {
        guard let detail = cache.exhibitDetails[id] else { return nil }
        return Self(state: .ready, data: ExhibitDetailData(detail: detail))
    }
}

nonisolated struct ExhibitDetailData: Equatable, Mockable {
    var detail: ExhibitDetail
    static let mock: Self = Self(detail: .mock)
}
```

Rules:
- `@dynamicMemberLookup` + `@ProxyMembers var data` — lets callers write `projection.title` instead of `projection.data.title`. Requires `import ProxyMembers`.
- `nonisolated` on both the projection struct and its `Data` struct — cross-isolation safety (see `concurrency.md`).
- `typealias ID` is only needed when the projection is keyed (ID ≠ Void). The protocol defaults `ID` to `Void`.
- `data(from:)` is always required. `data(for:from:)` has a default `nil` implementation when `ID == Void`; for real IDs, implement it.

## Observation — use computed properties

Expose the projection as a computed property on the ComponentModel:

```swift
@Observable
final class ExhibitDetailComponentModel: ExhibitDetailComponentModelProtocol {
    private let dataCache: DataCache<DataCacheModel>
    private let id: String

    var projection: ExhibitDetailCacheProjection {
        ExhibitDetailCacheProjection.data(for: id, from: dataCache.value)
            ?? .empty(state: .loading)
    }
}
```

Rules:
- **No Combine.** Do not write `dataCache.$value.compactMap(...).assign(to:)`. Do not store the projection as `@Published`. Reading `dataCache.value` inside the computed getter registers observation automatically because both types are `@Observable`.
- Mocks store the projection as a plain `var` for previews: `var projection: ExhibitDetailCacheProjection = .empty(state: .ready)`.

## States — ComponentState / ItemState / ArrayState

Three enums, three jobs:

| Type | Purpose | Empty case |
|------|---------|------------|
| `ComponentState` | Whole-screen lifecycle | `.empty(StateInfoConfig)` — config required |
| `ItemState<Value>` | Single data element inside a populated screen | no `.empty` — `.populated` implies presence |
| `ArrayState<Value>` | Collection state (cache-side) | no `.empty` — convert to `ItemState` for rendering |

`ArrayState` **does not have a dedicated view**. Always derive an `ItemState<MyListViewType>` via a computed property on the `Data` struct, then render with `ItemStateView`. Arrays almost always need filtering/sorting/grouping during render; converting up-front keeps that logic out of views.

## Rendering — ComponentStateView

```swift
var body: some View {
    ComponentStateView(state: model.projection.state) {
        content
    }
    .task { await model.onAppear() }
}
```

- The `.empty` and `.error` cases carry a `StateInfoConfig` and render via `StateInfoView` by default. To override, use the initializers that accept `emptyView:` / `errorView:` closures.
- `LoadingView == PopulatedView` — the convenience init reuses the populated view with `.redacted(reason: .placeholder)` applied. Custom loading views disable redaction.

## StateInfoConfig

Always construct a designed empty state. The `ComponentState.empty` case requires a config — there is no "silent empty". If the designer hasn't defined an empty state, ask for one before shipping.

```swift
StateInfoConfig(
    icon: Image(systemName: "tray"),
    title: "No exhibits yet",
    message: "Scan a code or browse the collection.",
    actions: [
        .init(title: "Browse", action: { [weak self] in await self?.browse() })
    ]
)
```

`StateInfoView` ships as a baseline SwiftUI implementation. **Each project must swap it for the design system's equivalent** — tokens, typography, button styles, spacing. The config shape stays the same; the view renders it with project-specific visuals.
