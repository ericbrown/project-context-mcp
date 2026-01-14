# API Patterns

Guidelines for implementing API endpoints.

## Request/Response Format

All endpoints use JSON for request and response bodies.

### Success Response

```json
{
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [ ... ]
  }
}
```

## Authentication

- Use Bearer tokens in the Authorization header
- Tokens expire after 24 hours
- Refresh tokens are valid for 7 days

## Rate Limiting

- Default: 100 requests per minute per API key
- Bulk endpoints: 10 requests per minute
- Rate limit headers included in all responses

## Versioning

API versions are specified in the URL path: `/api/v1/...`
