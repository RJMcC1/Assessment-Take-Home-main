---
name: take-home-test-strategy
description: 'Use for take-home tasks to design and implement unit tests, prioritize edge cases, and verify correctness before submission.'
argument-hint: 'Feature or module under test'
user-invocable: true
---

# Take-Home Test Strategy

## When to Use
- Before or during implementation.
- When adding regression protection after bug fixes.
- Before final submission.

## Procedure
1. Identify core behaviors and map them to test cases.
2. Add happy-path unit tests.
3. Add edge-case tests (invalid input, boundaries, large values, offline/error states where relevant).
4. Assert error handling behavior explicitly.
5. Keep test names descriptive and deterministic.
6. Run tests and summarize pass/fail with known gaps.

## Output Format
- `Test matrix`
- `Implemented tests`
- `Edge cases covered`
- `Known gaps`
