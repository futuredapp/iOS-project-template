# AGENTS.md

Guidance for coding agents (Claude Code, Codex, Cursor, …) working in this repository. `CLAUDE.md` is a symlink to this file; keep `AGENTS.md` the single source of truth.

<!-- Maintainers: keep this file under 200 lines. Add a rule only when an agent got it
     wrong twice or a reviewer had to explain it. If SwiftLint/SwiftFormat can enforce a rule, put it
     there instead of here. Replace every TODO when starting a project; delete sections that do not apply. -->

## Project

- If the TODO lines below are still here, ask for the values and fill them in before doing anything else.
- TODO: one sentence on what the app does. Deployment target: iOS XX. Localizations: cs, en.
- TODO: backend kind (REST via FTAPIKit / GraphQL via GraphQLAPIKit), where the base URL lives, third-party SDKs (Firebase, …).
- TODO: anything an agent cannot infer from code — generated files, flaky simulators, external dashboards, approval steps.
- Team, links and release info live in `README.md`. Futured iOS standards: https://engineering.futured.app/teams/ios/

## Commands

```bash
bundle install                                    # Ruby deps (Fastlane)
bundle exec fastlane provisioning                 # development certificate + profiles
brew install swiftlint swiftformat                # binaries used by the Xcode build phases

# Build — the generic destination works on any machine
xcodebuild -project AppName.xcodeproj -scheme AppName \
  -destination 'generic/platform=iOS Simulator' -skipMacroValidation build

# Tests need a concrete simulator: take a UDID from -showdestinations
xcodebuild -project AppName.xcodeproj -scheme AppName -showdestinations
xcodebuild -project AppName.xcodeproj -scheme AppName \
  -destination 'platform=iOS Simulator,id=<udid>' -skipMacroValidation test
bundle exec fastlane test                         # same, the way CI runs it

# Format + lint the whole tree (build phases do this on every Xcode build)
swiftformat . && swiftlint --fix --quiet && swiftlint
```

- Run one `xcodebuild` at a time; concurrent builds lock DerivedData. Do not add `-derivedDataPath` unless asked.
- Build with `xcodebuild`, never `swift build`: the `swift` on `PATH` may not be the Xcode toolchain.
- CI (`.github/workflows/`) and the `beta`/`release`/`test` lanes come from Futured shared repos (`futuredapp/.github`, `futuredapp/fastlane`); the local `Fastfile` only sets environment variables.

## Working principles

- Simplest change that works. Delete before adding. No abstraction, helper or protocol until a second concrete use exists.
- Before writing a new type, open the nearest existing file of the same role (Component, ComponentModel, coordinator, service, test) and mirror its shape.
- Multi-file or unclear changes: state assumptions, list the files you will touch, then implement. Trivial fixes: just do them.
- Definition of done: the project builds, `swiftlint` reports no warnings on touched files, relevant tests pass, new views render in `#Preview`. Report exactly what you ran and what it returned.
- Never stage, commit, amend, push, rebase or otherwise change git state unless the user asks for it in the current conversation. Read-only git (`status`, `diff`, `log`, `show`, `blame`) is always fine.
- Code, comments, identifiers and commit messages in English. User-facing text goes through localization.

## Git workflow

- `develop` is the integration branch, `main` holds released code. Both are protected; changes land only via PR.
- Branches: `feature|fix|hotfix/<JIRA-ID>-short-description`, `housekeep/<topic>`, `release/<version>`.
- Commits follow Conventional Commits: `type(scope): description`, imperative present tense, subject under 50 characters, no trailing period (`feat(experts): add list search`). Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`. One concern per commit.
- PRs: at least one approval, green CI, screenshots or GIFs for UI changes. Use `/commit` and `/pull-request` (see Skills).

## Architecture — FuturedArchitecture (FuturedKit)

SwiftUI-only app on [FuturedKit](https://github.com/futuredapp/FuturedKit) (`FuturedArchitecture`, optionally `FuturedHelpers`) and [futured-macros](https://github.com/futuredapp/futured-macros) (`EnumIdentable`). Swift 6, `@Observable`, structured concurrency. No Combine, no `ObservableObject`, no UIKit scenes. Handbook: https://engineering.futured.app/teams/ios/ios_architecture/

```
AppName/
├── AppNameApp.swift          @main; creates AppCoordinator(container:) and sets appDelegate.delegate
├── AppDelegate.swift         UIApplicationDelegate adaptor forwarding to AppDelegateProtocol
├── AppCoordinator.swift      root coordinator; owns Container, exposes rootView, configures SDKs, routes deep links
├── Container.swift           DI hub: DataCache + every app-wide service, created once at launch
├── Configuration/            Debug/Beta/Release.xcconfig; Local.xcconfig holds secrets and is git-ignored
├── Model/                    nonisolated value types, DataCacheModel, app error type, and the template-generated
│                             state layer: ComponentState, ItemState, StateInfoConfig, CacheProjection, Mockable
├── Flow Coordinators/        @Observable final class XxxFlowCoordinator: @MainActor NavigationStackCoordinator
├── Scenes/<Name>/            <Name>Component.swift, <Name>ComponentModel.swift[, <Name>CacheProjection.swift | <Name>Resource.swift]
├── Services/                 protocol + ProductionXxxService; business logic, persistence, SDK wrappers
├── Networking/               FTAPIKit servers, Endpoints/<Feature>/, configurings, observers (REST projects)
├── UI/Views, UI/Modifiers    reusable views and modifiers; template ships ComponentStateView, ItemStateView, StateInfoView
└── Resources/                Assets.xcassets (Colors/, Icons/), Localizable.strings generated by ACKLocalization
```

Roles:

- **Component** — `struct XComponent<Model: XComponentModelProtocol>: View` holding `@State var model: Model` (plain `var model` when a parent view owns the model). Renders state and forwards user actions as plain method calls. No business logic, no navigation.
- **ComponentModel** — `XComponentModelProtocol: ComponentModel` + `@Observable final class` implementation + `#if DEBUG` mock conforming to the same protocol. Holds scene state, calls services/resources, reports upward through `onEvent(Event)`. Screen state goes through the template-generated state layer, not ad-hoc flags: the model exposes `var projection: XCacheProjection { XCacheProjection.data(from: dataCache.value) ?? .empty(state: .loading) }`, a `nonisolated struct` conforming to `CacheProjection` (`state: ComponentState` + `@ProxyMembers var data`, `import ProxyMembers`); the Component wraps its content in `ComponentStateView(state: model.projection.state)`. `ComponentState.empty`/`.error` require a `StateInfoConfig`, so every non-populated state is designed, never a silent placeholder. Use `ItemState` for one loadable item inside a populated screen.
- **FlowCoordinator** — owns `path: [Destination]` and `modalCover`, builds scenes in `scene(for:)`, handles child events. `Destination` is `@EnumIdentable nonisolated enum`. Capture the coordinator weakly in `onEvent` closures: `[weak self]` in methods, `[weak instance = instance]` in the static `rootView` (the explicit form avoids the Swift 6.4 implicit-strong-capture warning).
- **Container** — plain `final class` holding `DataCache<DataCacheModel>` and services. Coordinators receive the container and inject only the concrete dependencies each ComponentModel needs.
- **DataCache** — single source of truth for shared state. **Read it through computed properties** (`var items: [Item] { dataCache.value.items }`); a stored copy is a one-time snapshot and silently stops updating. Write with `update(with:)`, `update(\.key, with:)`, `populate(\.items, with:)`.
- **Service / Resource** — a service is app-wide (auth, API, persistence, analytics) and lives in `Container`; a Resource is per-scene data access with `Production` and `Mock` implementations behind one protocol.

Rules:

- New screen: create `Scenes/<Name>/` from the Xcode "Scene" template (variants: Scene, Resource Scene, Projection Scene) or `/component-create`, add a `Destination` case, return the component from `scene(for:)`, handle its events. Mirror a neighbouring scene for the exact shape.
- Modals only via `present(modal:type:)` / `modalCover` with a `Destination` case, dismissed with `dismissModal()`. Never raw `.sheet(isPresented:)` or `.fullScreenCover(isPresented:)`.
- Alerts: one `AlertModel?` per screen shown with `.defaultAlert(model:)`. Keep `.confirmationDialog` for action-sheet choices.
- `@ObservationIgnored` only on stored `var`s that must not drive view updates (in-flight `Task`s, internal flags). `let`s are never tracked, so leave them bare; never annotate computed properties.
- Deep links and notification targets enter through `AppCoordinator` and are routed to flow coordinators. Scenes never parse URLs.
- A coordinator's `onEvent` handler only navigates (`navigate(to:)`, `present(modal:type:)`, `pop()`, `dismissModal()`). Cache writes, service calls and business decisions stay in the ComponentModel.
- Logout and other session resets bubble up as an event to `AppCoordinator`, which resets `Container` state in one place.
- Every screen inside a `NavigationStack` sets `.navigationTitle` even when the bar is hidden; otherwise the back-button long-press menu shows blank entries.

## Swift 6 & concurrency

Build settings on **every** target (app, extensions, tests): `SWIFT_VERSION` 6.x, `SWIFT_APPROACHABLE_CONCURRENCY = YES`, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, `SWIFT_UPCOMING_FEATURE_MEMBER_IMPORT_VISIBILITY = YES`. Xcode 26+ project templates set them for new projects; re-check them on any target added later.

- Everything is MainActor by default. Do not add redundant `@MainActor`; keep only the `: @MainActor NavigationStackCoordinator` conformance the protocol needs.
- Opt out with `nonisolated` on value types (models, `DataCacheModel`, projections and their `Data`, `Destination` enums) so `Equatable`/`Hashable`/`Sendable` synthesize without isolation, and on extensions of those types. A nested type declared in an `extension` does not inherit `nonisolated`; declare it in the type body or mark it explicitly. Views and other UI helpers stay MainActor.
- IMPORTANT: every type conforming to an FTAPIKit protocol (`Endpoint`, `ResponseEndpoint`, `URLServer`, `RequestConfiguring`, `NetworkObserver`, …) and every WidgetKit, AppIntents, ActivityKit, `URLSessionDelegate` or `BGTaskScheduler` type must be `nonisolated struct` / `nonisolated final class`. A MainActor-isolated endpoint compiles, but the nonisolated request builder reads its `body`/`headers` as empty: POSTs leave with no body and no error (hit in production on a Futured project). A clean build is not evidence here.
- CPU-heavy work: an `@concurrent` function (Swift 6.2+, Xcode 26+) that returns a value, awaited from a `Task`. Never `Task.detached` or `MainActor.run`; `await` hops back to MainActor by itself.
- `@Sendable` SDK callbacks (Firebase, AVFoundation, notifications) that touch MainActor state: wrap the body in `Task { @MainActor in … }`. Prefer `NotificationCenter.default.notifications(named:)` sequences over `addObserver`.
- `MemberImportVisibility` is on: import the defining module explicitly (`import Observation` in every ComponentModel file, `import EnumIdentable` for `@EnumIdentable`, `import ProxyMembers` for `@ProxyMembers`).
- Async APIs are `async throws`; use typed throws (`throws(AppError)`) once the project defines a domain error. No completion handlers, no `Result` for async work.

## Networking

- REST → **FTAPIKit 2.x**: one endpoint per file under `Networking/Endpoints/<Feature>/<Action><Entity>Endpoint.swift`; servers conform to `URLServer`; pick the endpoint protocol by the decision tree in `/ftapikit-expert`. Cross-cutting headers belong in a `RequestConfiguring`, request logging in a `NetworkObserver` behind `#if DEBUG`.
- GraphQL → **GraphQLAPIKit** (Apollo): operations in `GraphQLGenerated/{Queries,Mutations,Fragments}/*.graphql`, generated Swift is committed, codegen runs as a build phase. Reuse existing fragments before adding fields. Details in `/graphqlkit-expert`.
- An `ApiService` protocol wraps the adapter so ComponentModels and Resources never see Apollo or `URLSession` types; the `Production…` implementation maps transport errors to the app error type.
- Base URLs and keys come from `.xcconfig` via Info.plist and FuturedHelpers `ConfigKey`; secrets only in the git-ignored `Local.xcconfig`. Check FuturedHelpers (and FTNetworkTracer for request logging) before writing a helper.
- Before calling something a backend bug, reproduce it against the environment that has real data, with the same headers and query the app sends.

## Code style

Enforced by **SwiftFormat** (`.swiftformat`) and then **SwiftLint** (`.swiftlint.yml`) as build phases; both rewrite files in place. The FuturedKit app template generates both phases; after creating the project move them above Compile Sources (SwiftFormat first). Anything they autofix is not worth a review comment. Rules they cannot enforce:

- Comments are rare, one line (two at most), and say *why*. Exception: doc comments describing function parameters may use one line per parameter. No file headers (Xcode adds them, SwiftFormat leaves them alone). Never narrate what the code already says.
- `// MARK: Section` without dash. Typical sections: `// MARK: Views`, `// MARK: Actions`, `// MARK: Utilities`.
- Member order is a soft rule; mirror the sibling file first. Default: stored properties → computed properties → `init` → public/internal API in workflow order → private helpers under `// MARK: Utilities`. Views: `body` first, then helper views. Protocol conformances in trailing extensions.
- `final class` by default. Property wrappers limited to `@State`, `@Binding`, `@Environment`, `@FocusState`; never `@StateObject`, `@ObservedObject`, `@EnvironmentObject`.
- No force unwrap, force cast or force try outside tests and previews.
- No one-liner closures or functions; even `Task { await x() }` is multi-line. Inline braces only for void early exits (`guard cond else { return }`); a non-void `return` goes on its own line.
- Pattern matching: `case let .failure(error)`. Pass method references (`action: model.save`) instead of `{ model.save() }` when the signature matches.
- `[weak self]` closures: optional chaining (`self?.`) when the body is short; `guard let self else { return }` only for multi-statement bodies.
- `String` raw-value enums for stable keys (analytics, `UserDefaults`) instead of switch-to-string helpers.
- OS-version branches: mark the old path `@available(iOS, deprecated: <version>, message: "…")` so it is flagged once the deployment target rises.
- Skip explicit `self.` and `return` where the compiler does not need them, but do not touch existing code just for that.
- `DateFormatter`s are `static let`s on an extension, never created in `body`. Constant URLs use a `URL(staticString:)` helper instead of `URL(string:)!`.

## SwiftUI

- Every view gets `#Preview` with its `…Mock` model. One `#if DEBUG` block wraps the whole preview section including mock models and sample data; `Mockable` conformances stay outside it, `.empty(state:)` needs them at runtime.
- Colors come from `Assets.xcassets/Colors`, fonts from the project typography helper. No system colors or fonts for styled UI once the project has a design system (`Color(.separator)` on dividers is the accepted exception). Before building a new visual pattern, find the closest existing one and match it.
- Design tokens: typography through a `TextStyles` enum backed by FuturedHelpers `TextStyle` (`.textStyle(_:foregroundStyle:)` in one modifier), spacing and corner radii as named `CGFloat` tokens. No magic numbers or raw `.font(.system(size:))` in feature code.
- Layout: `.frame(maxWidth: .infinity, alignment:)` instead of `Spacer()`; `List`/`LazyVStack` for long content; keep `body` a composition of named helper views. No fixed `.frame(width:height:)` on the root of a reusable view.
- Interaction: animate state changes with `.animation(_:value:)` on the view, not `withAnimation`; a button running async work disables itself and shows progress while it runs; give tappable rows `.contentShape(.rect)`. Remote images go through one app-level image view, never raw `AsyncImage`.
- Custom modifiers are a `private struct: ViewModifier` exposed through a `View` extension.
- Modifier order: view-specific → navigation/toolbar → `.task`/`.onAppear`/`.onChange`. A modifier after a closing `}` starts a new line.
- Dynamic Type: text styles, not fixed sizes; `@ScaledMetric` for icon and frame sizes; `minHeight` rather than fixed heights on text containers.
- Localization: strings live in the project's Google Sheet and ACKLocalization pulls them into `Localizable.strings` (`localization.json`, run the `Localization` target); keys are lowerCamelCase; never hand-edit the generated files or add string literals in views. Projects that use a String Catalog instead: `Text("literal")` localizes, `Text(variable)` does not, so view helpers take `LocalizedStringKey`, not `String`.
- Accessibility baseline: labels on icon-only controls, Reduce Motion gates the animation not the state change, colour is never the only cue. Test identifiers via `.accessibilityIdentifier` referencing constants, never string literals (`/add-test-tags`).

## Testing

- **Swift Testing** (`@Test`, `#expect`, `#require`) in `AppNameTests/`. `@Suite` only for traits or a display name.
- Test ComponentModel logic and services through their protocols with hand-written mocks; keep test fixtures separate from `#Preview` mocks.
- Every lookup or predicate test includes a non-matching case; otherwise an implementation that ignores its argument passes.
- Propose the scenarios before writing tests, avoid duplicate coverage, use the minimal data that proves the behaviour.

## Skills & agents (Claude Code, Futured marketplace)

Company-maintained plugins live in [futuredapp/FTClaudeMarketplace](https://github.com/futuredapp/FTClaudeMarketplace). `.claude/settings.json` in this repo registers the marketplace and enables the iOS set, so trusting the folder installs them. Marked entries (*) are not enabled by default: install `knowledge-hub` and `futured-git-workflows-plugin` via `/plugin`. Reach for them at these points:

| When | Use |
|---|---|
| Unclear or large feature request | `/interview` to produce a spec, then plan mode |
| Architecture or FuturedKit question, new screen | `/futuredkit-expert`, `/component-create <Name>`; `ios-architect` agent for design trade-offs |
| New endpoint or API-layer work | `/ftapikit-expert` (REST) or `/graphqlkit-expert` (GraphQL); `networking-architect` agent |
| "How did another Futured project do X?" | `/knowledge-hub` * (needs company network) |
| Figma hand-off of colors, typography, icons | `/figma-to-xcode` |
| Adding UI automation identifiers | `/add-test-tags` |
| Before opening a PR, and after addressing review comments | `/ios-review` — independent multi-lens review against this file; `code-reviewer` agent for a quick FuturedKit pass |
| Accessibility claims or VoiceOver work | `/accessibility-nutrition-labels`, `/swiftui-voiceover` |
| Performance regression (launch, hangs, hitches, memory) | `/performance-metrics [metric]` |
| Committing and opening the PR | `/commit`, `/pull-request` |
| CI workflow changes | `/workflow-create`, `/workflow-review` * |
| Official standards lookup | `/handbook ios <topic>` |
| Legacy FuturedKit or FTAPIKit 1.x code | `/migrate-futuredkit-swift6`, `/migrate-ftapikit-to-2` |

A review finding must quote a rule from this file or give a concrete failure scenario. When a divergence turns out to be deliberate, record it here as one line so the next review does not repeat it.

## Review checklist

- Component, ComponentModel and coordinator roles respected; navigation only through `Destination`.
- Cache-derived state is computed, not stored.
- No redundant `@MainActor`; FTAPIKit, WidgetKit and AppIntents types are `nonisolated`.
- No `Task.detached`, `MainActor.run`, Combine, `ObservableObject`, force unwrap or `Spacer()` for alignment.
- New views ship with `#Preview`, asset colors and typography, Dynamic Type, localized strings and test identifiers.
- New logic has tests, `swiftlint` is clean, and this file is updated when a convention changed.
