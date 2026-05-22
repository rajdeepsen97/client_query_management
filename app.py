import streamlit as st
from utils.auth import register_user, login_user

st.set_page_config(page_title="Client Query System")

# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("Client Query Management System")

menu = ["Login", "Register"]

choice = st.sidebar.selectbox("Menu", menu)

# REGISTER
if choice == "Register":

    st.subheader("Create Account")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        ["Client", "Support"]
    )

    if st.button("Register"):

        register_user(
            username,
            password,
            role
        )

        st.success("Registration Successful!")

# LOGIN
elif choice == "Login":

    st.subheader("Login Here")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(username, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.role = user[3]
            st.session_state.username = username

            st.success("Login Successful!")

            if user[3] == "Client":
                st.switch_page("pages/client_page.py")

            elif user[3] == "Support":
                st.switch_page(
                    "pages/support_dashboard.py"
                )

        else:
            st.error("Invalid Credentials")