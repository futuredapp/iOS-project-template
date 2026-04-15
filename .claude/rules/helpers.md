---
paths:
  - "**/*.swift"
---
# FuturedHelpers

Before writing a helper, check `FuturedHelpers` first. Re-creating an existing helper fragments behavior across projects.

## ConfigKey — Info.plist Configuration

Read typed values from `Info.plist` with automatic Base64 decoding support. Use for API keys, environment URLs, feature flags.

```swift
import FuturedHelpers

enum AppConfigKey: String, CaseIterable, ConfigKey {
    case apiKey = "API_KEY"
    case baseURL = "BASE_URL"
}

// Usage — returns decoded string or throws ConfigKeyError.valueNotFound
let key = try AppConfigKey.apiKey.value
```

Values are set per build configuration in `.xcconfig` files. Base64-encoded values are decoded automatically; plain strings pass through.

## CoordinatorSceneFlowProvider — Reusable Sub-Flows

Extract shared navigation flows into a reusable provider that can be embedded in any parent coordinator:

```swift
@MainActor
public protocol CoordinatorSceneFlowProvider {
    associatedtype Destination: Hashable & Identifiable
    associatedtype DestinationViews: View

    @ViewBuilder func scene(for destination: Destination) -> DestinationViews
    var navigateTo: (Destination) -> Void { get }
    var pop: () -> Void { get }
    // Optional: present, dismissModal, onModalDismiss, popTo
}
```

Wire up in the parent coordinator via lazy initialization:

```swift
private lazy var sharedFlow: SharedFlowProvider = {
    SharedFlowProvider(
        container: container,
        navigateTo: { [weak self] destination in
            self?.navigate(to: .embedded(destination: destination))
        },
        pop: { [weak self] in self?.pop() }
    )
}()
```

Then delegate in `scene(for:)`:
```swift
case let .embedded(destination):
    sharedFlow.scene(for: destination)
```

## SceneDelegate — App Lifecycle Integration

`AppSceneDelegate` protocol provides `@Observable` UIWindowSceneDelegate integration:

```swift
@Observable
final class MySceneDelegate: NSObject, AppSceneDelegate {
    var delegate: SceneDelegate?
    // UIWindowSceneDelegate methods...
}
```

Inject via `.environment()` and activate with `.set(appSceneDelegateClass:sceneDelegate:)` modifier on the root view.

## TextStyle

Underlying struct for the `TextStyles` enum pattern (see `@.claude/rules/text-styling.md`).

---

# Companion frameworks (reference only)

The helpers below are not shipped in every Futured iOS project. **Only consult these sections if the project already depends on the framework** — don't introduce any of them without a deliberate decision.

- **FTNetworkTracer** — request/response logging with privacy masking (`NetworkTraceEntry`, `MaskingUtilities`, `GraphQLFormatter`). See repo README.
- **FormStateKit** — declarative form state + validation (`FormModel`, `FormState<T>`, `FormValidation`, `FormValidationRule`). See repo README.
- **SecureStorage** — typed Keychain wrapper with biometric support (`SecureStorageManagerProtocol`, `KeychainServiceIdentifier`, `SecureStorageManagerError`). Register in `Container` as a protocol for testability. See `jt-assets-ios/LocalPackages/SecureStorage` for a reference implementation.

If a project needs detailed patterns for one of these frameworks, add a project-specific rule file (e.g. `.claude/rules/secure-storage.md`) rather than expanding this one.
