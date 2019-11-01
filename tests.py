import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        """Test that we DO show the RSVP form if the user has not RSVP'd"""
        result = self.client.get("/")
        self.assertIn(b'<h2>Please RSVP</h2>', result.data)

    def test_rsvp(self):

        """Test that we don't show the RSVP form if a user has RSVP'd"""

        app.config['SECRET_KEY'] = 'secret'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)

        self.assertIn(b'<h2>Party Details</h2>', result.data)
        self.assertNotIn(b'<h2>Please RSVP</h2>', result.data)
        # FIXME: Once we RSVP, we should see the party details, but
        # not the RSVP form



class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        """Test test data"""
        # FIXME: test that the games page displays the game from example_data()
        result = self.client.get("/games")
        self.assertIn(b'why does anyone', result.data)
        self.assertIn(b'Chinese Checkers', result.data)


if __name__ == "__main__":
    unittest.main()
