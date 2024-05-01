from icecream import ic
import streamlit as st
from utils import *
 
# Streamlit UI
# Set page title
st.set_page_config(page_title="Your Project Name", page_icon="🚀")

# Add a title to the sidebar
st.sidebar.title("Data Query Tool 🚀")

# Add a logo to the sidebar
st.sidebar.image("/workspaces/common_bot/swati_stremlit_app/data_query.png", width=200)

# Main content of the app
st.title('Upload CSV and Query Data')
 
csv_dir = st.text_input('Enter directory path containing CSV files')
db_name = "new_db.sqlite3"
if st.button('Load CSV files'):
    if csv_dir and os.path.isdir(csv_dir):
        load_csv_to_sqlite(csv_dir, db_name)
        get_table_structure()
        st.write("CSV files loaded into SQLite database successfully!")
    else:
        st.write("Please provide a valid directory path containing CSV files")
 
 
# st.subheader("Click the button below once before asking question to load the table infos")
# if st.button('Prepare to ask question'):
#     get_table_structure()
#     st.write("Data prepared to ask question")
 
with st.form("my_form"):
    question = st.text_input("Enter your question")
    submit_button = st.form_submit_button("Submit")
 
    if question and submit_button:
 
 
        # code to get the description
        description = f'''
        Given a questions: {question} some tables with description.
        Tables : Description,
        '''

        tables = get_tables()
 
        # get table structure from table_data
        with open("table_data.json", 'r') as file:
            table_structure = json.load(file)
               
        # add the description
        for key in table_structure.keys():
            description = description + key + " : " + table_structure[key]
 
        description = description + "name the tables which you think can help answer the question."
        
        # code to get the tables (unique ones)
        gemini_resp_tables = get_gemini_response(description)
        st.write("gemeni table suggestions response is", gemini_resp_tables)
        step1_tables = []
        for word in gemini_resp_tables.split():
            if word.lower() in [table[0].lower() for table in tables]:
                step1_tables.append(word.lower())
        step1_tables = list(set(step1_tables))
        st.write("suggested tables are", step1_tables )
 
 
        for table in step1_tables:
            st.write(f"From the table {table}")
            complete_question = "given question" + question + "write an sql query to answer the question from the table " + table_structure[table]
            query_response = get_gemini_response(complete_question)
            st.write(query_response)
            result = process_query(query_response)
            st.table(result)