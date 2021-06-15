from youtube_discussion_tree_api._conflicts import _tf_idf_automatic_algorithm, _calculate_document_frequency, _calculate_tf_idf, _cosine_sim, _cosine_similarity, _gen_vector, _in_doc_freq, _preprocessing
from unittest import TestCase
from youtube_discussion_tree_api.utils import Node
import numpy as np


class TestConflistSolvingAlgorithm(TestCase):

    def setUp(self):
        self.candidates = [
            Node(
                id = "comment1",
                author_name = "Ororo",
                author_id = "author1",
                text = "Hello, I love turtles and dogs",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            ),
            Node(
                id = "comment2",
                author_name = "Horno Microondas",
                author_id = "author2",
                text = "Cats are the best animals in the whole world",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            ),
            Node(
                id = "comment3",
                author_name = "Kekino",
                author_id = "author3",
                text = "I'm more of a dogs person, they are so cute",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            )
        ]
        self.candidates_preprocessed = [["hello", "love", "turtl", "dog"]
                                        , ["cat", "best", "anim", "whole", "world"]
                                        , ["dog", "person", "cute"]]

    def test_preprocessing(self):
        self.assertEqual(self.candidates_preprocessed, _preprocessing(self.candidates))

    def test_calculate_document_frequency(self):
        expected = {
            "hello" : 1,
            "love" : 1,
            "turtl" : 1,
            "dog" : 2,
            "cat" : 1,
            "best" : 1,
            "anim" : 1,
            "whole" : 1,
            "world" : 1,
            "person" : 1,
            "cute" : 1
        }
        self.assertEqual(expected, _calculate_document_frequency(self.candidates_preprocessed))

    def test_in_doc_frequency(self):
        df = {
            "hello" : 1,
            "love" : 1,
            "turtl" : 1,
            "dog" : 2,
            "cat" : 1,
            "best" : 1,
            "anim" : 1,
            "whole" : 1,
            "world" : 1,
            "person" : 1,
            "cute" : 1
        }
        self.assertEqual(1, _in_doc_freq("love", df))
        self.assertEqual(2, _in_doc_freq("dog", df))
        self.assertEqual(0, _in_doc_freq("patata", df))

    def test_calculate_tf_idf(self):
        df = {
            "hello" : 1,
            "love" : 1,
            "turtl" : 1,
            "dog" : 2,
            "cat" : 1,
            "best" : 1,
            "anim" : 1,
            "whole" : 1,
            "world" : 1,
            "person" : 1,
            "cute" : 1
        }
        tf_idf = _calculate_tf_idf( self.candidates_preprocessed 
                                                ,df 
                                                ,len(self.candidates_preprocessed)
                                                ,len(df.keys()))
        self.assertDictEqual({
            (0, "hello") : (1/11 * np.log(3/2)),
            (0, "love") : (1/11 * np.log(3/2)),
            (0, "turtl") : (1/11 * np.log(3/2)),
            (0, "dog") : (1/11 * np.log(3/3)),
            (1, "cat") : (1/11 * np.log(3/2)),
            (1, "best") : (1/11 * np.log(3/2)),
            (1, "anim") : (1/11 * np.log(3/2)),
            (1, "whole") : (1/11 * np.log(3/2)),
            (1, "world") : (1/11 * np.log(3/2)),
            (2, "dog") : (1/11 * np.log(3/3)),
            (2, "person") : (1/11 * np.log(3/2)),
            (2, "cute") : (1/11 * np.log(3/2)),
        }, tf_idf)

    def test_cosine_similarity(self):
        pass

    def test_gen_vector(self):
        pass

    def test_cosine_sim(self):
        pass

    def test_tf_idf_algorithm(self):
        pass