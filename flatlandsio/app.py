import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

import modules.data as data
import modules.database


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flatlands.db'
db = SQLAlchemy(app)

root_dir = os.path.dirname(os.path.abspath(__file__))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    tags = db.Column(db.String())
    strap = db.Column(db.String())
    content = db.Column(db.String())
    pub_date = db.Column(db.String())
    published = db.Column(db.String())

    def __repr__(self):
        return '<Post %r>' % self.title


class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    tags = db.Column(db.String())
    strap = db.Column(db.String())
    content = db.Column(db.String())
    type = db.Column(db.String())

    def __repr__(self):
        return '<Software %r>' % self.title

db.create_all()


@app.route('/')
def index():
    posts = modules.database.to_json(Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('blog.html', posts=posts, years=years)


@app.route('/blog')
def blog():
    posts = modules.database.to_json(Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('blog.html', posts=posts, years=years)


@app.route('/blog/<title>')
def post(title):
    title = title.replace('-', ' ')

    blog_post = modules.database.to_json((Post.query.filter_by(title=title).first(),))[1]
    blog_post['content'] = modules.database.markdown_to_html(title)

    return render_template('blog_post.html', post=blog_post)


@app.route('/blog/new', methods=['GET', 'POST'])
def post_new():
    if request.method == 'POST':
        form = request.form
        title = form['inputTitle'].replace(' ', '-')
        article = modules.database.create_markdown(title, '')

        admin = Post(
            title=form['inputTitle'], author='rory jarrel', 
            published='False', content=article, 
            pub_date=modules.database.date_format(), tags='', strap=''
        )

        db.session.add(admin)
        db.session.commit()

    posts = modules.database.to_json(Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('settings.html', posts=posts, years=years)


@app.route('/blog/edit/<title>', methods=["GET", "POST"])
def post_edit(title):
    if request.method == 'GET':
        title = title.replace('-', ' ')
        post = modules.database.to_json((Post.query.filter_by(title=title).first(),))[1]
        post['content'] = modules.database.markdown_to_html(post['title'])

        return render_template('post_edit.html', post=post)


    if request.method == 'POST':
        form = modules.database.form_to_dict(request.form)
        modules.database.edit_post(form, title)
        title = form['inputTitle'].replace(' ', '-')

        return redirect(f'/blog/{title}')


@app.route('/blog/publish/<title>')
def post_publish(title):
    title = title.replace('-', ' ')
    get_post = Post.query.filter_by(title=title).first()

    if get_post.published == 'True':
        get_post.published = 'False'

    else:
        get_post.published = 'True'

    db.session.commit()

    return redirect('/settings')


@app.route('/blog/delete/<title>')
def post_delete(title):
    del_markdown = modules.database.delete_markdown_file(title)
    if del_markdown:
        title = title.replace('-', ' ')
        get_post = Post.query.filter_by(title=title).first()
        db.session.delete(get_post)
        db.session.commit()

    else:
        print('markdown file not deleted')

    posts = modules.database.to_json(Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('settings.html', posts=posts, years=years)


@app.route('/tag/<tag>')
def tag(tag):
    all_posts = modules.database.to_json(Post.query.all())
    posts = modules.database.get_post_by_tag(str(tag), all_posts)
    years = modules.database.get_post_years(posts)

    return render_template('tag.html', posts=posts, years=years)


@app.route('/software')
def software():
    software = data.software
    software_types = data.get_software_types(software)

    return render_template('software.html', software=software, software_types=software_types)


@app.route('/software/<title>')
def project(title):
    product = data.get_software_by_title(title.replace('-', ' '))

    return render_template('product.html', product=product)


@app.route('/about')
def about():
    about = data.about

    return render_template('about.html', about=about)


@app.route('/settings')
def settings():
    posts = modules.database.to_json(Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('settings.html', posts=posts, years=years)


if __name__ == '__main__':
    app.run(debug='true')