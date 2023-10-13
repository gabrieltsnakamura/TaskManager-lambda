import json
import pymsql
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

getMethod = "GET"
postMethod = "POST"
putMethod = "PUT"
deleteMethod = "DELETE"

tasksPath = "/user_tasks"

def lambda_handler(event, context):
    httpMethod = event["httpMethod"]
    path = event["path"]

    if httpMethod == getMethod and path == tasksPath:
        return get_tasks(event)
    elif httpMethod == postMethod and path == tasksPath:
        return create_task(event)
    elif httpMethod == putMethod and path == tasksPath:
        return update_task(event)
    elif httpMethod == deleteMethod and path == tasksPath:
        return delete_task(event)
    else:
        return build_response(404, "Not Found")
    
def get_tasks(event):
    try:
        user_tasks_list = []
        cur = get_mysql_connection().cursor()
        cur.execute('SELECT * FROM user_tasks')
        user_tasks = cur.fetchall()
        cur.close()
        for i in range(len(user_tasks)):
            user_task_obj = {
                'id': user_tasks[i][0],
                'user_id': user_tasks[i][1],
                'description': user_tasks[i][2],
                'status': user_tasks[i][3],
                'date': user_tasks[i][4]
        }
        user_tasks_list.append(user_task_obj)
        build_response(200, user_tasks_list)
    except Exception as error:
        logger.exception("Error: could not fetch tasks: {}".format(error))
        raise Exception("Error: could not fetch tasks: {}".format(error))

def create_task(event):
    try:
        body = json.loads(event["body"])
        pathPrameters = event["pathParameters"]
        user_id = pathPrameters["user_id"]
        description = body["description"]
        status = body["status"]
        date = body["date"]
        conn = get_mysql_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO user_tasks (user_id, description, status, date) VALUES (%s, %s, %s, %s)', (user_id, description, status, date))
        conn.commit()
        cur.close()
        build_response(200, "Task created successfully")
    except Exception as error:
        logger.exception("Error: could not create task: {}".format(error))
        raise Exception("Error: could not create task: {}".format(error))
    
def update_task(event):
    try:
        body = json.loads(event["body"])
        pathPrameters = event["pathParameters"]
        user_id = pathPrameters["user_id"]
        description = body["description"]
        status = body["status"]
        date = body["date"]
        conn = get_mysql_connection()
        cur = conn.cursor()
        cur.execute('UPDATE user_tasks SET description = %s, status = %s, date = %s WHERE user_id = %s', (description, status, date, user_id))
        conn.commit()
        cur.close()
        build_response(200, "Task updated successfully")
    except Exception as error:
        logger.exception("Error: could not update task: {}".format(error))
        raise Exception("Error: could not update task: {}".format(error))
    
def delete_task(event):
    try:
        pathPrameters = event["pathParameters"]
        user_id = pathPrameters["user_id"]
        conn = get_mysql_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM user_tasks WHERE user_id = %s', (user_id))
        conn.commit()
        cur.close()
        build_response(200, "Task deleted successfully")
    except Exception as error:
        logger.exception("Error: could not delete task: {}".format(error))
        raise Exception("Error: could not delete task: {}".format(error))

def build_response(statusCode, body=None):
    return {
        "statusCode": statusCode,
        "body": json.dumps(body)
    }

def get_mysql_connection():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='password', db='todo', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        return conn
    except Exception as error:
        logger.exception("Error: connection to RDS could not be established {}".format(error))
        raise Exception("Connection to RDS could not be established {}".format(error))