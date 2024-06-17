import pandas as pd;
import psycopg2
import psycopg2.extras as extras

def main(): 
    df = read_excel_file()
    # print(df)

    conn = psycopg2.connect(
        host="localhost",
        database="medinfo",
        user="postgres",
        password = read_password()
    )

    # insert_data(df, conn) //uncomment to insert data
    read_data(conn)

    conn.close()

def read_excel_file():
    df = pd.read_excel('flow.xlsx', header=0, dtype={
    'patientid': int,
    'firstname': str,
    'lastname': str,
    'email': str,
    'city': str,
    'dob': object})
    df['dob'] = pd.to_datetime(df['dob'], format='%m/%d/%y')
    return df

def insert_data(df, conn):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query  = "INSERT INTO patient(%s) VALUES %%s" % cols
    cur = conn.cursor()
    try:
        extras.execute_values(cur, query, tuples)
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error: %s" % error)
        conn.rollback()
    finally:
        cur.close()

def read_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM patient;")
    results = cur.fetchall()

    for row in results:
        print(row)
    
    cur.close()

def read_password():
    with open('password.txt', 'r') as file:
        content = file.read()
        words = content.split()
        password = words[0]
    return password

if __name__ == "__main__":
    main()