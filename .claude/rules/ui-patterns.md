# UI patterns

## Dynamic Type — `@ScaledMetric` for non-text elements

Text scales automatically via `TextStyle`. Icons, images, and fixed-dimension UI elements do not — they need `@ScaledMetric`:

```swift
@ScaledMetric private var scale: CGFloat = 1

Image(.checkmark)
    .resizable()
    .scaledToFit()
    .frame(width: 40 * scale, height: 40 * scale)
```

Rules:
- Every hardcoded `width`/`height` on an icon or image must be multiplied by a `@ScaledMetric` scale factor.
- Declare one `@ScaledMetric private var scale: CGFloat = 1` per View that contains fixed-size non-text elements.
- Do not set image sizes via `.font(.system(size:))` — use `.resizable().scaledToFit().frame(width:height:)` with scale.

## Async buttons with loading state

Action buttons that trigger async work must:
1. Accept `() async -> Void` as the action.
2. Auto-disable while the action executes.
3. Show a loading indicator during execution.

This prevents double-tap and gives the user immediate feedback.

```swift
struct AppButton: View {
    @State private var isLoading: Bool = false
    let action: () async -> Void

    var body: some View {
        Button {
            guard !isLoading else { return }
            Task {
                isLoading = true
                defer { isLoading = false }
                await action()
            }
        } label: {
            // swap label for ProgressView when isLoading
        }
        .disabled(isLoading)
    }
}
```

Rules:
- Wrap `Button` with `Task` + `isLoading` guard — never fire-and-forget an async action from a tap.
- The caller passes `await model.onLoginTapped()`, not a synchronous wrapper that hides the async nature.
- Each project defines its own `AppButton`; the pattern above is the baseline.

## Scroll bounce behavior

When a `ScrollView`'s content might not fill the screen, disable unnecessary bounce:

```swift
ScrollView {
    content
}
.scrollBounceBehavior(.basedOnSize)
```

Use `.basedOnSize` by default. Only omit it when the screen always has enough content to scroll (e.g. long forms) or when pull-to-refresh is present (`.refreshable` needs bounce).

## Animation for state transitions

Showing or hiding content via `if`/`else` or state changes should be animated. Attach the `.animation(_:value:)` modifier to the view — do not wrap state changes in `withAnimation { ... }`:

```swift
VStack {
    if model.isExpanded {
        detailView
    }
}
.animation(.default, value: model.isExpanded)
```

Rules:
- Animate visibility toggles (expand/collapse, error appearance).
- **Prefer the `.animation(_:value:)` modifier on the view over `withAnimation { ... }` wrapping state changes.** Declarative scoping is clearer, animates only the intended property, and composes with other modifiers.
- Do not animate bulk data loads or list reloads — only user-initiated state changes.
- The project's CLAUDE.md defines the concrete animation curve and duration to use for each category (toggles, expands, errors). Follow that spec — do not invent timings per scene.

## State toggles (favorite, selection, expand)

When a UI element toggles between two distinct states (favorite/unfavorite, selected/unselected, expanded/collapsed), the interaction **must** include:

1. **An animation** on the state change — attached via `.animation(_:value:)` on the view.
2. **Haptic feedback** triggered on the user action.
3. **Visual response** on the affected element (scale bounce, fill change, color shift).

```swift
import SwiftUI
import UIKit

Button {
    model.toggleFavorite()
    UIImpactFeedbackGenerator(style: /* see project CLAUDE.md */ .light).impactOccurred()
} label: {
    Image(systemName: model.isFavorite ? "heart.fill" : "heart")
        .scaleEffect(model.isFavorite ? 1.1 : 1.0)
}
.animation(/* see project CLAUDE.md */ .default, value: model.isFavorite)
```

Rules:
- Every toggle has animation + haptic. Instant swaps without visual/tactile feedback are a bug.
- Trigger the haptic on the **user action**, not in a `didSet` on the state — no-op retaps (already favorited) still feel responsive this way.
- Concrete animation curve (spring params, duration) and haptic style are **defined per project in CLAUDE.md** so they match the design system's motion spec. Reference those values; do not hardcode new ones.
- **Attach `.animation(_:value:)` to the view** — do **not** wrap `model.toggleFavorite()` in `withAnimation { }`.

## AsyncImage — use an app-level wrapper

Native `AsyncImage` has no disk cache. Wrap it in a project-level `AppAsyncImage` (or `ImageView`) that can later be swapped for a caching implementation (Kingfisher, Nuke, or custom):

```swift
struct AppAsyncImage: View {
    let url: URL?
    // ... placeholder, error view, sizing
}
```

Rules:
- Never use `AsyncImage` directly in scene views — always go through the app wrapper.
- The wrapper owns the placeholder and error states so they stay consistent across the app.

## ViewModifier pattern

Custom modifiers are a `private struct` implementing `ViewModifier`, exposed via a `View` extension:

```swift
private struct CardShadowModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .shadow(color: .black.opacity(0.1), radius: 8, y: 4)
    }
}

extension View {
    func cardShadow() -> some View {
        modifier(CardShadowModifier())
    }
}
```

Rules:
- The struct is `private` — callers only see the extension method.
- Name the extension method descriptively (`.cardShadow()`, `.homeToolbar(...)`) — not `.modifier1()`.

## No fixed frames on whole views

Never apply a fixed `.frame(width:height:)` to the root of a reusable view. It kills adaptability across screen sizes and Dynamic Type settings.

```swift
// Wrong — locks the entire card to 320 x 200
EventCardView(event: event)
    .frame(width: 320, height: 200)

// Correct — constrain internal elements, let the card size itself
struct EventCardView: View {
    var body: some View {
        VStack { ... }
            .frame(maxWidth: .infinity) // flexible
    }
}
```

If a design calls for a fixed-width element (e.g. a carousel card), set it at the call site via `.frame(width:)` and document why. Internal layout must remain flexible.

## Supporting Dynamic Type in sheets

`TextStyle` handles Dynamic Type scaling internally. Do not override with fixed `.font(.custom:size:)` unless the design explicitly calls for a non-scaling label (in which case document why).

Sheets with dynamic content should measure their height and use `.presentationDetents([.height(measuredHeight)])` so the sheet grows with the user's text size.
