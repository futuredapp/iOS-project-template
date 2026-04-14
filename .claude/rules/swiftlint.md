---
paths:
  - "**/*.swift"
  - ".swiftlint.yml"
---
# SwiftLint compliance

**Before writing Swift, read `.swiftlint.yml`.** Configuration drifts; rules can change per project. This file summarizes the baseline, not the source of truth.

## Configuration baseline

- `line_length` — disabled. Long lines are allowed where they aid readability.
- `identifier_name` — single-letter excludes: `id`, `x`, `y`, `z`.
- `type_name.max_length` — 50.
- `function_parameter_count` — 5.
- `large_tuple` — warn at 3, error at 4.
- `cyclomatic_complexity` — warn at 10.
- `force_cast`, `force_try` — warnings only, but treat them as errors in code review.

## Opt-in rules (partial list — all in `.swiftlint.yml`)

These are enforced and cannot be disabled ad-hoc:

- `closure_body_length`, `closure_end_indentation`, `closure_spacing`
- `collection_alignment`
- `conditional_returns_on_newline`
- `convenience_type`
- `empty_collection_literal`, `empty_count`, `empty_string`
- `explicit_init`
- `first_where`, `last_where`
- `force_unwrapping` — do not use `!` except in test setup
- `implicit_return`
- `implicitly_unwrapped_optional`
- `let_var_whitespace`
- `modifier_order`
- `multiline_arguments`, `multiline_parameters`, `multiline_literal_brackets`, `multiline_parameters_brackets`
- `no_extension_access_modifier` — put access modifiers on members, not on the `extension` keyword
- `operator_usage_whitespace`
- `optional_enum_case_matching`
- `pattern_matching_keywords`
- `private_action`, `private_outlet`
- `sorted_imports`, `sorted_first_last`
- `toggle_bool`
- `trailing_closure`
- `vertical_parameter_alignment_on_call`
- `vertical_whitespace_closing_braces`

Analyzer rules (also enforced):
- `unused_declaration`
- `unused_import`

## Disabling a rule

Only `// swiftlint:disable:this <rule>` or `// swiftlint:disable:next <rule>` at the specific line. **Never** add file-level `// swiftlint:disable` blocks unless you are adding a generated file.

When a rule fights you, prefer restructuring the code. Examples:
- `type_name` warning on `ID` associated type: `associatedtype ID // swiftlint:disable:this type_name` (unavoidable — ID is conventional).
- `force_unwrapping` in a pre-condition you've just checked: refactor to `if let` / `guard let`.

## Before pushing or commiting

Run locally:

```
swiftlint lint
```

CI enforces this on PRs. Do not merge with violations — fix them.
