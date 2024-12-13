from search import keyword_to_titles, title_to_info, search, article_length, key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main
import time
import datetime
class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)
    
    def test_keyword_to_titles(self):
        metadata = [
            ["Article 1", "Author A", 123456, 500, ["cat", "dog"]],
            ["Article 2", "Author B", 654321, 300, ["dog", "bird"]],
            ["Article 3", "Author C", 789012, 400, ["cat"]]
        ]
        expected = {"cat": ["Article 1", "Article 3"], "dog": ["Article 1", "Article 2"], "bird": ["Article 2"]}
        self.assertEqual(keyword_to_titles(metadata), expected)

        # Test empty metadata
        self.assertEqual(keyword_to_titles([]), {})

        # Test with one keyword and one article
        metadata = [["Article 4", "Author D", 987654, 200, ["fish"]]]
        expected = {"fish": ["Article 4"]}
        self.assertEqual(keyword_to_titles(metadata), expected)
    
    def test_title_to_info(self):
        metadata = [
            
            ["Article 1", "Author A", 123456, 500, ["cat"]],
            ["Article 2", "Author B", 654321, 300, ["dog"]]
        ]
        expected = {
            "Article 1": {"author": "Author A", "timestamp": 123456, "length": 500},
            "Article 2": {"author": "Author B", "timestamp": 654321, "length": 300}
        }
        self.assertEqual(title_to_info(metadata), expected)

        # Test empty metadata
        self.assertEqual(title_to_info([]), {})

        # Test single article
        metadata = [["Article 3", "Author C", 789012, 400, ["cat"]]]
        expected = {"Article 3": {"author": "Author C", "timestamp": 789012, "length": 400}}
        self.assertEqual(title_to_info(metadata), expected)

    def test_search(self):
        keyword_dict = {
            "cat": ["Article 1", "Article 2"],
            "dog": ["Article 3"]
        }
        # Basic functionality
        self.assertEqual(search("cat", keyword_dict), ["Article 1", "Article 2"])

        # Test keyword not in dictionary
        self.assertEqual(search("bird", keyword_dict), [])

        # Test case sensitivity
        self.assertEqual(search("Cat", keyword_dict), [])
    
    def test_article_length(self):
        title_info = {
            "Article 1": {"author": "Author A", "timestamp": 123456, "length": 300},
            "Article 2": {"author": "Author B", "timestamp": 654321, "length": 500}
        }
        titles = ["Article 1", "Article 2"]

        # Articles within the length limit
        self.assertEqual(article_length(400, titles, title_info), ["Article 1"])

        # No articles meet the length limit
        self.assertEqual(article_length(200, titles, title_info), [])

        # All articles meet the length limit
        self.assertEqual(article_length(600, titles, title_info), ["Article 1", "Article 2"])
        
    def test_key_by_author(self):
        title_info = {
            "Article 1": {"author": "Author A", "timestamp": 123456, "length": 300},
            "Article 2": {"author": "Author A", "timestamp": 654321, "length": 500},
            "Article 3": {"author": "Author B", "timestamp": 789012, "length": 700}
        }
        titles = ["Article 1", "Article 2", "Article 3"]

        expected = {"Author A": ["Article 1", "Article 2"], "Author B": ["Article 3"]}
        self.assertEqual(key_by_author(titles, title_info), expected)

        # Test empty title list
        self.assertEqual(key_by_author([], title_info), {})

        # Test single author
        self.assertEqual(key_by_author(["Article 1", "Article 2"], title_info), {"Author A": ["Article 1", "Article 2"]})
    
    def test_filter_to_author(self):
        title_info = {
            "Article 1": {"author": "Author A", "timestamp": 123456, "length": 300},
            "Article 2": {"author": "Author B", "timestamp": 654321, "length": 500}
        }
        titles = ["Article 1", "Article 2"]

        # Filter to existing author
        self.assertEqual(filter_to_author("Author A", titles, title_info), ["Article 1"])

        # Filter to non-existent author
        self.assertEqual(filter_to_author("Author C", titles, title_info), [])

        # Single title list
        self.assertEqual(filter_to_author("Author B", ["Article 2"], title_info), ["Article 2"])
    
    def test_filter_out(self):
        keyword_dict = {
            "cat": ["Article 1", "Article 2"],
            "dog": ["Article 3"]
        }
        titles = ["Article 1", "Article 2", "Article 3"]

        # Exclude articles with keyword
        self.assertEqual(filter_out("cat", titles, keyword_dict), ["Article 3"])

        # Exclude non-existent keyword
        self.assertEqual(filter_out("bird", titles, keyword_dict), ["Article 1", "Article 2", "Article 3"])

        # All titles excluded
        self.assertEqual(filter_out("cat", ["Article 1", "Article 2"], keyword_dict), [])


    def test_articles_from_year(self):
        title_info = {
            "Article 1": {"author": "Author A", "timestamp": time.mktime(datetime.date(2009, 5, 17).timetuple()), "length": 300},
            "Article 2": {"author": "Author B", "timestamp": time.mktime(datetime.date(2008, 7, 24).timetuple()), "length": 500}
        }
        titles = ["Article 1", "Article 2"]

        # Articles from the year 2009
        self.assertEqual(articles_from_year(2009, titles, title_info), ["Article 1"])

        # No articles from 2010
        self.assertEqual(articles_from_year(2010, titles, title_info), [])

        # Multiple articles from the same year
        title_info["Article 3"] = {"author": "Author C", "timestamp": time.mktime(datetime.date(2009, 9, 10).timetuple()), "length": 400}
        titles.append("Article 3")
        self.assertEqual(articles_from_year(2009, titles, title_info), ["Article 1", "Article 3"])




    #####################
    # INTEGRATION TESTS #
    #####################

    # @patch('builtins.input')
    # def test_example_integration_test(self, input_mock):
    #     keyword = 'soccer'
    #     advanced_option = 5
    #     advanced_response = 2009

    #     output = get_print(input_mock, [keyword, advanced_option, advanced_response])
    #     expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

    #     self.assertEqual(output, expected)

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
