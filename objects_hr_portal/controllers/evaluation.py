from odoo import http,SUPERUSER_ID
from odoo.http import request
from datetime import datetime,date,timedelta
import json,requests
import subprocess
import csv
import io
# from dotenv import load_dotenv
import os
# import mysql.connector
import logging
_logger = logging.getLogger(__name__)
import psycopg2
from odoo.exceptions import ValidationError

class Evaluation(http.Controller):

    @http.route(['/objects/evaluation'], type='http', auth='user', website=True)
    def evaluation(self, **kwargs):
        # conn = psycopg2.connect(
        #     dbname="limesurvey",
        #     user="odoo",
        #     password="odoo",
        #     host="db",
        #     port="5432"
        # )

        # cursor = conn.cursor()
        # cursor.execute("SELECT sid,gsid FROM lime_surveys where active='Y';")
        # rows = cursor.fetchall()
        # for row in rows:
        #     _logger.info(f"{row}#################################################")

        # cursor.close()
        # conn.close()        
 
        return request.render('objects_hr_portal.objects_evaluation_id',{})
    



    @http.route(['/objects/evaluation/questions'], type='http', auth='user', website=True)
    def evaluation_questions(self, **kwargs):
        try:

            LIME_DB_HOST = os.environ.get("LIME_DB_HOST")
            LIME_DB_PORT = int(os.environ.get("LIME_DB_PORT"))
            LIME_DB_USER = os.environ.get("LIME_DB_USER")
            LIME_DB_PASSWORD = os.environ.get("LIME_DB_PASSWORD")
            LIME_DB_NAME = os.environ.get("LIME_DB_NAME")            

            # LIME_DB_HOST = 'db'
            # LIME_DB_PORT = 5432
            # LIME_DB_USER = "odoo"
            # LIME_DB_PASSWORD = "odoo"
            # LIME_DB_NAME = "limesurvey"            

            # Database connection
            conn = psycopg2.connect(
                dbname=LIME_DB_NAME,
                user=LIME_DB_USER, 
                password=LIME_DB_PASSWORD,
                host=LIME_DB_HOST,
                port=LIME_DB_PORT
            )
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            employee = request.env.user.employee_id
            surveys_participants = {3:[],4:[]}
            
            # Get active surveys
            cursor.execute("SELECT sid, gsid FROM lime_surveys WHERE active='Y';")
            surveys_ids = cursor.fetchall()
            for row in surveys_ids:
                if row['gsid'] not in (3,4):
                    continue
                sid = row["sid"]
                gsid = row["gsid"]
                table = f"lime_tokens_{sid}"
                filter_value = f"{employee.first_name} {employee.last_name}" if employee.first_name and employee.last_name else employee.name
                
                # Check if table exists and get participants
                check_table_query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
                """
                
                cursor.execute(check_table_query, (table,))
                table_exists = list(cursor.fetchone())
                
                if len(table_exists) > 0:
                    # Get participants for this survey
                    participants_query = f"""
                    SELECT firstname, lastname, token, attribute_1 
                    FROM {table} 
                    WHERE firstname = %s AND lastname = %s;
                    """
                    
                    try:
                        cursor.execute(participants_query, (str(employee.first_name),str(employee.last_name)))
                        participants = cursor.fetchall()
                        
                        if participants:
                            # Convert RealDictRow to regular dict and add sid
                            participants_list = [dict(p, sid=sid) for p in participants]
                            if gsid not in surveys_participants:
                                surveys_participants[gsid] = participants_list
                            else:
                                surveys_participants[gsid].extend(participants_list)
                                
                            _logger.info(f"Found {len(participants)} participants for survey {sid}")
                            
                    except psycopg2.Error as e:
                        raise ValidationError(f"Error querying table {table}: {e}")
                        # continue
                else:
                    raise ValidationError(f"Table {table} does not exist")
            
            cursor.close()
            conn.close()
            return request.render('objects_hr_portal.objects_evaluation_questions_id', {
                'participants': surveys_participants,
                'host': "https://surveys.objects.ws"
            })
            
        except psycopg2.Error as e:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
                
            raise ValidationError(f"Database connection error: {e}")

            # Handle error appropriately - maybe return error page or empty results
            # return request.render('objects_hr_portal.objects_evaluation_questions_id', {
            #     'participants': {},
            #     'host': "https://surveys.objects.ws"
            # })
            
        except Exception as e:
            # Clean up database connections
            if 'cursor' in locals():
                cursor.close() 
            if 'conn' in locals():
                conn.close()
            raise ValidationError(f"Unexpected error: {e}")
 

        # try:

        #     # # Access variables
        #     # load_dotenv()
        #     db_host = os.environ.get('LIME_DB_HOST') #os.getenv('DB_HOST')
        #     db_port = os.environ.get('LIME_DB_PORT') #os.getenv('DB_PORT')
        #     db_user = os.environ.get('LIME_DB_USER') #os.getenv('DB_USER')
        #     db_password = os.environ.get('LIME_DB_PASSWORD') #os.getenv('DB_PASSWORD')
        #     db_name = os.environ.get('LIME_DB_NAME') #os.getenv('DB_NAME')
        #     # survay_port = os.environ.get('SURVAY_PORT') #os.getenv('SURVAY_PORT')
        #     employee = request.env.user.employee_id
        #     surveys_participants = {}

        #     command = [
        #         "mysql",
        #         "-h", db_host,
        #         "-P", db_port,  # Correct port (make sure it's open)
        #         "-u", db_user,
        #         "-p" + db_password,   # Be careful with special characters
        #         "-D", db_name,  # <-- ADD this to select database
        #         "-e", "SELECT sid,gsid FROM surveys where active='Y';"
        #     ]
        #     result = subprocess.run(command, capture_output=True, text=True)
        #     # Check for errors
        #     if result.returncode != 0:
        #         print("Error:", result.stderr)
        #         exit()

        #     # Convert tab-separated output to CSV format
        #     output = result.stdout.strip()
        #     # Use CSV reader to parse the result
        #     reader = csv.DictReader(io.StringIO(output), delimiter='\t')
        #     # Convert to list of dictionaries
        #     surveys_ids = list(reader)


        #     for row in surveys_ids:
        #         sid = row["sid"]
        #         table = f"tokens_{sid}"
        #         filter_value = f"{employee.first_name} {employee.last_name}" if employee.first_name and employee.last_name else employee.name
        #         # , ' WHERE attribute_1 = \\'{filter_value}\\''
                
        #         query = f"""
        #         SET @table := '{table}';
        #         SET @sql := (
        #         SELECT IF(
        #             EXISTS (
        #             SELECT 1 FROM information_schema.tables
        #             WHERE table_schema = 'limesurvey' AND table_name = @table
        #             ),
        #             CONCAT('SELECT firstname,lastname,token FROM ', @table, ' WHERE attribute_1 = \\'{filter_value}\\''),
        #             'SELECT NULL LIMIT 0'
        #         )
        #         );
        #         PREPARE stmt FROM @sql;
        #         EXECUTE stmt;
        #         DEALLOCATE PREPARE stmt;
        #         """

        #         command = [
        #             "mysql",
        #             "-h", db_host,
        #             "-P", db_port,  # Correct port (make sure it's open)
        #             "-u", db_user,
        #             "-p" + db_password,   # Be careful with special characters
        #             "-D", db_name,  # <-- ADD this to select database
        #             # "-e", f"SELECT firstname,lastname,token,attribute_1 FROM tokens_{row['sid']} where attribute_1 = 'Ahmed Mokhtar' ;"
        #             "-e", query
        #         ]
        #         result = subprocess.run(command, capture_output=True, text=True)
        #         # Check for errors
        #         if result.returncode != 0:
        #             print("Error:", result.stderr)
        #             exit()

        #         # Convert tab-separated output to CSV format
        #         output = result.stdout.strip()
        #         # Use CSV reader to parse the result
        #         reader = csv.DictReader(io.StringIO(result.stdout.strip()), delimiter='\t')
        #         # Convert to list of dictionaries
        #         participants = list(reader)

        #         if type(participants) == list:
        #             # surveys_participants.extend(participants)
        #             if row['gsid'] not in surveys_participants:
        #                 surveys_participants[row['gsid']] = list(map(lambda p: {**p,'sid': sid} ,participants))
        #             else:
        #                 surveys_participants[row['gsid']].extend(list(map(lambda p: {**p,'sid': sid} ,participants)))


        #     return request.render('objects_hr_portal.objects_evaluation_questions_id',{'participants': surveys_participants,'host': "https://surveys.objects.ws"
        #                                                                               #  ,'port': survay_port
        #                                                                                })
        # except ValueError:
        #     print("Failed to parse JSON. Raw response:")




        # grouped_survays = {}
        # participants = {}
        # url = "http://localhost:8082/index.php/admin/remotecontrol"

        # headers = {
        #     "Accept": "application/json",
        #     "Content-Type": "application/json"
        # }

        # payload_survays = {
        #     "method": "list_surveys",
        #     "params": ["wx1rKmvqURALbedpOyMOPd1WGTpIRz4P"],
        #     "id": 2
        # }



        # try:
        #     response_survays = requests.post(url, headers=headers, data=json.dumps(payload_survays))
        #     active_survays = list(map(lambda s:s['sid'],filter(lambda sur: sur['active'] == 'Y',response_survays.json()['result'])))
            
        #     for active in active_survays:
        #         response_group = requests.post(url, headers=headers, data=json.dumps({
        #                                                                               "method": "list_groups", 
        #                                                                               "params": ["wx1rKmvqURALbedpOyMOPd1WGTpIRz4P", int(active)],
        #                                                                               "id": 2
        #                                                                             }))
        #         groups = list(map(lambda g:g['id'],response_group.json()['result']))
        #         if 4 in groups or 5 in groups:
        #             if 4 in groups:
        #                 if 4 not in grouped_survays:
        #                     grouped_survays[4] = [active]
        #                 else:
        #                     grouped_survays[4] += [active]
        #             if 5 in groups:
        #                 if 5 not in grouped_survays:
        #                     grouped_survays[5] = [active]
        #                 else:
        #                     grouped_survays[5] += [active]



        #     for key in grouped_survays.keys():
        #           for s in grouped_survays[key]:
        #               response_participants = requests.post(url, headers=headers, data=json.dumps({
        #                                                                                             "method": "list_participants",
        #                                                                                             "params": [
        #                                                                                                 "wx1rKmvqURALbedpOyMOPd1WGTpIRz4P", 
        #                                                                                                 int(s),
        #                                                                                                 0,
        #                                                                                                 1000,
        #                                                                                                 False,
        #                                                                                                 ["attribute_1"]
        #                                                                                             ],
        #                                                                                             "id": 2
        #                                                                                         }))
        #               part_res = response_participants.json()['result']
                      
        #               for part in part_res:
        #                 if key not in participants:
        #                     participants[key] = [{'firstname': part['participant_info']['firstname'],'lastname': part['participant_info']['lastname'], 'token': part['token'],'attr':  part['attribute_1']}]
        #                 else:
        #                     participants[key] += [{'firstname': part['participant_info']['firstname'],'lastname': part['participant_info']['lastname'], 'token': part['token'],'attr':  part['attribute_1']}]

        #     print(participants,'#####################################################################')


    # @http.route(['/objects/evaluation/questions'], type='http', auth='user', website=True)
    # def evaluation_questions(self, **kwargs):
    #     try:

    #         load_dotenv()
    #         db_host = os.environ.get('LIME_DB_HOST') #os.getenv('DB_HOST')
    #         # survay_port = os.environ.get('SURVAY_PORT') #os.getenv('SURVAY_PORT')


    #         db_config = {
    #             "host": os.environ.get("LIME_DB_HOST"),
    #             "port": int(os.environ.get("LIME_DB_PORT", 3306)),
    #             "user": os.environ.get("LIME_DB_USER"),
    #             "password": os.environ.get("LIME_DB_PASSWORD"),
    #             "database": os.environ.get("LIME_DB_NAME")
    #         }
    #         employee = request.env.user.employee_id
    #         filter_value = f"{employee.first_name} {employee.last_name}" if employee.first_name and employee.last_name else employee.name
    #         surveys_participants = {}

    #         try:
    #                 conn = mysql.connector.connect(**db_config)
    #                 cursor = conn.cursor(dictionary=True)

    #                 # Step 1: Fetch all active surveys
    #                 cursor.execute("SELECT sid, gsid FROM surveys WHERE active = 'Y'")
    #                 surveys_ids = cursor.fetchall()

    #                 for row in surveys_ids:
    #                     sid = row["sid"]
    #                     gsid = row["gsid"]
    #                     table_name = f"tokens_{sid}"

    #                     # Step 2: Check if token table exists
    #                     cursor.execute("""
    #                         SELECT COUNT(*) as count FROM information_schema.tables
    #                         WHERE table_schema = %s AND table_name = %s
    #                     """, (db_config["database"], table_name))
    #                     result = cursor.fetchone()

    #                     if result["count"] == 0:
    #                         continue  # Skip if the token table does not exist

    #                     # Step 3: Fetch participants from the token table
    #                     query = f"""
    #                         SELECT firstname, lastname, token FROM `{table_name}`
    #                         WHERE attribute_1 = %s
    #                     """
    #                     cursor.execute(query, (filter_value,))
    #                     participants = cursor.fetchall()

    #                     if gsid not in surveys_participants:
    #                         surveys_participants[gsid] = [{**p, 'sid': sid} for p in participants]
    #                     else:
    #                         surveys_participants[gsid].extend([{**p, 'sid': sid} for p in participants])

    #         except mysql.connector.Error as err:
    #             _logger.error(f"MySQL Error: {err}")
    #         finally:
    #             if cursor:
    #                 cursor.close()
    #             if conn:
    #                 conn.close()

    #         return request.render('objects_hr_portal.objects_evaluation_questions_id',{'participants': surveys_participants,'host': "https://surveys.objects.ws"
    #                                                                                   #  ,'port': survay_port
    #                                                                                    })
    #     except ValueError:
    #         print("Failed to parse JSON. Raw response:")




    #     # grouped_survays = {}
    #     # participants = {}
    #     # url = "http://localhost:8082/index.php/admin/remotecontrol"

    #     # headers = {
    #     #     "Accept": "application/json",
    #     #     "Content-Type": "application/json"
    #     # }

    #     # payload_survays = {
    #     #     "method": "list_surveys",
    #     #     "params": ["wx1rKmvqURALbedpOyMOPd1WGTpIRz4P"],
    #     #     "id": 2
    #     # }



    #     # try:
    #     #     response_survays = requests.post(url, headers=headers, data=json.dumps(payload_survays))
    #     #     active_survays = list(map(lambda s:s['sid'],filter(lambda sur: sur['active'] == 'Y',response_survays.json()['result'])))
            
    #     #     for active in active_survays:
    #     #         response_group = requests.post(url, headers=headers, data=json.dumps({
    #     #                                                                               "method": "list_groups", 
    #     #                                                                               "params": ["wx1rKmvqURALbedpOyMOPd1WGTpIRz4P", int(active)],
    #     #                                                                               "id": 2
    #     #                                                                             }))
    #     #         groups = list(map(lambda g:g['id'],response_group.json()['result']))
    #     #         if 4 in groups or 5 in groups:
    #     #             if 4 in groups:
    #     #                 if 4 not in grouped_survays:
    #     #                     grouped_survays[4] = [active]
    #     #                 else:
    #     #                     grouped_survays[4] += [active]
    #     #             if 5 in groups:
    #     #                 if 5 not in grouped_survays:
    #     #                     grouped_survays[5] = [active]
    #     #                 else:
    #     #                     grouped_survays[5] += [active]



    #     #     for key in grouped_survays.keys():
    #     #           for s in grouped_survays[key]:
    #     #               response_participants = requests.post(url, headers=headers, data=json.dumps({
    #     #                                                                                             "method": "list_participants",
    #     #                                                                                             "params": [
    #     #                                                                                                 "wx1rKmvqURALbedpOyMOPd1WGTpIRz4P", 
    #     #                                                                                                 int(s),
    #     #                                                                                                 0,
    #     #                                                                                                 1000,
    #     #                                                                                                 False,
    #     #                                                                                                 ["attribute_1"]
    #     #                                                                                             ],
    #     #                                                                                             "id": 2
    #     #                                                                                         }))
    #     #               part_res = response_participants.json()['result']
                      
    #     #               for part in part_res:
    #     #                 if key not in participants:
    #     #                     participants[key] = [{'firstname': part['participant_info']['firstname'],'lastname': part['participant_info']['lastname'], 'token': part['token'],'attr':  part['attribute_1']}]
    #     #                 else:
    #     #                     participants[key] += [{'firstname': part['participant_info']['firstname'],'lastname': part['participant_info']['lastname'], 'token': part['token'],'attr':  part['attribute_1']}]

    #     #     print(participants,'#####################################################################')

