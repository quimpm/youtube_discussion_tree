import nltk
from nltk.corpus import stopwords
import re

def similarity_in_imporant_words():
    pass

def get_maximum_per_comment(all_comments):
    pass

def clean_text(replie, candidates):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    stop_words = stopwords.words('english')
    new_candidates = []
    new_replie = (replie.id, [word for word in tokenizer.tokenize(replie.text) if word not in stop_words])
    for candidate in candidates:
        new_candidates.append((candidate.id, [word for word in tokenizer.tokenize(candidate.text) if word not in stop_words]))
    return new_replie, new_candidates 

def tf_idf(replie, candidates):
    probability_distribution = []
    replie, candidates = clean_text(replie, candidates)
    print(replie, candidates)
    maximum_per_comment = get_maximum_per_comment(candidates.append(replie))
    for candidate in candidates:
        probability_distribution += (candidate, similarity_in_imporant_words(replie, candidate))


