from elasticsearch import Elasticsearch
import ast
import nltk
import string
import sys

# specific json text parsing for this data-set. Must re-implement for other data sets
# Returns a list of review text
def pull_data(query_size=50):
    es = Elasticsearch(['localhost:9200'], http_auth=('elastic','changeme'))
    train_set = []
    test_set = []
    for i in range(1,6):
            res = es.search(index='yelp', q='stars:'+str(i),size=query_size)
            for j in range(0,query_size/2):
                try:
                    train_set.append((res['hits']['hits'][j]['_source']['text'],res['hits']['hits'][j]['_source']['stars']))
                except Exception as e:
                    pass
            for j in range(query_size/2,query_size):
                try:
                    test_set.append((res['hits']['hits'][j]['_source']['text'],res['hits']['hits'][j]['_source']['stars']))
                except Exception as e:
                    pass
    return train_set, test_set



# Returns a dictionary of the word features of a string
def word_feats(words, n=1):
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(words.lower())
    word_copy = []
    if n > 1:
        for i in range(0, len(words) - n + 1):
            for j in range(1, n):
                words[i] = words[i] + " " + words[i+j]
            word_copy.append(words[i])
        return dict([(word, True) for word in word_copy])
    return dict([(word, True) for word in words])

# argv[1] = number of reviews to pull from db
# argv[2] = top n most informative features
# argv[3] = n for n-gram (optional, default to unigram if omitted)
if __name__ == "__main__":
    train_set, test_set = pull_data(int(sys.argv[1]))
    n_gram = 1
    if len(sys.argv) > 3:
        n_gram = int(sys.argv[3])
    train_set = [(word_feats(review, n_gram), stars) for (review, stars) in train_set]
    test_set = [(word_feats(review, n_gram), stars) for (review, stars) in test_set]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, test_set)
    classifier.labels()
    classifier.show_most_informative_features(int(sys.argv[2]))
