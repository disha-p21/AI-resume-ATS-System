

import streamlit as st
import sys
from pathlib import Path

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ATS Resume Scorer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

DEFAULT_STATE = {
    "access_token": None,
    "refresh_token": None,
    "user_id": None,
    "user_email": None,
    "auth_error": None,
    "auth_info": None,
    "current_view": "landing",
    "password_recovery_mode": False,
}

for key, default in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = default


from frontend.services import supabase_client


# --------------------------------------------------
# HELPER: STORE AUTH SESSION
# --------------------------------------------------

def store_auth_session(result):
    st.session_state.access_token = result["access_token"]
    st.session_state.refresh_token = result["refresh_token"]
    st.session_state.user_id = result["user_id"]
    st.session_state.user_email = result["email"]


# --------------------------------------------------
# AUTH CALLBACK HANDLING
# --------------------------------------------------

query_params = st.query_params


# --------------------------------------------------
# 1. HANDLE SUPABASE AUTH ERRORS
# --------------------------------------------------

if "error_description" in query_params:

    error_description = query_params.get("error_description")

    st.session_state.auth_error = (
        f"Authentication failed: {error_description}"
    )

    st.query_params.clear()
    st.rerun()


# --------------------------------------------------
# 2. HANDLE EMAIL CONFIRMATION TOKEN HASH
# --------------------------------------------------

if "token_hash" in query_params:

    token_hash = query_params.get("token_hash")
    token_type = query_params.get("type", "signup")

    if not token_hash:

        st.session_state.auth_error = (
            "Email verification failed: Missing verification token."
        )

    elif token_type != "signup":

        st.session_state.auth_error = (
            f"Unexpected verification type: {token_type}"
        )

    else:

        result = supabase_client.verify_signup_token_hash(
            token_hash
        )

        if "error" in result:

            st.session_state.auth_error = (
                f"Email verification failed: {result['error']}"
            )

        elif result.get("access_token") and result.get("refresh_token"):

            store_auth_session(result)

            st.session_state.password_recovery_mode = False

            st.session_state.auth_info = (
                "Email verified successfully! "
                "Your account is ready."
            )

        else:

            st.session_state.auth_error = (
                "Email verification did not return a valid session."
            )

    st.query_params.clear()
    st.rerun()


# --------------------------------------------------
# 3. HANDLE GOOGLE OAUTH / PASSWORD RECOVERY CALLBACK
# --------------------------------------------------

if "code" in query_params:

    auth_code = query_params.get("code")

    recovery_mode = (
        query_params.get("mode") == "recovery"
    )

    if auth_code:

        result = supabase_client.exchange_code_for_session(
            auth_code
        )

        if "error" in result:

            st.session_state.auth_error = (
                f"Authentication failed: {result['error']}"
            )

        else:

            store_auth_session(result)

            if recovery_mode:

                st.session_state.password_recovery_mode = True

                st.session_state.auth_info = (
                    "Password reset link verified. "
                    "You can now create a new password."
                )

            else:

                st.session_state.password_recovery_mode = False

                st.session_state.auth_info = (
                    "Successfully signed in!"
                )

    else:

        st.session_state.auth_error = (
            "Authentication failed: Missing authorization code."
        )

    st.query_params.clear()
    st.rerun()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

def load_css():

    try:

        css_path = (
            Path(__file__).parent
            / "assets"
            / "styles.css"
        )

        with open(css_path, "r", encoding="utf-8") as file:
            return f"<style>{file.read()}</style>"

    except FileNotFoundError:

        return ""


st.markdown(
    load_css(),
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("## Navigation")

    if st.button("🏠 Home", use_container_width=True):

        st.session_state.current_view = "landing"
        st.rerun()

    if st.button("🎯 ATS Scorer", use_container_width=True):

        st.session_state.current_view = "scorer"
        st.rerun()

    if st.button("📊 History", use_container_width=True):

        st.session_state.current_view = "history"
        st.rerun()

    if st.button("📚 Resources", use_container_width=True):

        st.session_state.current_view = "resources"
        st.rerun()


    st.markdown("---")
    st.markdown("### 👤 Account")


    # --------------------------------------------------
    # ACCOUNT: LOGGED IN
    # --------------------------------------------------

    if st.session_state.access_token:

        st.success("Logged in")

        if st.session_state.auth_info:

            st.success(st.session_state.auth_info)
            st.session_state.auth_info = None

        st.caption(
            f"Signed in as **{st.session_state.user_email}**"
        )


        # --------------------------------------------------
        # PASSWORD RECOVERY SCREEN
        # --------------------------------------------------

        if st.session_state.password_recovery_mode:

            st.markdown("### 🔐 Create New Password")

            with st.form("new_password_form"):

                new_password = st.text_input(
                    "New Password",
                    type="password"
                )

                confirm_password = st.text_input(
                    "Confirm New Password",
                    type="password"
                )

                update_submitted = st.form_submit_button(
                    "Update Password",
                    use_container_width=True
                )


            if update_submitted:

                if len(new_password) < 6:

                    st.error(
                        "Password must be at least 6 characters."
                    )

                elif new_password != confirm_password:

                    st.error("Passwords do not match.")

                else:

                    result = supabase_client.update_user_password(
                        new_password
                    )

                    if "error" in result:

                        st.error(result["error"])

                    else:

                        st.session_state.password_recovery_mode = False

                        st.session_state.auth_info = (
                            "Password updated successfully!"
                        )

                        st.rerun()


        # --------------------------------------------------
        # SIGN OUT
        # --------------------------------------------------

        if st.button(
            "🚪 Sign Out",
            use_container_width=True
        ):

            supabase_client.sign_out()

            for key in (
                "access_token",
                "refresh_token",
                "user_id",
                "user_email",
            ):

                st.session_state[key] = None

            st.session_state.password_recovery_mode = False
            st.session_state.auth_info = None
            st.session_state.auth_error = None
            st.session_state.current_view = "landing"

            st.rerun()


    # --------------------------------------------------
    # ACCOUNT: LOGGED OUT
    # --------------------------------------------------

    else:

        if st.session_state.auth_error:

            st.error(st.session_state.auth_error)
            st.session_state.auth_error = None


        if st.session_state.auth_info:

            st.info(st.session_state.auth_info)
            st.session_state.auth_info = None


        tab_in, tab_up = st.tabs(
            ["Sign In", "Sign Up"]
        )


        # --------------------------------------------------
        # SIGN IN
        # --------------------------------------------------

        with tab_in:

            with st.form("signin_form", clear_on_submit=False):

                email = st.text_input(
                    "Email Address",
                    key="signin_email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    key="signin_pw"
                )

                submitted = st.form_submit_button(
                    "Sign In",
                    use_container_width=True
                )


            if submitted:

                if not email.strip() or not password:

                    st.error(
                        "Please enter your email and password."
                    )

                else:

                    result = supabase_client.sign_in_with_password(
                        email.strip(),
                        password
                    )

                    if "error" in result:

                        st.session_state.auth_error = result["error"]

                    else:

                        store_auth_session(result)

                        st.session_state.auth_info = (
                            "Successfully signed in!"
                        )

                    st.rerun()


            # --------------------------------------------------
            # FORGOT PASSWORD
            # --------------------------------------------------

            with st.expander("Forgot Password?"):

                st.write(
                    "Enter your registered email address "
                    "to receive a password reset link."
                )

                reset_email = st.text_input(
                    "Registered Email",
                    key="reset_email"
                )

                if st.button(
                    "Send Password Reset Link",
                    use_container_width=True
                ):

                    if not reset_email.strip():

                        st.error(
                            "Please enter your email address."
                        )

                    else:

                        result = (
                            supabase_client.send_password_reset_email(
                                reset_email.strip()
                            )
                        )

                        if "error" in result:

                            st.error(result["error"])

                        else:

                            st.success(
                                "Password reset email requested. "
                                "Please check your inbox."
                            )


        # --------------------------------------------------
        # SIGN UP
        # --------------------------------------------------

        with tab_up:

            with st.form(
                "signup_form",
                clear_on_submit=False
            ):

                email_up = st.text_input(
                    "Email Address",
                    key="signup_email"
                )

                password_up = st.text_input(
                    "Create Password (minimum 6 characters)",
                    type="password",
                    key="signup_pw"
                )

                submitted_up = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )


            if submitted_up:

                if not email_up.strip() or not password_up:

                    st.error(
                        "Please enter your email and create a password."
                    )

                elif len(password_up) < 6:

                    st.error(
                        "Password must be at least 6 characters."
                    )

                else:

                    result = supabase_client.sign_up_with_password(
                        email_up.strip(),
                        password_up
                    )

                    if "error" in result:

                        st.session_state.auth_error = result["error"]

                    elif result.get("pending_confirmation"):

                        st.session_state.auth_info = (
                            f"Confirmation email sent to "
                            f"{result['email']}. "
                            "Please verify your email."
                        )

                    elif result.get("access_token"):

                        store_auth_session(result)

                        st.session_state.auth_info = (
                            "Account created successfully!"
                        )

                    else:

                        st.session_state.auth_error = (
                            "Sign-up failed. Please try again."
                        )

                    st.rerun()


        # --------------------------------------------------
        # GOOGLE SIGN IN
        # --------------------------------------------------

        st.markdown(
            "<div style='text-align:center; margin: 12px 0; "
            "color:#94a3b8;'>OR</div>",
            unsafe_allow_html=True
        )

        oauth = supabase_client.google_oauth_url()

        if "error" in oauth:

            st.error(
                f"Google Sign In unavailable: {oauth['error']}"
            )

        else:

            st.link_button(
                "Continue with Google",
                url=oauth["url"],
                use_container_width=True
            )


# --------------------------------------------------
# MAIN CONTENT
# --------------------------------------------------

if st.session_state.current_view == "landing":

    from frontend.views import landing
    landing.render()


elif st.session_state.current_view == "scorer":

    from frontend.views import scorer
    scorer.render()


elif st.session_state.current_view == "history":

    from frontend.views import history
    history.render()


elif st.session_state.current_view == "resources":

    from frontend.views import resources
    resources.render()
