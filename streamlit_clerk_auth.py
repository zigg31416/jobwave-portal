import streamlit as st
import requests
import json
import time
from typing import Optional, Dict, Any
import hmac
import base64
import os

class ClerkAuthError(Exception):
    """Exception raised for errors in Clerk authentication."""
    pass

def authenticate() -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with Clerk using a simpler approach that works with Streamlit.
    
    Returns:
        Optional[Dict[str, Any]]: The user object if authenticated, or None if not authenticated
    """
    # Initialize session state variables if they don't exist
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    # If already authenticated, return the user
    if st.session_state.authenticated and st.session_state.user:
        return st.session_state.user
    
    # Get Clerk keys from Streamlit secrets
    clerk_secret_key = st.secrets.get("CLERK_API_KEY", "")
    clerk_publishable_key = st.secrets.get("CLERK_FRONTEND_API", "")
    
    if not clerk_secret_key or not clerk_publishable_key:
        st.error("Clerk API keys not found in secrets. Please check your configuration.")
        return None
    
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
        </div>
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
            # For demo purposes, we'll simulate authentication
            # In a production app, you would use Clerk's API properly
            try:
                if email and password:
                    with st.spinner("Processing..."):
                        # Simulate API delay
                        time.sleep(1)
                        
                        if auth_mode == "Sign In":
                            # Demo login logic - in a real app you'd call Clerk's API
                            user_data = {
                                "id": f"user_{hash(email) % 10000}",
                                "email_addresses": [{"email_address": email}],
                                "first_name": "Demo",
                                "last_name": "User",
                                "public_metadata": {
                                    "role": "jobseeker" if "jobseeker" in email else "employer"
                                }
                            }
                        else:
                            # Demo registration logic
                            if not first_name or not last_name:
                                st.error("Please fill in all fields")
                                return None
                                
                            user_data = {
                                "id": f"user_{hash(email) % 10000}",
                                "email_addresses": [{"email_address": email}],
                                "first_name": first_name,
                                "last_name": last_name,
                                "public_metadata": {
                                    "role": user_role
                                }
                            }
                        
                        st.session_state.authenticated = True
                        st.session_state.user = user_data
                        
                        # Success message and rerun to update the UI
                        message = "Signed in successfully!" if auth_mode == "Sign In" else "Account created successfully!"
                        st.success(message)
                        time.sleep(1)  # Give time for the success message to be seen
                        st.rerun()
                else:
                    st.error("Please enter your email and password")
            
            except Exception as e:
                st.error(f"Authentication error: {str(e)}")
    
    return st.session_state.user
