# Navigation

Navigation is a coordinator concern. Components never call `NavigationLink(destination:)`, never assign to `path` themselves, never push/pop imperatively.

## Stack-based flows

Use `NavigationStackCoordinator` + `NavigationStackFlow`:

```swift
@Observable
final class ExampleFlowCoordinator: NavigationStackCoordinator {
    var path: [Destination] = []
    var modalCover: ModalCoverModel<Destination>?

    static func rootView(with instance: ExampleFlowCoordinator) -> some View {
        NavigationStackFlow(coordinator: instance) {
            ExampleComponent(model: ...)
        }
    }

    @ViewBuilder
    func scene(for destination: Destination) -> some View { ... }
}

extension ExampleFlowCoordinator {
    @EnumIdentable
    nonisolated enum Destination {
        case detail(id: String)
        case settings
    }
}
```

## Tab-based flows

Use `TabCoordinator` + `TabViewFlow`. Each tab has its own child `NavigationStackCoordinator`. The tab coordinator owns only the selected tab and the root of each tab's flow.

## Modal sheets

- **Shared**: `modalCover: ModalCoverModel<Destination>?` on the coordinator. Reach `present(_:)` / `dismissModal()`.
- **View-scoped**: when a sheet's inputs and callbacks belong to a single parent Component, declare `@State` on the parent and bind with `.sheet(item:)`. Do not push view-scoped state into the coordinator.

## Destination enum

- `@EnumIdentable` to auto-generate `Identifiable` conformance while preserving associated values.
- `nonisolated enum` — destinations are enqueued in `path`/`modalCover` which can be touched from non-UI paths.
- Names describe the destination, not the trigger. `.detail(id:)`, not `.didTapDetail`.

## Events out of components

Components send intent to their coordinator via `onEvent: (Event) -> Void`. The coordinator switches on the event and calls `navigate(to:)` or `present(_:)`. Components do not know their coordinator's API.

```swift
// In the coordinator's rootView closure:
ExampleComponent(model: ExampleComponentModel(
    dataCache: container.dataCache,
    onEvent: { [weak instance] event in
        switch event {
        case .openDetail(let id): instance?.navigate(to: .detail(id: id))
        case .openSettings: instance?.present(.settings, style: .sheet)
        }
    }
))
```
