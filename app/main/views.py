from flask import render_template, session, current_app, request

from . import main
from .. import db

@main.route('/posts')
def get_posts():
    query = """
select t.id as id, t.content, wp.guid  as image_url from wp_posts wp join
(select id , post_title as content from wp_posts p where p.post_status='publish') t
on t.id = wp.post_parent  Left join
user_post_view up on t.id = up.post_id and 
up.user_id = :user_id where wp.post_type='attachment' and up.id is null order by rand() limit 10;
    """

    res = db.session.execute(query, {'user_id':session['user_id']})

    if res.rowcount == 0:
        query = """
select t.id as id, t.content, wp.guid  as image_url from wp_posts wp join
(select id , post_title as content from wp_posts p where p.post_status='publish') t
on t.id = wp.post_parent 
where wp.post_type='attachment' order by rand() limit 10;
        """
        res = db.session.execute(query)


    response = render_template('posts.html', posts = res)

    return response


@main.route('/', methods=['GET'])
def index():

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


    


    response = current_app.make_response(render_template('index.html'))

    response.set_cookie('user_id',value=('%s'%session['user_id']))


    return response
