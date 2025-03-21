from flask import Flask, jsonify 
from worker import celery_init_app
from tasks import add , say_hello
from celery.result import AsyncResult
from celery import Celery
from celery.schedules import crontab
from tasks import send_emails
app = Flask(__name__)

celery_app = celery_init_app(app)   # Initialize Celery


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # sender.add_periodic_task(10.0, add.s(5,9), name='add every 10')        # 's' is a method instead of "delay"         #every 10 seconds invoke add function
    
    sender.add_periodic_task(
        crontab(hours = 19, minute=56),         #sends email at 19:56 every day 
        send_emails.s(),
    )
# for more crontab configuration visit https://crontab.guru/

@app.route('/')
def home():
    return 'Hello World'
    
@app.route('/num1/<int:num1>/num2/<int:num2>')
def add_numbers(x, y):
    result = add.delay(x, y)
    print(result.id)
    return str(result.id)

@app.route('/result/<task_id>')             #monitor task status
def get_result(task_id):
    result = AsyncResult(task_id)
    return_obj ={
        "status": result.status,
        "ready_status": result.ready(),
        "result": result.result
    }
    return return_obj
     
if __name__ == '__main__':                  # Ensure this file is being run directly and not from a different module
    app.run(debug=True)
    