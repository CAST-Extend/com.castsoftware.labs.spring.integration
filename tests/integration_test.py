import unittest
from cast.application.test import run
from cast.application import create_postgres_engine
import logging

logging.root.setLevel(logging.DEBUG)

class TestIntegration(unittest.TestCase):

    def test1(self):
        
        run(kb_name='cafe_local', application_name='cafeapp', engine=create_postgres_engine())


if __name__ == "__main__":
    unittest.main()
