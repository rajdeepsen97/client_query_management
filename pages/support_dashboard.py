import streamlit as st

# LOGIN CHECK
if "logged_in" not in st.session_state:

    st.warning("Please login first")

    st.stop()

if st.session_state.role != "Support":

    st.error("Access Denied")

    st.stop()

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

import streamlit as st
import pandas as pd
from datetime import datetime
from db import create_connection

st.title("Support Team Dashboard")

st.write(f"Welcome, {st.session_state.username}")

if st.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.username = ""

    st.switch_page("app.py")

# DATABASE CONNECTION
connection = create_connection()

# FETCH DATA
query = "SELECT * FROM queries"

df = pd.read_sql(query, connection)

# FILTER
status_filter = st.selectbox(
    "Filter by Status",
    ["All", "Open", "Closed"]
)

if status_filter != "All":
    df = df[df["status"] == status_filter]

# METRICS
total_queries = len(df)

open_count = len(df[df["status"] == "Open"])

closed_count = len(df[df["status"] == "Closed"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Queries", total_queries)

col2.metric("Open Queries", open_count)

col3.metric("Closed Queries", closed_count)    

# AVERAGE RESOLUTION TIME

closed_df = df[
    (df["status"] == "Closed") &
    (df["query_closed_time"].notnull())
].copy()

if not closed_df.empty:

    closed_df["resolution_time"] = (
        pd.to_datetime(closed_df["query_closed_time"]) -
        pd.to_datetime(closed_df["query_created_time"])
    )

    avg_resolution = (
        closed_df["resolution_time"]
        .mean()
    )

    st.info(
        f"Average Resolution Time: {avg_resolution}"
    )

# SHOW TABLE
st.dataframe(df)

# OPEN QUERIES
open_queries = df[df["status"] == "Open"]

if not open_queries.empty:

    query_id = st.selectbox(
        "Select Query ID to Close",
        open_queries["query_id"]
    )

    if st.button("Close Query"):

        cursor = connection.cursor()

        update_query = """
        UPDATE queries
        SET status=%s,
            query_closed_time=%s
        WHERE query_id=%s
        """

        values = (
            "Closed",
            datetime.now(),
            int(query_id)
        )

        cursor.execute(update_query, values)

        connection.commit()

        st.success("Query Closed Successfully!")

connection.close()