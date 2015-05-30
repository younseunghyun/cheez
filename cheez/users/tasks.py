from __future__ import absolute_import
from cheez import celery_app
from django.db import connections

@celery_app.task
def send_user_data(data):
    conn = connections['recommendation']
    cursor = conn.cursor()
    query = """
    insert into users_user_current (id)
    values (%s)
    """
    cursor.execute(query, [data['id'],])
    conn.commit()