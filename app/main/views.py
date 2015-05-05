#-*- coding: utf-8 -*-
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
select content_id , context , img_url from content ct
  left join user_post_view up on ct.content_id =  up.post_id and up.user_id = :user_id
  and up.id is null
   where content_id not in """+str(tuple(post_ids))+"""
     order by rand() limit 10;
"""

#"""
#select tmp.id as id , tmp.content ,concat("image/",wm.meta_value) as image_url from 
#(select p.id as id , p.post_title as content, pm.meta_value as value from wp_posts p
#  join wp_postmeta pm on p.id = pm.post_id 
#  left join user_post_view up on p.id =  up.post_id and up.user_id = :user_id
#  where pm.meta_key ='_thumbnail_id' 
#  and p.post_status='publish'
#  and up.id is null) tmp 
#  join wp_postmeta wm on tmp.value = wm.post_id 
#   where meta_key ='_wp_attached_file'
#    and tmp.id not in """+str(tuple(post_ids))+"""
#     order by rand() limit 10;
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
        select content_id , context , img_url from content ct
   where content_id not in """+str(tuple(post_ids))+"""
     order by rand() limit 10;

        """
#        """
#select tmp.id as id , tmp.content ,concat("image/",wm.meta_value) as image_url from 
#(select p.id as id , p.post_title as content, pm.meta_value as value from wp_posts p
#  join wp_postmeta pm on p.id = pm.post_id 
#  where pm.meta_key ='_thumbnail_id' 
#  and p.post_status='publish'
#  ) tmp 
#  join wp_postmeta wm on tmp.value = wm.post_id 
#   where meta_key ='_wp_attached_file'
#    and tmp.id not in """+str(tuple(post_ids))+"""
#     order by rand() limit 10;
#"""

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
        select content_id , context , img_url as image_url from content ct
   where ct.content_id = :post_id
     limit 1;

        """
#        """
#select tmp.id as id , tmp.content as content ,concat("image/",wm.meta_value) as image_url from
#(select p.id as id , p.post_title as content, pm.meta_value as value from wp_posts p
#  join wp_postmeta pm on p.id = pm.post_id
#  where pm.meta_key ='_thumbnail_id'
#  and p.post_status='publish'
#  ) tmp
#  join wp_postmeta wm on tmp.value = wm.post_id
#   where meta_key ='_wp_attached_file'  and tmp.id = :post_id limit 1;
#"""

#"""
#select t.id as id, t.content, wp.guid  as image_url from wp_posts wp join
#(select id , post_title as content from wp_posts p where p.post_status='publish') t
#on t.id = wp.post_parent
#    where t.id = :post_id limit 1;
#    """
        res = db.session.execute(query, {'post_id':post_id})
        row = res.fetchone()

        post_html = render_template('posts.html', posts=[row])
        title = BS(row['context'])
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

@main.route('/app_touch_log', methods=['POST'])
def app_touch_log():
    query = '''
    INSERT INTO app_touch_log (user_id, post_id, device_width, device_height, x, y, action)
    values (:user_id, :post_id, :device_width, :device_height, :x, :y, :action)
    '''
    db.session.execute(query, {
            'user_id': session['user_id'],
            'post_id': request.form['post_id'],
            'device_width': request.form['device_width'],
            'device_height': request.form['device_height'],
            'x': request.form['x'],
            'y': request.form['y'],
            'action': request.form['action']
        })
    db.session.commit()

    return ''

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


import pymysql

@main.route('/upload')
def upload():

    return render_template('upload.html')

@main.route('/upload_content',methods=['POST'])
def upload_content():
    title = request.form['title']
    subtitle = request.form['subtitle']
    url= request.form['url']
    img_url = request.form['img_url']
    tag = request.form['tag']
    class_name = request.form['class']
    upload_to_db(title,subtitle,img_url,tag,url,class_name)
    return redirect('/upload')


def upload_to_db(title='',subtitle='',img_url='',tag='',url='',class_name=''):
    con = pymysql.connect(host='localhost',user='root',passwd='cheez',db='wordpress',charset='utf8')
    cur = con.cursor()
    insert_query = 'insert into content (class,content_id, title, sub_title, img_url, tag, context,url, author) values(%s,%s,%s,%s,%s,%s,%s,%s,"admin_web");'
    cur.execute('select max(content_id) from content;')
    con.commit()
    content_id= cur.fetchall()[0][0]+1
    img_path = img_crawl(content_id,img_url)
    context=''
    if title.strip() is not '':
        basic1 = '{0}<br>'.format(title)
        context += basic1
    if subtitle.strip() is not '':
        basic2 = '<font size="3">{0}</font>'.format(subtitle)
        context += basic2
    title = str(unicode(title))
    subtitle = str(subtitle)
    tag=str(unicode(tag))
    class_name=str(unicode(class_name))
    basic3 = '<br><br><a class="btn btn-medium btn-white btn-radius" href="{0}" target="_blank" style="padding-left:10px; padding-right:10px;"><font size="3">보러가기</font></a>'.format(url)
    context +=basic3
    context = con.escape(context)

    print(insert_query %(class_name,content_id,title,subtitle,img_path,tag,context,url))
    cur.execute(insert_query %(con.escape(class_name),content_id,con.escape(title),con.escape(subtitle),con.escape(img_path),con.escape(tag),context,con.escape(url)))
    con.commit()


import os
def img_crawl(content_id,img_url):
    content_dummy_path='/home/cheeze/contents_uploads'
    if '.gif' in img_url:
        os.system('wget %s -P '%(img_url)+content_dummy_path+'/img_temp/')
        fi = os.listdir(content_dummy_path+'/img_temp')[0]
        os.system('mv '+content_dummy_path+'/img_temp/{0} /home/cheeze/cheez/image/content/{1}.gif'.format(fi,content_id))
        os.system('rm '+content_dummy_path+'/img_temp/* ')
        modified_img_url = '/image/content/{0}.gif'.format(content_id)
    else:
        os.system('wget %s -P '%(img_url)+content_dummy_path+'/img_temp/')
        fi = os.listdir(content_dummy_path+'/img_temp')[0]
        os.system('convert '+content_dummy_path+'/img_temp/{0} -define jpeg:extent=50kb ./img_temp/{1}.jpg'.format(fi,content_id))
        if os.path.isfile(content_dummy_path+'/img_temp/{0}.jpg'.format(content_id)):
            os.system('mv '+content_dummy_path+'/img_temp/{0} /home/cheeze/cheez/image/content/'.format(content_id))
        else:
            os.system('mv '+content_dummy_path+'/img_temp/{0}.jpg /home/cheeze/cheez/image/content/{1}.jpg'.format(fi,content_id))
        os.system('rm '+content_dummy_path+'/img_temp/* ')
        modified_img_url = '/image/content/{0}.jpg'.format(content_id) 
    return modified_img_url
    