import streamlit as st

# LOGIN CHECK
if "logged_in" not in st.session_state:

    st.warning("Please login first")

    st.stop()

if st.session_state.role != "Client":

    st.error("Access Denied")

    st.stop()

import streamlit as st
from datetime import datetime
from db import create_connection

st.title("Client Query Submission Page")

st.write(f"Welcome, {st.session_state.username}")

if st.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.username = ""

    st.switch_page("app.py")

st.write("Submit your support query here")

# INPUTS
mail_id = st.text_input("Email ID")

mobile_number = st.text_input("Mobile Number")

query_heading = st.text_input("Query Heading")

query_description = st.text_area("Query Description")

# BUTTON
if st.button("Submit Query"):

    connection = create_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO queries
    (
        mail_id,
        mobile_number,
        query_heading,
        query_description,
        status,
        query_created_time
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        mail_id,
        mobile_number,
        query_heading,
        query_description,
        "Open",
        datetime.now()
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()

    connection.close()

    st.success("Query Submitted Successfully!")