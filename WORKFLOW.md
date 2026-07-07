# WORKFLOW.md

## Sprint Lifecycle

1. Define the sprint.
2. Update:
   - current_sprint.md
   - current_sprint.yaml
   - current_sprint.json
3. Codex performs Startup Review.
4. Codex implements only the current sprint.
5. Run documented verification.
6. If verification passes:
   - Update documentation.
   - Perform sprint closeout.
7. Stop. Await the next sprint.

## Verification Policy

### Application Failure
- Code defects
- Test failures
- Unmet acceptance criteria

Result:
- Stop.

### Tool/Runtime Failure
Examples:
- Codex cannot launch the project virtual environment.
- Host runtime restrictions.
- Permission limitations unrelated to repository code.

Result:
- User runs the documented verification manually.
- Manual verification is authoritative for sprint closeout.
- Do not modify application code to work around tooling limitations.

## Documentation First
No sprint may begin unless current_sprint.md contains:
- Goal
- Expected Files
- Acceptance Criteria
- Verification
