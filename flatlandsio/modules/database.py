"""Contains all database interaction code"""

import os
import datetime

import app
import markdown
import modules.models
import modules.data
import config

class User():
    """handles all database interations related to Users"""
    def new(self, email, password):
        user = modules.models.User(username=email, password=password)

        modules.models.db.session.add(user)
        modules.models.db.session.commit()

        return True


class Solutions():
    """fake data"""
    def _query_solutions(self):
        return modules.data.software


    def _query_types(self):
        solutions = modules.data.software
        types = []

        for id, data in solutions.items():
            types.append(data['type'])

        return list(set(types))

    def all(self):
        to_json = self._query_solutions()

        return to_json

    def types(self, solutions=None):
        """gets solution types from database
        AUG:
        solutions: iterable
        return: list"""
        if solutions:
            # return types found in these solutions
            pass

        else:
            return self._query_types()


class Post():
    """handles all database interaction related to Posts"""
    def _retrive_posts(self, published=None):
        if published == None:
            return modules.models.Post.query.all()

        else:
            return modules.models.Post.query.filter_by(published=published).all()


    def _retrive_post_by_title(self, title):
        return modules.models.Post.query.filter_by(title=title[0].replace('-', ' ')).first()


    def to_json(self, results):
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


    def all(self):
        return self.to_json(self._retrive_posts())


    def all_published(self):
        return self.to_json(self._retrive_posts(published=True))


    def by_title(self, title):
        return self.to_json((self._retrive_post_by_title(title),))


    def years_from_posts(self, posts):
        """returns sorted list of all years related to `posts`
        AUG: posts: dict
        return: list
        """
        years = []

        for code, data in posts.items():
            day, month, year = data['pub_date'].split('.')
            years.append(year)

        return sorted(list(set(years)), reverse=True)


    def query_tags(self, tag):
        """retrives all `posts` that contain `tag`
        AUG: 
            tag: str: tag words, separated with a space (' ')
            posts: dict

        return: dict
        """
        output = {}
        for code, data in self.to_json(self._retrive_posts()).items():
            if tag in data['tags'].split(' '):
                output[code] = data

        return output


    def edit(self, form, title):
        """uses form data to edit .md files
        AUG: form: dict
        title: str
        return: boolean
        """
        post = self._retrive_post_by_title(title)

        if form['inputTitle']:
            post.title = form['inputTitle']
            post.content = f"{form['inputTitle'].replace(' ', '-')}.md"

            rename_file = rename_markdown_file(f'{title}.md', f'{form["inputTitle"].replace(" ", "-")}.md')

        modules.models.db.session.add(post)
        modules.models.db.session.commit()

        return True


def date_today_as_ddmmyy():
    """returns current date as dd.mm.yyyy"""
    datetime_now = datetime.datetime.now()

    return f'{datetime_now.day}.{datetime_now.month}.{datetime_now.year}'


def form_to_dict(form_request):
    """converts flask form request data to dict"""
    output = {}
    for k, v in form_request.items():
        if v != '':
            output[k] = v

        else:
            output[k] = None

    return output


def create_markdown(post_name, content):
    """creates .md file
    AUG: post_name: str
    content: str

    returns: str: name of new file.
    """
    post_dir = os.path.join(config.APP_ROOT, 'posts')

    with open(os.path.join(post_dir, f'{post_name}.md'), 'w') as f: 
        f.write(str(content)) 

    return f'{post_name}.md'


def markdown_to_html(title):
    """converts .md to html
    AUG: title: str
    return: str: .md as html
    """
    post_dir = os.path.join(config.APP_ROOT, 'posts')

    with open(os.path.join(post_dir, f"{title.replace(' ', '-')}.md")) as f: 
        text = f.read()
        html = markdown.markdown(text, extensions=['markdown.extensions.fenced_code'])

    return html


def markdown_to_string(file_name):
    """converts .md to str
    AUG: file_name: str: name of the file (plus extension)
    return: str: .md as str
    """
    output = None
    post_dir = os.path.join(config.APP_ROOT, 'posts')

    with open(os.path.join(post_dir, f'{file_name}')) as f: 
        output = f.read()

    return output


def delete_markdown_file(title):
    """deletes physical .md file
    AUG: title: str: hypon separated title
    return: boolean
    """
    post_dir = os.path.join(config.APP_ROOT, 'posts')

    try:
        os.remove(os.path.join(post_dir, f'{title}.md'))

        return True

    except:
        return False


def rename_markdown_file(src, dst):
    """renames markdown file
    AUG: src: source name
    dst: destination name
    return: boolean
    """
    post_dir = os.path.join(config.APP_ROOT, 'posts')

    try:
        os.rename(
            os.path.join(post_dir, src),
            os.path.join(post_dir, dst)
            )

        return True

    except:
        return False