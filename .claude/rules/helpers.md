---
paths:
  - "**/*.swift"
---
# FuturedHelpers & Companion Frameworks

**Before writing a helper, check these libraries first.** Re-creating an existing helper fragments behavior across projects.

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

Underlying struct for the `TextStyles` enum pattern (see @.claude/rules/text-styling.md).

---

# Companion Frameworks

## FTNetworkTracer — Network Logging & Privacy

Network tracing library for request/response logging with privacy masking. Supports both REST and GraphQL.

**Key types:**
- `NetworkTraceEntry` — data struct for a network event (request/response/error) with `requestId` for correlation
- `NetworkTraceFormatter` — human-readable output with `.default`, `.compact`, `.verbose` configurations
- `MaskingUtilities` — privacy masking with three levels:
  - `.none` — development only, no masking
  - `.private` — selective masking with configurable exceptions (`unmaskedHeaders`, `unmaskedBodyParams`)
  - `.sensitive` — aggressive masking for production (strips bodies, variables, query params)
- `GraphQLFormatter` — pretty-prints GraphQL queries, removes `__typename` noise, masks query literals

**Usage pattern:** Create `NetworkTraceEntry` instances in your `NetworkObserver` implementation, then format for logs and mask for analytics:

```swift
let formatted = NetworkTraceFormatter.format(entry)              // dev logs
let masked = MaskingUtilities.mask(entry, configuration: .private) // analytics
```

The library does not include SwiftUI debug views — build your own list view over stored entries if needed.

## FormStateKit — Form Validation

SPM package (`futuredapp/FormStateKit`) for declarative form state and validation.

**Key types:**
- `FormModel` — protocol for form structs defining fields and validation rules
- `FormState<T: FormModel>` — state container holding form data + validation errors
- `FormValidation<T>` — single validation rule bound to a keyPath
- `FormValidationRule<Value>` — validation logic (built-in: `.required`, `.email`; extensible)

```swift
struct SignInForm: FormModel {
    var email: String
    var password: String
    static let empty = Self(email: "", password: "")

    let validations: [FormValidation<SignInForm>] = [
        FormValidation(for: \.email, description: "Required", rule: .required),
        FormValidation(for: \.email, description: "Invalid format", rule: .email),
    ]
}

// In ComponentModel:
@State var formState: FormState<SignInForm> = FormState(form: .empty)
guard formState.validate() else { return }
```

Bind fields with `$formState.form.email`, display errors with `formState.errors(for: \.email)`.

## SecureStorage — Keychain Wrapper

Local package pattern for typed Keychain access with optional biometric protection. Reference implementation: [jt-assets-ios/LocalPackages/SecureStorage](https://github.com/futuredapp/jt-assets-ios/tree/develop/LocalPackages/SecureStorage).

**Key types:**
- `SecureStorageManagerProtocol` — CRUD interface (`@mockable` for testing)
- `SecureStorageManager` — concrete Keychain implementation
- `KeychainServiceIdentifier` — namespace for stored items
- `SecureStorageManagerError` — typed errors (`.itemNotFound`, `.authorizationFailed`, `.userCanceled`)

**API pattern:**
```swift
// Save (async, optional biometric protection)
await keychainService.save(value: token, key: "authToken", withBiometricProtection: false, serviceIdentifier: .core, accessGroup: nil)

// Load (synchronous)
let token = try keychainService.load(AccessToken.self, key: "authToken", serviceIdentifier: .core, accessGroup: nil).get()

// Delete
await keychainService.deleteItem(key: "authToken", serviceIdentifier: .core, accessGroup: nil)

// Biometry check
keychainService.isBiometryAvailable
```

Register in `Container` as `SecureStorageManagerProtocol` for testability.
