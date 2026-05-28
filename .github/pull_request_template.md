## Description

This PR adds comprehensive test coverage for the activity management API endpoints, specifically focusing on:

- **Signup functionality**: Tests for signing up students to activities with validation for duplicates and non-existent activities
- **Participant removal**: Tests for removing students from activities with proper error handling

### Changes

- Added `conftest.py` with a pytest fixture to reset activities state between tests
- Added `test_app.py` with 8 comprehensive test cases covering:
  - Root redirect to static index
  - Getting the list of activities
  - Signup success and error scenarios (duplicates, missing activities)
  - Participant removal success and error scenarios (missing participants, missing activities)

### Related Issues

Closes #[issue-number] (if applicable)

### Testing

All tests pass locally:
```bash
pytest
```

### Checklist

- [ ] Tests added/updated
- [ ] Code follows project style guidelines
- [ ] Documentation updated (if applicable)
- [ ] No breaking changes
