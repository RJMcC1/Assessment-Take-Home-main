---
name: take-home-implementation-quality
description: 'Use during take-home implementation to enforce clean code standards: naming, type hints, small functions, DRY structure, constants, formatting, linting, performance, and security basics.'
argument-hint: 'Target language and style guide'
user-invocable: true
---

# Take-Home Implementation Quality

## When to Use
- While implementing features.
- During code cleanup and refactoring.
- Before opening a PR or final submission.

## Procedure
1. Ensure variable and function names are short, descriptive, and style-consistent.
2. Keep functions focused on one responsibility.
3. Remove commented-out code and unused variables/imports.
4. Extract repeated logic into reusable functions/modules.
5. Replace hard-coded values with named constants.
6. Add type hints where language supports them.
7. Run formatter and linter; fix issues.
8. Check obvious performance pitfalls (unneeded nested loops, repeated heavy work).
9. Check core security basics relevant to stack (input validation, injection risks, CORS/auth boundaries).

## Quality Gate
- Code is readable, DRY, and consistently styled.
- No dead code remains.
- Type, lint, and format checks pass.
