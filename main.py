import logging
import traceback

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from auth import create_access_token, verify_password
from database import engine, get_db
from errors import AppError
import models
import crud
import schemas


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

logger = logging.getLogger("uvicorn.error")


# ── Global error handling ──────────────────────────────────────────────────
# NOTE: This only catches *unhandled* exceptions. HTTPException (e.g. the 400
# we raise for a duplicate email) and 422 validation errors are still handled
# by FastAPI's built-in handlers, so they return their proper status codes.
# We log the full traceback so real errors are visible in the server console.
@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled error on %s %s:\n%s",
        request.method,
        request.url.path,
        "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong. Please try again."},
    )


# ── Pages ───────────────────────────────────────────────────────────────────
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# ── API ─────────────────────────────────────────────────────────────────────
@app.post("/api/signup", response_model=schemas.MessageResponse, status_code=201)
def signup(user: schemas.SignupRequest, db: Session = Depends(get_db)):

    result = crud.create_user(db, user)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return {
        "message": "User registered successfully",
        "user_id": result["user_id"],
    }


@app.post("/api/login", response_model=schemas.TokenResponse)
def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Step 1 — fetch user from DB
    db_user = crud.get_user_by_email(db, user.email)

    if not db_user:
        raise AppError.INVALID_CREDS

    # Step 2 — verify password
    if not verify_password(user.password, db_user["password_hash"]):
        raise AppError.INVALID_CREDS

    # Step 3 — create JWT token
    token = create_access_token(data={
        "sub":      str(db_user["user_id"]),
        "email":    db_user["email"],
        "name":     db_user["name"],
        "phone_no": str(db_user["phone_no"]),
    })

    return {
        "access_token": token,
        "token_type":   "bearer",
        "user_name":    db_user["name"],
    }


# @app.get("/api/dashboard")
# def get_dashboard(current_user: dict = Depends(get_current_user)):
#     return {
#         "message":  f"Welcome, {current_user['name']}!",
#         "user_id":  current_user["sub"],
#         "email":    current_user["email"]
#     }
