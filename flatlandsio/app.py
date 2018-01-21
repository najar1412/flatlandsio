import os

from flask import Flask, render_template, request, redirect, abort, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

import modules.data as data
import modules.database
import modules.models


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flatlands.db'
app.config['SECRET_KEY'] = 'jkh34k5jh3k4j5hk3j4h5'

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

modules.models.db.init_app(app)
modules.models.db.create_all(app=app)

root_dir = os.path.dirname(os.path.abspath(__file__))

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return modules.models.User.query.filter_by(id=userid).first()


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # validate cred
        validate_username = modules.models.User.query.filter_by(username=username).first()
        if validate_username:
            if validate_username.password == password:
                login_user(validate_username)

                return redirect(request.args.get("next"))

        else:
            return abort(401)

    else:
        return Response('''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        ''')


# somewhere to logoutlogout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    # module.query.session_close(session)


    return redirect("/login")


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.route('/')
def index():
    posts = modules.database.to_json(modules.models.Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('blog.html', posts=posts, years=years)


@app.route('/blog')
def blog():
    posts = modules.database.to_json(modules.models.Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('blog.html', posts=posts, years=years)


@app.route('/blog/<title>')
def post(title):
    title = title.replace('-', ' ')

    blog_post = modules.database.to_json((modules.models.Post.query.filter_by(title=title).first(),))[1]
    blog_post['content'] = modules.database.markdown_to_html(title)

    return render_template('blog_post.html', post=blog_post)


@app.route('/blog/new', methods=['GET', 'POST'])
def post_new():
    if request.method == 'POST':
        form = request.form
        title = form['inputTitle'].replace(' ', '-')
        article = modules.database.create_markdown(title, '')

        admin = modules.models.Post(
            title=form['inputTitle'], author='rory jarrel', 
            published='False', content=article, 
            pub_date=modules.database.date_format(), tags='', strap=''
        )

        modules.models.db.session.add(admin)
        modules.models.db.session.commit()

    posts = modules.database.to_json(modules.models.Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('settings.html', posts=posts, years=years)


@app.route('/blog/edit/<title>', methods=["GET", "POST"])
def post_edit(title):
    if request.method == 'GET':
        title = title.replace('-', ' ')
        post = modules.database.to_json((modules.models.Post.query.filter_by(title=title).first(),))[1]
        post['content'] = modules.database.markdown_to_string(f"{post['title'].replace(' ', '-')}.md")

        return render_template('post_edit.html', post=post)


    if request.method == 'POST':
        form = modules.database.form_to_dict(request.form)
        modules.database.edit_post(form, title)
        title = form['inputTitle'].replace(' ', '-')

        return redirect(f'/blog/{title}')


@app.route('/blog/publish/<title>')
def post_publish(title):
    title = title.replace('-', ' ')
    get_post = modules.models.Post.query.filter_by(title=title).first()

    if get_post.published == 'True':
        get_post.published = 'False'

    else:
        get_post.published = 'True'

    modules.models.db.session.commit()

    return redirect('/settings')


@app.route('/blog/delete/<title>')
def post_delete(title):
    del_markdown = modules.database.delete_markdown_file(title)
    if del_markdown:
        title = title.replace('-', ' ')
        get_post = modules.models.Post.query.filter_by(title=title).first()
        modules.models.db.session.delete(get_post)
        modules.models.db.session.commit()

    else:
        print('markdown file not deleted')

    posts = modules.database.to_json(modules.models.Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('settings.html', posts=posts, years=years)


@app.route('/tag/<tag>')
def tag(tag):
    all_posts = modules.database.to_json(modules.models.Post.query.all())
    posts = modules.database.get_post_by_tag(str(tag), all_posts)
    years = modules.database.get_post_years(posts)

    return render_template('tag.html', posts=posts, years=years)


@app.route('/portfolio')
def portfolio():
    portfolio = data.software
    portfolio_types = data.get_software_types(portfolio)

    return render_template('portfolio.html', software=portfolio, software_types=portfolio_types)


@app.route('/software/<title>')
def project(title):
    product = data.get_software_by_title(title.replace('-', ' '))

    return render_template('product.html', product=product)


@app.route('/about')
def about():
    about = data.about

    return render_template('about.html', about=about)


@app.route('/settings')
@login_required
def settings():
    posts = modules.database.to_json(modules.models.Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('settings.html', posts=posts, years=years)


if __name__ == '__main__':
    app.run(debug=True)