import streamlit as st
import pandas as pd
import sqlite3

# Function to create database tables
def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS departments (
                        id INTEGER PRIMARY KEY,
                        department TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY,
                        job TEXT)''')  
    cursor.execute('''CREATE TABLE IF NOT EXISTS hired_employees (
                         id INTEGER PRIMARY KEY,
                        name TEXT,
                        datetime TEXT,
                        department_id INTEGER,
                        job_id INTEGER,
                        FOREIGN KEY (department_id) REFERENCES departments(id),
                        FOREIGN KEY (job_id) REFERENCES jobs(id))''')
    conn.commit()
    conn.close()

# Function to insert data into the corresponding table
def insert_data(table_name, data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.executemany(f'INSERT INTO {table_name} VALUES ({",".join(["?"] * len(data.columns))})', data.values)
        conn.commit()
        st.success(f'CSV inserted successfully into {table_name} table.')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f'Error inserting data into {table_name} table: {e}')
    finally:
        conn.close()


# Streamlit app
def main():
    st.title('Database Migration Tool')
    create_tables()

    # Upload CSV files
    st.header('Upload CSV Files')
    uploaded_files = st.file_uploader('Upload CSV files', accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file, header= None)
                table_name = file.name.split('.')[0]
                insert_data(table_name, data)
                st.success(f'Data from {file.name} uploaded successfully to {table_name} table.')

   # Insert batch transactions
    st.header('Insert Batch Transactions')
    table_name = st.selectbox('Select Table', ['departments', 'jobs', 'hired_employees'], index=0)
    st.write(f'Selected Table: {table_name}')

    st.write('Enter data for batch insertion (separate rows by semicolon and columns by comma):')
    data_input = st.text_area('Data', 'data1,data2,data3;data4,data5,data6')

    if st.button('Insert Batch'):
        rows = [row.split(',') for row in data_input.split(';')]
        insert_data(table_name, pd.DataFrame(rows))

if __name__ == '__main__':
    main()

