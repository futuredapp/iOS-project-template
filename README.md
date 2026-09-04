# ~~Project name~~ (iOS)

~~Short project description.~~

## Project info

- Deadline: ~~**--. --. ----**~~
- Next release: ~~**1.0.0**~~
- Deployment target: ~~**17.0**~~
- Bundle identifiers: ~~`app.futured.project`, `app.futured.project.beta, `app.customer.project``~~
- Supports: ~~**Dark mode, Landscape orientation, iPadOS, Accessibility**~~
- Design: ~~Figma (add link)~~
- Backend: ~~(add link)~~

### Team:

- ~~Jana Nováková, PM, <jana.novakova@futured.app>~~
- ~~Hans Novak, designer, <hans.novak@futured.app>~~
- ~~Jan Novák, iOS developer, <jan.novak@futured.app>~~
- ~~Hansina Novak, Android developer, <hansina.novak@futured.app>~~
- ~~John Newman, tester, <john.newman@futured.app>~~

## Configuration management

### Tools

- Language: ~~**Swift 6.3**~~
- IDE: ~~**Xcode 27.0**~~
- Dependency management: ~~**[Swift package manager](https://swift.org/package-manager/)**~~
- Command line tools: **[Fastlane](https://docs.fastlane.tools)**
- Code style:
	- **[SwiftLint](https://github.com/realm/SwiftLint)** (`.swiftlint.yml`)
	- **[SwiftFormat](https://github.com/nicklockwood/SwiftFormat)** (`.swiftformat`)
- Coding agents: **[AGENTS.md](AGENTS.md)** (`CLAUDE.md` is a symlink to it) — architecture, conventions and the Futured Claude skills to use
- ~~Localizations: Czech, English~~

### Dependencies

- **[FuturedKit](https://github.com/futuredapp/FuturedKit)** (`FuturedArchitecture`: coordinators, `ComponentModel`, `DataCache`; optionally `FuturedHelpers`)
- **[futured-macros](https://github.com/futuredapp/futured-macros)** (`FuturedMacros`: `@EnumIdentable`, `@ProxyMembers`)
- ~~**[FTAPIKit](https://github.com/futuredapp/FTAPIKit)** (Declarative access to REST API.)~~
- ~~**[GraphQLAPIKit](https://github.com/futuredapp/GraphQLAPIKit)** (Apollo-based GraphQL client.)~~

~~Manually added:~~
- ~~**[ACKLocalization](https://github.com/AckeeCZ/ACKLocalization.git)** (Localize your Cocoa apps from Google Spreadsheet.)~~

## Installation

In the project folder from Terminal:

1. `bundle install` - install gemfile dependencies
2. `brew install swiftlint swiftformat` - lint and format tools used by the build phases
3. `bundle exec fastlane provisioning` - download development provisioning profiles and certificate
4. build using Xcode
