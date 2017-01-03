from flask_script import Manager, prompt_bool
from sqlalchemy.exc import SQLAlchemyError
from blagging import app, db
from blagging.models import Post, Author, Tag


manager = Manager(app)

@manager.command
def initdb():
    try:
        db.create_all()
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating database: {}".format(e))
    print('Database Initialized')


@manager.command
def dropdb():
    if prompt_bool('Are you sure you want to drop the database?'):
        try:
            db.drop_all()
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error dropping data: {}".format(e))
        print('Database tables dropped')


@manager.command
def create_admin():
    admin = Author(display_name="admin", email="admin@fake.com", password="admin")
    placeholder = Post(title="Placeholder", display_title="Placeholder", short_desc="Placeholder", body="Placeholder", tags="Placeholder",
                       author=admin)
    try:
        db.session.add(admin)
        db.session.commit()
        db.session.add(placeholder)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error inserting adding: {}".format(e))
    print("admin and first entry created")

@manager.command
def test_data():
    """Command to populate database with test data"""
    with db.session.no_autoflush:

        test_short = 'This is going to be the portion of the post that is displayed to the end user when they first \
            log into the app.'

        test_body = "Lorem ipsum dolor sit amet, debet gubergren duo at, tamquam veritus verterem mea in, eu cibo iudico \
            pri. Postea discere perfecto cum ut. Mel agam melius repudiare at. Eu voluptua nominati vix, mandamus \
            inciderint pri in. Accommodare mediocritatem has ex. Mel et hinc facer lobortis, at officiis corrumpit \
            consetetur pri, quo no ignota tritani."

        androiddrew = Author(display_name='Androiddrew', email='drew@androiddrew.com', password='test')
        lauraurban = Author(display_name='UrbanDecayed', email='kolady.laura@fake.com', password='test')
        try:
            db.session.add(androiddrew)
            db.session.add(lauraurban)
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error inserting users: {}".format(e))

        def add_post(title, short_desc, body, tags):
            post = Post(title=title, display_title=title, short_desc=short_desc, body=body, tags=tags,
                        author=androiddrew)
            db.session.add(post)

        try:
            for name in ['programming', 'flask', 'dirp', 'food']:
                db.session.add(Tag(name=name))
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error inserting Tags: {}".format(e))

        try:
            add_post(title='First post', short_desc=test_short, body=test_body, tags='programming,flask')
            add_post(title='Second post', short_desc=test_short, body=test_body, tags='dirp,flask')
            add_post(title='Third post', short_desc=test_short, body=test_body, tags='programming,food')
            add_post(title='Fourth post', short_desc=test_short, body=test_body, tags='programming,food')
            add_post(title='Inactive', short_desc=test_short, body=test_body, tags='dirp,food')
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error inserting posts: {}".format(e))

    print('Test data created')


if __name__ == '__main__':
    manager.run()
