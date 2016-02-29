from flask_script import Manager, prompt_bool

from blagging import app, create_app, db
from blagging.models import Post, Author

#app = create_app('dev')
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
def testdata():
    author = Author(display_name='Androiddrew', )
    db.session.add(author)
    db.session.commit()
    post_title = 'This is a test post'
    post1 = Post(
        title=post_title,
        author_id=author.id,
        display_title=Post.slugify(post_title),
        short_desc='This is going to be the portion of the post that is displayed to the end user when they first \
        log into the app.',
        body="Lorem ipsum dolor sit amet, debet gubergren duo at, tamquam veritus verterem mea in, eu cibo iudico \
        pri. Postea discere perfecto cum ut. Mel agam melius repudiare at. Eu voluptua nominati vix, mandamus \
        inciderint pri in. Accommodare mediocritatem has ex. Mel et hinc facer lobortis, at officiis corrumpit \
        consetetur pri, quo no ignota tritani.",
    )
    db.session.add(post1)
    db.session.commit()
    print('Test data created')


if __name__ == '__main__':
    manager.run()