from unittest import TestCase

from app import app
from models import db, User

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of a hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()

class UserRoutesTests(TestCase):
    """Tests the user routes"""

    def setUp(self):
        """Adds sample users"""

        db.create_all() 

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

        # add users to session
        db.session.add(chan)
        db.session.add(stiller)
        db.session.add(wilson)
        db.session.add(alba)
        db.session.add(liu)

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
            d = {"first-name": "Daniel", "last-name": "Tressel", "image-url": "https://www.dt.com/pic"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Daniel Tressel</a>', html)
            self.assertIn('<h2>Users</h2>', html)

    def test_user_details_page(self):
        with app.test_client() as client:
            resp = client.get('/user/4')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Jessica Alba</h2>', html)
            self.assertIn('<a href="/users" class="btn btn-outline-info">Back</a>', html)