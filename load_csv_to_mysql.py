import pandas as pd
from db import create_connection

# READ CSV
df = pd.read_csv("query_data.csv")

print(df.head())

# DATABASE CONNECTION
connection = create_connection()

cursor = connection.cursor()

# INSERT QUERY
insert_query = """
INSERT INTO queries
(
    mail_id,
    mobile_number,
    query_heading,
    query_description,
    status,
    query_created_time,
    query_closed_time
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# LOOP THROUGH ROWS
for index, row in df.iterrows():

    values = (
        row["client_email"],
        str(row["client_mobile"]),
        row["query_heading"],
        row["query_description"],
        row["status"],
        row["date_raised"],
        row["date_closed"]
    )

    cursor.execute(insert_query, values)

# SAVE
connection.commit()

print("GUVI Dataset Loaded Successfully!")

cursor.close()
connection.close()