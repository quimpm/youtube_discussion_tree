import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
import numpy as np
import math

def _calculate_document_frequency(comments):
    DF = {}
    for comment in comments:
        for word in comment:
            if word in DF:
                DF[word] += 1
            else:
                DF[word] = 1
    return DF

def _in_doc_freq(word, doc_freq):
    if word in doc_freq:
        return doc_freq[word]
    else:
        return 0

def _preprocessing(comments):
    new_comments = []
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    stemmer = PorterStemmer()
    stop_words = stopwords.words('english')
    for comment in comments:
        new_comments.append([stemmer.stem(word.lower()) for word in tokenizer.tokenize(comment.text) if word not in stop_words and len(word) != 1])
    return new_comments

def _calculate_tf_idf(candidates, doc_freq, N, word_count):
    tf_idf = {}
    for i,candidate in enumerate(candidates):
        counter = Counter(candidate)
        for token in np.unique(candidate):
            tf = counter[token]/word_count
            df = _in_doc_freq(token, doc_freq)
            idf = np.log(N/(df+1))
            tf_idf[i, token] = tf*idf
    return tf_idf

def _cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

def _gen_vector(tokens, total_vocab, doc_freq, N):
    Q = np.zeros((len(total_vocab)))
    counter = Counter(tokens)
    words_count = len(tokens)
    for token in np.unique(tokens):
        tf = counter[token]/words_count
        df = _in_doc_freq(token, doc_freq)
        idf = math.log((N+1)/(df+1))
        try:
            ind = total_vocab.index(token)
            Q[ind] = tf*idf
        except:
            pass
    return Q

def _cosine_similarity(query, D, total_vocab, doc_freq, N):
    tokens = _preprocessing([query])[0]
    d_cosines = []
    query_vector = _gen_vector(tokens, total_vocab, doc_freq, N)
    for d in D:
        d_cosines.append((d[0], _cosine_sim(query_vector, d)))
    return d_cosines

def _tf_idf_automatic_algorithm(reply, candidates):
    clean_candidates = _preprocessing(candidates)
    doc_freq = _calculate_document_frequency(clean_candidates)
    total_vocab = [x for x in doc_freq.keys()]
    word_count = len(total_vocab)
    N = len(clean_candidates)
    tf_idf = _calculate_tf_idf(clean_candidates, doc_freq, N, word_count)
    D = np.zeros((N, word_count))
    for i in tf_idf:
        ind = total_vocab.index(i[1])
        D[i[0]][ind] = tf_idf[i]
    similarities = _cosine_similarity(reply, D, total_vocab, doc_freq, N)
    return candidates[similarities.index(max(similarities))].id