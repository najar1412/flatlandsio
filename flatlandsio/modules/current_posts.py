import app
import modules.models

"""Until I build something better this is how im keeping
posts persistant accross dev/prod databases"""

# current posts
def current_posts(db):
    user = 'Rory Jarrel'
    with app.app.app_context():

        post_all = modules.models.Post.query.all()
        if len(post_all) == 0:
            print('--------------------')
            print('Adding Posts')
            print('--------------------')
        
            post_01 = modules.models.Post(
                title='how to serve flask applications with gunicorn and nginx on ubuntu 1604',
                author=user,
                tags='ubuntu flask gunicorn nginx reference digitalocean',
                strap='This guide is originally from Digitalocean. Full credit goes to them, this is just a condensed version for my reference.',
                content='how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-1604.md',
                pub_date='15.12.2016',
                published=True
            )
            db.session.add(post_01)

            post_02 = modules.models.Post(
                title='https using letsencrypt with nginx flask on ubuntu',
                author=user,
                tags='ubuntu flask nginx letsencrypt digitalocean miguelgrinberg reference',
                strap='This guide is originally from Miguel Grinberg and Digitalocean. Full credit goes to them, this is just a condensed version for my reference.',
                content='https-using-letsencrypt-with-nginx-flask-on-ubuntu.md',
                pub_date='9.11.2017',
                published=True
            )
            db.session.add(post_02)

            post_03 = modules.models.Post(
                title='initial celery setup on ubuntu 1604',
                author=user,
                tags='ubuntu celery reference',
                strap='This guide is originally from pythad.github.io. Full credit goes to them, this is just a condensed version for my reference.',
                content='initial-cellery-setup-on-ubunut-1604.md',
                pub_date='7.11.2017',
                published=True
            )
            db.session.add(post_03)

            post_04 = modules.models.Post(
                title='initial server setup with ubuntu 1604',
                author=user,
                tags='ubuntu server security reference digitalocean',
                strap='This guide is originally from Digitalocean. Full credit goes to them, this is just a condensed version for my reference.',
                content='initial-server-setup-with-ubuntu-1604.md',
                pub_date='7.12.2016',
                published=True
            )
            db.session.add(post_04)

            post_05 = modules.models.Post(
                title='writing a library in python',
                author=user,
                tags='python pypi reference tutsplus',
                strap='This guide is originally from Tutsplus. Full credit goes to them, this is just a condensed version for my reference.',
                content='writing-a-library-in-python.md',
                pub_date='26.12.2017',
                published=True
            )
            db.session.add(post_05)


            db.session.commit()

        else:
            print('--------------------')
            print('Posts already exist')
            print('--------------------')
            pass