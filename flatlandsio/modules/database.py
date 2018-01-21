import os
import datetime

import app
import markdown
import modules.models
import config


APP_ROOT = config.APP_ROOT

def to_json(results):
    result = {}
    item = {}
    count = 1
    for row in results:
        for k, v in row.__dict__.items():
            if not k.startswith('_') and k != 'id':
                item[k] = v

        result[count] = item
        count += 1
        item = {}

    return result


def date_format():
    datetime_now = datetime.datetime.now()

    return f'{datetime_now.day}.{datetime_now.month}.{datetime_now.year}'


def get_post_years(posts=None):
    years = []
    for code, data in posts.items():
        day, month, year = data['pub_date'].split('.')
        years.append(year)

    return sorted(list(set(years)), reverse=True)


def create_markdown(post_name, content):
    post_dir = os.path.join(APP_ROOT, 'posts')

    with open(os.path.join(post_dir, f'{post_name}.md'), 'w') as f: 
        f.write(str(content)) 

    return f'{post_name}.md'


def markdown_to_html(title):
    post_dir = os.path.join(APP_ROOT, 'posts')

    with open(os.path.join(post_dir, f"{title.replace(' ', '-')}.md")) as f: 
        text = f.read()
        html = markdown.markdown(text, extensions=['markdown.extensions.fenced_code'])

    return html


def markdown_to_string(markdown_file):
    output = None
    post_dir = os.path.join(APP_ROOT, 'posts')

    with open(os.path.join(post_dir, f'{markdown_file}')) as f: 
        output = f.read()

    return output


def delete_markdown_file(content):
    post_dir = os.path.join(APP_ROOT, 'posts')

    try:
        os.remove(os.path.join(post_dir, f'{content}.md'))

        return True

    except:
        return False


def rename_markdown_file(src, dst):
    post_dir = os.path.join(APP_ROOT, 'posts')

    try:
        os.rename(
            os.path.join(post_dir, src),
            os.path.join(post_dir, dst)
            )

        return True

    except:
        return False


def get_post_by_tag(tag, posts):
    output = {}
    for code, data in posts.items():
        if tag in data['tags'].split(' '):
            output[code] = data

    return output


def form_to_dict(form_request):
    output = {}
    for k, v in form_request.items():
        if v != '':
            output[k] = v

        else:
            output[k] = None

    return output


def edit_post(form, title):
    get_post = modules.models.Post.query.filter_by(title=title.replace('-', ' ')).first()

    if form['inputTitle']:
        get_post.title = form['inputTitle']
        get_post.content = f"{form['inputTitle'].replace(' ', '-')}.md"

        rename_file = rename_markdown_file(f'{title}.md', f'{form["inputTitle"].replace(" ", "-")}.md')

    modules.models.db.session.add(get_post)
    modules.models.db.session.commit()

    return True
    
