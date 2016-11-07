import process_corpus as pc
import sys
from sklearn.metrics import pairwise

import tokenizer
from nltk import Tree

# TODO: move these functions into more specific modules
def process_question(question, counter, tfidf):
  term_doc = counter.transform([question])
  norm_matrix = tfidf.transform(term_doc)
  tokens = tokenizer.tokenize_by_word(question)
  question_type = "" # [wh.lower() for wh in tokens if wh.lower() in ["where","when","what","why","how","who","did","is","are","does", "do"]][0]
  return norm_matrix,question_type

def answer_question(question, counter, tfidf, doc):
  norm_matrix,q_type = process_question(question, counter, tfidf)
  
  answers = pairwise.cosine_similarity(doc, norm_matrix)
  temp = []
  for i,vec in enumerate(answers):
    temp.append((i,vec[0]))
  answers = temp
  a = sorted(answers,key=lambda tup: tup[1], reverse=True)
  return a, q_type
def extract_answers(answers,question_type, orig_sentence_tokens):
  top_sentences = []
  top_ranks = []
  for i,(ind,rank) in enumerate(answers):
    top_sentences.append(orig_sentence_tokens[ind]) 
    top_ranks.append(rank)
    if i > 20:
      break
  # good_sentences = []
  # for sent in top_sentences:
  #   toks = tokenizer.tokenize_by_word(sent)
  #   if len(toks) > 4:
  #     good_sentences.append(sent)
  # if question_type == "how":
  #   ind, rank = answers[0]
  #   return orig_sentence_tokens[ind-1] + orig_sentence_tokens[ind]  
  return top_sentences,top_ranks

def answer(text, question):
  orig_sentence_tokens = pc.process_corpus(text=text, stem=False, lemmatize=False, stopword=False)
  sentence_tokens = pc.process_corpus(text=text, stem=True, lemmatize=True)
  matrix, tfidf, counter = pc.tfidf_matrix(sentence_tokens)

  answers, q_type = answer_question(question, counter, tfidf, matrix)
    
    
  best_answers, top_ranks = extract_answers(answers,q_type, orig_sentence_tokens)
  return best_answers[0],top_ranks[0]

  # parses = pc.parsed_sentences(orig_sentence_tokens)
# orig_sentence_tokens = pc.process_corpus(sys.argv[1], stem=False, lemmatize=False, stopword=False)
# sentence_tokens = pc.process_corpus(sys.argv[1], stem=False, lemmatize=True)
# matrix, tfidf, counter = pc.tfidf_matrix(sentence_tokens)
# parses = pc.parsed_sentences(orig_sentence_tokens)
# parses[1].pretty_print()
# print matrix
# try:
#   with open(sys.argv[2]) as f:
#     for question in f:
#       print "\n" + question + "\n"
#       answers, q_type = answer_question(question, counter, tfidf, matrix)
      
      
#       best_answer = extract_answers(answers,q_type)
#       print best_answer[0]
# except: 
#   while True:
#     question=raw_input("What's your question? \n")
#     answers, q_type = answer_question(question, counter, tfidf, matrix)
      
      
#     best_answer = extract_answers(answers,q_type)
#     for i in best_answer:
#       print i
#       break
        
    
    


