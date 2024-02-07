
from db import conn
import pandas as pd
from datetime import datetime, timedelta, date
import itertools
import os

def get_record_by_table_name(table_name: str, record_id: int):
    
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name} WHERE id = {record_id}')
    result = cursor.fetchone()
    cursor.close()
    
    return result

def delete_record_by_table_name(table_name: str, record_id: int):

    cur = conn.cursor()
    cur.execute(f'DELETE FROM {table_name} WHERE id = {record_id}')
    conn.commit()

def delete_all_record_by_table_name(table_name: str):
    
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {table_name}')
    conn.commit()

def filter_data(table_name: str, **kwargs):

    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    conditions = []

    for column, value in kwargs.items():
        op, value = value
        if value is not None and value != '':
            if op == "LIKE":
                conditions.append(f"{column} LIKE '%{value}%'")
            elif op == 'DATE':
                conditions.append(f"DATE({column}) = '{value}'")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)                

    cursor.execute(query)
    return cursor.fetchall()    

def insert_data_for_anomaly_boa(file_path):
    df = pd.read_excel(file_path)
    df = df.fillna('-')
    cursor = conn.cursor()

    for row in df.values:
        cursor.execute(f"SELECT * FROM t_anomaly WHERE anomaly = '{row[0]}'")
        existing_anomaly = cursor.fetchall()  
        if existing_anomaly is not None and len(existing_anomaly)> 0:
            query = f"""INSERT INTO t_anomaly_boa VALUES (NULL,
                {existing_anomaly[0][0]},
                '{row[1]}',
                '{row[2]}',
                '{row[3]}'
            )"""    
            cursor.execute(query)
            conn.commit()
            
def insert_data_from_excel_anomaly(table_name, file_path, date_index=[]):
    # Read the Excel file into a DataFrame
    try:
        df = pd.read_excel(file_path)
        df = df.fillna('-')
        # Convert DataFrame to list of tuples
        data = [(None,) + tuple(x) for x in df.values]    
        final_data = []
        for row in data:
            arr = []
            try:
                for index, col in enumerate(row):
                    if index == 8:
                        arr.append(col.strftime("%m-%d-%Y"))
                    else:    
                        arr.append(col)
            except Exception as e:
                print(row, e)
            final_data.append(tuple(arr)) 

        placeholders = "?, " + ", ".join(["?" for _ in range(len(df.columns))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"    
        cursor = conn.cursor()
        cursor.executemany(query, final_data)
        conn.commit()
    except Exception as e:
        print("Error: ", e)

def insert_data_from_excel(table_name, file_path, date_index=[]):
    # Read the Excel file into a DataFrame
    try:
        df = pd.read_excel(file_path)
        df = df.fillna('-')
        # Convert DataFrame to list of tuples
        data = [(None,) + tuple(x) for x in df.values]    
        final_data = []
        print("1")
        for row in data:
            arr = []
            try:
                print("2")
                for index, col in enumerate(row):
                    if index in date_index:
                        try:
                            if not isinstance(col, str):
                                d = col.strftime('%Y-%m-%d %H:%M:%S')
                                arr.append(d)
                            else:
                                datetime_obj = datetime.strptime(col, "%m/%d/%y %H:%M")
                                output_string = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                                arr.append(output_string)
                        except Exception as e:
                            try:
                                d = datetime.fromisoformat(col)
                                arr.append(d)                    
                            except Exception as e:
                                print(e)
                    else:    
                        arr.append(col)
            except Exception as e:
                print(row, e)
            final_data.append(tuple(arr)) 

        placeholders = "?, " + ", ".join(["?" for _ in range(len(df.columns))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"    
        cursor = conn.cursor()
        cursor.executemany(query, final_data)
        conn.commit()
    except Exception as e:
        print("Error: ", e)
    
def update_data(table_name, id_value, **kwargs):

    folder_name = "files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for file in kwargs.get('affected_files', []):
        if file.filename != '':
            file_path = os.path.join(folder_name, file.filename)
            with open(file_path, 'wb') as file_object:
                file_object.write(file.read())

    affected_files = ','.join([file.filename for file in kwargs.get('affected_files')]).strip()
    kwargs['affected_files'] = affected_files
    # Generate the SET clause for the update query
    set_clause = ", ".join([f"`{col}` = ?" for col in kwargs.keys()])
    # Generate the list of values for the update query
    values = list(kwargs.values())
    # Add the ID value to the list of values
    values.append(id_value)
    # Generate the update query
    update_query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(update_query, tuple(values))
    conn.commit()

def check_user_login(username, password):
    query = f"""SELECT `is_admin` FROM `t_users` WHERE `username` = '{username}' AND `password` = '{password}'"""
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.commit()

    return result[0]


def insert_user(username, password, is_admin):
    is_admin = 1 if is_admin else 0
    query = f"""
        INSERT INTO t_users VALUES (NULL, '{username}', '{password}', {is_admin})
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    

def get_schedule_for_week(table_name, start_date, end_date, date_column_index, 
                          display_column_index, date_formats, flag=False):

    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    
    cursor.execute(query)
    data = cursor.fetchall()
    data_dict = {}
    default_val = [0,'']
    for row in data:
        dateObj = None
        for date_format in date_formats:
            try:
                dateObj = datetime.strptime(row[date_column_index], date_format).date()
                break
            except Exception as e:
                print(e)
        if dateObj is not None:
            if start_date <= dateObj <= end_date:
                if dateObj not in data_dict.keys():
                    data_dict[dateObj] = []
                data_dict[dateObj].append([row[0], row[display_column_index], row[-1]])

    week_data = []

    while start_date <= end_date:
        if start_date not in data_dict.keys():
            data_dict[start_date] = []
        start_date += timedelta(days=1)


    for key in data_dict.keys():
        week_data.append([key] + data_dict[key])

    week_data.sort(key=lambda x: x[0])
    week_data = [sublist[1:] for sublist in week_data]

    data = list(map(list, itertools.zip_longest(*week_data, fillvalue=default_val)))
    if flag:
        for row in data:
            for col in row:
                if col[-1] != '-':
                    return data, col[-1]
                
        return data, '-'

    return data

def get_timer_data():
    with open('timer.txt') as f:
        data = f.readlines()
        
    data  = [line.strip().split(',') for line in data]

    return data[0]


def get_entries_data(filename):
    with open(filename) as f:
        data = f.readlines()
    data  = [line.strip().split(',') for line in data]

    return data[0], data[1], data[2], data[3], data[4], data[5]

def save_update_request(table_name, **kwargs):
    tables = ','.join(kwargs.get('table')).strip()

    folder_name = "files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for file in kwargs.get('affected_files', []):
        if file.filename != '':
            file_path = os.path.join(folder_name, file.filename)
            with open(file_path, 'wb') as file_object:
                file_object.write(file.read())

    affected_files = ','.join([file.filename for file in kwargs.get('affected_files')]).strip()
    
    DUE_DATE = kwargs.get('due_date')
    DUE_DATE = DUE_DATE if DUE_DATE else "NULL"
    if DUE_DATE != "NULL":
        # Parse the string date into a datetime object
        date_obj = datetime.strptime(DUE_DATE, "%Y-%m-%d")

        # Convert datetime object to a string in SQLite-compatible format
        sqlite_date_str = date_obj.strftime("%Y-%m-%d")
        DUE_DATE = sqlite_date_str
    
    query = f"""
        INSERT INTO {table_name} VALUES (NULL, 
        '{kwargs.get('s_c')}',
        'NOT VERIFIED',
        'NOT VERIFIED',
        '{kwargs.get('person')}',
        '{datetime.now().strftime("%Y-%m-%d %H:%M")}',
        '{kwargs.get('type')}',
        '{kwargs.get('description')}',
        '{tables}',
        '{kwargs.get('title')}',
        '{kwargs.get('wodb_ref')}',
        '{kwargs.get('srdb_ref')}',
        '{affected_files}', 
        '{kwargs.get("implemented")}',
        '{kwargs.get("tl")}',
        '{kwargs.get("analyst_name")}',
        '{datetime.now().strftime("%Y-%m-%d %H:%M")}',
        NULL, NULL,
        '{DUE_DATE}'
        )
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

def save_action_request(table_name, **kwargs):
    tables = ','.join(kwargs.get('table')).strip()

    folder_name = "files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for file in kwargs.get('affected_files', []):
        if file.filename != '':
            file_path = os.path.join(folder_name, file.filename)
            with open(file_path, 'wb') as file_object:
                file_object.write(file.read())

    affected_files = ','.join([file.filename for file in kwargs.get('affected_files')]).strip()
    query = f"""
        INSERT INTO {table_name} VALUES (NULL, 
        '{kwargs.get('s_c')}',
        'NOT VERIFIED',
        '{kwargs.get('person')}',
        '{datetime.now().strftime("%Y-%m-%d %H:%M")}',
        '{kwargs.get('type')}',
        '{kwargs.get('description')}',
        '{tables}',
        '{kwargs.get('title')}',
        '{kwargs.get('wodb_ref')}',
        '{kwargs.get('srdb_ref')}',
        '{affected_files}', 
        '{kwargs.get("implemented")}'
        )
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

def get_file_name(table, id):
    cur = conn.cursor()
    cur.execute(f'SELECT affected_files FROM {table} WHERE `id` = {id}')
    filenames = cur.fetchall()[0][0]
    cur.close()

    return None if filenames == '' else filenames 