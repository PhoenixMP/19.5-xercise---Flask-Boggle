from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_boggle_home(self):
        """Test the message displayed in html depending on the different score values"""

        with self.client as client:
            message1 = "Get ready to rack up some points!"
            message2 = "Your High-Score is 2"
            with client.session_transaction() as change_session:
                change_session['score'] = 0
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

        html = resp.get_data(as_text=True)
        self.assertIn(message1, html)
        with client.session_transaction() as change_session:
            change_session['score'] = 2
        resp2 = self.client.get('/')
        html2 = resp2.get_data(as_text=True)
        self.assertIn(message2, html2)

    def test_process_guess(self):
        """Test if word is not on the board or not in the dictionary"""

        self.client.get('/')
        resp = self.client.get('/guess?guess=lkjsdflkjsdfjs')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['result'], 'not-word')

        self.client.get('/')
        resp2 = self.client.get('/guess?guess=abacination')
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.json['result'], 'not-on-board')
