import os
import datetime

import app

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


def markdown_to_string(markdown_file):
    output = None
    post_dir = os.path.join(app.root_dir, 'posts')

    with open(os.path.join(post_dir, f'{markdown_file}')) as f: 
        output = f.read()

    return output


def delete_markdown_file(content):
    post_dir = os.path.join(app.root_dir, 'posts')

    try:
        os.remove(os.path.join(post_dir, f'{content}.md'))
        return True
    except:
        return False


def get_post_by_tag(tag, posts):
    output = {}
    for code, data in posts.items():
        if tag in data['tags'].split(' '):
            output[code] = data

    return output