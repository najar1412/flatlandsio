import os

from flask import Flask, render_template, request, redirect, abort, Response, session
from flask_login import LoginManager, login_required, login_user, logout_user

import modules.data as data
import modules.database
import modules.models
import modules.current_posts


app = Flask(__name__)
app.config.from_object('config')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

modules.models.db.init_app(app)
modules.models.db.create_all(app=app)

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return modules.models.User.query.filter_by(id=userid).first()

# TODO: below is the current solution for post persistancy between dev and prod
# databases.
# Eventually build something that gets posts from the post folder.
modules.current_posts.current_posts(modules.models.db)

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
    session.clear()

    return redirect("/")


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

    return render_template('article.html', posts=posts, years=years)


@app.route('/article')
def article():
    posts = modules.database.to_json(modules.models.Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('article.html', posts=posts, years=years)


@app.route('/article/<title>')
def post(title):
    title = title.replace('-', ' ')

    blog_post = modules.database.to_json((modules.models.Post.query.filter_by(title=title).first(),))[1]
    blog_post['content'] = modules.database.markdown_to_html(title)

    return render_template('blog_post.html', post=blog_post)


@app.route('/article/new', methods=['GET', 'POST'])
def post_new():
    if request.method == 'POST':
        form = request.form
        title = form['inputTitle'].replace(' ', '-')
        article = modules.database.create_markdown(title, '')

        admin = modules.models.Post(
            title=form['inputTitle'], author='rory jarrel', 
            published=False, content=article, 
            pub_date=modules.database.date_format(), tags='', strap=''
        )

        modules.models.db.session.add(admin)
        modules.models.db.session.commit()

    posts = modules.database.to_json(modules.models.Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('settings.html', posts=posts, years=years)


@app.route('/article/edit/<title>', methods=["GET", "POST"])
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

        return redirect(f'/article/{title}')


@app.route('/article/publish/<title>')
def post_publish(title):
    title = title.replace('-', ' ')
    get_post = modules.models.Post.query.filter_by(title=title).first()

    if get_post.published == True:
        get_post.published = False

    else:
        get_post.published = True

    modules.models.db.session.commit()

    return redirect(request.referrer)


@app.route('/article/delete/<title>')
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
    return render_template('settings.html')


@app.route('/login/article')
@login_required
def login_article():
    posts = modules.database.to_json(modules.models.Post.query.all())
    years = modules.database.get_post_years(posts)

    return render_template('login_article.html', posts=posts, years=years)


@app.route('/login/solution')
@login_required
def login_solution():
    return render_template('login_solution.html')


@app.route('/login/about')
@login_required
def login_about():
    return render_template('login_about.html')


if __name__ == '__main__':
    app.run(debug=True)