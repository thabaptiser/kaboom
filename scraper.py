from bs4 import BeautifulSoup
from threading import Thread
from n4j import Page, Word
import tokenizer
import process_corpus as pc
import re
import urllib2
import time
import string
wiki = "https://en.wikipedia.org/wiki/{page}"

def scrape_page(url):
  print("starting: " + url)
  try:
    Page.nodes.get(link=unicode(url, "utf-8"))
    return
  except Page.DoesNotExist:
    pass
  try:
    page = urllib2.urlopen(url)
  except:
    return
  soup = BeautifulSoup(page, "html.parser")
  data = []
  for p in soup.find_all('p'):
    while p.find('math'):
      p.find('math').replace_with('')
    #while p.find('a'):
    #  p.find('a').replace_with('')
    while p.find('annotation'):
      p.find('annotation').replace_with('')
    data.append(p.text)
  data = unicode(" ".join(data))
  try:
    new_page = Page.nodes.get(link=unicode(url, "utf-8"))
    if new_page.page_text == data:
      return
    else:
        new_page.delete()
  except Page.DoesNotExist:
    pass
  new_page = Page(link=unicode(url, "utf-8"), page_text=data).save()
  # data = re.sub('[^a-z\ \']+', " ", data)
  # data = [tokenizer.tokenize_by_word(t) for t in tokenizer.tokenize_by_sentence(data)]
  data = pc.process_corpus(text=data)
  temp = []
  for sent in data:
    for word in tokenizer.tokenize_by_word(sent):
      if word not in string.punctuation:
        temp.append(word)
  data = temp
  for i in set(data):
    i = i.lower()
    # if len(i) < 3:
    #   continue
    try:
      w = Word(text=i.decode('utf-8')).save()
    except:
      w = Word.nodes.get(text=i)
    new_page.contained_word.connect(w)
  print("finished: " + url)


print("opening file")
with open('./enwiki-latest-all-titles-in-ns0') as f:
  print("opened file")
  x = 0
  t = []
  for page in f:
    count = 0
    for c in page:
      if c.isdigit():
        count += 1
    if count > 0:
       continue
    x+=1
    if x%10000==0:
      t.append(Thread(target=scrape_page, args=[wiki.format(page=page),]))
      t[-1].start()
    if len(t) > 10:
       done = False
       while not done:
         time.sleep(0.1)
         for i in t:
           if not i.isAlive():
             done=True
             t.remove(i)
             break
