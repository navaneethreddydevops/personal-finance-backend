# Authentication

The API uses **stateless JWT authentication** with Bearer tokens.

## Flow

```
POST /api/v1/auth/register  →  create account
POST /api/v1/auth/login     →  receive access_token
GET  /api/v1/auth/me        →  use token in Authorization header
POST /api/v1/auth/logout    →  client discards token
```

## Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "myuser", "password": "secret123"}'
```

**Validation rules:**

- `username` — alphanumeric only
- `password` — minimum 8 characters

**Response `201`:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "myuser",
  "is_active": true,
  "created_at": "2026-04-21T10:00:00Z"
}
```

## Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
```

**Response `200`:**

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

## Authenticated Requests

Pass the token in the `Authorization` header:

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

## Token Details

| Property | Value |
|---|---|
| Algorithm | HS256 |
| Default TTL | 24 hours |
| Claim | `sub` = user ID (string) |

Tokens are not revocable server-side. Logout is client-side only (discard the token).
