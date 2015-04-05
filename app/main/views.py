import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, session, current_app, request, redirect, url_for, jsonify
from bs4 import BeautifulSoup as BS
import datetime

from . import main
from .. import db

@main.route('/posts')
@main.route('/posts/<int:to_json>')
def get_posts(to_json=0):
    if 'user_id' not in session:
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

    if 'post_ids' not in session:
        session['post_ids'] = [0, 0]

    post_ids = session['post_ids']

    query = """
select tmp.id as id , tmp.content ,concat("image/",wm.meta_value) as image_url from 
(select p.id as id , p.post_title as content, pm.meta_value as value from wp_posts p
  join wp_postmeta pm on p.id = pm.post_id 
  left join user_post_view up on p.id =  up.post_id and up.user_id = :user_id
  where pm.meta_key ='_thumbnail_id' 
  and p.post_status='publish'
  and up.id is null) tmp 
  join wp_postmeta wm on tmp.value = wm.post_id 
   where meta_key ='_wp_attached_file'
    and tmp.id not in """+str(tuple(post_ids))+"""
     order by rand() limit 10;
"""
#"""
#select t.id as id, t.content, wp.guid  as image_url from wp_posts wp join
#(select id , post_title as content from wp_posts p where p.post_status='publish') t
#on t.id = wp.post_parent  Left join
#user_post_view up on t.id = up.post_id and 
#up.user_id = :user_id where wp.post_type='attachment' and up.id is null order by rand() limit 10;
#    """

    res = db.session.execute(query, {'user_id':session['user_id']})

    if res.rowcount == 0:
        query = """
select tmp.id as id , tmp.content ,concat("image/",wm.meta_value) as image_url from 
(select p.id as id , p.post_title as content, pm.meta_value as value from wp_posts p
  join wp_postmeta pm on p.id = pm.post_id 
  where pm.meta_key ='_thumbnail_id' 
  and p.post_status='publish'
  ) tmp 
  join wp_postmeta wm on tmp.value = wm.post_id 
   where meta_key ='_wp_attached_file'
    and tmp.id not in """+str(tuple(post_ids))+"""
     order by rand() limit 10;
"""
#"""
#select t.id as id, t.content, wp.guid  as image_url from wp_posts wp join
#(select id , post_title as content from wp_posts p where p.post_status='publish') t
#on t.id = wp.post_parent 
#where wp.post_type='attachment' order by rand() limit 10;
#        """
        res = db.session.execute(query)


    def to_list(row):
        session['post_ids'].append(row[0])
        return row

    res = map(to_list, res)

    if to_json:
        def to_json_serializable(row):
            row = dict(zip(row.keys(), row))
            bs = BS(row['content'])
            link = bs.select('a')[0]
            row['url'] = link.attrs['href']
            row['image_url'] = 'http://cheez.co/' + row['image_url']
            link.extract()


            subtitle = bs.select('font')
            
            if subtitle:
                row['subtitle'] = subtitle[0].get_text()
                subtitle[0].extract()
            row['title'] = bs.get_text()
            return row
        res = map(to_json_serializable, res)
        response = jsonify(
            status = 200,
            data = res
            )

        now = datetime.datetime.now()
        expires = now + datetime.timedelta(days=30)
        response.set_cookie('user_id',value=('%s'%session['user_id']),expires=expires)
        return response
    else:
        response = render_template('posts.html', posts = res)

        return response
        


@main.route('/link-click', methods=["POST"])
def link_click():
    query = """INSERT INTO user_post_view (user_id, post_id, liked, link_clicked) values (:user_id, :post_id, '-1', '1')

    ON DUPLICATE KEY UPDATE
    link_clicked = VALUES(link_clicked);


    INSERT INTO view_log (user_id, post_id, liked, link_clicked) values (:user_id, :post_id, '-1', '1');
    
    """

    params = {
        'user_id': session['user_id']
    }
    params['post_id'] = request.form['post_id']

    db.session.execute(query, params)
    db.session.commit()


    return ''

@main.route('/pass/<int:post_id>', methods=["POST"])
def pass_post(post_id):
    query = """INSERT IGNORE INTO 
    user_post_view (user_id, post_id, liked) values (:user_id, :post_id, '-1')

    """

    db.session.execute(query, {'user_id':session['user_id'], 'post_id':post_id})
    db.session.commit()
    return ''

@main.route('/like', methods=["POST"])
def like():
    query = """
    INSERT INTO user_post_view (user_id, post_id, liked) values (:user_id, :post_id, :is_liked)

    ON DUPLICATE KEY UPDATE
    liked = VALUES(liked);


    INSERT INTO view_log (user_id, post_id, liked) values (:user_id, :post_id, :is_liked);


    """
    params = {
        'user_id': session['user_id']
    }
    params['post_id'] = request.form['post_id']
    params['is_liked'] = request.form['is_liked']

    db.session.execute(query, params)
    db.session.commit()
    return ''

@main.route('/')
@main.route('/<int:post_id>')
def index(post_id = 0):

    session['post_ids'] = [0, 0]
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

    
    if post_id > 0:
        query = """
select tmp.id as id , tmp.content as content ,concat("image/",wm.meta_value) as image_url from
(select p.id as id , p.post_title as content, pm.meta_value as value from wp_posts p
  join wp_postmeta pm on p.id = pm.post_id
  where pm.meta_key ='_thumbnail_id'
  and p.post_status='publish'
  ) tmp
  join wp_postmeta wm on tmp.value = wm.post_id
   where meta_key ='_wp_attached_file'  and tmp.id = :post_id limit 1;
"""
#"""
#select t.id as id, t.content, wp.guid  as image_url from wp_posts wp join
#(select id , post_title as content from wp_posts p where p.post_status='publish') t
#on t.id = wp.post_parent
#    where t.id = :post_id limit 1;
#    """
        res = db.session.execute(query, {'post_id':post_id})
        row = res.fetchone()

        post_html = render_template('posts.html', posts=[row])
        title = BS(row['content'])
        [s.extract() for s in title('a')]
        image = row['image_url'].replace('.gif','.jpg')
        post_meta = render_template('post_meta.html', image=image, title=title.get_text())
        
    else:
        post_meta = ''
        post_html = ''

    response = current_app.make_response(render_template('index.html', post_meta = post_meta, post_html = post_html))

    now = datetime.datetime.now()
    expires = now + datetime.timedelta(days=30)

    response.set_cookie('user_id',value=('%s'%session['user_id']),expires=expires)


    query = """
    INSERT INTO referrer_log (user_id, referrer, request_url)
    VALUES (:user_id, :referrer, :request_url)"""
    referrer = request.referrer

    db.session.execute(query, {
        'user_id':session['user_id'],
        'referrer':request.referrer,
        'request_url':request.url
        })
        
    db.session.commit()

    return response

@main.route('/touch_log', methods=["POST"])
def touch_log():
    query = """
    
    INSERT INTO touch_log (user_id, post_id, x,y) values (:user_id, :post_id, :x,:y);

    """
    params = {
        'user_id': session['user_id']
    }
    params['post_id'] = request.form['post_id']
    params['x'] = request.form['x']
    params['y'] = request.form['y']

    db.session.execute(query, params)
    db.session.commit()
    return ''

@main.route('/sns_log', methods=["POST"])
def sns_log():
    query = """
    
    INSERT INTO sns_log (user_id, post_id, sns) values (:user_id, :post_id, :sns);

    """
    params = {
        'user_id': session['user_id']
    }
    params['post_id'] = request.form['post_id']
    params['sns'] = request.form['sns']
    

    db.session.execute(query, params)
    db.session.commit()
    return ''

@main.route('/sendmail', methods=["POST"])
def sendmail():

    query = """
    INSERT INTO report (username, email, title, body, user_id)
    values (:username, :email, :title, :body, :user_id)
    """

    db.session.execute(query, {
        'username':request.form['name'],
        'email':request.form['email'],
        'title':request.form['title'],
        'body':request.form['body'],
        'user_id':session['user_id']

        })
    db.session.commit()
    return ''
