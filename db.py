import sqlite3 as sq
import os 
script_path = os.path.abspath(__file__)
dir_path = os.path.dirname(os.path.abspath(__file__))
dir_path = dir_path.replace('\\', '/')
db = dir_path + '/' + 'schedule.db'
conn = sq.connect(db, check_same_thread=False)


#######################################################
### CREATING REQUIRED TABLES

def init():

    schedule_table = """CREATE TABLE IF NOT EXISTS 't_schedule' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    's_c' varchar(1000) NOT NULL,
    'year' year(4) NOT NULL,
    'qtr' int(11) NOT NULL,
    'month' int(11) NOT NULL,
    'cw' int(11) NOT NULL,
    'doy' int(11) NOT NULL,    
    'start_of_operation' datetime NOT NULL, 
    'end_of_operation' datetime NOT NULL,
    'status' varchar(1000) NOT NULL,
    'operations_title' varchar(1000) NOT NULL,
    'outage' varchar(1000) NOT NULL,
    'link' carchar(1000)
    )"""

    schedule_2_table = """CREATE TABLE IF NOT EXISTS 't_schedule_2' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    's_c' varchar(1000) NOT NULL,
    'year' year(4) NOT NULL,
    'qtr' int(11) NOT NULL,
    'month' int(11) NOT NULL,
    'cw' int(11) NOT NULL,
    'doy' int(11) NOT NULL,    
    'start_of_operation' datetime NOT NULL, 
    'end_of_operation' datetime NOT NULL,
    'status' varchar(1000) NOT NULL,
    'operations_title' varchar(1000) NOT NULL,
    'outage' varchar(1000) NOT NULL,
    'link' carchar(1000)
    )"""

    schedule_3_table = """CREATE TABLE IF NOT EXISTS 't_schedule_3' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    's_c' varchar(1000) NOT NULL,
    'year' year(4) NOT NULL,
    'qtr' int(11) NOT NULL,
    'month' int(11) NOT NULL,
    'cw' int(11) NOT NULL,
    'doy' int(11) NOT NULL,    
    'start_of_operation' datetime NOT NULL, 
    'end_of_operation' datetime NOT NULL,
    'status' varchar(1000) NOT NULL,
    'operations_title' varchar(1000) NOT NULL,
    'outage' varchar(1000) NOT NULL,
    'link' carchar(1000)
    )"""

    anomaly_table = """CREATE TABLE IF NOT EXISTS 't_anomaly' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'facility' varchar(1000) NOT NULL,
    'anomaly' varchar(1000) NOT NULL,
    'event' varchar(1000) NOT NULL,
    'cell_cnt' int(11) NOT NULL,
    'impact' varchar(1000) NOT NULL,
    'ar_number' varchar(1000) NOT NULL,
    'recover_action' varchar(1000) NOT NULL,
    'date' varchar(1000) NOT NULL,
    'week' int(11) NOT NULL,
    'folder_link' varchar(1000) NOT NULL
    )"""

    anomaly_boa_table = """ CREATE TABLE IF NOT EXISTS 't_anomaly_boa' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'anomaly_id' INTEGER,
    'boa_hex' varchar(1000),
    'boa_parameter' varchar(1000),
    'boa_parameter_detail' varchar(1000)
    )"""
    
    soi_table = """ CREATE TABLE IF NOT EXISTS 't_soi' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'soi_number' varchar(1000) NOT NULL,
    'soi_name' varchar(1000) NOT NULL,
    'version' int(11) NOT NULL,
    'link' varchar(1000) NOT NULL,
    'from_date' datetime NOT NULL,
    'to' datetime NOT NULL,
    'validity' varchar(1000) NOT NULL,
    'today_date' datetime NOT NULL
    )"""
    
    parameter_table = """ CREATE TABLE IF NOT EXISTS 't_parameter' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' varchar(1000) NOT NULL,
    'descr' varchar(1000) NOT NULL,
    'pid' int(11) NOT NULL,
    'unit' varchar(1000) NOT NULL,
    'type_code' varchar(1000) NOT NULL,
    'format_code' varchar(1000) NOT NULL,
    'width' varchar(1000) NOT NULL,
    'valid' varchar(1000) NOT NULL,
    'related' varchar(1000) NOT NULL,
    'categ' varchar(1000) NOT NULL,
    'natur' varchar(1000) NOT NULL,
    'curtx' varchar(1000) NOT NULL,
    'inter' varchar(1000) NOT NULL,
    'uscon' varchar(1000) NOT NULL,
    'decim' varchar(1000) NOT NULL,
    'parval' varchar(1000) NOT NULL,
    'subsys' varchar(1000) NOT NULL,
    'valpar' varchar(1000) NOT NULL,
    'sptype' varchar(1000) NOT NULL,
    'coor' varchar(1000) NOT NULL,
    'obtid' varchar(1000) NOT NULL,
    'darc' varchar(1000) NOT NULL,
    'endian' varchar(1000) NOT NULL,
    'mon_check_name' varchar(1000) NOT NULL,
    'mon_check_nbchck' varchar(1000) NOT NULL,
    'mon_check_nbool' varchar(1000) NOT NULL,
    'mon_check_inter' varchar(1000) NOT NULL,
    'mon_check_codin' varchar(1000) NOT NULL,
    'ool_name' varchar(1000) NOT NULL,
    'ool_pos' varchar(1000) NOT NULL,
    'ool_type' varchar(1000) NOT NULL,
    'ool_vlalu' varchar(1000) NOT NULL,
    'ool_hvalu' varchar(1000) NOT NULL,
    'ool_rlchk' varchar(1000) NOT NULL,
    'ool_valpar' varchar(1000) NOT NULL
    )"""

    procedure_table = """ CREATE TABLE IF NOT EXISTS 't_procedure' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' varchar(1000) NOT NULL,
    'sub_system' varchar(1000) NOT NULL,
    'version' int(11) NOT NULL,
    'pdf_link' varchar(1000) NOT NULL
    )"""

    pus_table = """ CREATE TABLE IF NOT EXISTS 't_pus' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'service' varchar(1000) NOT NULL,
    'name' varchar(1000) NOT NULL,
    'service_subservice' varchar(1000) NOT NULL,
    'des_service' varchar(1000) NOT NULL,
    'space_segment_app' varchar(1000) NOT NULL
    )"""

    event_table = """ CREATE TABLE IF NOT EXISTS 't_event' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'week' int(11) NOT NULL,
    'year' int(11) NOT NULL,
    't_time' varchar(1000) NOT NULL,
    'to' varchar(1000) NOT NULL,
    'duration' varchar(1000) NOT NULL,
    'facility' varchar(1000) NOT NULL,
    'event' varchar(1000) NOT NULL,
    'description' varchar(1000) NOT NULL,
    'ar_link' varchar(1000) NOT NULL,
    'impact' varchar(1000) NOT NULL
    )"""

    login_table = """ CREATE TABLE IF NOT EXISTS 't_users' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'username' varchar(1000) NOT NULL UNIQUE,
    'password' varchar(1000) NOT NULL,
    'is_admin' int(1000) NOT NULL
    )"""

    srdb_table = """ CREATE TABLE IF NOT EXISTS 't_srdb' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'srdb_name' varchar(1000) NOT NULL,
    'version' varchar(1000) NOT NULL,
    'reason_for_update' int(1000) NOT NULL,
    'link' int(1000) NOT NULL,
    's_c' varchar(1000) NOT NULL
    )"""

    tmtcdb_table = """ CREATE TABLE IF NOT EXISTS 't_tmtcdb' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'tmtcdb_name' varchar(1000) NOT NULL,
    'version' varchar(1000) NOT NULL,
    'reason_for_update' int(1000) NOT NULL,
    'link' int(1000) NOT NULL,
    's_c' varchar(1000) NOT NULL
    )"""

    fd_schedule_table = """CREATE TABLE IF NOT EXISTS 't_fd_schedule' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        day INTEGER,
        date DATE,
        penumbra_entry DATETIME NOT NULL,
        penumbra_exit DATETIME,
        umbra_entry DATETIME,
        umbra_exit DATETIME,
        duration VARCHAR(1000),
        ECL_TIME VARCHAR(255),
        S_C VARCHAR(255)
    )"""

    fd_schedule_2_table = """CREATE TABLE IF NOT EXISTS 't_fd_schedule_2' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        day INTEGER,
        date DATE,
        penumbra_entry DATETIME NOT NULL,
        penumbra_exit DATETIME,
        umbra_entry DATETIME,
        umbra_exit DATETIME,
        duration VARCHAR(1000),
        ECL_TIME VARCHAR(255),
        S_C VARCHAR(255)
    )"""

    fd_schedule_3_table = """CREATE TABLE IF NOT EXISTS 't_fd_schedule_3' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        day INTEGER,
        date DATE,
        penumbra_entry DATETIME NOT NULL,
        penumbra_exit DATETIME,
        umbra_entry DATETIME,
        umbra_exit DATETIME,
        duration VARCHAR(1000),
        ECL_TIME VARCHAR(255),
        S_C VARCHAR(255)
    )"""

    srdb_update_request_table = """ CREATE TABLE IF NOT EXISTS 't_srdb_update_request' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    's_c' varchar(1000) NOT NULL,
    'status' varchar(1000) NOT NULL,
    'status_tl' varchar(1000) NOT NULL,
    'originator' varchar(1000) NOT NULL,
    'date' varchar(1000) NOT NULL,
    'type' varchar(1000) NOT NULL,
    'reason_for_update' varchar(1000) NOT NULL,
    'affected_tables' varchar(1000) NOT NULL,
    'title' varchar(1000),
    'wodb_ref' varchar(1000),
    'srdb_ref' varchar(1000),
    'affected_files' varchar(3000),
    'implemented' varchar(100),
    'tl'        varchar(100),
    'analyst_name'   varchar(100),
    'originator_date'  datetime, 
    'tl_date' datetime,
    'analyst_date' datetime,
    'due_date' datetime
    )"""

    procedure_update_request_table = """ CREATE TABLE IF NOT EXISTS 't_procedure_update_request' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    's_c' varchar(1000) NOT NULL,
    'status' varchar(1000) NOT NULL,
    'status_tl' varchar(1000) NOT NULL,
    'originator' varchar(1000) NOT NULL,
    'date' varchar(1000) NOT NULL,
    'type' varchar(1000) NOT NULL,
    'reason_for_update' varchar(1000) NOT NULL,
    'affected_tables' varchar(1000) NOT NULL,
    'title' varchar(1000),
    'ar_ref' varchar(1000),
    'swet_ref' varchar(1000),
    'affected_files' varchar(3000),
    'implemented' varchar(100),
    'tl'        varchar(100),
    'analyst_name'   varchar(100),
    'originator_date'  datetime, 
    'tl_date' datetime,
    'analyst_date' datetime,
    'due_date' datetime
    )"""

    
    action_1 = """ CREATE TABLE IF NOT EXISTS 't_action1' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    's_c' varchar(1000) NOT NULL,
    'status' varchar(1000) NOT NULL,
    'originator' varchar(1000) NOT NULL,
    'date' varchar(1000) NOT NULL,
    'type' varchar(1000) NOT NULL,
    'reason_for_update' varchar(1000) NOT NULL,
    'affected_tables' varchar(1000) NOT NULL,
    'title' varchar(1000),
    'wodb_ref' varchar(1000),
    'srdb_ref' varchar(1000),
    'affected_files' varchar(3000),
    'implemented' varchar(100)
    )"""

    action_2 = """ CREATE TABLE IF NOT EXISTS 't_action2' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    's_c' varchar(1000) NOT NULL,
    'status' varchar(1000) NOT NULL,
    'originator' varchar(1000) NOT NULL,
    'date' varchar(1000) NOT NULL,
    'type' varchar(1000) NOT NULL,
    'reason_for_update' varchar(1000) NOT NULL,
    'affected_tables' varchar(1000) NOT NULL,
    'title' varchar(1000),
    'ar_ref' varchar(1000),
    'swet_ref' varchar(1000),
    'affected_files' varchar(3000),
    'implemented' varchar(100)
    )"""

    soi_1_table = """ CREATE TABLE IF NOT EXISTS 't_soi_1' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'soi_number' varchar(1000) NOT NULL,
    'soi_name' varchar(1000) NOT NULL,
    'version' int(11) NOT NULL,
    'link' varchar(1000) NOT NULL,
    'from_date' datetime NOT NULL,
    'to' datetime NOT NULL,
    'validity' varchar(1000) NOT NULL,
    'today_date' datetime NOT NULL
    )"""
    
    parameter_1_table = """ CREATE TABLE IF NOT EXISTS 't_parameter_1' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' varchar(1000) NOT NULL,
    'descr' varchar(1000) NOT NULL,
    'pid' int(11) NOT NULL,
    'unit' varchar(1000) NOT NULL,
    'type_code' varchar(1000) NOT NULL,
    'format_code' varchar(1000) NOT NULL,
    'width' varchar(1000) NOT NULL,
    'valid' varchar(1000) NOT NULL,
    'related' varchar(1000) NOT NULL,
    'categ' varchar(1000) NOT NULL,
    'natur' varchar(1000) NOT NULL,
    'curtx' varchar(1000) NOT NULL,
    'inter' varchar(1000) NOT NULL,
    'uscon' varchar(1000) NOT NULL,
    'decim' varchar(1000) NOT NULL,
    'parval' varchar(1000) NOT NULL,
    'subsys' varchar(1000) NOT NULL,
    'valpar' varchar(1000) NOT NULL,
    'sptype' varchar(1000) NOT NULL,
    'coor' varchar(1000) NOT NULL,
    'obtid' varchar(1000) NOT NULL,
    'darc' varchar(1000) NOT NULL,
    'endian' varchar(1000) NOT NULL,
    'mon_check_name' varchar(1000) NOT NULL,
    'mon_check_nbchck' varchar(1000) NOT NULL,
    'mon_check_nbool' varchar(1000) NOT NULL,
    'mon_check_inter' varchar(1000) NOT NULL,
    'mon_check_codin' varchar(1000) NOT NULL,
    'ool_name' varchar(1000) NOT NULL,
    'ool_pos' varchar(1000) NOT NULL,
    'ool_type' varchar(1000) NOT NULL,
    'ool_vlalu' varchar(1000) NOT NULL,
    'ool_hvalu' varchar(1000) NOT NULL,
    'ool_rlchk' varchar(1000) NOT NULL,
    'ool_valpar' varchar(1000) NOT NULL
    )"""

    procedure_1_table = """ CREATE TABLE IF NOT EXISTS 't_procedure_1' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' varchar(1000) NOT NULL,
    'sub_system' varchar(1000) NOT NULL,
    'version' int(11) NOT NULL,
    'pdf_link' varchar(1000) NOT NULL
    )"""

    event_1_table = """ CREATE TABLE IF NOT EXISTS 't_event_1' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'week' int(11) NOT NULL,
    'year' int(11) NOT NULL,
    't_time' varchar(1000) NOT NULL,
    'to' varchar(1000) NOT NULL,
    'duration' varchar(1000) NOT NULL,
    'facility' varchar(1000) NOT NULL,
    'event' varchar(1000) NOT NULL,
    'description' varchar(1000) NOT NULL,
    'ar_link' varchar(1000) NOT NULL,
    'impact' varchar(1000) NOT NULL
    )"""

    schedule_1_table = """CREATE TABLE IF NOT EXISTS 't_schedule_1' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    's_c' varchar(1000) NOT NULL,
    'year' year(4) NOT NULL,
    'qtr' int(11) NOT NULL,
    'month' int(11) NOT NULL,
    'cw' int(11) NOT NULL,
    'doy' int(11) NOT NULL,    
    'start_of_operation' datetime NOT NULL, 
    'end_of_operation' datetime NOT NULL,
    'status' varchar(1000) NOT NULL,
    'operations_title' varchar(1000) NOT NULL,
    'outage' varchar(1000) NOT NULL,
    'link' carchar(1000)
    )"""

    fd_schedule_1_table = """CREATE TABLE IF NOT EXISTS 't_fd_schedule_1' (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'fd_id' int(11) NOT NULL,
    'version' int(11) NOT NULL,
    'creation_date' varchar(1000) NOT NULL,
    'originator' varchar(1000) NOT NULL,
    'object_name' varchar(1000) NOT NULL,
    'object_id' varchar(1000) NOT NULL,
    'center_name' varchar(1000) NOT NULL,
    'ref_frame' varchar(1000) NOT NULL,
    'time_system' varchar(1000) NOT NULL,
    'start_time' datetime NOT NULL,
    'stop_time' datetime NOT NULL,
    'type' varchar(1000) NOT NULL,
    'epoch' datetime NOT NULL,
    'duration' varchar(1000) NOT NULL,
    'units' varchar(1000) NOT NULL,
    'unique_id' varchar(1000) NOT NULL,
    'sensor_id' varchar(1000) NOT NULL,
    'target' varchar(1000) NOT NULL,   
    'station' varchar(1000) NOT NULL,
    'co_linearity_angle' varchar(1000) NOT NULL
    )"""

    
    
    c = conn.cursor()
    # c.execute("DROP TABLE 't_fd_schedule';")
    # c.execute("DROP TABLE 't_fd_schedule_2';")
    # c.execute("DROP TABLE 't_fd_schedule_3';")
    c.execute(schedule_table)
    c.execute(schedule_2_table)
    c.execute(schedule_3_table)
    c.execute(anomaly_table)
    c.execute(anomaly_boa_table)    
    c.execute(soi_table)
    c.execute(parameter_table)
    c.execute(procedure_table)
    c.execute(pus_table)
    c.execute(event_table)
    c.execute(login_table)
    c.execute(srdb_table)
    c.execute(tmtcdb_table)
    c.execute(fd_schedule_table)    
    c.execute(fd_schedule_2_table)    
    c.execute(fd_schedule_3_table)    
    c.execute(srdb_update_request_table)
    c.execute(procedure_update_request_table)
    c.execute(soi_1_table)
    c.execute(parameter_1_table)
    c.execute(procedure_1_table)
    c.execute(event_1_table)
    c.execute(schedule_1_table)
    c.execute(fd_schedule_1_table)
    c.execute(action_1)
    c.execute(action_2)
    

    query = f"""SELECT `is_admin` FROM `t_users` WHERE `username` = 'Admin' """
    admin_insert = """INSERT INTO t_users VALUES(NULL, 'Admin', 'Admin', 1)"""
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    if not result:    
        c.execute(admin_insert)
    
    conn.commit()

