import nltk

"""
read_file: string -> string

read_file takes in a string containing a path to a file and returns the
contents of the file in a string
"""
def read_file(filename):
	f = open(filename, 'r')
	contents = f.read().decode("utf8").strip()
	f.close()
	return contents

# idk how to make this clean rn
def read_formatted_file(filename):
  sentences = []
  with open(filename, 'r') as f:
    sentences = f.read().decode("utf8").strip().split("\n")
  return sentences
def tokenize_formatted_file(lines):
  sentence_tokens = []
  for line in lines:
    sentence_tokens.extend(tokenize_by_sentence(line))
  return sentence_tokens

"""
tokenize_by_word: string -> string list

tokenize_by_word takes in a string containing a sentence, tokenizes the
sentence by word, and returns a list of the tokens.
"""
def tokenize_by_word(sentence):
	return nltk.word_tokenize(sentence)

"""
tokenize_by_sentence: string -> string list

tokenize_by_sentence takes in a string containing English text (e.g. the text
from an article), tokenizes the text by sentence, and returns a list of the
tokens.
"""
def tokenize_by_sentence(article):
	sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	return sentence_tokenizer.tokenize(article)

# uncomment for test
#print '\n-----\n'.join(tokenize_by_sentence(read_file("train-data/set1/a1.txt")))
