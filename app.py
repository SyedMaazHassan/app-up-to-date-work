# app.py

from flask import Flask, render_template, request, \
    redirect, url_for, make_response, session
import pandas as pd
import csv
from io import StringIO
from db import conn, init
from db_helper import *
import datetime
from functools import wraps
from flask import send_file

init()
app = Flask(__name__)
app.secret_key = '$cheDule'

def check_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            session['user'] = check_user_login(request.form.get('username'),
                            request.form.get('password'))
        except Exception as e:
            return render_template('login.html', error='No Such user exists')
        return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['user'] = None
    return redirect(url_for('login'))

@app.route('/home', methods = ['GET'])
def home():
    with open('timer.txt') as f:
        data = f.readline()
    date_obj = datetime.datetime.strptime(data, '%m/%d/%Y %H:%M')

    # Get the difference from now in seconds
    diff_seconds = (date_obj - datetime.datetime.now()).total_seconds()
    timerFlag = "down"
    if (diff_seconds < 0):
        timerFlag = "up"
    seconds = int(abs(diff_seconds))    
    return render_template('home.html', is_admin = session.get('user'), seconds = seconds, timerFlag=timerFlag)

@app.route('/schedules', methods=['GET'])
@check_login
def get_schedules():
    
    week_number = request.args.get('week')
    today = datetime.date.today()
    year = today.isocalendar()[0]
    if week_number is None:        
        week_number = today.isocalendar()[1] + 1

    week_number = int(week_number)
    first_day = datetime.datetime.strptime(f'{year}-W{week_number-1}-1', '%G-W%V-%u').date()
    day_number =first_day.strftime("%j")
    days = [first_day + datetime.timedelta(days=i) for i in range(7)]
    weekday_numbers = [(i + int(day_number)) for i in range(7)]
    data, link = get_schedule_for_week('t_schedule', first_day, first_day + datetime.timedelta(days=6), 7, 10, ['%Y-%m-%d %H:%M:%S'], True)
    return render_template('schedule/schedule.html', week_number = week_number,
                           schedules = data,
                           link = link,
                           days = days, week = weekday_numbers,
                           is_admin = session.get('user'),
                           menuVal = 'submenu1')    


@app.route('/schedules_2', methods=['GET'])
@check_login
def get_schedules_2():
    
    week_number = request.args.get('week')
    today = datetime.date.today()
    year = today.isocalendar()[0]
    if week_number is None:        
        week_number = today.isocalendar()[1] + 1

    week_number = int(week_number)
    first_day = datetime.datetime.strptime(f'{year}-W{week_number-1}-1', '%G-W%V-%u').date()
    day_number =first_day.strftime("%j")
    days = [first_day + datetime.timedelta(days=i) for i in range(7)]
    weekday_numbers = [(i + int(day_number)) for i in range(7)]
    data, link = get_schedule_for_week('t_schedule_2', first_day, first_day + datetime.timedelta(days=6), 7, 10, ['%Y-%m-%d %H:%M:%S'], True)
    return render_template('schedule_2/schedule.html', week_number = week_number,
                           schedules = data,
                           link = link,
                           days = days, week = weekday_numbers,
                           is_admin = session.get('user'),
                           menuVal = 'submenu1')    


@app.route('/schedules_3', methods=['GET'])
@check_login
def get_schedules_3():
    
    week_number = request.args.get('week')
    today = datetime.date.today()
    year = today.isocalendar()[0]
    if week_number is None:        
        week_number = today.isocalendar()[1] + 1

    week_number = int(week_number)
    first_day = datetime.datetime.strptime(f'{year}-W{week_number-1}-1', '%G-W%V-%u').date()
    day_number =first_day.strftime("%j")
    days = [first_day + datetime.timedelta(days=i) for i in range(7)]
    weekday_numbers = [(i + int(day_number)) for i in range(7)]
    data, link = get_schedule_for_week('t_schedule_3', first_day, first_day + datetime.timedelta(days=6), 7, 10, ['%Y-%m-%d %H:%M:%S'], True)
    return render_template('schedule_3/schedule.html', week_number = week_number,
                           schedules = data,
                           link = link,
                           days = days, week = weekday_numbers,
                           is_admin = session.get('user'),
                           menuVal = 'submenu1')    





    
@app.route('/schedules/<int:schedule_id>')
@check_login
def schedule_detail(schedule_id):
    data = get_record_by_table_name('t_schedule', schedule_id)
    return render_template('schedule/schedule_detail.html', schedule=data, is_admin = session.get('user'))



@app.route('/api/schedules/delete/<int:schedule_id>')
@check_login
def delete_schedule(schedule_id):
    delete_record_by_table_name('t_schedule', schedule_id)
    url = url_for('get_schedules')
    return redirect(url)
    
@app.route('/api/schedule/upload', methods=['POST'])
@check_login
def upload():    
    insert_data_from_excel('t_schedule', request.files['file'], [7,8])
    url = url_for('get_schedules')
    return redirect(url)


@app.route('/api/schedule_2/upload', methods=['POST'])
@check_login
def upload_schedule_2():    
    insert_data_from_excel('t_schedule_2', request.files['file'], [7,8])
    url = url_for('get_schedules_2')
    return redirect(url)


@app.route('/api/schedule_3/upload', methods=['POST'])
@check_login
def upload_schedule_3():    
    insert_data_from_excel('t_schedule_3', request.files['file'], [7,8])
    url = url_for('get_schedules_3')
    return redirect(url)


@app.route('/api/export/csv')
@check_login
def export_csv():
    cur = conn.cursor()
    cur.execute('SELECT * FROM t_schedule')
    schedules = cur.fetchall()
    cur.close()
    
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    
    # Add headers to the CSV data
    writer.writerow(['id', 'title', 's_c', 'year', 'qtr', 'month', 'cw', 'doy', 'start_of_operation', 'end_of_operation', 'uplink_date', 'status', 'unit', 'execution_type', 'ops_scenario', 'operations_title', 'outage', 'operations_reference', 'request_id', 'request_source', 'una'])
    # Add rows of data to the CSV data
    for schedule in schedules:
         writer.writerow(list(schedule))
    
    # Create a response with the CSV data
    response = make_response(csv_data.getvalue().encode('utf-8'))
    response.headers.set('Content-Disposition', 'attachment', filename='schedules.csv')
    response.headers.set('Content-Type', 'text/csv')
    return response

@app.route('/schedule/update/<int:schedule_id>')
@check_login
def schedule_update_view(schedule_id):
    data = get_record_by_table_name('t_schedule', schedule_id)
    return render_template('schedule/schedule_update.html', schedule=data)

@app.route('/api/schedule/update/<int:schedule_id>', methods=['POST'])
@check_login
def schedule_update(schedule_id):

    update_data('t_schedule', schedule_id, 
                s_c = request.form.get('s_c'),
                year = request.form.get('year'),
                qtr = request.form.get('qtr'),
                month = request.form.get('month'),
                cw = request.form.get('cw'),
                doy = request.form.get('doy'),
                start_of_operation = request.form.get('start_of_operation'),
                end_of_operation = request.form.get('end_of_operation'),
                status = request.form.get('status'),
                operations_title = request.form.get('operations_title'),
                outage = request.form.get('outage'))

    url = url_for('schedule_update_view', schedule_id = schedule_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/anomaly', methods=['GET'])
@check_login
def get_anomalies():
    
    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_anomaly'
    if filters:
        data = filter_data(table_name, event = ('LIKE', filters.get('event')),
                           anomaly = ('LIKE', filters.get('anomaly')),
                           facility = ('LIKE', filters.get('facility')))
    else:
        data = filter_data(table_name)
    return render_template('anomaly/anomaly.html', anomalies = data, menuVal = 'submenu1', is_admin = session.get('user'))    

# Create a route to handle the API request
@app.route('/api/anomaly/upload', methods=['POST'])
@check_login
def upload_anomaly():    
    
    insert_data_from_excel_anomaly('t_anomaly', request.files['file'])
    url = url_for('get_anomalies')
    return redirect(url)

@app.route('/api/anomaly/upload/boa', methods=['POST'])
@check_login
def upload_anomaly_boa():    
    
    try:
        insert_data_for_anomaly_boa(request.files['file'])
        url = url_for('get_anomalies')
        return redirect(url)
    except Exception as e:
        print(e)
        
@app.route('/api/anomaly/delete/<int:anomaly_id>')
@check_login
def delete_anomaly(anomaly_id):

    delete_record_by_table_name('t_anomaly', anomaly_id)
    url = url_for('get_anomalies')
    return redirect(url)

@app.route('/anomaly/<int:anomaly_id>')
@check_login
def anomaly_detail(anomaly_id):

    anomaly = get_record_by_table_name('t_anomaly', anomaly_id)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM t_anomaly_boa WHERE anomaly_id = {anomaly[0]}')
    anomaly_boa = cursor.fetchall()
    cursor.close()
    anomaly_boa = [] if anomaly_boa is None else anomaly_boa
    return render_template('anomaly/anomaly_detail.html', anomaly=anomaly, anomaly_boa = anomaly_boa, is_admin = session.get('user'))

@app.route('/anomaly/update/<int:anomaly_id>')
@check_login
def anomaly_update_view(anomaly_id):
    data = get_record_by_table_name('t_anomaly', anomaly_id)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM t_anomaly_boa WHERE anomaly_id = {data[0]}')
    anomaly_boa = cursor.fetchall()
    cursor.close()
    anomaly_boa = [] if anomaly_boa is None else anomaly_boa
    return render_template('anomaly/anomaly_update.html', anomaly=data, anomaly_boa = anomaly_boa,  is_admin = session.get('user'))

@app.route('/api/anomaly/boa/update/<int:anomaly_id>', methods=['POST'])
@check_login
def anomaly_update_boa(anomaly_id):
    boa1 = request.form.getlist('boa1')
    boa2 = request.form.getlist('boa2')
    boa3 = request.form.getlist('boa3')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM t_anomaly_boa WHERE anomaly_id = {anomaly_id}")
    query = """INSERT INTO t_anomaly_boa VALUES (NULL, ?, ?, ?, ?)"""
    data = [(anomaly_id, boa1[i], boa2[i], boa3[i]) for i in range(len(boa1))]
    cursor.executemany(query, data)
    conn.commit()
    url = url_for('anomaly_update_view', anomaly_id = anomaly_id, is_admin = session.get('user'))
    return redirect(url)


@app.route('/api/anomaly/update/<int:anomaly_id>', methods=['POST'])
@check_login
def anomaly_update(anomaly_id):

    update_data('t_anomaly', anomaly_id, 
                facility = request.form.get('facility'),
                anomaly = request.form.get('anomaly'),
                event = request.form.get('event'),
                cell_cnt = request.form.get('cell_cnt'),
                impact = request.form.get('impact'),
                ar_number = request.form.get('ar_number'),
                recover_action = request.form.get('recover_action'),
                date = request.form.get('date'),
                week = request.form.get('week'))

    url = url_for('anomaly_update_view', anomaly_id = anomaly_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/soi', methods=['GET'])
@check_login
def get_all_soi():
    
    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_soi'
    if filters:
        data = filter_data(table_name, soi_number = ('LIKE', filters.get('soiNumber')),
                           soi_name = ('LIKE', filters.get('soiName')),
                           validity = ('LIKE', filters.get('valid')),
                           version = ('LIKE', filters.get('version')))
    else:
        data = filter_data(table_name)
    
    return render_template('soi/soi.html', soi_all = data, is_admin = session.get('user'), menuVal = 'submenu1')    

@app.route('/api/soi/upload', methods=['POST'])
@check_login
def upload_soi():    

    insert_data_from_excel('t_soi', request.files['file'], [5,6,8])
    url = url_for('get_all_soi')
    return redirect(url)

@app.route('/api/soi/delete/<int:soi_id>')
@check_login
def delete_soi(soi_id):

    delete_record_by_table_name('t_soi', soi_id)
    url = url_for('get_all_soi')
    return redirect(url)

@app.route('/soi/<int:soi_id>')
@check_login
def soi_detail(soi_id):
    soi = get_record_by_table_name('t_soi', soi_id)

    return render_template('soi/soi_detail.html', soi=soi, is_admin = session.get('user'))

@app.route('/soi/update/<int:soi_id>')
@check_login
def soi_update_view(soi_id):
    data = get_record_by_table_name('t_soi', soi_id)
    return render_template('soi/soi_update.html', soi=data, is_admin = session.get('user'))

@app.route('/api/soi/update/<int:soi_id>', methods=['POST'])
@check_login
def soi_update(soi_id):

    update_data('t_soi', soi_id, 
                soi_number = request.form.get('soi_number'),
                soi_name = request.form.get('soi_name'),
                version = request.form.get('version'),
                link = request.form.get('link'),
                from_date = request.form.get('from_date'),
                to = request.form.get('to'),
                validity = request.form.get('validity'),
                today_date = request.form.get('today_date'))

    url = url_for('soi_update_view', soi_id = soi_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/parameter', methods=['GET'])
@check_login
def get_parameters():
    
    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_parameter'
    if filters:
        data = filter_data(table_name, name = ('LIKE', filters.get('parameterName')),
                           descr = ('LIKE', filters.get('parameterDescr')),
                           pid = ('LIKE', filters.get('parameterPid')),
                           unit = ('LIKE', filters.get('parameterUnit')))
    else:
        data = filter_data(table_name)
    
    return render_template('parameter/parameter.html', parameters = data, is_admin = session.get('user'), menuVal = 'submenu1')    

# Create a route to handle the API request
@app.route('/api/parameter/upload', methods=['POST'])
@check_login
def upload_parameter():    
    
    insert_data_from_excel('t_parameter', request.files['file'])
    url = url_for('get_parameters')
    return redirect(url)

@app.route('/api/parameter/delete/<int:parameter_id>')
@check_login
def delete_parameter(parameter_id):

    delete_record_by_table_name('t_parameter', parameter_id)
    url = url_for('get_parameters')
    return redirect(url)

@app.route('/parameter/<int:parameter_id>')
@check_login
def parameter_detail(parameter_id):
    parameter = get_record_by_table_name('t_parameter', parameter_id)
    return render_template('parameter/parameter_detail.html', parameter=parameter, is_admin = session.get('user'))

@app.route('/parameter/update/<int:parameter_id>')
@check_login
def parameter_update_view(parameter_id):
    data = get_record_by_table_name('t_parameter', parameter_id)
    return render_template('parameter/parameter_update.html', parameter=data, is_admin = session.get('user'))

@app.route('/api/parameter/update/<int:parameter_id>', methods=['POST'])
@check_login
def parameter_update(parameter_id):

    update_data('t_parameter',parameter_id, 
                name = request.form.get('name'),
                descr = request.form.get('descr'),
                pid = request.form.get('pid'),
                unit = request.form.get('unit'),
                type_code = request.form.get('type_code'),
                format_code = request.form.get('format_code'),
                width = request.form.get('width'),
                valid = request.form.get('valid'),
                related = request.form.get('related'),
                categ = request.form.get('categ'),
                natur = request.form.get('natur'),
                curtx = request.form.get('curtx'),
                inter = request.form.get('inter'),
                uscon = request.form.get('uscon'),
                decim = request.form.get('decim'),
                parval = request.form.get('parval'),
                subsys = request.form.get('subsys'),
                valpar = request.form.get('valpar'),
                sptype = request.form.get('sptype'),
                coor = request.form.get('coor'),
                obtid = request.form.get('obtid'),
                darc = request.form.get('darc'),
                endian = request.form.get('endian'),
                mon_check_name = request.form.get('mon_check_name'),
                mon_check_nbchck = request.form.get('mon_check_nbchck'),
                mon_check_nbool = request.form.get('mon_check_nbool'),
                mon_check_inter = request.form.get('mon_check_inter'),
                mon_check_codin = request.form.get('mon_check_codin'),
                ool_name = request.form.get('ool_name'),
                ool_pos = request.form.get('ool_pos'),
                ool_type = request.form.get('ool_type'),
                ool_vlalu = request.form.get('ool_vlalu'),
                ool_hvalu = request.form.get('ool_hvalu'),
                ool_rlchk = request.form.get('ool_rlchk'),
                ool_valpar = request.form.get('ool_valpar'))

    url = url_for('parameter_update_view', parameter_id = parameter_id, is_admin = session.get('user'))
    return redirect(url)


@app.route('/procedure', methods=['GET'])
@check_login
def get_procedures():

    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_procedure'
    if filters:
        data = filter_data(table_name, name = ('LIKE', filters.get('procedureName')),
                           sub_system = ('LIKE', filters.get('subSystem')),
                           version = ('LIKE', filters.get('version')))
    else:
        data = filter_data(table_name)

    return render_template('procedure/procedure.html', procedures = data, is_admin = session.get('user'), menuVal = 'submenu1')    

# Create a route to handle the API request
@app.route('/api/procedure/upload', methods=['POST'])
@check_login
def upload_procedure():    

    insert_data_from_excel('t_procedure', request.files['file'])
    url = url_for('get_procedures')
    return redirect(url)

@app.route('/api/procedure/delete/<int:procedure_id>')
@check_login
def delete_procedure(procedure_id):

    delete_record_by_table_name('t_procedure', procedure_id)
    url = url_for('get_procedures')
    return redirect(url)

@app.route('/procedure/<int:procedure_id>')
@check_login
def procedure_detail(procedure_id):
    
    data = get_record_by_table_name('t_procedure', procedure_id)
    return render_template('procedure/procedure_detail.html', procedure=data, is_admin = session.get('user'))

@app.route('/procedure/update/<int:procedure_id>')
@check_login
def procedure_update_view(procedure_id):
    data = get_record_by_table_name('t_procedure', procedure_id)
    return render_template('procedure/procedure_update.html', procedure=data, is_admin = session.get('user'))

@app.route('/api/procedure/update/<int:procedure_id>', methods=['POST'])
@check_login
def procedure_update(procedure_id):

    update_data('t_procedure', procedure_id, 
                name = request.form.get('name'),
                sub_system = request.form.get('sub_system'),
                version = request.form.get('version'),
                pdf_link = request.form.get('pdf_link'))

    url = url_for('procedure_update_view', procedure_id = procedure_id)
    return redirect(url)

@app.route('/pus', methods=['GET'])
@check_login
def get_pus_all():

    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_pus'
    if filters:
        data = filter_data(table_name, service = ('LIKE', filters.get('service')),
                           name = ('LIKE', filters.get('name')),
                           service_subservice = ('LIKE', filters.get('ssa')),
                           space_segment_app = ('LIKE', filters.get('subService')))
    else:
        data = filter_data(table_name)

    return render_template('pus/pus.html', pus_all = data, is_admin = session.get('user'), menuVal = 'submenu2')    

# Create a route to handle the API request
@app.route('/api/pus/upload', methods=['POST'])
@check_login
def upload_pus():    
    
    insert_data_from_excel('t_pus', request.files['file'])
    url = url_for('get_pus_all')
    return redirect(url)

@app.route('/api/pus/delete/<int:pus_id>')
@check_login
def delete_pus(pus_id):
    
    delete_record_by_table_name('t_pus', pus_id)    
    url = url_for('get_pus_all')
    return redirect(url)

@app.route('/pus/<int:pus_id>')
@check_login
def pus_detail(pus_id):
    data = get_record_by_table_name('t_pus', pus_id)
    return render_template('pus/pus_detail.html', pus=data, is_admin = session.get('user'))

@app.route('/pus/update/<int:pus_id>')
@check_login
def pus_update_view(pus_id):
    data = get_record_by_table_name('t_pus', pus_id)
    return render_template('pus/pus_update.html', pus=data, is_admin = session.get('user'))

@app.route('/api/pus/update/<int:pus_id>', methods=['POST'])
@check_login
def pus_update(pus_id):

    update_data('t_pus', pus_id, 
                service = request.form.get('service'),
                name = request.form.get('name'),
                service_subservice = request.form.get('service_subservice'),
                des_service = request.form.get('des_service'),
                space_segment_app = request.form.get('space_segment_app'))

    url = url_for('pus_update_view', pus_id = pus_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/event', methods=['GET'])
@check_login
def get_event_all():

    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_event'
    if filters:
        data = filter_data(table_name,
                           facility = ('LIKE', filters.get('facility')),
                           event = ('LIKE', filters.get('event')),
                           impact = ('LIKE', filters.get('impact')),
                           )
    else:
        data = filter_data(table_name)
    from_time = filters.get('from')
    to_time = filters.get('to')
    format_string = "%Y-%m-%d %H:%M:%S"
    if from_time is not None and from_time != '':
        from_time = datetime.datetime.strptime(from_time, format_string)
    else:
        from_time = None
    if to_time is not None and to_time != '':
        to_time = datetime.datetime.strptime(to_time, format_string)
    else:
        to_time = None

    ids = ""
    filtered_data = []
    for row in data:
        ids = ids + str(row[0]) + ','
        row_date = datetime.datetime.strptime(row[3], format_string)
        flag = False
        if to_time is None and from_time is None:
            flag = True
        elif to_time is None and from_time is not None and from_time <= row_date:
            flag = True                
        elif to_time is not None and from_time is None and to_time >= row_date:
            flag = True
        elif from_time <= row_date <= to_time:
            flag = True
        
        if flag:        
            filtered_data.append(row)
            ids = ids[:-1]
    return render_template('event/event.html', event_all = filtered_data, is_admin = session.get('user'), ids = ids, menuVal = 'submenu1')    

# Create a route to handle the API request
@app.route('/api/event/upload', methods=['POST'])
@check_login
def upload_event():    
    insert_data_from_excel('t_event', request.files['file'], [3,4])
    url = url_for('get_event_all')
    return redirect(url)

@app.route('/api/event/export', methods=['POST'])
@check_login
def export_event():    
    ids = request.form.get('event_id')
    cur = conn.cursor()
    cur.execute(f'SELECT t_time, `to`, facility, `event`, ar_link, impact FROM t_event WHERE `id` in ({ids}) ')
    events = cur.fetchall()
    cur.close()
    
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    
    # Add headers to the CSV data
    writer.writerow(['T Time', 'To', 'Facility', 'Events', 'AR Link', 'Impact'])
    # Add rows of data to the CSV data
    for event in events:
         writer.writerow(list(event))
    
    # Create a response with the CSV data
    response = make_response(csv_data.getvalue().encode('utf-8'))
    response.headers.set('Content-Disposition', 'attachment', filename='events.csv')
    response.headers.set('Content-Type', 'text/csv')
    return response
    

@app.route('/api/event/delete/<int:event_id>')
@check_login
def delete_event(event_id):
    
    delete_record_by_table_name('t_event', event_id)    
    url = url_for('get_event_all')
    return redirect(url)

@app.route('/event/<int:event_id>')
@check_login
def event_detail(event_id):
    data = get_record_by_table_name('t_event', event_id)
    return render_template('event/event_detail.html', event=data, is_admin = session.get('user'))

@app.route('/event/update/<int:event_id>')
@check_login
def event_update_view(event_id):
    data = get_record_by_table_name('t_event', event_id)
    return render_template('event/event_update.html', event=data, is_admin = session.get('user'))

@app.route('/api/event/update/<int:event_id>', methods=['POST'])
@check_login
def event_update(event_id):

    update_data('t_event', event_id, 
                week = request.form.get('week'),
                year = request.form.get('year'),
                t_time = request.form.get('t_time'),
                to = request.form.get('to'),
                duration = request.form.get('duration'),
                facility = request.form.get('facility'),
                ar_link = request.form.get('ar_link'),
                event = request.form.get('event'),
                description = request.form.get('description'),
                impact = request.form.get('impact'))

    url = url_for('event_update_view', event_id = event_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/user', methods = ['GET', 'POST'])
@check_login
def user():
    if request.method == 'POST':
        flag = True
        try:
            insert_user(request.form['username'], request.form['password'], bool('is_admin' in request.form and request.form['is_admin']))
        except Exception as e:
            flag = False
        return render_template('admin/add_user_screen.html',success=flag, is_admin = session.get('user'))    
    return render_template('admin/add_user_screen.html', is_admin = session.get('user'))    

@app.route('/srdb', methods=['GET'])
@check_login
def get_all_srdb():

    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_srdb'
    if filters:
        data = filter_data(table_name,
                           srdb_name = ('LIKE', filters.get('srdb_name')),
                           s_c = ('LIKE', filters.get('s_c')),
                           version = ('LIKE', filters.get('version')),
                           reason_for_update = ('LIKE', filters.get('reason_for_update')))
    else:
        data = filter_data(table_name)

    return render_template('SRDB/srdb.html', srdb_all = data, is_admin = session.get('user'), menuVal = 'submenu2')    

# Create a route to handle the API request
@app.route('/api/srdb/upload', methods=['POST'])
@check_login
def upload_srdb():    
    insert_data_from_excel('t_srdb', request.files['file'])
    url = url_for('get_all_srdb')
    return redirect(url)

@app.route('/api/srdb/delete/<int:srdb_id>')
@check_login
def delete_srdb(srdb_id):
    
    delete_record_by_table_name('t_srdb', srdb_id)    
    url = url_for('get_all_srdb')
    return redirect(url)

@app.route('/srdb/<int:srdb_id>')
@check_login
def srdb_detail(srdb_id):
    data = get_record_by_table_name('t_srdb', srdb_id)
    return render_template('SRDB/srdb_detail.html', srdb=data, is_admin = session.get('user'))

@app.route('/srdb/update/<int:srdb_id>')
@check_login
def srdb_update_view(srdb_id):
    data = get_record_by_table_name('t_srdb', srdb_id)
    return render_template('srdb/srdb_update.html', srdb=data, is_admin = session.get('user'))

@app.route('/api/srdb/update/<int:srdb_id>', methods=['POST'])
@check_login
def srdb_update(srdb_id):

    update_data('t_srdb', srdb_id, 
                srdb_name = request.form.get('srdb_name'),
                version = request.form.get('version'),
                s_c = request.form.get('s_c'),
                reason_for_update = request.form.get('reason_for_update'),
                link = request.form.get('link'))
    
    url = url_for('srdb_update_view', srdb_id = srdb_id, is_admin = session.get('user'))
    return redirect(url)
    

@app.route('/tmtcdb', methods=['GET'])
@check_login
def get_all_tmtcdb():

    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_tmtcdb'
    if filters:
        data = filter_data(table_name,
                           tmtcdb_name = ('LIKE', filters.get('tmtcdb_name')),
                           s_c = ('LIKE', filters.get('s_c')),
                           version = ('LIKE', filters.get('version')),
                           reason_for_update = ('LIKE', filters.get('reason_for_update')))
    else:
        data = filter_data(table_name)

    return render_template('TMTCDB/tmtcdb.html', tmtcdb_all = data, is_admin = session.get('user'), menuVal = 'submenu1')    

# Create a route to handle the API request
@app.route('/api/tmtcdb/upload', methods=['POST'])
@check_login
def upload_tmtcdb():    
    insert_data_from_excel('t_tmtcdb', request.files['file'])
    url = url_for('get_all_tmtcdb')
    return redirect(url)

@app.route('/api/tmtcdb/delete/<int:tmtcdb_id>')
@check_login
def delete_tmtcdb(tmtcdb_id):
    
    delete_record_by_table_name('t_tmtcdb', tmtcdb_id)    
    url = url_for('get_all_tmtcdb')
    return redirect(url)

@app.route('/tmtcdb/<int:tmtcdb_id>')
@check_login
def tmtcdb_detail(tmtcdb_id):
    data = get_record_by_table_name('t_tmtcdb', tmtcdb_id)
    return render_template('TMTCDB/tmtcdb_detail.html', tmtcdb=data, is_admin = session.get('user'))

@app.route('/tmtcdb/update/<int:tmtcdb_id>')
@check_login
def tmtcdb_update_view(tmtcdb_id):
    data = get_record_by_table_name('t_tmtcdb', tmtcdb_id)
    return render_template('tmtcdb/tmtcdb_update.html', tmtcdb=data, is_admin = session.get('user'))

@app.route('/api/tmtcdb/update/<int:tmtcdb_id>', methods=['POST'])
@check_login
def tmtcdb_update(tmtcdb_id):

    update_data('t_tmtcdb', tmtcdb_id, 
                tmtcdb_name = request.form.get('tmtcdb_name'),
                s_c = request.form.get('s_c'),
                version = request.form.get('version'),
                reason_for_update = request.form.get('reason_for_update'),
                link = request.form.get('link'))
    
    url = url_for('tmtcdb_update_view', tmtcdb_id = tmtcdb_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/fd_schedules', methods=['GET'])
@check_login
def get_fd_schedules():
    t_fd_schedule = filter_data('t_fd_schedule')
    print(t_fd_schedule)
    return render_template('fd_schedule/fd_schedule.html',
                           fd_schedules = t_fd_schedule,
                           menuVal = 'submenu1',
                           is_admin = session.get('user')
                        )    
    
@app.route('/fd_schedules_2', methods=['GET'])
@check_login
def get_fd_schedules_2():
    t_fd_schedule_2 = filter_data('t_fd_schedule_2')
    print(t_fd_schedule_2)
    return render_template('fd_schedule_2/fd_schedule.html',
                           fd_schedules = t_fd_schedule_2,
                           menuVal = 'submenu1',
                           is_admin = session.get('user')
                        )    


@app.route('/fd_schedules_3', methods=['GET'])
@check_login
def get_fd_schedules_3():
    t_fd_schedule_3 = filter_data('t_fd_schedule_3')
    print(t_fd_schedule_3)
    return render_template('fd_schedule_3/fd_schedule.html',
                           fd_schedules = t_fd_schedule_3,
                           menuVal = 'submenu1',
                           is_admin = session.get('user')
                        )    

@app.route('/fd_schedules/<int:fd_schedule_id>')
@check_login
def fd_schedule_detail(fd_schedule_id):
    data = get_record_by_table_name('t_fd_schedule', fd_schedule_id)
    return render_template('fd_schedule/fd_schedule_detail.html', fd_schedule=data, is_admin = session.get('user'))

@app.route('/api/fd_schedules/delete/<int:fd_schedule_id>')
@check_login
def fd_delete_schedule(fd_schedule_id):

    delete_record_by_table_name('t_fd_schedule', fd_schedule_id)
    url = url_for('get_fd_schedules')
    return redirect(url)

# Function to convert string to datetime
def parse_datetime(datetime_obj):
    if pd.isna(datetime_obj):
        return ""
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

# Function to convert string to date
def parse_date(date_obj):
    if pd.isna(date_obj):
        return ""
    return date_obj.strftime('%Y-%m-%d')


# Function to insert data into SQLite database
def insert_data_into_db_new(data, table_name='t_fd_schedule'):
    cursor = conn.cursor()
    for row in data.itertuples(index=False):
        if len(row) < 4:  # Ensure row has at least 4 elements
            continue
        
        penumbra_entry = parse_datetime(row[3])
        if not penumbra_entry:  # Check if penumbra_entry is None or NaT
            continue
        
        # Convert duration to string if not already
        duration = str(row[7]) if len(row) > 7 and row[7] is not None else None
        
        # Insert data into the database
        cursor.execute(f'''
            INSERT INTO {table_name} (year, day, date, penumbra_entry, penumbra_exit, umbra_entry, umbra_exit, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row[0], row[1], parse_date(row[2]), penumbra_entry, parse_datetime(row[4]), parse_datetime(row[5]), parse_datetime(row[6]), duration))
    
    conn.commit()


@app.route('/api/fd_schedule/upload', methods=['POST'])
@check_login
def fd_schedule_upload():    
    # insert_data_from_excel('t_fd_schedule', request.files['file'], [3,10,11,13])
    file = request.files['file']
    df = pd.read_excel(file)
    insert_data_into_db_new(df)
    url = url_for('get_fd_schedules')
    return redirect(url)


@app.route('/api/fd_schedule_2/upload', methods=['POST'])
@check_login
def fd_schedule_upload_2():    
    # insert_data_from_excel('t_fd_schedule', request.files['file'], [3,10,11,13])
    file = request.files['file']
    df = pd.read_excel(file)
    insert_data_into_db_new(df, 't_fd_schedule_2')
    url = url_for('get_fd_schedules_2')
    return redirect(url)


@app.route('/api/fd_schedule_3/upload', methods=['POST'])
@check_login
def fd_schedule_upload_3():    
    # insert_data_from_excel('t_fd_schedule', request.files['file'], [3,10,11,13])
    file = request.files['file']
    df = pd.read_excel(file)
    insert_data_into_db_new(df, 't_fd_schedule_3')
    url = url_for('get_fd_schedules_3')
    return redirect(url)


@app.route('/fd_schedule/update/<int:fd_schedule_id>')
@check_login
def fd_schedule_update_view(fd_schedule_id):
    data = get_record_by_table_name('t_fd_schedule', fd_schedule_id)
    return render_template('fd_schedule/fd_schedule_update.html', fd_schedule=data)

@app.route('/api/fd_schedule/update/<int:fd_schedule_id>', methods=['POST'])
@check_login
def fd_schedule_update(fd_schedule_id):

    update_data('t_fd_schedule', fd_schedule_id, 
                fd_id = request.form.get('fd_id'),
                version = request.form.get('version'),
                creation_date = request.form.get('creation_date'),
                originator = request.form.get('originator'),
                object_name = request.form.get('object_name'),
                object_id = request.form.get('object_id'),
                center_name = request.form.get('center_name'),
                ref_frame = request.form.get('ref_frame'),
                time_system = request.form.get('time_system'),
                start_time = request.form.get('start_time'),
                stop_time = request.form.get('stop_time'),
                type = request.form.get('type'),
                epoch = request.form.get('epoch'),
                duration = request.form.get('duration'),
                units = request.form.get('units'),
                unique_id = request.form.get('unique_id'),
                sensor_id = request.form.get('sensor_id'),
                target = request.form.get('target'),
                station = request.form.get('station'),
                co_linearity_angle = request.form.get('co_linearity_angle'))

    url = url_for('fd_schedule_update_view', fd_schedule_id = fd_schedule_id, is_admin = session.get('user'))
    return redirect(url)
    
@app.route('/srdb/update/request', methods=['GET'])
@check_login
def get_all_srdb_update_request():
    
    data = filter_data('t_srdb_update_request')
    return render_template('srdb_update_request/srdb_update_request.html', rows = data, is_admin = session.get('user'))


@app.route('/srdb/add/update/request', methods=['GET', 'POST'])
@check_login
def add_srdb_update_request():
    if request.method == 'POST':
        save_update_request('t_srdb_update_request', 
                            person=request.form.get('person'),
                            type=request.form.get('type'),
                            table=request.form.getlist('table'),
                            title=request.form.get('title'),
                            description=request.form.get('description'),
                            s_c=request.form.get('s_c'),
                            wodb_ref=request.form.get('wodb_ref'),
                            affected_files = request.files.getlist('affected_files'),
                            srdb_ref=request.form.get('srdb_ref'),
                            tl=request.form.get('tl'),
                            analyst_name=request.form.get('analyst_name'),
                            implemented= "Not Implemented",
                            due_date=request.form.get('due_date')
                            )
        
        url = url_for('get_all_srdb_update_request')
        return redirect(url)
    
    analyst_names, tl_names, persons, tables, types, s_c_values = get_entries_data("srdb_entries.txt")    
    return render_template('srdb_update_request/add_srdb_update_request.html', persons=persons, s_c_values = s_c_values, 
                        tables=tables, types=types, is_admin = session.get('user'), analyst_names=analyst_names, tl_names=tl_names)

@app.route('/update/srdb/update/request/<int:srdb_update_request_id>', methods=['GET', 'POST'])
@check_login
def update_srdb_update_request(srdb_update_request_id):
    if request.method == 'POST':
        tables = ','.join(request.form.getlist('table')).strip()
        update_data('t_srdb_update_request', srdb_update_request_id,
                        originator=request.form.get('person'),
                        type=request.form.get('type'),
                        affected_tables=tables,
                        title=request.form.get('title'),
                        reason_for_update=request.form.get('description'),
                        s_c=request.form.get('s_c'),
                        tl=request.form.get('tl'),
                        affected_files = request.files.getlist('affected_files'),
                        analyst_name=request.form.get('analyst_name'),
                        wodb_ref=request.form.get('wodb_ref'),
                        srdb_ref=request.form.get('srdb_ref'),
                        due_date=request.form.get('due_date'),
                        )
        
    analyst_names, tl_names, persons, tables, types, s_c_values = get_entries_data("srdb_entries.txt")    
    data = get_record_by_table_name('t_srdb_update_request', srdb_update_request_id)
    data = list(data)
    data[7] = data[7].split(',')
    return render_template('srdb_update_request/update_srdb_update_request.html', persons=persons, s_c_values = s_c_values, 
                        tables=tables, types=types, data = data, is_admin = session.get('user'), analyst_names=analyst_names, tl_names=tl_names)


@app.route('/srdb/update/request/verify/<int:srdb_update_request_id>')
@check_login
def srdb_update_request_verify(srdb_update_request_id):
    update_data('t_srdb_update_request', srdb_update_request_id,
                status = 'VERIFIED', analyst_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    url = url_for('get_all_srdb_update_request')
    return redirect(url)

@app.route('/srdb/update/request/verify_tl/<int:srdb_update_request_id>')
@check_login
def srdb_update_request_verify_tl(srdb_update_request_id):
    update_data('t_srdb_update_request', srdb_update_request_id,
                status_tl = 'VERIFIED', tl_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    url = url_for('get_all_srdb_update_request')
    return redirect(url)

@app.route('/srdb/update/request/implement/<int:srdb_update_request_id>')
@check_login
def srdb_update_request_implemented(srdb_update_request_id):
    update_data('t_srdb_update_request', srdb_update_request_id,
                implemented = 'Implemented')

    url = url_for('get_all_srdb_update_request')
    return redirect(url)


@app.route('/srdb/update/request/<int:srdb_update_request_id>')
@check_login
def srdb_update_request_detail(srdb_update_request_id):
    data = get_record_by_table_name('t_srdb_update_request', srdb_update_request_id)
    return render_template('srdb_update_request/srdb_update_request_detail.html', data=data, is_admin = session.get('user'))

@app.route('/api/srdb/update/request/delete/<int:srdb_update_request_id>')
@check_login
def delete_srdb_update_request(srdb_update_request_id):

    delete_record_by_table_name('t_srdb_update_request', srdb_update_request_id)
    url = url_for('get_all_srdb_update_request')
    return redirect(url)
    
@app.route('/api/srdb/update/request/upload', methods=['POST'])
@check_login
def srdb_update_request_upload():    
    df = pd.read_excel(request.files['file'])
    df = df.fillna('-')

    table_name = 't_srdb_update_request'
    data = [(None,) + tuple(x) for x in df.values]
    final_data = []
    for row in data:
        arr = []
        for _, col in enumerate(row):
            arr.append(col)
        final_data.append(tuple(arr)) 

    placeholders = "?, " + ", ".join(["?" for _ in range(len(df.columns))])
    query = f"INSERT INTO {table_name}(id, s_c, `status`,originator, `date`, `type`, reason_for_update, affected_tables, affected_files) VALUES ({placeholders})"    
    cursor = conn.cursor()
    cursor.executemany(query, final_data)
    conn.commit()

    url = url_for('get_all_srdb_update_request')
    return redirect(url)

@app.route('/procedure/update/request', methods=['GET'])
@check_login
def get_all_procedure_update_request():
    
    data = filter_data('t_procedure_update_request')
    return render_template('procedure_update_request/procedure_update_request.html', rows = data, is_admin = session.get('user'))

@app.route('/procedure/add/update/request', methods=['GET', 'POST'])
@check_login
def add_procedure_update_request():
    if request.method == 'POST':
        save_update_request('t_procedure_update_request',
                            person=request.form.get('person'),
                            type=request.form.get('type'),
                            table=request.form.getlist('table'),
                            title=request.form.get('title'),
                            description=request.form.get('description'),
                            s_c=request.form.get('s_c'),
                            ar_ref=request.form.get('ar_ref'),
                            affected_files = request.files.getlist('affected_files'),
                            swet_ref=request.form.get('swet_ref'),
                            tl=request.form.get('tl'),
                            analyst_name=request.form.get('analyst_name'),
                            implemented= "Not Implemented",
                            due_date = request.form.get('due_date')
                            )
        
        url = url_for('get_all_procedure_update_request')
        return redirect(url)
    
    analyst_names, tl_names, persons, tables, types, s_c_values = get_entries_data("procedure_entries.txt")    
    return render_template('procedure_update_request/add_procedure_update_request.html', persons=persons, s_c_values = s_c_values, 
                        tables=tables, types=types, is_admin = session.get('user'), analyst_names=analyst_names, tl_names=tl_names)

@app.route('/srdb_update_request/download/file/<int:id>', methods=['GET'])
@check_login
def download_srdb_update_request_file(id):

    filename = get_file_name('t_srdb_update_request', id)
    if filename:
        return send_file(f"files/{filename}", as_attachment=True)
    else:
        url = url_for('get_all_srdb_update_request')
        return redirect(url)

@app.route('/update/procedure/update/request/<int:procedure_update_request_id>', methods=['GET', 'POST'])
@check_login
def update_procedure_update_request(procedure_update_request_id):
    if request.method == 'POST':
        tables = ','.join(request.form.getlist('table')).strip()
        update_data('t_procedure_update_request', procedure_update_request_id,
                        originator=request.form.get('person'),
                        type=request.form.get('type'),
                        affected_tables=tables,
                        title=request.form.get('title'),
                        reason_for_update=request.form.get('description'),
                        affected_files = request.files.getlist('affected_files'),
                        s_c=request.form.get('s_c'),
                        ar_ref=request.form.get('ar_ref'),
                        tl=request.form.get('tl'),
                        analyst_name=request.form.get('analyst_name'),
                        swet_ref=request.form.get('swet_ref'),
                        due_date=request.form.get('due_date')
                        )
        
    analyst_names, tl_names, persons, tables, types, s_c_values = get_entries_data("srdb_entries.txt")    
    data = get_record_by_table_name('t_procedure_update_request', procedure_update_request_id)
    data = list(data)
    data[7] = data[7].split(',')
    return render_template('procedure_update_request/update_procedure_update_request.html', persons=persons, s_c_values = s_c_values, 
                        tables=tables, types=types, data = data, is_admin = session.get('user'), analyst_names=analyst_names, tl_names=tl_names)

@app.route('/procedure_update_request/download/file/<int:id>', methods=['GET'])
@check_login
def download_procedure_update_request_file(id):

    filename = get_file_name('t_procedure_update_request', id)
    if filename:
        return send_file(f"files/{filename}", as_attachment=True)
    else:
        url = url_for('get_all_procedure_update_request')
        return redirect(url)


@app.route('/procedure/update/request/verify/<int:procedure_update_request_id>')
@check_login
def procedure_update_request_verify(procedure_update_request_id):
    update_data('t_procedure_update_request', procedure_update_request_id,
                status = 'VERIFIED', analyst_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    url = url_for('get_all_procedure_update_request')
    return redirect(url)

@app.route('/procedure/update/request/verify_tl/<int:procedure_update_request_id>')
@check_login
def procedure_update_request_verify_tl(procedure_update_request_id):
    update_data('t_procedure_update_request', procedure_update_request_id,
                status_tl = 'VERIFIED', tl_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    url = url_for('get_all_procedure_update_request')
    return redirect(url)

@app.route('/procedure/update/request/implement/<int:procedure_update_request_id>')
@check_login
def procedure_update_request_implement(procedure_update_request_id):
    update_data('t_procedure_update_request', procedure_update_request_id,
                implemented = 'implemented')

    url = url_for('get_all_procedure_update_request')
    return redirect(url)


@app.route('/procedure/update/request/<int:procedure_update_request_id>')
@check_login
def procedure_update_request_detail(procedure_update_request_id):
    data = get_record_by_table_name('t_procedure_update_request',procedure_update_request_id)
    return render_template('procedure_update_request/procedure_update_request_detail.html', data=data, is_admin = session.get('user'))

@app.route('/api/procedure/update/request/delete/<int:procedure_update_request_id>')
@check_login
def delete_procedure_update_request(procedure_update_request_id):

    delete_record_by_table_name('t_procedure_update_request', procedure_update_request_id)
    url = url_for('get_all_procedure_update_request')
    return redirect(url)
                
@app.route('/api/procedure/update/request/upload', methods=['POST'])
@check_login
def procedure_update_request_upload():    
    df = pd.read_excel(request.files['file'])
    df = df.fillna('-')

    table_name = 't_procedure_update_request'
    data = [(None,) + tuple(x) for x in df.values]
    final_data = []
    for row in data:
        arr = []
        for _, col in enumerate(row):
            arr.append(col)
        final_data.append(tuple(arr)) 

    placeholders = "?, " + ", ".join(["?" for _ in range(len(df.columns))])
    query = f"INSERT INTO {table_name}(id, s_c, `status`,originator, `date`, `type`, reason_for_update, affected_tables, affected_files) VALUES ({placeholders})"    
    cursor = conn.cursor()
    cursor.executemany(query, final_data)
    conn.commit()

    url = url_for('get_all_procedure_update_request')
    return redirect(url)

@app.route('/action1/update/request', methods=['GET'])
@check_login
def get_all_action1_update_request():
    
    data = filter_data('t_action1')
    return render_template('action1_update_request/action1_update_request.html', rows = data, is_admin = session.get('user'))


@app.route('/action1/add/update/request', methods=['GET', 'POST'])
@check_login
def add_action1_update_request():
    if request.method == 'POST':
        save_action_request('t_action1', 
                            person=request.form.get('person'),
                            type=request.form.get('type'),
                            table=request.form.getlist('table'),
                            title=request.form.get('title'),
                            description=request.form.get('description'),
                            s_c=request.form.get('s_c'),
                            wodb_ref=request.form.get('wodb_ref'),
                            affected_files = request.files.getlist('affected_files'),
                            srdb_ref=request.form.get('srdb_ref'),
                            tl=request.form.get('tl'),
                            analyst_name=request.form.get('analyst_name'),
                            implemented= "Not Implemented")
        
        url = url_for('get_all_action1_update_request')
        return redirect(url)
    
    analyst_names, tl_names, persons, tables, types, s_c_values = get_entries_data("srdb_entries.txt")    
    return render_template('action1_update_request/add_action1_update_request.html', persons=persons, s_c_values = s_c_values, 
                        tables=tables, types=types, is_admin = session.get('user'), analyst_names=analyst_names, tl_names=tl_names)

@app.route('/update/action1/update/request/<int:action1_update_request_id>', methods=['GET', 'POST'])
@check_login
def update_action1_update_request(action1_update_request_id):
    if request.method == 'POST':
        tables = ','.join(request.form.getlist('table')).strip()
        update_data('t_action1', action1_update_request_id,
                        originator=request.form.get('person'),
                        type=request.form.get('type'),
                        affected_tables=tables,
                        title=request.form.get('title'),
                        reason_for_update=request.form.get('description'),
                        s_c=request.form.get('s_c'),
                        wodb_ref=request.form.get('wodb_ref'),
                        srdb_ref=request.form.get('srdb_ref'))
        
    analyst_names, tl_names, persons, tables, types, s_c_values = get_entries_data("srdb_entries.txt")    
    data = get_record_by_table_name('t_action1', action1_update_request_id)
    data = list(data)
    data[7] = data[7].split(',')
    return render_template('action1_update_request/update_action1_update_request.html', persons=persons, s_c_values = s_c_values, 
                        tables=tables, types=types, data = data, is_admin = session.get('user'), analyst_names=analyst_names, tl_names=tl_names)


@app.route('/action1/update/request/verify/<int:action1_update_request_id>')
@check_login
def action1_update_request_verify(action1_update_request_id):
    update_data('t_action1', action1_update_request_id,
                status = 'VERIFIED')

    url = url_for('get_all_action1_update_request')
    return redirect(url)

@app.route('/action1/update/request/implement/<int:action1_update_request_id>')
@check_login
def action1_update_request_implemented(action1_update_request_id):
    update_data('t_action1', action1_update_request_id,
                implemented = 'Implemented')

    url = url_for('get_all_action1_update_request')
    return redirect(url)


@app.route('/action1/update/request/<int:action1_update_request_id>')
@check_login
def action1_update_request_detail(action1_update_request_id):
    data = get_record_by_table_name('t_action1', action1_update_request_id)
    return render_template('action1_update_request/action1_update_request_detail.html', data=data, is_admin = session.get('user'))

@app.route('/api/action1/update/request/delete/<int:action1_update_request_id>')
@check_login
def delete_action1_update_request(action1_update_request_id):

    delete_record_by_table_name('t_action1', action1_update_request_id)
    url = url_for('get_all_action1_update_request')
    return redirect(url)
    
@app.route('/api/action1/update/request/upload', methods=['POST'])
@check_login
def action1_update_request_upload():    
    df = pd.read_excel(request.files['file'])
    df = df.fillna('-')

    table_name = 't_action1'
    data = [(None,) + tuple(x) for x in df.values]
    final_data = []
    for row in data:
        arr = []
        for _, col in enumerate(row):
            arr.append(col)
        final_data.append(tuple(arr)) 

    placeholders = "?, " + ", ".join(["?" for _ in range(len(df.columns))])
    query = f"INSERT INTO {table_name}(id, s_c, `status`,originator, `date`, `type`, reason_for_update, affected_tables, affected_files) VALUES ({placeholders})"    
    cursor = conn.cursor()
    cursor.executemany(query, final_data)
    conn.commit()

    url = url_for('get_all_action1_update_request')
    return redirect(url)

@app.route('/action2/update/request', methods=['GET'])
@check_login
def get_all_action2_update_request():
    
    data = filter_data('t_action2')
    return render_template('action2_update_request/action2_update_request.html', rows = data, is_admin = session.get('user'))

@app.route('/action2/add/update/request', methods=['GET', 'POST'])
@check_login
def add_action2_update_request():
    if request.method == 'POST':
        save_action_request('t_action2',
                            person=request.form.get('person'),
                            type=request.form.get('type'),
                            table=request.form.getlist('table'),
                            title=request.form.get('title'),
                            description=request.form.get('description'),
                            s_c=request.form.get('s_c'),
                            ar_ref=request.form.get('ar_ref'),
                            affected_files = request.files.getlist('affected_files'),
                            swet_ref=request.form.get('swet_ref'),
                            implemented= "Not Implemented")
        
        url = url_for('get_all_action2_update_request')
        return redirect(url)
    
    analyst_names, tl_names, persons, tables, types, s_c_values = get_entries_data("procedure_entries.txt")    
    return render_template('action2_update_request/add_action2_update_request.html', persons=persons, s_c_values = s_c_values, 
                        tables=tables, types=types, is_admin = session.get('user'), analyst_names=analyst_names, tl_names=tl_names)

@app.route('/action1_update_request/download/file/<int:id>', methods=['GET'])
@check_login
def download_action1_update_request_file(id):

    filename = get_file_name('t_action1', id)
    if filename:
        return send_file(f"files/{filename}", as_attachment=True)
    else:
        url = url_for('get_all_action1_update_request')
        return redirect(url)

@app.route('/update/action2/update/request/<int:action2_update_request_id>', methods=['GET', 'POST'])
@check_login
def update_action2_update_request(action2_update_request_id):
    if request.method == 'POST':
        tables = ','.join(request.form.getlist('table')).strip()
        update_data('t_action2', action2_update_request_id,
                        originator=request.form.get('person'),
                        type=request.form.get('type'),
                        affected_tables=tables,
                        title=request.form.get('title'),
                        reason_for_update=request.form.get('description'),
                        s_c=request.form.get('s_c'),
                        ar_ref=request.form.get('ar_ref'),
                        swet_ref=request.form.get('swet_ref'))
        
    analyst_names, tl_names, persons, tables, types, s_c_values = get_entries_data("srdb_entries.txt")    
    data = get_record_by_table_name('t_action2', action2_update_request_id)
    data = list(data)
    data[7] = data[7].split(',')
    return render_template('action2_update_request/update_action2_update_request.html', persons=persons, s_c_values = s_c_values, 
                        tables=tables, types=types, data = data, is_admin = session.get('user'), analyst_names=analyst_names, tl_names=tl_names)

@app.route('/action2_update_request/download/file/<int:id>', methods=['GET'])
@check_login
def download_action2_update_request_file(id):

    filename = get_file_name('t_action2', id)
    if filename:
        return send_file(f"files/{filename}", as_attachment=True)
    else:
        url = url_for('get_all_action2_update_request')
        return redirect(url)


@app.route('/action2/update/request/verify/<int:action2_update_request_id>')
@check_login
def action2_update_request_verify(action2_update_request_id):
    update_data('t_action2', action2_update_request_id,
                status = 'VERIFIED')

    url = url_for('get_all_action2_update_request')
    return redirect(url)

@app.route('/action2/update/request/implement/<int:action2_update_request_id>')
@check_login
def action2_update_request_implement(action2_update_request_id):
    update_data('t_action2', action2_update_request_id,
                implemented = 'implemented')

    url = url_for('get_all_action2_update_request')
    return redirect(url)


@app.route('/action2/update/request/<int:action2_update_request_id>')
@check_login
def action_2_update_request_detail(action2_update_request_id):
    data = get_record_by_table_name('t_action2',action2_update_request_id)
    return render_template('action2_update_request/action2_update_request_detail.html', data=data, is_admin = session.get('user'))

@app.route('/api/action2/update/request/delete/<int:action2_id>')
@check_login
def delete_action2_update_request(action2_id):

    delete_record_by_table_name('t_action2', action2_id)
    url = url_for('get_all_action2_update_request')
    return redirect(url)
                
@app.route('/api/action2/update/request/upload', methods=['POST'])
@check_login
def action2_update_request_upload():    
    df = pd.read_excel(request.files['file'])
    df = df.fillna('-')

    table_name = 't_action2'
    data = [(None,) + tuple(x) for x in df.values]
    final_data = []
    for row in data:
        arr = []
        for _, col in enumerate(row):
            arr.append(col)
        final_data.append(tuple(arr)) 

    placeholders = "?, " + ", ".join(["?" for _ in range(len(df.columns))])
    query = f"INSERT INTO {table_name}(id, s_c, `status`,originator, `date`, `type`, reason_for_update, affected_tables, affected_files) VALUES ({placeholders})"    
    cursor = conn.cursor()
    cursor.executemany(query, final_data)
    conn.commit()

    url = url_for('get_all_action2')
    return redirect(url)

@app.route('/api/delete/all/<int:table_id>')
@check_login
def delete_all_table_data(table_id):

    table_name = ""
    url_for_value = ""
    
    if table_id == 1:
        table_name = "t_schedule"
        url_for_value = "get_schedules"
    elif table_id == 2:        
        table_name = "t_anomaly"
        url_for_value = "get_anomalies"
    elif table_id == 3:
        table_name = "t_soi"
        url_for_value = "get_all_soi"
    elif table_id == 4:        
        table_name = "t_parameter"
        url_for_value = "get_parameters"
    elif table_id == 5:        
        table_name = "t_procedure"
        url_for_value = "get_procedures"
    elif table_id == 6:        
        table_name = "t_pus"
        url_for_value = "get_pus_all"
    elif table_id == 7:        
        table_name = "t_event"
        url_for_value = "get_event_all"
    elif table_id == 8:        
        table_name = "t_srdb"
        url_for_value = "get_all_srdb"
    elif table_id == 9:        
        table_name = "t_tmtcdb"
        url_for_value = "get_all_tmtcdb"
    elif table_id == 10:        
        table_name = "t_fd_schedule"
        url_for_value = "get_fd_schedules"
    elif table_id == 50:
        table_name = "t_fd_schedule_2"
    elif table_id == 51:
        table_name = "t_fd_schedule_3"
    elif table_id == 11:        
        table_name = "t_srdb_update_request"
        url_for_value = "get_all_srdb_update_request"
    elif table_id == 12:        
        table_name = "t_procedure_update_request"
        url_for_value = "get_all_procedure_update_request"
    elif table_id == 13:
        table_name = "t_soi_1"
        url_for_value = "get_all_soi_1"
    elif table_id == 14:        
        table_name = "t_parameter_1"
        url_for_value = "get_parameters_1"
    elif table_id == 15:        
        table_name = "t_procedure_1"
        url_for_value = "get_procedures_1"
    elif table_id == 16:        
        table_name = "t_event_1"
        url_for_value = "get_event_1_all"
    elif table_id == 17:
        table_name = "t_schedule_1"
        url_for_value = "get_schedules_1"
    elif table_id == 18:
        table_name = "t_fd_schedule_1"
        url_for_value = "get_fd_schedules_1"
    elif table_id == 19:
        table_name = "t_action1"
        url_for_value = "get_all_action1_update_request"
    elif table_id == 20:
        table_name = "t_action2"
        url_for_value = "get_all_action2_update_request"

    delete_all_record_by_table_name(table_name)
    url = url_for(url_for_value)
    return redirect(url)


@app.route('/soi_1', methods=['GET'])
@check_login
def get_all_soi_1():
    
    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_soi_1'
    if filters:
        data = filter_data(table_name, soi_number = ('LIKE', filters.get('soiNumber')),
                           soi_name = ('LIKE', filters.get('soiName')),
                           validity = ('LIKE', filters.get('valid')),
                           version = ('LIKE', filters.get('version')))
    else:
        data = filter_data(table_name)
    
    return render_template('soi_1/soi_1.html', soi_1_all = data, is_admin = session.get('user'), menuVal = 'submenu2')    

@app.route('/api/soi_1/upload', methods=['POST'])
@check_login
def upload_soi_1():    

    insert_data_from_excel('t_soi_1', request.files['file'], [5,6,8])
    url = url_for('get_all_soi_1')
    return redirect(url)

@app.route('/api/soi_1/delete/<int:soi_1_id>')
@check_login
def delete_soi_1(soi_1_id):

    delete_record_by_table_name('t_soi_1', soi_1_id)
    url = url_for('get_all_soi_1')
    return redirect(url)

@app.route('/soi_1/<int:soi_1_id>')
@check_login
def soi_1_detail(soi_1_id):
    soi_1 = get_record_by_table_name('t_soi_1', soi_1_id)

    return render_template('soi_1/soi_1_detail.html', soi_1=soi_1, is_admin = session.get('user'))

@app.route('/soi_1/update/<int:soi_1_id>')
@check_login
def soi_1_update_view(soi_1_id):
    data = get_record_by_table_name('t_soi_1', soi_1_id)
    return render_template('soi_1/soi_1_update.html', soi_1=data, is_admin = session.get('user'))

@app.route('/api/soi_1/update/<int:soi_1_id>', methods=['POST'])
@check_login
def soi_1_update(soi_1_id):

    update_data('t_soi_1', soi_1_id, 
                soi_number = request.form.get('soi_number'),
                soi_name = request.form.get('soi_name'),
                version = request.form.get('version'),
                link = request.form.get('link'),
                from_date = request.form.get('from_date'),
                to = request.form.get('to'),
                validity = request.form.get('validity'),
                today_date = request.form.get('today_date'))

    url = url_for('soi_1_update_view', soi_1_id = soi_1_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/parameter_1', methods=['GET'])
@check_login
def get_parameters_1():
    
    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_parameter_1'
    if filters:
        data = filter_data(table_name, name = ('LIKE', filters.get('parameterName')),
                           descr = ('LIKE', filters.get('parameterDescr')),
                           pid = ('LIKE', filters.get('parameterPid')),
                           unit = ('LIKE', filters.get('parameterUnit')))
    else:
        data = filter_data(table_name)
    return render_template('parameter_1/parameter_1.html', parameters_1 = data, is_admin = session.get('user'), menuVal = 'submenu2')    

# Create a route to handle the API request
@app.route('/api/parameter_1/upload', methods=['POST'])
@check_login
def upload_parameter_1():    
    
    insert_data_from_excel('t_parameter_1', request.files['file'])
    url = url_for('get_parameters_1')
    return redirect(url)

@app.route('/api/parameter_1/delete/<int:parameter_1_id>')
@check_login
def delete_parameter_1(parameter_1_id):

    delete_record_by_table_name('t_parameter_1', parameter_1_id)
    url = url_for('get_parameters_1')
    return redirect(url)

@app.route('/parameter_1/<int:parameter_1_id>')
@check_login
def parameter_1_detail(parameter_1_id):
    parameter_1 = get_record_by_table_name('t_parameter_1', parameter_1_id)
    return render_template('parameter_1/parameter_1_detail.html', parameter_1=parameter_1, is_admin = session.get('user'))

@app.route('/parameter_1/update/<int:parameter_1_id>')
@check_login
def parameter_1_update_view(parameter_1_id):
    data = get_record_by_table_name('t_parameter_1', parameter_1_id)
    return render_template('parameter_1/parameter_1_update.html', parameter_1=data, is_admin = session.get('user'))

@app.route('/api/parameter_1/update/<int:parameter_1_id>', methods=['POST'])
@check_login
def parameter_1_update(parameter_1_id):

    update_data('t_parameter_1',parameter_1_id, 
                name = request.form.get('name'),
                descr = request.form.get('descr'),
                pid = request.form.get('pid'),
                unit = request.form.get('unit'),
                type_code = request.form.get('type_code'),
                format_code = request.form.get('format_code'),
                width = request.form.get('width'),
                valid = request.form.get('valid'),
                related = request.form.get('related'),
                categ = request.form.get('categ'),
                natur = request.form.get('natur'),
                curtx = request.form.get('curtx'),
                inter = request.form.get('inter'),
                uscon = request.form.get('uscon'),
                decim = request.form.get('decim'),
                parval = request.form.get('parval'),
                subsys = request.form.get('subsys'),
                valpar = request.form.get('valpar'),
                sptype = request.form.get('sptype'),
                coor = request.form.get('coor'),
                obtid = request.form.get('obtid'),
                darc = request.form.get('darc'),
                endian = request.form.get('endian'),
                mon_check_name = request.form.get('mon_check_name'),
                mon_check_nbchck = request.form.get('mon_check_nbchck'),
                mon_check_nbool = request.form.get('mon_check_nbool'),
                mon_check_inter = request.form.get('mon_check_inter'),
                mon_check_codin = request.form.get('mon_check_codin'),
                ool_name = request.form.get('ool_name'),
                ool_pos = request.form.get('ool_pos'),
                ool_type = request.form.get('ool_type'),
                ool_vlalu = request.form.get('ool_vlalu'),
                ool_hvalu = request.form.get('ool_hvalu'),
                ool_rlchk = request.form.get('ool_rlchk'),
                ool_valpar = request.form.get('ool_valpar'))

    url = url_for('parameter_1_update_view', parameter_1_id = parameter_1_id, is_admin = session.get('user'))
    return redirect(url)


@app.route('/procedure_1', methods=['GET'])
@check_login
def get_procedures_1():

    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_procedure_1'
    if filters:
        data = filter_data(table_name, name = ('LIKE', filters.get('procedureName')),
                           sub_system = ('LIKE', filters.get('subSystem')),
                           version = ('LIKE', filters.get('version')))
    else:
        data = filter_data(table_name)

    return render_template('procedure_1/procedure_1.html', procedures_1 = data, is_admin = session.get('user'), menuVal = 'submenu2')    

# Create a route to handle the API request
@app.route('/api/procedure_1/upload', methods=['POST'])
@check_login
def upload_procedure_1():    

    insert_data_from_excel('t_procedure_1', request.files['file'])
    url = url_for('get_procedures_1')
    return redirect(url)

@app.route('/api/procedure_1/delete/<int:procedure_1_id>')
@check_login
def delete_procedure_1(procedure_1_id):

    delete_record_by_table_name('t_procedure_1', procedure_1_id)
    url = url_for('get_procedures_1')
    return redirect(url)

@app.route('/procedure_1/<int:procedure_1_id>')
@check_login
def procedure_1_detail(procedure_1_id):
    
    data = get_record_by_table_name('t_procedure_1', procedure_1_id)
    return render_template('procedure_1/procedure_1_detail.html', procedure_1=data, is_admin = session.get('user'))

@app.route('/procedure_1/update/<int:procedure_1_id>')
@check_login
def procedure_1_update_view(procedure_1_id):
    data = get_record_by_table_name('t_procedure_1', procedure_1_id)
    return render_template('procedure_1/procedure_1_update.html', procedure_1=data, is_admin = session.get('user'))

@app.route('/api/procedure_1/update/<int:procedure_1_id>', methods=['POST'])
@check_login
def procedure_1_update(procedure_1_id):
    update_data('t_procedure_1', procedure_1_id, 
                name = request.form.get('name'),
                sub_system = request.form.get('sub_system'),
                version = request.form.get('version'),
                pdf_link = request.form.get('pdf_link'))

    url = url_for('procedure_1_update_view', procedure_1_id = procedure_1_id)
    return redirect(url)

@app.route('/event_1', methods=['GET'])
@check_login
def get_event_1_all():

    query_parameters = request.args
    filters = {key: query_parameters.get(key) for key in query_parameters}
    table_name = 't_event_1'
    if filters:
        data = filter_data(table_name,
                           facility = ('LIKE', filters.get('facility')),
                           event = ('LIKE', filters.get('event')),
                           impact = ('LIKE', filters.get('impact')),
                           )
    else:
        data = filter_data(table_name)
    from_time = filters.get('from')
    to_time = filters.get('to')
    format_string = "%Y-%m-%d %H:%M:%S"
    if from_time is not None and from_time != '':
        from_time = datetime.datetime.strptime(from_time, format_string)
    else:
        from_time = None
    if to_time is not None and to_time != '':
        to_time = datetime.datetime.strptime(to_time, format_string)
    else:
        to_time = None

    ids = ""
    filtered_data = []
    for row in data:
        ids = ids + str(row[0]) + ','
        row_date = datetime.datetime.strptime(row[3], format_string)
        flag = False
        if to_time is None and from_time is None:
            flag = True
        elif to_time is None and from_time is not None and from_time <= row_date:
            flag = True                
        elif to_time is not None and from_time is None and to_time >= row_date:
            flag = True
        elif from_time <= row_date <= to_time:
            flag = True
        
        if flag:        
            filtered_data.append(row)
            ids = ids[:-1]
    return render_template('event_1/event_1.html', event_all = filtered_data, is_admin = session.get('user'), ids = ids, menuVal = 'submenu2')    

# Create a route to handle the API request
@app.route('/api/event_1/upload', methods=['POST'])
@check_login
def upload_event_1():    
    insert_data_from_excel('t_event_1', request.files['file'], [3,4])
    url = url_for('get_event_1_all')
    return redirect(url)

@app.route('/api/event_1/export', methods=['POST'])
@check_login
def export_event_1():    
    ids = request.form.get('event_id')
    cur = conn.cursor()
    cur.execute(f'SELECT t_time, `to`, facility, `event`, ar_link, impact FROM t_event_1 WHERE `id` in ({ids}) ')
    events = cur.fetchall()
    cur.close()
    
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    
    # Add headers to the CSV data
    writer.writerow(['T Time', 'To', 'Facility', 'Events', 'AR Link', 'Impact'])
    # Add rows of data to the CSV data
    for event in events:
         writer.writerow(list(event))
    
    # Create a response with the CSV data
    response = make_response(csv_data.getvalue().encode('utf-8'))
    response.headers.set('Content-Disposition', 'attachment', filename='events.csv')
    response.headers.set('Content-Type', 'text/csv')
    return response
    

@app.route('/api/event_1/delete/<int:event_id>')
@check_login
def delete_event_1(event_id):
    
    delete_record_by_table_name('t_event_1', event_id)    
    url = url_for('get_event_1_all')
    return redirect(url)

@app.route('/event_1/<int:event_id>')
@check_login
def event_1_detail(event_id):
    data = get_record_by_table_name('t_event_1', event_id)
    return render_template('event_1/event_1_detail.html', event=data, is_admin = session.get('user'))

@app.route('/event_1/update/<int:event_id>')
@check_login
def event_1_update_view(event_id):
    data = get_record_by_table_name('t_event_1', event_id)
    return render_template('event_1/event_1_update.html', event=data, is_admin = session.get('user'))

@app.route('/api/event_1/update/<int:event_id>', methods=['POST'])
@check_login
def event_1_update(event_id):

    update_data('t_event_1', event_id, 
                week = request.form.get('week'),
                year = request.form.get('year'),
                t_time = request.form.get('t_time'),
                to = request.form.get('to'),
                duration = request.form.get('duration'),
                facility = request.form.get('facility'),
                ar_link = request.form.get('ar_link'),
                event = request.form.get('event'),
                description = request.form.get('description'),
                impact = request.form.get('impact'))

    url = url_for('event_1_update_view', event_id = event_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/schedules_1', methods=['GET'])
@check_login
def get_schedules_1():
    
    week_number = request.args.get('week')
    today = datetime.date.today()
    year = today.isocalendar()[0]
    if week_number is None:        
        week_number = today.isocalendar()[1] + 1

    week_number = int(week_number)
    first_day = datetime.datetime.strptime(f'{year}-W{week_number-1}-1', '%G-W%V-%u').date()
    day_number =first_day.strftime("%j")
    days = [first_day + datetime.timedelta(days=i) for i in range(7)]
    weekday_numbers = [(i + int(day_number)) for i in range(7)]
    data, link = get_schedule_for_week('t_schedule_1', first_day, first_day + datetime.timedelta(days=6), 7, 10, ['%Y-%m-%d %H:%M:%S'], True)
    return render_template('schedule_1/schedule_1.html', week_number = week_number,
                           schedules = data,
                           link = link,
                           days = days, week = weekday_numbers,
                           menuVal = 'submenu2',
                           is_admin = session.get('user'))    
    
@app.route('/schedules_1/<int:schedule_id>')
@check_login
def schedule_1_detail(schedule_id):
    data = get_record_by_table_name('t_schedule_1', schedule_id)
    return render_template('schedule_1/schedule_1_detail.html', schedule=data, is_admin = session.get('user'))

@app.route('/api/schedules_1/delete/<int:schedule_id>')
@check_login
def delete_schedule_1(schedule_id):

    delete_record_by_table_name('t_schedule_1', schedule_id)
    url = url_for('get_schedules_1')
    return redirect(url)
    
@app.route('/api/schedule_1/upload', methods=['POST'])
@check_login
def upload_schedule_1():    
    insert_data_from_excel('t_schedule_1', request.files['file'], [7,8])
    url = url_for('get_schedules_1')
    return redirect(url)


@app.route('/api/export/csv/schedule_1')
@check_login
def export_csv_schedule():
    cur = conn.cursor()
    cur.execute('SELECT * FROM t_schedule_1')
    schedules = cur.fetchall()
    cur.close()
    
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    
    # Add headers to the CSV data
    writer.writerow(['id', 'title', 's_c', 'year', 'qtr', 'month', 'cw', 'doy', 'start_of_operation', 'end_of_operation', 'uplink_date', 'status', 'unit', 'execution_type', 'ops_scenario', 'operations_title', 'outage', 'operations_reference', 'request_id', 'request_source', 'una'])
    # Add rows of data to the CSV data
    for schedule in schedules:
         writer.writerow(list(schedule))
    
    # Create a response with the CSV data
    response = make_response(csv_data.getvalue().encode('utf-8'))
    response.headers.set('Content-Disposition', 'attachment', filename='schedules.csv')
    response.headers.set('Content-Type', 'text/csv')
    return response

@app.route('/schedule_1/update/<int:schedule_id>')
@check_login
def schedule_1_update_view(schedule_id):
    data = get_record_by_table_name('t_schedule_1', schedule_id)
    return render_template('schedule_1/schedule_1_update.html', schedule=data)

@app.route('/api/schedule_1/update/<int:schedule_id>', methods=['POST'])
@check_login
def schedule_1_update(schedule_id):

    update_data('t_schedule_1', schedule_id, 
                s_c = request.form.get('s_c'),
                year = request.form.get('year'),
                qtr = request.form.get('qtr'),
                month = request.form.get('month'),
                cw = request.form.get('cw'),
                doy = request.form.get('doy'),
                start_of_operation = request.form.get('start_of_operation'),
                end_of_operation = request.form.get('end_of_operation'),
                status = request.form.get('status'),
                operations_title = request.form.get('operations_title'),
                outage = request.form.get('outage'))

    url = url_for('schedule_1_update_view', schedule_id = schedule_id, is_admin = session.get('user'))
    return redirect(url)

@app.route('/fd_schedules_1', methods=['GET'])
@check_login
def get_fd_schedules_1():
    
    week_number = request.args.get('week')
    today = datetime.date.today()
    year = today.isocalendar()[0]
    if week_number is None:        
        week_number = today.isocalendar()[1] + 1

    week_number = int(week_number)
    first_day = datetime.datetime.strptime(f'{year}-W{week_number-1}-1', '%G-W%V-%u').date()
    day_number =first_day.strftime("%j")
    days = [first_day + datetime.timedelta(days=i) for i in range(7)]
    weekday_numbers = [(i + int(day_number)) for i in range(7)]
    data = get_schedule_for_week('t_fd_schedule_1', first_day, first_day + datetime.timedelta(days=6), 13, 12, ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"])
    return render_template('fd_schedule_1/fd_schedule_1.html', week_number = week_number,
                           fd_schedules = data,
                           days = days, week = weekday_numbers,
                           menuVal = 'submenu2',
                           is_admin = session.get('user'))    
    
@app.route('/fd_schedules_1/<int:fd_schedule_id>')
@check_login
def fd_schedule_1_detail(fd_schedule_id):
    data = get_record_by_table_name('t_fd_schedule_1', fd_schedule_id)
    return render_template('fd_schedule_1/fd_schedule_1_detail.html', fd_schedule=data, is_admin = session.get('user'))

@app.route('/api/fd_schedules_1/delete/<int:fd_schedule_id>')
@check_login
def fd_delete_schedule_1(fd_schedule_id):

    delete_record_by_table_name('t_fd_schedule_1', fd_schedule_id)
    url = url_for('get_fd_schedules_1')
    return redirect(url)
    
@app.route('/api/fd_schedule_1/upload', methods=['POST'])
@check_login
def fd_schedule_1_upload():    
    insert_data_from_excel('t_fd_schedule_1', request.files['file'], [3,10,11,13])
    url = url_for('get_fd_schedules_1')
    return redirect(url)

@app.route('/fd_schedule_1/update/<int:fd_schedule_id>')
@check_login
def fd_schedule_1_update_view(fd_schedule_id):
    data = get_record_by_table_name('t_fd_schedule_1', fd_schedule_id)
    return render_template('fd_schedule_1/fd_schedule_1_update.html', fd_schedule=data)

@app.route('/api/fd_schedule_1/update/<int:fd_schedule_id>', methods=['POST'])
@check_login
def fd_schedule_1_update(fd_schedule_id):

    update_data('t_fd_schedule_1', fd_schedule_id, 
                fd_id = request.form.get('fd_id'),
                version = request.form.get('version'),
                creation_date = request.form.get('creation_date'),
                originator = request.form.get('originator'),
                object_name = request.form.get('object_name'),
                object_id = request.form.get('object_id'),
                center_name = request.form.get('center_name'),
                ref_frame = request.form.get('ref_frame'),
                time_system = request.form.get('time_system'),
                start_time = request.form.get('start_time'),
                stop_time = request.form.get('stop_time'),
                type = request.form.get('type'),
                epoch = request.form.get('epoch'),
                duration = request.form.get('duration'),
                units = request.form.get('units'),
                unique_id = request.form.get('unique_id'),
                sensor_id = request.form.get('sensor_id'),
                target = request.form.get('target'),
                station = request.form.get('station'),
                co_linearity_angle = request.form.get('co_linearity_angle'))

    url = url_for('fd_schedule_1_update_view', fd_schedule_id = fd_schedule_id, is_admin = session.get('user'))
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True, port=8000)