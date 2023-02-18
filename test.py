from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

 
class FlaskTests(TestCase):

    def setUp(self):
        """Running setup needed before running tests"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Check session is storing information properly and HTML is rendering"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('timesplayed'))
            self.assertIn(b'Score', res.data)
            self.assertIn(b'Seconds', res.data)

    def test_valid_word(self):
        """test for checking validity of word and if it's on the board"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["C","H","E","C","K"],
                                    ["C","H","E","C","K"],
                                    ["C","H","E","C","K"],
                                    ["C","H","E","C","K"],
                                    ["C","H","E","C","K"]]
        res = self.client.get('/validate?word=check')
        self.assertEqual(res.json['result'], "ok")

    def test_not_valid(self):
        """Test to see if word is in dictionary"""

        self.client.get('/')
        res = self.client.get('/validate?word=jslwjjhih')
        self.assertEqual(res.json['result'], "not-word")

    def test_not_found(self):
        """Test to see if word is in on the board"""

        self.client.get('/')
        res = self.client.get('/validate?word=aardvark')
        self.assertEqual(res.json['result'], "not-on-board")


        




   

