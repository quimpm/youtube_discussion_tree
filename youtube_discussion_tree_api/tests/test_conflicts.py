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

    def test_cosine_sim(self):
        v1 = [1/11 * np.log(3/2),1/11 * np.log(3/2),1/11 * np.log(3/2),1/11 * np.log(3/3),1/11 * np.log(3/2),1/11 * np.log(3/2),1/11 * np.log(3/2),1/11 * np.log(3/2),1/11 * np.log(3/2),1/11 * np.log(3/2),1/11 * np.log(3/2)]
        v2 = [0,0,0,0,1,1,1,1,1,0,0]
        self.assertEqual(np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)), _cosine_sim(v1,v2))

    def test_gen_vector(self):
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
        expected = np.zeros(len(df.keys()))
        expected[1]= 1/11 * np.log(4/2)
        expected[2]= 1/11 * np.log(4/2)
        expected[10] = 1/11 * np.log(4/2)
        self.assertEqual(
            expected.all(),_gen_vector(['hey', 'dude', 'also', 'love', 'turtl', 'cute', 'slow'], list(df.keys()), df , 3).all()
            ) 

    def test_cosine_similarity(self):
        reply = Node(
                id = "comment1",
                author_name = "Quim10^-12",
                author_id = "author1",
                text = "Hey dude! I also love turtle, they are so cute and slow.",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            )
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
        D = [[1,1,1,1,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,1,0,0],
            [0,0,0,1,0,0,0,0,0,1,1]]
        cosines = _cosine_similarity(   reply
                                        , D
                                        , list(df.keys())
                                        , df,
                                        3)
        v = [0, 1/7 * np.log(4/2), 1/7 * np.log(4/2), 0, 0, 0, 0, 0, 0, 0, 1/7 * np.log(4/2)]
        self.assertEqual([
            (1,np.dot(v, D[0])/(np.linalg.norm(v)*np.linalg.norm(D[0]))),
            (0,np.dot(v, D[1])/(np.linalg.norm(v)*np.linalg.norm(D[1]))),
            (0,np.dot(v, D[2])/(np.linalg.norm(v)*np.linalg.norm(D[2])))
        ],cosines)
        
        
    def test_tf_idf_algorithm(self):
        reply = Node(
                id = "comment1",
                author_name = "Quim10^-12",
                author_id = "author1",
                text = "Hey dude! I also love turtle, they are so cute and slow.",
                like_count = 10000000,
                parent_id = None,
                published_at = "12-12-2012"
            )
        self.assertEqual("comment1", _tf_idf_automatic_algorithm(reply, self.candidates))