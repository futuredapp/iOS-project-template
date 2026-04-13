# FuturedHelpers

`FuturedHelpers` is the sibling library to `FuturedArchitecture` in FuturedKit. It carries reusable UI and non-UI helpers that do not belong to a specific scene.

**Before writing a helper, grep `FuturedHelpers` first.** Re-creating an existing helper fragments behavior across projects.

Known helpers:

- `ConfigKey` — read keyed values from `Info.plist` with typed accessors and optional Base64 decoding. Use for API keys, environment URLs, feature flags.
- `CoordinatorSceneFlowProvider` — protocol for composable, reusable scene flows that can be dropped into any parent coordinator.
- `SceneDelegate` helpers — lifecycle hooks (`sceneDidEnterBackground()`, `sceneWillEnterForeground()`) and environment injection for `UIWindowSceneDelegate` integration.
- `GalleryImagePicker`, `CameraImagePicker` — SwiftUI image pickers. Don't wrap `PHPickerViewController` by hand.
- `TextStyle` — underlying struct for the `TextStyles` enum pattern (see `text-styling.md`).

When extending `FuturedHelpers` in a specific project, do it as a local extension, not by copying the type.
