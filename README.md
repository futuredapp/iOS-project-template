# ~~Project name~~ (iOS)

![Bitrise](https://img.shields.io/bitrise/appid.svg?token=apptoken)

~~Short project description.~~

## Project info

- Deadline: ~~**--. --. ----**~~
- Next release: ~~**1.0.0**~~
- Deployment target: ~~**12.0**~~
- Bundle identifier: ~~`com.thefuntasty.project`~~
- Supports: ~~**Dark mode, landscape orientation, iPadOS, watchOS**~~
- Design: ~~Figma (add link)~~
- ~~Backend: Apiary (add link)~~

### Team:

- ~~Jana Nováková, PM, <jana.novakova@thefuntasty.com>~~
- ~~Jan Novák, iOS developer, <jan.novak@thefuntasty.com>~~
- ~~John Newman, tester, <john.newman@thefuntasty.com>~~

## Configuration management

### Tools

- Language: ~~**Swift 5.0**~~
- IDE: ~~**Xcode 11.0**~~
- Dependency management: ~~**[Swift package manager](https://swift.org/package-manager/)**~~
- Command line tools: **[Fastlane](https://docs.fastlane.tools)**
- Code style:
	- **[SwiftLint](https://swift.org/package-manager/)**
	- **[Danger](https://github.com/thefuntasty/danger)**
- ~~Localizations: Czech, English – **[POEditor](https://poeditor.com)**~~

### Dependencies

- ~~**[FTAPIKit](https://github.com/thefuntasty/FTAPIKit)** (Declarative access to REST API.)~~
- ~~**[FTTestingKit](https://github.com/thefuntasty/FTTestingKit)** (Helpers for testing long-running tasks and generating mockups)~~
- ~~**[FuntastyKit](https://github.com/thefuntasty/FuntastyKit)** (Basics of MVVM-C architecture, coordinators, UIKit extensions and helpers.)~~
- ~~**[PromiseKit](https://github.com/mxcl/PromiseKit)** (Functional library for chaining and using backround and long running tasks.)~~

## Installation

1. Install all required tools:
	- Install ruby: `brew install ruby`
	- In the project folder install all ruby tools: `bundle install`
2. Download development provisioning profiles and certificate: `bundle exec fastlane provisioning`
3. Build using Xcode or using Fastlane:
	- Debug build and run tests: `bundle exec fastlane test`
	- Build for enterprise distribution and submit to App Center: `bundle exec fastlane enteprise`
	- Build and submit to App store connect: `bundle exec fastlane beta`
