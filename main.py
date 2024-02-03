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

def Query():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT         
        d.department AS Department,
        j.job AS Job,
        COUNT(CASE WHEN strftime('%m', e.datetime) BETWEEN '01' AND '03' THEN 1 END) AS Q1,
        COUNT(CASE WHEN strftime('%m', e.datetime) BETWEEN '04' AND '06' THEN 1 END) AS Q2,
        COUNT(CASE WHEN strftime('%m', e.datetime) BETWEEN '07' AND '09' THEN 1 END) AS Q3,
        COUNT(CASE WHEN strftime('%m', e.datetime) BETWEEN '10' AND '12' THEN 1 END) AS Q4
    FROM 
        hired_employees e
    JOIN 
        departments d ON e.department_id = d.id
    JOIN 
        jobs j ON e.job_id = j.id
    WHERE 
        strftime('%Y', e.datetime) = '2021'
    GROUP BY 
        Department, Job
    ORDER BY 
        Department ASC, Job ASC;
    """)
    # Recuperar los resultados de la consulta
    rows = cursor.fetchall()
    # Procesar los resultados
    for row in rows:
        st.write(row)
    # Cerrar la conexión
    conn.close()

def Query2():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        d.id AS Department_ID,
        d.department AS Department_Name,
        COUNT(e.id) AS Number_of_Employees_Hired
    FROM 
        departments d
    JOIN 
        hired_employees e ON d.id = e.department_id
    WHERE 
        strftime('%Y', e.datetime) = '2021'
    GROUP BY 
        d.id, d.department
    HAVING 
        COUNT(e.id) > (
            SELECT 
                AVG(employees_count)
            FROM 
                (SELECT 
                    COUNT(*) AS employees_count
                FROM 
                    hired_employees
                WHERE 
                    strftime('%Y', datetime) = '2021'
                GROUP BY 
                    department_id)
        )
    ORDER BY 
        Number_of_Employees_Hired DESC;

    """)
    # Recuperar los resultados de la consulta
    rows = cursor.fetchall()
    # Procesar los resultados
    for row in rows:
        st.write(row)
    # Cerrar la conexión
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

    if st.button('QUERY SQL'):
        st.write("department_____job____________Q1__Q2__Q3__Q4")
        Query()

    if st.button('QUERY SQL2'):
        st.write("id_____department____hired")
        Query2()
    

if __name__ == '__main__':
    main()

