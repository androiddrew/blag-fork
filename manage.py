import random

from flask_script import Manager, prompt_bool

from blagging import app, create_app, db
from blagging.models import Post, Author, Tag

# app = create_app('dev')
manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    print('Database Initialized')


@manager.command
def dropdb():
    if prompt_bool('Are you sure you want to drop the database?'):
        db.drop_all()
        print('Database tables dropped')


@manager.command
def test_data():
    """Command to populate database with test data"""

    test_short = 'This is going to be the portion of the post that is displayed to the end user when they first \
        log into the app.'

    test_body = "Lorem ipsum dolor sit amet, debet gubergren duo at, tamquam veritus verterem mea in, eu cibo iudico \
        pri. Postea discere perfecto cum ut. Mel agam melius repudiare at. Eu voluptua nominati vix, mandamus \
        inciderint pri in. Accommodare mediocritatem has ex. Mel et hinc facer lobortis, at officiis corrumpit \
        consetetur pri, quo no ignota tritani."

    androiddrew = Author(display_name='Androiddrew', email='bednar.andrew@gmail.com', password='test')
    lauraurban = Author(display_name='UrbanDecayed', email='kolady.laura@fake.com', password='test')
    db.session.add(androiddrew)
    db.session.add(lauraurban)


    def add_post(title, short_desc, body, tags):
        post = Post(title=title, display_title=title, short_desc=short_desc, body=body, tags=tags,
                    author=androiddrew)
        db.session.add(post)

    for name in ['programming', 'flask', 'dirp', 'food']:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_post(title='First post', short_desc=test_short, body=test_body, tags='programming,flask')
    add_post(title='Second post', short_desc=test_short, body=test_body, tags='dirp,flask')
    add_post(title='Third post', short_desc=test_short, body=test_body, tags='programming,food')
    add_post(title='Fourth post', short_desc=test_short, body=test_body, tags='programming,food')
    add_post(title='Inactive', short_desc=test_short, body=test_body, tags='dirp,food')
    db.session.commit()
    print('Test data created')


if __name__ == '__main__':
    manager.run()
