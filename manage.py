from flask_script import Manager, prompt_bool

from blagging import app, create_app, db
from blagging.models import Post, Author, Tag, Comment

#app = create_app('dev')
manager = Manager(app)


test_short='This is going to be the portion of the post that is displayed to the end user when they first \
        log into the app.'
test_body="Lorem ipsum dolor sit amet, debet gubergren duo at, tamquam veritus verterem mea in, eu cibo iudico \
        pri. Postea discere perfecto cum ut. Mel agam melius repudiare at. Eu voluptua nominati vix, mandamus \
        inciderint pri in. Accommodare mediocritatem has ex. Mel et hinc facer lobortis, at officiis corrumpit \
        consetetur pri, quo no ignota tritani."


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
def insert_data():
    androiddrew = Author(display_name='Androiddrew', email='bednar.andrew@gmail.com')
    lauraurban = Author(display_name='UrbanDecayed', email='kolady.laura@fake.com')
    db.session.add(androiddrew)
    db.session.add(lauraurban)

    def add_comment(text, post):
        db.session.add(Comment(text=text, post=post, user=lauraurban))

    def add_post(title, short_desc, body, tags):
        post = Post(title=title, display_title=Post.slugify(title), short_desc=short_desc,
                            body=body, tags=tags, author=androiddrew)
        db.session.add(post)
        add_comment('This is a default comment', post)


    for name in ['programming', 'flask', 'dirp', 'food']:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_post(title='First post', short_desc=test_short, body=test_body, tags='programming, flask')
    add_post(title='Second post', short_desc=test_short, body=test_body, tags='dirp, flask')
    add_post(title='Third post', short_desc=test_short, body=test_body, tags='programming, food')
    db.session.commit()
    print('Test data created')


if __name__ == '__main__':
    manager.run()
