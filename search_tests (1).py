from search import search, article_length, unique_authors, most_recent_article, favorite_author, title_and_author, refine_search, display_result
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        expected_search_soccer_results = [
            ['Spain national beach soccer team', 'jack johnson', 1233458894, 1526],
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],
            ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]
        ]
        self.assertEqual(search('soccer'), expected_search_soccer_results)

    def test_search_keyword(self):
        expected_search_CANADA_results = [
            ['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023], 
            ['Lights (musician)', 'Burna Boy', 1213914297, 5898], 
            ['Old-time music', 'Nihonjoe', 1124771619, 12755], 
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]
        ]
        self.assertEqual(search('CANADA'), expected_search_CANADA_results)

        expected_search_no_keyword_results = []
        self.assertEqual(search(''), expected_search_no_keyword_results)

        expected_search_CAN_results = [
            ['Noise (music)', 'jack johnson', 1194207604, 15641], 
            ['Rock music', 'Mack Johnson', 1258069053, 119498], 
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746], 
            ['Arabic music', 'RussBot', 1209417864, 25114], 
            ['C Sharp (programming language)', 'Burna Boy', 1232492672, 52364], 
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], 
            ['Time travel', 'Jack Johnson', 1140826049, 35170], 
            ['Python (programming language)', 'Burna Boy', 1137530195, 41571], 
            ['Endoglin', 'Bearcat', 1212259031, 6778], 
            ['Sun dog', 'Mr Jake', 1208969289, 18050], 
            ['Lua (programming language)', 'Burna Boy', 1113957128, 0], 
            ['Covariance and contravariance (computer science)', 'Bearcat', 1167547364, 7453], 
            ['Personal computer', 'Pegship', 1220391790, 45663], 
            ['Digital photography', 'Mr Jake', 1095727840, 18093], 
            ['Comparison of programming languages (basic instructions)', 'RussBot', 1238781354, 61644], 
            ['Ruby (programming language)', 'Bearcat', 1193928035, 30284], 
            ['Mode (computer interface)', 'Pegship', 1182732608, 2991], 
            ['Semaphore (programming)', 'Nihonjoe', 1144850850, 7616]
        ]
        self.assertEqual(search('CAN'), expected_search_CAN_results)


    def test_article_length(self):
        canada_metadata = [
            ['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023], 
            ['Lights (musician)', 'Burna Boy', 1213914297, 5898], 
            ['Old-time music', 'Nihonjoe', 1124771619, 12755], 
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]
        ]
        expected_5000_results = [
           ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]
        ]
        self.assertEqual(article_length(5000, canada_metadata), expected_5000_results)

        expected_0_results = []
        self.assertEqual(article_length(0, canada_metadata), expected_0_results)

        expected_20000_results = [
            ['Lights (musician)', 'Burna Boy', 1213914297, 5898], 
            ['Old-time music', 'Nihonjoe', 1124771619, 12755], 
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]
        ]
        self.assertEqual(article_length(20000, canada_metadata), expected_20000_results)


    def test_unique_authors(self):
        can_metadata = [
            ['Noise (music)', 'jack johnson', 1194207604, 15641], 
            ['Rock music', 'Mack Johnson', 1258069053, 119498], 
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746], 
            ['Arabic music', 'RussBot', 1209417864, 25114], 
            ['C Sharp (programming language)', 'Burna Boy', 1232492672, 52364], 
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], 
            ['Time travel', 'Jack Johnson', 1140826049, 35170], 
            ['Python (programming language)', 'Burna Boy', 1137530195, 41571], 
            ['Endoglin', 'Bearcat', 1212259031, 6778], 
            ['Sun dog', 'Mr Jake', 1208969289, 18050], 
            ['Lua (programming language)', 'Burna Boy', 1113957128, 0], 
            ['Covariance and contravariance (computer science)', 'Bearcat', 1167547364, 7453], 
            ['Personal computer', 'Pegship', 1220391790, 45663], 
            ['Digital photography', 'Mr Jake', 1095727840, 18093], 
            ['Comparison of programming languages (basic instructions)', 'RussBot', 1238781354, 61644], 
            ['Ruby (programming language)', 'Bearcat', 1193928035, 30284], 
            ['Mode (computer interface)', 'Pegship', 1182732608, 2991], 
            ['Semaphore (programming)', 'Nihonjoe', 1144850850, 7616]
        ]

        expected_20_results = [
            ['Noise (music)', 'jack johnson', 1194207604, 15641], 
            ['Rock music', 'Mack Johnson', 1258069053, 119498], 
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746], 
            ['Arabic music', 'RussBot', 1209417864, 25114], 
            ['C Sharp (programming language)', 'Burna Boy', 1232492672, 52364], 
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], 
            ['Endoglin', 'Bearcat', 1212259031, 6778], 
            ['Semaphore (programming)', 'Nihonjoe', 1144850850, 7616]
        ]
        expected_0_results = []
        expected_negative_results = []
        expected_7_results = [
            ['Noise (music)', 'jack johnson', 1194207604, 15641], 
            ['Rock music', 'Mack Johnson', 1258069053, 119498], 
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746], 
            ['Arabic music', 'RussBot', 1209417864, 25114], 
            ['C Sharp (programming language)', 'Burna Boy', 1232492672, 52364], 
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], 
            ['Endoglin', 'Bearcat', 1212259031, 6778]
        ]

        self.assertEqual(unique_authors(20, can_metadata), expected_20_results)
        self.assertEqual(unique_authors(0, can_metadata), expected_0_results)
        self.assertEqual(unique_authors(-5, can_metadata), expected_negative_results)
        self.assertEqual(unique_authors(7, can_metadata), expected_7_results)


    def test_most_recent_article(self):
        can_metadata = [
            ['Noise (music)', 'jack johnson', 1194207604, 15641], 
            ['Rock music', 'Mack Johnson', 1258069053, 119498], 
            ['Black dog (ghost)', 'Pegship', 1220471117, 14746], 
            ['Arabic music', 'RussBot', 1209417864, 25114], 
            ['C Sharp (programming language)', 'Burna Boy', 1232492672, 52364], 
            ['Dalmatian (dog)', 'Mr Jake', 1207793294, 26582], 
            ['Time travel', 'Jack Johnson', 1140826049, 35170], 
            ['Python (programming language)', 'Burna Boy', 1137530195, 41571], 
            ['Endoglin', 'Bearcat', 1212259031, 6778], 
            ['Sun dog', 'Mr Jake', 1208969289, 18050], 
            ['Lua (programming language)', 'Burna Boy', 1113957128, 0], 
            ['Covariance and contravariance (computer science)', 'Bearcat', 1167547364, 7453], 
            ['Personal computer', 'Pegship', 1220391790, 45663], 
            ['Digital photography', 'Mr Jake', 1095727840, 18093], 
            ['Comparison of programming languages (basic instructions)', 'RussBot', 1238781354, 61644], 
            ['Ruby (programming language)', 'Bearcat', 1193928035, 30284], 
            ['Mode (computer interface)', 'Pegship', 1182732608, 2991], 
            ['Semaphore (programming)', 'Nihonjoe', 1144850850, 7616]
        ]

        canada_metadata = [
            ['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023], 
            ['Lights (musician)', 'Burna Boy', 1213914297, 5898], 
            ['Old-time music', 'Nihonjoe', 1124771619, 12755], 
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]
        ]

        cherish_metadata = []

        self.assertEqual(most_recent_article(can_metadata), ['Rock music', 'Mack Johnson', 1258069053, 119498])
        self.assertEqual(most_recent_article(canada_metadata), ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562])
        self.assertEqual(most_recent_article(cherish_metadata), [])

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 3000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Spain national beach soccer team', 'jack johnson', 1233458894, 1526], ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]]\n"

        self.assertEqual(output, expected)

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
