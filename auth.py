import os
import bcrypt
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

USER = os.getenv("APP_USER")
PASS_HASH = os.getenv("APP_PASSWORD_HASH")

def check_password(password: str) -> bool:
    return bcrypt.checkpw(password.encode(), PASS_HASH.encode())

def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("Login")

    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user == USER and check_password(password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Credenciais inválidas")

    return False
