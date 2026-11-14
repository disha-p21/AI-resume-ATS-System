
import os
import logging
from pathlib import Path
from typing import Any, Dict

import streamlit as st
from supabase import Client, create_client

logger = logging.getLogger("ats_resume_scorer")


# --------------------------------------------------
# ENVIRONMENT CONFIGURATION
# --------------------------------------------------

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass


def _secret(key: str, section: str = "supabase") -> str:
    """Read configuration from environment or Streamlit secrets."""

    val = os.getenv(key, "")

    if val:
        return val

    try:
        return st.secrets[section][key]
    except (KeyError, FileNotFoundError, AttributeError):
        return ""


SUPABASE_URL = _secret("SUPABASE_URL")
SUPABASE_ANON_KEY = _secret("SUPABASE_ANON_KEY")

OAUTH_REDIRECT_URL = (
    os.getenv("AUTH_REDIRECT_URL")
    or _secret("redirect_uri", "google_oauth")
    or "http://localhost:8501"
).rstrip("/")


# --------------------------------------------------
# CONFIGURATION VALIDATION
# --------------------------------------------------

def _missing_config() -> str | None:

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:

        return (
            "Supabase is not configured. "
            "Set SUPABASE_URL and SUPABASE_ANON_KEY "
            "in .env or .streamlit/secrets.toml."
        )

    return None


# --------------------------------------------------
# SUPABASE CLIENT
# --------------------------------------------------

@st.cache_resource
def get_client() -> Client | None:
    """Create and cache Supabase client."""

    if _missing_config():
        return None

    return create_client(
        SUPABASE_URL,
        SUPABASE_ANON_KEY
    )


# --------------------------------------------------
# SESSION HELPER
# --------------------------------------------------

def _session_dict(session, user) -> Dict[str, Any]:

    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "user_id": user.id,
        "email": user.email,
    }


# --------------------------------------------------
# SIGN UP WITH EMAIL AND PASSWORD
# --------------------------------------------------

def sign_up_with_password(
    email: str,
    password: str
) -> Dict[str, Any]:

    err = _missing_config()

    if err:
        return {"error": err}

    try:

        client = get_client()

        resp = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "email_redirect_to": OAUTH_REDIRECT_URL
            }
        })

        if resp.session and resp.user:

            return _session_dict(
                resp.session,
                resp.user
            )

        if resp.user:

            return {
                "pending_confirmation": True,
                "email": email
            }

        return {
            "error": "Sign-up failed."
        }

    except Exception as exc:

        logger.exception("Sign-up failed")

        return {
            "error": _humanize(exc)
        }


# --------------------------------------------------
# VERIFY SIGNUP EMAIL USING TOKEN HASH
# --------------------------------------------------

def verify_signup_token_hash(
    token_hash: str
) -> Dict[str, Any]:

    err = _missing_config()

    if err:
        return {"error": err}

    if not token_hash:
        return {
            "error": "Verification token is missing."
        }

    try:

        client = get_client()

        resp = client.auth.verify_otp({
            "token_hash": token_hash,
            "type": "email"
        })

        if resp.session and resp.user:

            return _session_dict(
                resp.session,
                resp.user
            )

        return {
            "error": (
                "Email verification did not return "
                "a valid session."
            )
        }

    except Exception as exc:

        logger.exception(
            "Signup email verification failed"
        )

        return {
            "error": _humanize(exc)
        }


# --------------------------------------------------
# SIGN IN WITH EMAIL AND PASSWORD
# --------------------------------------------------

def sign_in_with_password(
    email: str,
    password: str
) -> Dict[str, Any]:

    err = _missing_config()

    if err:
        return {"error": err}

    try:

        resp = get_client().auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not resp.session or not resp.user:

            return {
                "error": "Invalid credentials."
            }

        return _session_dict(
            resp.session,
            resp.user
        )

    except Exception as exc:

        logger.warning(
            "Sign-in failed: %s",
            exc
        )

        return {
            "error": _humanize(exc)
        }


# --------------------------------------------------
# GOOGLE OAUTH
# --------------------------------------------------

def google_oauth_url() -> Dict[str, Any]:

    err = _missing_config()

    if err:
        return {"error": err}

    try:

        resp = get_client().auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": OAUTH_REDIRECT_URL
            }
        })

        return {
            "url": resp.url
        }

    except Exception as exc:

        logger.warning(
            "Google OAuth URL generation failed: %s",
            exc
        )

        return {
            "error": _humanize(exc)
        }


# --------------------------------------------------
# EXCHANGE OAUTH CODE FOR SESSION
# --------------------------------------------------

def exchange_code_for_session(
    auth_code: str
) -> Dict[str, Any]:

    err = _missing_config()

    if err:
        return {"error": err}

    client = get_client()

    try:

        storage_key = (
            f"{client.auth._storage_key}-code-verifier"
        )

        code_verifier = (
            client.auth._storage.get_item(storage_key) or ""
        )

        if not code_verifier:

            return {
                "error": (
                    "PKCE code verifier is missing. "
                    "Please restart the authentication flow."
                )
            }

        resp = client.auth.exchange_code_for_session({
            "auth_code": auth_code,
            "code_verifier": code_verifier,
            "redirect_to": OAUTH_REDIRECT_URL
        })

        if not resp.session or not resp.user:

            return {
                "error": "OAuth exchange returned no session."
            }

        return _session_dict(
            resp.session,
            resp.user
        )

    except Exception as exc:

        logger.exception(
            "OAuth code exchange failed"
        )

        return {
            "error": _humanize(exc)
        }


# --------------------------------------------------
# RESEND SIGNUP CONFIRMATION EMAIL
# --------------------------------------------------

def resend_signup_confirmation(
    email: str
) -> Dict[str, Any]:

    err = _missing_config()

    if err:
        return {"error": err}

    try:

        get_client().auth.resend({
            "type": "signup",
            "email": email,
            "options": {
                "email_redirect_to": OAUTH_REDIRECT_URL
            }
        })

        return {
            "success": True
        }

    except Exception as exc:

        logger.exception(
            "Resend confirmation email failed"
        )

        return {
            "error": _humanize(exc)
        }


# --------------------------------------------------
# FORGOT PASSWORD / SEND RESET EMAIL
# --------------------------------------------------

def send_password_reset_email(
    email: str
) -> Dict[str, Any]:

    err = _missing_config()

    if err:
        return {"error": err}

    try:

        client = get_client()

        redirect_url = (
            f"{OAUTH_REDIRECT_URL}?mode=recovery"
        )

        client.auth.reset_password_for_email(
            email,
            {
                "redirect_to": redirect_url
            }
        )

        return {
            "success": True
        }

    except Exception as exc:

        logger.exception(
            "Password reset email failed"
        )

        return {
            "error": _humanize(exc)
        }


# --------------------------------------------------
# UPDATE PASSWORD AFTER RECOVERY
# --------------------------------------------------

def update_user_password(
    new_password: str
) -> Dict[str, Any]:

    err = _missing_config()

    if err:
        return {"error": err}

    try:

        client = get_client()

        response = client.auth.update_user({
            "password": new_password
        })

        if not response.user:

            return {
                "error": "Password could not be updated."
            }

        return {
            "success": True
        }

    except Exception as exc:

        logger.exception(
            "Password update failed"
        )

        return {
            "error": _humanize(exc)
        }


# --------------------------------------------------
# SIGN OUT
# --------------------------------------------------

def sign_out() -> None:

    if _missing_config():
        return

    try:

        get_client().auth.sign_out()

    except Exception as exc:

        logger.warning(
            "Sign-out failed: %s",
            exc
        )


# --------------------------------------------------
# ERROR HANDLING
# --------------------------------------------------

def _humanize(exc: Exception) -> str:

    msg = str(exc)
    lower_msg = msg.lower()

    if (
        "invalid_grant" in lower_msg
        or "invalid login" in lower_msg
        or "invalid_credentials" in lower_msg
    ):

        return "Wrong email or password."

    if (
        "user already registered" in lower_msg
        or "already been registered" in lower_msg
    ):

        return (
            "An account with this email already exists. "
            "Please sign in or resend confirmation email."
        )

    if "password should be at least" in lower_msg:

        return (
            "Password too short. "
            "Supabase requires at least 6 characters."
        )

    if "email not confirmed" in lower_msg:

        return (
            "Please verify your email before signing in."
        )

    if "otp_expired" in lower_msg or "token has expired" in lower_msg:

        return (
            "This link has expired. "
            "Please request a new confirmation email."
        )

    return msg
