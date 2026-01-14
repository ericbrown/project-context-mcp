# Architecture Overview

This document describes the high-level architecture of the sample project.

## System Components

- **API Layer**: REST endpoints for client communication
- **Service Layer**: Business logic and data processing
- **Data Layer**: Database access and caching

## Directory Structure

```
src/
├── api/          # REST endpoint handlers
├── services/     # Business logic
├── models/       # Data models
└── utils/        # Shared utilities
```

## Key Design Decisions

1. **Layered Architecture**: Clear separation between API, service, and data layers
2. **Dependency Injection**: Services are injected rather than imported directly
3. **Async First**: All I/O operations use async/await patterns
