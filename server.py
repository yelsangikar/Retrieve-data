import pandas as pd
import pyodbc
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import time

def execute_sql_query(sql_query, database):
    try:
        # Create the connection string
        connection = pyodbc.connect(driver='ODBC Driver 17 for SQL Server',
                                    server='TKTHP-SN566\\SQLEXPRESS04',
                                    Timeout=30,
                                    database=database,
                                    trusted_connection='yes')

        # Create a cursor from the connection
        cur = connection.cursor()

        # Execute the SQL query
        cur.execute(sql_query)

        # Check if the query is a SELECT statement
        if sql_query.strip().upper().startswith("SELECT"):
            # Fetch all the results
            rows = cur.fetchall()

            # Get column names from the cursor
            columns = [column[0] for column in cur.description]

            # Close the connection
            connection.close()

            # Convert the results into a DataFrame
            df = pd.DataFrame.from_records(rows, columns=columns)
            return df, rows, None  # No error, return None for error message
        else:
            # For non-SELECT queries (like UPDATE, INSERT, DELETE)
            connection.commit()
            connection.close()
            return None, None, "Query executed successfully but no results to display."

    except Exception as e:
        return None, None, str(e)  # Return the error message if SQL fails

# Set page config with a custom icon, layout, and styling
st.set_page_config(page_title='Retrieve Data', layout="centered", page_icon=":bar_chart:")
st.markdown(
    """
    <style>
    body {
        background-image: url('https://www.transparenttextures.com/patterns/shattered.png');
        background-size: cover;
    }
    h1, h3 {
        text-align: center;
    }
    h1 {
        color: #4CAF50;
    }
    h3 {
        color: #ff6f61;
        text-shadow: 1px 1px 2px black;
    }
    </style>
    <h1>------------------ Retrieve SQL Data ------------------ <br> <small>Retrieve SQL Data Seamlessly</small></h1>
    <h3>Your SQL Data at Your Fingertips!</h3>
    """,
    unsafe_allow_html=True
)

# Input and button
question = st.text_input('Enter your SQL query here:', key='input', placeholder='SELECT * FROM your_table WHERE ...', help='E.g., Retrieve specific rows, filter results, or join tables')
submit = st.button('Ask The Question', key='submit', help='Click to run your SQL query!', use_container_width=True)


# Display loading spinner while processing the query
if submit:
    with st.spinner('Processing your query...'):
        time.sleep(2)  # Simulating query processing delay
        st.success('Query executed successfully! :rocket:')

# Enhanced button CSS
st.markdown(
    """
    <style>
    div.stButton > button {
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        color: white;
        padding: 10px;
        font-size: 16px;
        border-radius: 10px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: linear-gradient(to right, #feb47b, #ff7e5f);
        transform: scale(1.05);
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

if submit:
    # Get the SQL query from the AI model

    query_result, rows, error_message = execute_sql_query(question, 'master')


    if error_message:
        if "no results" in error_message:
            st.warning(f"{error_message}")
        else:
            st.error(f"SQL Error after correction: {error_message}")
    else:
        st.subheader('Query Result:')
        st.table(query_result)



