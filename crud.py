# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas import SignupRequest
from auth import hash_password


# ── SIGNUP ────────────────────────────────────────────────────────────────
def create_user(db: Session, user: SignupRequest):

    # Step 1 — Check if email already exists
    existing_user = db.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": user.email},
    ).fetchone()

    if existing_user:
        return {"success": False, "message": "Email already registered"}

    # Step 2 — Hash the password in Python (no stored procedure)
    hashed = hash_password(user.password)

    # Step 3 — Insert new user. created_at is filled by the DB default,
    # so we do NOT list it here. Columns and bind params now match exactly.
    result = db.execute(
        text("""
            INSERT INTO users (name, email, password_hash, phone_no)
            VALUES (:name, :email, :password_hash, :phone_no)
            RETURNING id
        """),
        {
            "name": user.name,
            "email": user.email,
            "password_hash": hashed,
            "phone_no": user.phone_no,
        },
    )
    new_user_id = result.fetchone()[0]
    db.commit()
    return {"success": True, "user_id": new_user_id}


# ── FETCH USER FOR LOGIN ──────────────────────────────────────────────────
def get_user_by_email(db: Session, email: str):

    user = db.execute(
        text("""
            SELECT id, name, email, password_hash, phone_no, created_at
            FROM users
            WHERE email = :email
        """),
        {"email": email},
    ).fetchone()

    if not user:
        return None

    # Return a plain dict so callers can use user["..."] access.
    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "password_hash": user.password_hash,
        "phone_no": user.phone_no,
    }
