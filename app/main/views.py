from flask import render_template, session, current_app, request

from . import main
from .. import db


@main.route('/', methods=['GET'])
def index():

    print dir(db)

    cookies = request.cookies
    if 'user_id' in cookies:
        session['user_id'] = cookies['user_id']
    else:
        query = """
        INSERT INTO cheez_user VALUES ()
        """

        res = db.session.execute(query)
        db.session.commit()

        session['user_id'] = res.lastrowid


    query = """
        SELECT p.ID as id, post_title as content, meta_value as image_url FROM wp_posts p
LEFT JOIN user_post_view up
on p.ID = up.post_id and up.user_id = :user_id
left join wp_postmeta m
on p.ID = m.post_id and meta_key = '_wp_attached_file'
where up.id is null
and p.post_status = 'publish'
limit 1

    """

    res = db.session.execute(query, {'user_id':session['user_id']})

    if res.rowcount == 0:
        query = """
        SELECT p.ID as id, post_title as content, meta_value as image_url FROM wp_posts p
        left join wp_postmeta m
on p.ID = m.post_id and meta_key = '_wp_attached_file'
where p.post_status = 'publish'
        order by rand() limit 1
        """
        res = db.session.execute(query)

    row = res.fetchone()

    print row
    query = """
    INSERT INTO user_post_view (user_id, post_id) values (:user_id, :post_id)
    """
    db.session.execute(query, {'user_id':session['user_id'], 'post_id':row[0]})
    db.session.commit()


    response = current_app.make_response(render_template('index.html',data=row))

    response.set_cookie('user_id',value=('%s'%session['user_id']))


    return response