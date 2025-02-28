import streamlit as st
import requests
import json
import time
from typing import Optional, Dict, Any

class ClerkAuthError(Exception):
    """Exception raised for errors in Clerk authentication."""
    pass

def authenticate() -> Optional[Dict[str, Any]]:
    """
    Authenticate a user using Clerk.
    
    Returns:
        Optional[Dict[str, Any]]: The user object if authenticated, or None if not authenticated
    """
    # Initialize session state variables if they don't exist
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if "auth_token" not in st.session_state:
        st.session_state.auth_token = None
    
    # If already authenticated, return the user
    if st.session_state.authenticated and st.session_state.user:
        return st.session_state.user
    
    # Get Clerk API key from Streamlit secrets
    clerk_api_key = st.secrets.get("CLERK_API_KEY", "your_clerk_api_key")
    clerk_frontend_api = st.secrets.get("CLERK_FRONTEND_API", "your_clerk_frontend_api")
    
    # Display login form
    with st.container():
        st.markdown("""
        <style>
        .auth-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .auth-title {
            text-align: center;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
        }
        
        .auth-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .auth-button {
            background-color: #00A8E8;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .auth-link {
            text-align: center;
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        </style>
        
        <div class="auth-container">
            <h2 class="auth-title">Welcome to JobWave</h2>
            <div class="auth-form">
        """, unsafe_allow_html=True)
        
        # Toggle between login and signup
        auth_mode = st.radio("", ["Sign In", "Create Account"], horizontal=True)
        
        # Common fields
        email = st.text_input("Email", key="auth_email")
        password = st.text_input("Password", type="password", key="auth_password")
        
        if auth_mode == "Create Account":
            first_name = st.text_input("First Name", key="auth_first_name")
            last_name = st.text_input("Last Name", key="auth_last_name")
            
            # User role selection
            user_role = st.selectbox(
                "I am a...",
                ["jobseeker", "employer"],
                format_func=lambda x: "Job Seeker" if x == "jobseeker" else "Employer"
            )
        
        # Sign in/Create account button
        button_label = "Sign In" if auth_mode == "Sign In" else "Create Account"
        if st.button(button_label, key="auth_submit"):
            try:
                if auth_mode == "Sign In":
                    # Perform sign in
                    # In a real implementation, this would use Clerk's API
                    
                    # Simulated API call for demonstration
                    # In production, you would use:
                    # response = requests.post(
                    #     f"https://api.clerk.dev/v1/sign_ins",
                    #     headers={"Authorization": f"Bearer {clerk_api_key}"},
                    #     json={"email": email, "password": password}
                    # )
                    
                    # Simulate successful login for demonstration
                    if email and password:
                        # For demo: simulate API response time
                        with st.spinner("Signing in..."):
                            time.sleep(1)
                        
                        # Mock user response
                        # In a real implementation, this would come from Clerk's API
                        user_data = {
                            "id": "user_123456789",
                            "email_addresses": [{"email_address": email}],
                            "first_name": "Demo",
                            "last_name": "User",
                            "public_metadata": {
                                "role": "jobseeker" if "jobseeker" in email else "employer"
                            }
                        }
                        
                        st.session_state.authenticated = True
                        st.session_state.user = user_data
                        st.session_state.auth_token = "mock_token_123456789"
                        
                        st.success("Signed in successfully!")
                        st.rerun()
                    else:
                        st.error("Please enter both email and password")
                else:
                    # Perform sign up
                    # In a real implementation, this would use Clerk's API
                    
                    # Check if all fields are filled
                    if not email or not password or not first_name or not last_name:
                        st.error("Please fill in all fields")
                        return None
                    
                    # Simulated API call for demonstration
                    # In production, you would use:
                    # response = requests.post(
                    #     f"https://api.clerk.dev/v1/users",
                    #     headers={"Authorization": f"Bearer {clerk_api_key}"},
                    #     json={
                    #         "email_address": email,
                    #         "password": password,
                    #         "first_name": first_name,
                    #         "last_name": last_name,
                    #         "public_metadata": {"role": user_role}
                    #     }
                    # )
                    
                    # Simulate successful registration
                    with st.spinner("Creating your account..."):
                        time.sleep(1.5)
                    
                    # Mock user response
                    user_data = {
                        "id": "user_987654321",
                        "email_addresses": [{"email_address": email}],
                        "first_name": first_name,
                        "last_name": last_name,
                        "public_metadata": {
                            "role": user_role
                        }
                    }
                    
                    st.session_state.authenticated = True
                    st.session_state.user = user_data
                    st.session_state.auth_token = "mock_token_987654321"
                    
                    st.success("Account created successfully!")
                    st.rerun()
            
            except ClerkAuthError as e:
                st.error(f"Authentication error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        # Toggle link
        toggle_text = "New to JobWave? Create an account" if auth_mode == "Sign In" else "Already have an account? Sign in"
        toggle_key = "create_account" if auth_mode == "Sign In" else "sign_in"
        
        st.markdown(f"<div class='auth-link'>{toggle_text}</div>", unsafe_allow_html=True)
        
        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    return st.session_state.user
