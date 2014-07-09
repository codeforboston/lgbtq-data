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

  def test_expand_all(self):
    # takes a lit of strings, ["a", "b", "c;d;e"]
    # splits any elements separated by semicolons
    # -> ["a", "b", "c", "d", "e"]
    result = csv_to_json.expand_all(["a", "b", "c; d ;e  "])
    self.assertEqual(result, ["a", "b", "c", "d", "e"])

  def test_expand_all_single(self):
    result = csv_to_json.expand_all(["a"])
    self.assertEqual(result, ["a"])

