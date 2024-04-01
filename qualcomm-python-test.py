# Given a words.txt file containing a newline-delimited list of dictionary
# words, please implement the Anagrams class so that the get_anagrams() method
# returns all anagrams from words.txt for a given word.
#
# Bonus requirements:
#   - Optimise the code for fast retrieval
#   - Write more tests
#   - Thread safe implementation

import os
import threading
import collections
import unittest


class Anagrams:

    readCount = 5

    def __init__(self,  filePath = 'qualcomm-test-words.txt'):
        if not os.path.isfile(filePath):
            raise FileNotFoundError(f"File '{filePath}' not found.")
        
        with open(filePath, 'r') as file:
            self.words = file.read().splitlines()

        self.write_lock = threading.RLock()                     # Lock for write operations
        self.read_sem = threading.Semaphore(self.readCount)     # Semaphore for read operations
        self.anagrams_dict = self._build_anagrams_dict()


    def _build_anagrams_dict(self):
        anagrams_dict = collections.defaultdict(list)
        with self.write_lock:
            for word in self.words:
                key = ''.join(sorted(word))
                anagrams_dict[key].append(word)
        return anagrams_dict
        
    def get_anagrams(self, word):
        key = ''.join(sorted(word.strip().lower()))
        with self.read_sem:  # Acquire read semaphore
            return self.anagrams_dict.get(key, [])




class TestAnagrams(unittest.TestCase):

    def setUp(self):
        self.anagrams = Anagrams()

    def test_anagrams(self):
        self.assertEqual(self.anagrams.get_anagrams('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])
        self.assertEqual(self.anagrams.get_anagrams('eat'), ['ate', 'eat', 'tea'])

    # Test getting anagrams for a word that doesn't exist
    def test_get_anagrams_nonexistent_word(self):
        self.assertEqual(self.anagrams.get_anagrams("nonexistentAnagram"), [])

    # Test handling of words with whitespace
    def test_words_with_whitespace(self):
        self.assertEqual(self.anagrams.get_anagrams(' eat '), ['ate', 'eat', 'tea'])

    # Test handling of single-character words
    def test_single_character_words(self):
        self.assertEqual(self.anagrams.get_anagrams('a'), [])

    # Test case insensitivity
    def test_case_insensitivity(self):
        self.assertEqual(self.anagrams.get_anagrams('PlaTeS'), ['palest', 'pastel', 'petals', 'plates', 'staple'])


if __name__ == '__main__':
    unittest.main()