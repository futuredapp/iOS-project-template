# {{APP_NAME}} — Claude guide

**After cloning this template**, replace all `{{placeholders}}` in this file with project-specific values. Keep this file up to date — update the reusable components table, key services, and project structure as the project evolves.

{{Brief description of the app — what it does, who it's for, 2-3 sentences.}}

## Principles

- **SOLID** — single responsibility per type, depend on protocols not concrete classes, open for extension.
- **DRY** — before creating any view, component, or modifier, check `UI/Components/` and `UI/Modifiers/` for existing reusable pieces. Extract shared UI into reusable components; don't duplicate.
- **MVVM-C** — all features follow the ComponentModel + Coordinator architecture from FuturedKit. No exceptions.

## Reusable UI components

Before creating or modifying UI, scan `UI/Components/` for existing reusable views. If a new reusable component is added, update this table. **This table must stay in sync with `UI/Components/`.**

| Component | Purpose |
|-----------|---------|
| {{e.g. `AppButton`}} | {{Primary/secondary action buttons}} |
| {{e.g. `AppTextField`}} | {{Styled text input with validation}} |
| {{Add components as they are created}} | |

## Project setup

- Language: **Swift 6** (default actor isolation: `MainActor`)
- UI: SwiftUI only — no UIKit unless wrapping a system API
- Minimum iOS: {{iOS version, e.g. 17.0}}
- Dependency management: Swift Package Manager
- Lint: SwiftLint — see `.swiftlint.yml`
- Automation: Fastlane (`bundle exec fastlane ...`)

## Build configurations

| Config | Bundle ID | API |
|--------|-----------|-----|
| DEBUG | `app.futured.{{app_id}}` | Development |
| BETA | `app.futured.{{app_id}}.beta` | Staging |
| RELEASE | `app.futured.{{app_id}}` | Production |

## Development commands

```bash
# Run tests
bundle exec fastlane test

# Build beta (TestFlight)
bundle exec fastlane beta

# Download provisioning profiles
bundle exec fastlane provisioning

# Lint
swiftlint lint
```

## Architecture rules

**Read these before writing Swift code.** They encode architectural decisions validated across Futured projects.

@.claude/rules/general.md
@.claude/rules/architecture.md
@.claude/rules/state-management.md
@.claude/rules/concurrency.md
@.claude/rules/navigation.md
@.claude/rules/futured-macros.md
@.claude/rules/helpers.md
@.claude/rules/ui-patterns.md
@.claude/rules/previews-and-debug.md
@.claude/rules/text-styling.md
@.claude/rules/swiftlint.md

## Project structure

**Update this tree to reflect the actual app structure.**

```
{{AppName}}/
├── App/                    # App entry point, AppDelegate
├── Container.swift         # DI container — services and caches
├── Model/
│   ├── API/Endpoints/      # FTAPIKit endpoint definitions
│   ├── DataCacheModel.swift
│   └── Domain/             # Business models (nonisolated, Equatable, Sendable)
├── Services/               # Protocol-based services
├── Flow Coordinators/      # Navigation coordinators
├── Scenes/                 # Feature screens
│   └── <SceneName>/
│       ├── <Name>Component.swift
│       ├── <Name>ComponentModel.swift
│       └── <Name>CacheProjection.swift
├── UI/
│   ├── Components/         # Reusable views
│   ├── Modifiers/          # View extensions
│   └── Theme/              # TextStyles, spacing, design tokens
├── Resources/              # Assets, localization
└── Extensions/
```

## Key services

**Keep this table in sync with `Container.swift`.** Update when adding or removing services.

| Service | Purpose |
|---------|---------|
| `APIService` | Backend communication via FTAPIKit |
| {{Add project-specific services here}} | |

## Common tasks

### Adding a new screen

1. Use FuturedKit Xcode templates: `File → New → File from Template → Futured`
2. Choose **Scene**, **Resource Scene**, or **Projection Scene** variant
3. Wire the component model in the parent coordinator's `scene(for:)` method
4. Add a `Destination` case in the coordinator's enum

### Adding a new service

1. Define a protocol in `Services/`
2. Create `Production<Name>Service` implementation
3. Create `Mock<Name>Service` for tests/previews
4. Register in `Container.init()`

## Notes

{{Add project-specific notes, quirks, known issues, ADR links here.}}
