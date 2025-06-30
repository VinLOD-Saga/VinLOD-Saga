from nltk.corpus import stopwords
from nltk.text import Text
from nltk import word_tokenize, ngrams, BigramAssocMeasures, BigramCollocationFinder, collocations

from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

import spacy
import string
import numpy as np

# * Before starting, nltk.download(), run this in order to download it properly
# * same here pip install scikit-learn
# * pip install spacy
# * python -m spacy download en_core_web_sm
# * pip install eng-spacysentiment
# * pip install vaderSentiment good for small corpora, had problems with spacy


class TextAnalyzer:
    def __init__(self, file):
        self.file = file
        self.text = ""
        self.words = []
        self.clean_text = []
    
    def load_and_tokenize(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            self.text = f.read().lower()
        self.words = word_tokenize(self.text)
        stop_words = set(stopwords.words('english'))
        excluded_punctuation = set(string.punctuation)
        self.clean_text = [w for w in self.words if w not in excluded_punctuation and w not in stop_words]
        print(f"Loaded and cleaned text. Total tokens: {len(self.clean_text)}")
    
    def word_frequency(self, top_n=20):
        freq = Counter(self.clean_text).most_common(top_n)
        print(f"Top {top_n} most common words:")
        for word, count in freq:
            print(f"{word}: {count}")
        return freq

    def extract_ngrams(self, n=2, top_n=20):
        n_grams = ngrams(self.clean_text, n)
        most_common = Counter(n_grams).most_common(top_n)
        print(f"Top {top_n} most common {n}-grams:")
        for gram, count in most_common:
            print(f"{gram}: {count}")
        return most_common

    def find_collocations(self, freq_filter=2):
        print("Collocations using PMI and chi-squared scores:")
        bigrams = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(self.clean_text)
        finder.apply_freq_filter(freq_filter)

        print("\nChi-squared:")
        scored_chi = finder.score_ngrams(bigrams.chi_sq)
        for bigram, score in scored_chi[:20]:
            print(bigram, score)

        print("\nPMI:")
        scored_pmi = finder.score_ngrams(bigrams.pmi)
        for bigram, score in scored_pmi[:20]:
            print(bigram, score)
        
        return scored_chi, scored_pmi

    def show_concordance(self, word, width=40, lines=20):
        tokens_text = Text(self.clean_text)
        print(f"Concordance for '{word}':")
        tokens_text.concordance(word, width=width, lines=lines)
    
    def tf_idf(self, max_features=500, top_n=10):
        # Join tokens into single string as single document
        document = ' '.join(self.clean_text)

        # Create vectorizer: sublinear_tf optional, max_features limits features
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_features=max_features, tokenizer=word_tokenize)

        tfidf_matrix = vectorizer.fit_transform([document])  # single document
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]

        # Get top_n terms with highest TF-IDF
        top_indices = np.argsort(scores)[::-1][:top_n]
        top_terms = [(feature_names[i], scores[i]) for i in top_indices]

        print(f"Top {top_n} terms by TF-IDF:")
        for term, score in top_terms:
            print(f"{term}: {score:.4f}")

        return top_terms
    

    def _nlp_(self):
        nlp=spacy.load('en_core_web_sm')
        doc= nlp(' '.join(self.clean_text)) # it expects a string 
        result=[(X.text, X.label_) for X in doc.ents]
        print(result)
    
    def sentiment_analysis(self):
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(self.clean_text)
        print(scores)



# --- USE ---
# put your file here
analyzer = TextAnalyzer(file=None) # pass the file path

# Methods
analyzer.load_and_tokenize()
# analyzer.word_frequency()
# analyzer.extract_ngrams(n=2) # pass a n-gram
# analyzer.find_collocations()
# analyzer.show_concordance('Othin') # pass a word
# analyzer.tf_idf() 
# analyzer._nlp_()
# analyzer.sentiment_analysis()


