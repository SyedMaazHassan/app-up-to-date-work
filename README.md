To add a new Tab in the Application:
- Open base.html and add a new ul after line:22
- Put href and it will be as per your page path. 
- The menu icon code will be given in the     i class    




Schedule/anomaly Page
- To change any Frontend related thing. You will need to edit schedule.html or anomaly.html
- Here you will find filters in the start You can add, remove filter here
- After that the next div will be of the upload functionality
- And the last div is of the table and you can add/remove or update any column here. 


Schedule-detail/ Anomaly-detail Page

- The detail of any object/row is shown using this page.
The [0], [1] corresponds to a field and fields corressponding number are defined at the end of the document.


The main application is ran using the app.py file.

- All the APIs are defined here. 
- A POST request is which is used to save the data
- A DELETE request is used to delete a record
- A GET request is used to fetch the record. This is also 
    used to filter the record

- If you want to add a new filter then get_anomalies (for anomalies filter) and get_schedules (for schedule) will be updated.
-  if status != '':
            if flag:
                query += ' AND '
            query += f" status like '%{status}%'"
            flag = True

Just add a new filter and replace the status with the actual field.
Note this field should be added in the .html file as explained above.


id => 0
title =>1
s_c =>2
year =>3
qtr => 4
month =>5
cw =>6
doy =>7
start_of_operation =>8
end_of_operation => 9
uplink_date =>10
status => 11
unit =>12
execution_type =>13
ops_scenario =>14
operations_title =>15
outage =>16
operations_reference =>17
request_id =>18
request_source =>19
una =>20

id =>0
facility =>1
anomaly =>2
event =>3
cell_cnt =>4
impact =>5
ar_number =>6
recover_action =>7
date =>8
week =>9