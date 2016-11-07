import tokenizer as tk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords as StopWord
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
import spacy
from nltk import Tree

# takes in a filename and outputs a set of sentence tokens according to the params
# input: filename, params
# output: sentence tokens 
def process_corpus(filename="", text="", lemmatize=True, stem=True, stopword=True):
  if filename != "" :

    doc = tk.read_file(filename)

    doc = tk.read_formatted_file(filename)
    sentence_tokens = tk.tokenize_formatted_file(doc)
  else:
    doc = text
    sentence_tokens = tk.tokenize_by_sentence(doc)
  
  
  tokenized_sentences = map(tk.tokenize_by_word,sentence_tokens)
  if stem:
    stemmer = PorterStemmer()
    
    tokenized_sentences = map(lambda x: map(stemmer.stem,x), tokenized_sentences)
    
  if lemmatize:
    lemmatizer = WordNetLemmatizer()
    tokenized_sentences = map(lambda sent: map(lemmatizer.lemmatize,sent), tokenized_sentences)
    
  if stopword:
    tokenized_sentences = map(remove_stopwords, tokenized_sentences)

  sentence_tokens = map(lambda x: ' '.join(x), tokenized_sentences)
  return sentence_tokens

# input: single sentence word tokens
# output: stopwords removed
def remove_stopwords(tokens):
    stopwords=StopWord.words('english')
    new_tokens = []
    for tok in tokens:
        if not tok in stopwords:
            new_tokens.append(tok)
    return new_tokens
# input: sentence tokens 
# output: tfidf normalized matrix of the sentences, and the transformer 
def tfidf_matrix(tokens):
    counter = CountVectorizer()
    matrix = counter.fit_transform(tokens)
    tfidf = TfidfTransformer()
    normalized_matrix = tfidf.fit_transform(matrix)
    return normalized_matrix,tfidf, counter
def parsed_sentences(tokens):
  parser = spacy.en.English()
  s = map(parser,tokens)
  def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_
  a = [to_nltk_tree(sent.root) for doc in s for sent in doc.sents]
  return a

# sents = process_corpus("train-data/set1/a1.txt",stem=False)
# for each in sents:
#   print each
# matrix, _ , _= tfidf_matrix(sents)
# print type(matrix)
  

