from fastapi import HTTPException

class AppError:
    # 400 — bad request (user did something wrong)
    EMAIL_EXISTS  = HTTPException(status_code=400, detail="Email already registered")
    INVALID_INPUT = HTTPException(status_code=400, detail="Invalid input provided")

    # 401 — unauthorized (wrong credentials or bad token)
    INVALID_CREDS = HTTPException(status_code=401, detail="Invalid email or password")
    TOKEN_EXPIRED = HTTPException(status_code=401, detail="Token expired, please login again")

    # 403 — forbidden (logged in but not allowed)
    FORBIDDEN     = HTTPException(status_code=403, detail="You don't have permission")

    # 404 — not found
    NOT_FOUND     = HTTPException(status_code=404, detail="Resource not found")

    # 500 — server errors
    SERVER_ERROR  = HTTPException(status_code=500, detail="Internal server error")