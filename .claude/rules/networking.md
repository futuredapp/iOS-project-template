---
paths:
  - "**/API/**/*.swift"
  - "**/Endpoints/**/*.swift"
  - "**/Model/API/**/*.swift"
  - "**/Services/*Service*.swift"
  - "**/Services/*Adapter*.swift"
---
# Networking

## FTAPIKit (REST)

All REST networking uses `FTAPIKit`. Define endpoints as structs conforming to `Endpoint`:

```swift
struct GetUserEndpoint: Endpoint {
    let path: String = "/api/users/me"
}

struct UpdateUserEndpoint: Endpoint {
    let path: String = "/api/users/me"
    let method: HTTPMethod = .patch
    let body: UpdateUserRequest
}
```

Call via a protocol-based service wrapper with typed throws:

```swift
protocol APIService {
    func call<E: Endpoint>(response: E) async throws(AppError) -> E.Response
}
```

Do not use raw `URLSession` directly. Do not create ad-hoc networking helpers — all requests go through `FTAPIKit`.

## GraphQLAPIKit (GraphQL)

For GraphQL projects, use `GraphQLAPIKit` with Apollo iOS:

- `GraphQLAPIAdapterProtocol` for query/mutation execution.
- Set `APOLLO_CODEGEN_CONFIG_PATH` in the Fastlane `Fastfile` for automatic codegen before builds.
- Use `GraphQLAPIConfiguration` for endpoint URL, default headers, and observers.
- `GraphQLNetworkObserver` for request/response logging.

## Build Configuration → API URL

Standard environment mapping — configure via `ConfigKey` reading from `Info.plist`:

| Build Config | API Target |
|-------------|------------|
| DEBUG | Development / localhost |
| BETA | Staging |
| RELEASE | Production |

```swift
enum APIBaseURL: String, ConfigKey {
    // Value set per build configuration in xcconfig
}
```

## Network Observability

Use `FTNetworkTracer` for request/response logging:

- Attach as a `NetworkObserver` on the server instance.
- Supports both REST and GraphQL formatting.
- Use `MaskingUtilities` to redact sensitive headers (auth tokens, API keys) in logs.

## Error Handling

Networking errors are wrapped in the app's typed `AppError`:

```swift
enum AppError: Error {
    case networking(NetworkingError)
    case persistence(PersistenceError)
    case custom(ErrorViewConfiguration)
}

func fetchData() async throws(AppError) { ... }
```

Never throw raw `URLError` or `DecodingError` from the service layer — always map to `AppError`. The `ComponentModel` converts `AppError` to `ComponentState.error(StateInfoConfig(...))` for display.
