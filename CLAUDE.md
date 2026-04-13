# Futured iOS project — Claude guide

This repository is the seed template for new Futured iOS apps. Apps cloned from here use **FuturedKit** (`FuturedArchitecture` + `FuturedHelpers`), **Swift 6** with default `MainActor` isolation, and **MVVM-C** with SwiftUI.

**Before writing Swift code, read the rules below.** They are not optional guidance — they encode architectural decisions other projects have already validated.

## Rules

@.claude/rules/general.md
@.claude/rules/architecture.md
@.claude/rules/state-management.md
@.claude/rules/concurrency.md
@.claude/rules/navigation.md
@.claude/rules/futured-macros.md
@.claude/rules/helpers.md
@.claude/rules/text-styling.md
@.claude/rules/swiftlint.md

## Project setup

- Language: **Swift 6** (default actor isolation: `MainActor`)
- UI: SwiftUI only — no UIKit unless wrapping a system API
- Dependency management: Swift Package Manager
- Lint: SwiftLint — see `.swiftlint.yml`
- Automation: Fastlane (`bundle exec fastlane ...`)
- Code review: Danger (`Dangerfile`)

## Typical task flow

1. **Scaffold** new scenes via the Xcode templates shipped with FuturedKit (`SwiftUI App`, `Scene` with `Projection Scene` variant, `Flow Coordinator`, etc.). Do not hand-roll Component/ComponentModel files.
2. **Implement** the scene following the rules — especially `state-management.md` for anything data-driven.
3. **Lint** locally (`swiftlint lint`) before committing.
4. **Commit** — never add `Co-Authored-By` footers.

## What lives where

- `Template/` — the source project that becomes a new app after search-and-replace.
- `.cursor/rules/` — the Cursor equivalents of these rules. Keep both sets in sync when updating; the Cursor versions use `.mdc` with YAML frontmatter but express the same policies.
- `.claude/rules/` — the Claude versions imported above.
- `.swiftlint.yml` — linter configuration; always reflects current rules.
- `fastlane/` — provisioning, builds, uploads.
