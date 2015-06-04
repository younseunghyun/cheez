from __future__ import absolute_import
from cheez import celery_app
from django.db import connections

@celery_app.task()
def send_post_data(data):
    conn = connections['recommendation']
    cursor = conn.cursor()
    query = """
    insert ignore into posts_post_current
    (id, user_id, image_url, source_url, title, subtitle, created, modified)
    values (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query,
                   [
                       data['id'],
                       data['user']['id'],
                       data['image_url'],
                       data['source_url'],
                       data['title'],
                       data['subtitle'],
                       data['created'],
                       data['modified'],
                   ]
                   )
    conn.commit()

@celery_app.task()
def send_read_log(data):
    conn = connections['recommendation']
    cursor = conn.cursor()

    query = """
        insert into posts_readpostrel_current (post_id, user_id, link_clicked, rating, saved,
            view_started_time,
            view_ended_time,
            link_opened_time,
            link_closed_time
        )
        values
            """

    params = []
    for d in data['data']:
        query += ' (%s, %s, %s, %s, %s,' \
                 '%s, %s, %s, %s),'
        params += [
            d['post'],
            d['user_id'],
            '1' if d['link_clicked'] else '0',
            d['rating'],
            '1' if d['saved'] else '0',
            d['view_started_time'],
            d['view_ended_time'],
            d['link_opened_time'],
            d['link_closed_time']
        ]

    query = query[:-1] + """
    on duplicate key update
    link_clicked = values(link_clicked),
    rating = values(rating),
    saved = values(saved),
    view_started_time = if(values(view_ended_time) - values(view_started_time) > view_ended_time - view_started_time,
        values(view_started_time), view_started_time),
    view_ended_time = if(values(view_ended_time) - values(view_started_time) > view_ended_time - view_started_time,
        values(view_ended_time), view_ended_time),
    link_opened_time = if(values(link_opened_time) > 0
        and (values(link_closed_time) - values(link_opened_time) > link_closed_time - link_opened_time),
        values(link_opened_time), link_opened_time),
    link_closed_time = if(values(link_opened_time) > 0
        and (values(link_closed_time) - values(link_opened_time) > link_closed_time - link_opened_time),
        values(link_closed_time), link_closed_time)
    """
    cursor.execute(query, params)
    conn.commit()