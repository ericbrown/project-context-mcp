# Coding Conventions

Standards and patterns used in this project.

## Naming Conventions

- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`

## Code Style

- Use type hints for all function parameters and return values
- Maximum line length: 88 characters (Black formatter)
- Use f-strings for string formatting

## Error Handling

- Use custom exception classes for domain errors
- Always log exceptions with full context
- Return appropriate HTTP status codes from API endpoints

## Testing

- Write unit tests for all service layer functions
- Use pytest fixtures for test setup
- Aim for >80% code coverage
