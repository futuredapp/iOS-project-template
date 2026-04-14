# Architecture — FuturedKit MVVM-C

Every scene in the app follows **MVVM-C** via `FuturedArchitecture`. Concurrency rules below rely on **Swift 6 default `MainActor` isolation** — the app target must enable it.

## Scene layout

Each scene lives in its own folder under `Scenes/` with at minimum:

- `<Name>Component.swift` — SwiftUI `View` struct.
- `<Name>ComponentModel.swift` — `@Observable` final class implementing `<Name>ComponentModelProtocol`, which conforms to `ComponentModel` from FuturedArchitecture.
- For data-driven scenes, add `<Name>CacheProjection.swift` (see `state-management.md`).

## Component (View)

Binding to the model is done through a generic parameter so the model is injectable (real or mock in previews):

```swift
struct ExampleComponent<Model: ExampleComponentModelProtocol>: View {
    @State var model: Model

    var body: some View {
        content
            .task { await model.onAppear() }
    }

    private var content: some View { ... }
}
```

Rules:
- `@State var model: Model` — **not** `@StateObject`, **not** `@ObservedObject`. Models are `@Observable` classes in Swift 6.
- Keep the body thin. Pull any non-trivial subtree into a private computed `var` (`content`, `header`, `list`, …).
- No business logic, no API calls, no navigation in the View.

## ComponentModel (ViewModel)

```swift
@Observable
final class ExampleComponentModel: ExampleComponentModelProtocol {
    let onEvent: (Event) -> Void

    private let dataCache: DataCache<DataCacheModel>

    init(
        dataCache: DataCache<DataCacheModel>,
        onEvent: @escaping (Event) -> Void
    ) {
        self.dataCache = dataCache
        self.onEvent = onEvent
    }

    func onAppear() async { ... }
}

extension ExampleComponentModel {
    enum Event { case ... }
}
```

Rules:
- `@Observable final class`, `MainActor` by default — do not mark `@MainActor` explicitly, it's redundant in Swift 6 default mode.
- A protocol `<Name>ComponentModelProtocol: ComponentModel` declares the public API. Always ship a `#if DEBUG` mock implementation for previews.
- Coordinator-bound events travel out of the model via `onEvent: (Event) -> Void`. Never call the coordinator directly.
- State is observed, not copied. See `state-management.md` for the computed-projection pattern over `DataCache`.

## Coordinator (Flow / Tab)

Navigation and dependency injection belong to coordinators:

- `NavigationStackCoordinator` for push/pop flows.
- `TabCoordinator` + `TabViewFlow` for tab-based flows; each tab owns its own child `FlowCoordinator`.
- `AppCoordinator` is the app root.

Rules (see also `navigation.md`):
- Coordinators own `path: [Destination]` and `modalCover: ModalCoverModel<Destination>?` state.
- `Destination` is an `@EnumIdentable nonisolated enum` with associated values where needed.
- Components never create coordinators, never `NavigationLink`-navigate, never call `present(_:)` on a UIKit controller.

## Dependency Injection

A single `Container` (in `Container.swift`) owns services and caches. The `AppCoordinator` constructs it; child coordinators receive it by reference. Do not use singletons, do not reach for globals, do not create ad-hoc `UserDefaults.shared` accessors in views.

## Modals

- Reusable modals: `ModalCoverModel<Destination>` on the coordinator.
- View-scoped modals (sheets whose data and callbacks belong to a single parent Component/ComponentModel): present directly from that Component using `.sheet` bound to a parent ComponentModel property. Do not pollute the coordinator with one-off sheets.

## Files to use (and not reinvent)

- `DataCache<Model>` — `@Observable @MainActor` cache. Mutate via `update(with:)`, `update(_:with:)`, and `populate(_:with:)`. Do not store raw `@Published` state for shared data.
- `AlertModel` + `.defaultAlert(model:)` — SwiftUI alert wrapper. Don't hand-roll alert state.

## Scaffolding

New scenes are created via the FuturedKit Xcode templates (`File → New → File from Template → Futured`). Choose:
- **Scene** — plain Component/ComponentModel.
- **Resource Scene** — same plus a typed `Resource` for per-scene inputs.
- **Projection Scene** — adds a `CacheProjection` stub for data-driven scenes.

Hand-writing these files produces drift. Use the templates and edit the result.
