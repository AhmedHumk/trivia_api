import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Question, Category
import random
import time


# an uneeded function to generate random date to my create question test 
def genrandomDate(start, end, format, rndnum):
    startTime = time.mktime(time.strptime(start, format))
    endTime = time.mktime(time.strptime(end, format))

    fullrandomTime = startTime + rndnum * (endTime - startTime)
    return time.strftime(format, time.localtime(fullrandomTime))

def RandomizeDate(start, end, rndnum):
    return genrandomDate(start, end, '%m/%d/%Y', rndnum)

# a constant variable that hold my random date each run
randomDatestr = RandomizeDate("1/1/2050", "1/1/2100", random.random())


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        
        self.dbName = "trivia_test"
        self.dbUser = "postgres"
        self.dbpass = "0000"
        self.dburl = "localhost:5432"
        self.DBFULLURI = "postgres://{}:{}@{}/{}".format(self.dbUser, self.dbpass, self.dburl, self.dbName)

        setup_db(self.app, self.DBFULLURI)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()



        ###########################################################
        # Create New Category Test
        ##############################################################
        self.CreateNewCat = {
            "catname": "Mars Cat in " + randomDatestr
            }

        ###########################################################
        # Create New question Test
        ##############################################################
        self.CreateNewQuestion = {
            "question": "are we Going To Mars in " + randomDatestr + " ?",
            "answer": "maybe",
            "category": "3",
            "difficulty": "2"
            }

            
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test our categories / collectCats Based on
    # lesson 4 practice Test in Flask
    def test_collectCats(self):
        res = self.client().get("/api/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_categories"])

    # Create a new random category For Test 
    def test_CreateNewCat(self):
        res = self.client().post("/api/categories", json=self.CreateNewCat)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["Created"])


    # CollectQuestions Test
    def test_CollectQuestions(self):
        res = self.client().get("/api/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        
    
    # start our create New random question For Test
    def test_CreateQuestion(self):
        res = self.client().post("/api/questions", json=self.CreateNewQuestion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["Created"])

    # test our playquizzes that we excpect to success
    # Based on my trivia.psql
    def test_playquizzes(self):
        res = self.client().post('/api/quizzes', json={'previous_questions': [1, 2], 'quiz_category': {'id': 3}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertTrue(data["previousQuestions"])

    # Test with an intention to raise error
    def test_playquizzes_that_have_invalid_category(self):
        res = self.client().post('/api/quizzes', json={'previous_questions': [1, 2], 'quiz_category': {'id': 5000}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['previousQuestions'])

    #catch the error 422
    def test_playquizzes_ERR_NotFound(self):
        res = self.client().post('/api/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
