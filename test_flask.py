# Run tests by command: python -m unittest test_flask.py

from unittest import TestCase

from app import app
from models import db, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of a hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# drop all tables in test database before start 
db.drop_all()

class UserRoutesTests(TestCase):
    """Tests the user routes"""

    def setUp(self):
        """Adds sample users and posts"""

        # create all tables in test database
        db.create_all() 

        # create users for test database
        chan = User(first_name='Jackie', last_name='Chan',
            image_url='https://m.media-amazon.com/images/M/MV5BMTk4MDM0MDUzM15BMl5BanBnXkFtZTcwOTI4MzU1Mw@@._V1_.jpg')
        stiller = User(first_name='Ben', last_name='Stiller',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkIpCSN42YT4TosyKMHWYWw2awXpPPKBSBACzviU7tlYbqYdv7')
        wilson = User(first_name='Owen', last_name='Wilson',
            image_url='https://www.themoviedb.org/t/p/w300_and_h450_bestv2/op8sGD20k3EQZLR92XtaHoIbW0o.jpg')
        alba = User(first_name='Jessica', last_name='Alba',
            image_url='https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcR43x1OlSVXS4fZD0IseZHlGAbygdKOfVgZP6Uthz3yOhbb2Qv8')
        liu = User(first_name='Lucy', last_name='Liu',
            image_url='https://www.emmys.com/sites/default/files/styles/bio_pics_detail/public/bios/lucy-liu-ap-450x600.jpg?itok=R_aziYvA')

        # add users to test database
        db.session.add_all([chan, stiller, wilson, alba, liu])
        db.session.commit()

        # create posts for test database
        chan_post1 = Post(title='The Dangers of Stunts',
            content='Stunts can be very dangerous. One time I broke my foot while doing a stunt. It hurt!',
            user_id=chan.id)
        chan_post2 = Post(title='My Buddy, Chris Tucker',
            content='Sometimes you it''s easy to get along with your co-stars, sometimes it''s not. Chris Tucker was one of the most fun persons to work with.',
            user_id=chan.id)
        stiller_post1 = Post(title='Meet the Pear Tree',
            content='I love pears, and I decided to plant a pear tree years ago. It now bears fruit every year. Those pears are so sweet!',
            user_id=stiller.id)
        stiller_post2 = Post(title='How to Be Funny',
            content='It''s not easy to be funny. It''s best not to try too hard and let your quirks and unique personality shine through.',
            user_id=stiller.id)
        wilson_post1 = Post(title='I''m a Cowboy',
            content='I can''t believe I starred in a movie, playing a cowboy in a movie with Jackie Chan. What an experience!',
            user_id=wilson.id)
        wilson_post2 = Post(title='My Poor Nose',
            content='Unfortunately, my nose is a bit oddly shaped. It''s because I broke it, but now it is an essential part of my signature look.',
            user_id=wilson.id)
        alba_post1 = Post(title='A Dictionary Can Sleep?',
            content='I once played a role in a move called "The Sleeping Dictionary." I never understood the title. A dictionary is just a book. It doesn''t sleep!',
            user_id=alba.id)
        alba_post2 = Post(title='Woah, Ben!',
            content='I played a part in a movie with Ben Stiller. He once made a joke that was borderline inappropriate. I said "woah, Ben!"',
            user_id=alba.id)
        liu_post1 = Post(title='Skiing Freestyle',
            content='I really like to ski in the winter. I like to ski without poles. I call it "skiing freestyle."',
            user_id=liu.id)
        liu_post2 = Post(title='Have a Good Burrito!',
            content='My friend decided to go get a burrito after we had been chatting for a while. I said "have a good burrito!" My other friend who had just entered the room said "that''s an interesting salutation!"',
            user_id=liu.id)

        posts = [chan_post1, chan_post2, stiller_post1, stiller_post2, wilson_post1, wilson_post2, alba_post1, alba_post2, liu_post1, liu_post2]

        # add posts to test database
        db.session.add_all(posts)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction and clear table"""

        db.session.rollback()
        db.drop_all()

    def test_users_page(self):
        with app.test_client() as client:
            resp = client.get('/users')       
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Users</h2>', html)
            self.assertIn('Lucy Liu</a>', html)
            self.assertIn('Ben Stiller</a>', html)

    def test_add_user_page(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Create a User</h2>', html)
            self.assertIn('<label for="last-name">Last Name</label>', html)
            self.assertIn('<a href="/users" class="btn btn-outline-info">Cancel</a>', html)

    def test_add_user_submit(self):
        with app.test_client() as client:
            data = {"first-name": "Daniel", "last-name": "Tressel", "image-url": "https://www.dt.com/pic"}
            resp = client.post('/users/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Daniel Tressel</a>', html)
            self.assertIn('<h2>Users</h2>', html)

    def test_user_details_page(self):
        with app.test_client() as client:
            alba = User.query.filter_by(last_name='Alba').first()
            resp = client.get(f'/users/{alba.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Jessica Alba</h2>', html)
            self.assertIn('<a href="/users" class="btn btn-outline-info">Back</a>', html)
            self.assertIn('A Dictionary Can Sleep?</a>', html)

    def test_edit_user_page(self):
        with app.test_client() as client:
            liu = User.query.filter_by(last_name='Liu').first()
            resp = client.get(f'/users/{liu.id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Edit User Liu</h2>', html)
            self.assertIn(f'<form method="post" action="/users/{liu.id}/edit">', html)

    def test_edit_user_submit(self):
        with app.test_client() as client:
            chan = User.query.filter_by(last_name='Chan').first()
            data = {"first-name": "Jackie", "last-name": "Choner", "image-url": f"{chan.image_url}"}
            resp = client.post(f'/users/{chan.id}/edit', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Jackie Choner</h2>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            wilson = User.query.filter_by(last_name='Wilson').first()
            resp = client.post(f'/users/{wilson.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Wilson', html)
            self.assertIn('Chan', html)
            self.assertIn('Alba', html)
            self.assertIn('Liu', html)
            self.assertIn('Stiller', html)

    def test_new_post_page(self):
        with app.test_client() as client:
            stiller = User.query.filter_by(last_name='Stiller').first()
            resp = client.get(f'/users/{stiller.id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Add Post for Ben Stiller</h2>', html)
            self.assertIn(f'<form method="post" action="/users/{stiller.id}/posts/new">', html)
            