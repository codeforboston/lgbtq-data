import unittest

import csv_to_json

class LGBTQTest(unittest.TestCase):
  def test_fix_email_okay(self):
    emails = ['alice@gmail.com', 'bob@yahoo.com']
    
    result = csv_to_json.cleanup_emails(emails)
    self.assertEqual(emails, result)

  def test_fix_email(self):
    emails = ['mailto:alice@gmail.com', 'bob@yahoo.com']

    result = csv_to_json.cleanup_emails(emails)
    self.assertEqual(['alice@gmail.com', 'bob@yahoo.com'], result)
