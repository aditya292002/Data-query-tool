from icecream import ic
import sqlite3
import pandas as pd
import os
import json

import google.generativeai as genai
 
# constants
db_name = 'new_db.sqlite3'
 
 
# ---------------------- GETTING LLM RESPONSE FROM GEMENI LLM ------------------------------
# configure our api key
genai.configure(api_key="AIzaSyCJyyGu0WEudYEtPJVHdYJlGFIaPV4avMQ")
 
# function to load local Gemini model and provide sql query as response
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text.strip("'")
 
 
# ------------------------ FUNCTION TO HANDLE FILE UPLOAD FROM DIR PATH ------------------------
# Function to read all CSV files from a directory and load them into a SQLite database
def load_csv_to_sqlite(csv_dir, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
 
    for file_name in os.listdir(csv_dir):
        if file_name.endswith('.csv'):
            table_name = os.path.splitext(file_name)[0]
            # Replace hyphens with underscores to create valid table names
            table_name = table_name.replace('-', '_').lower()
            file_path = os.path.join(csv_dir, file_name)
            df = pd.read_csv(file_path, encoding='latin-1')  # Use 'latin-1' encoding
            df.to_sql(table_name, conn, index=False, if_exists='append')
 
    conn.commit()
    conn.close()
 
 
# ----------------------------- function to get the all the table and their structure ----------------------------------
# function to get table names from sqlite database
def get_tables():
    # Connect to your SQLite database
    conn = sqlite3.connect('new_db.sqlite3')
    # Fetch table names and their columns dynamically
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    return tables
 
# function to get table structure and append to table_data.json
def get_table_structure():
    # "Inside get table st method"
    conn = sqlite3.connect('new_db.sqlite3')
   
    # Initialize an empty dictionary to store table names and their corresponding structure strings
    tables_structure = {}
    cursor = conn.cursor()
    # "[+] processing get tables"
    tables = get_tables()
    # "tables are ", tables
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        output_string = f"Table: {table_name}\n"
        for column_info in columns:
            column_name = column_info[1]
            data_type = column_info[2]
            output_string += f"Column: {column_name}, Type: {data_type}\n"
        output_string += "\n"
        tables_structure[table_name] = output_string
    cursor.close()
 
    
    # tables_structure
    with open("table_data.json", 'r') as file:
        data = json.load(file)
        # data
    for table_name, structure_string in tables_structure.items():
        # table_name, structure_string
        data[table_name] = structure_string
        # data
    with open('table_data.json', 'w') as file:
        json.dump(data, file, indent=2) 
    # Close the database connection
    conn.close()



def process_query(query_input):
    # query_input
    query = ""
    flag = 0
    for ch in query_input:
        if ch=='S':
            flag = 1
        elif ch == ';':
            query = query + ';'
            break
        if flag:
            query = query + ch
    # query
    query_input = query
    
    conn = sqlite3.connect('new_db.sqlite3')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute(query_input)
    result = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return the query result
    return result
