from bs4 import BeautifulSoup
from threading import Thread
from n4j import Page, Word
import tokenizer
import process_corpus as pc
import re
import urllib
import time
import string
wiki = "https://en.wikipedia.org/wiki/{page}"

def scrape_page(url):
  print("starting: " + url)
  #try:
  #  Page.nodes.get(link=unicode(url, "utf-8"))
  #  return
  #except Page.DoesNotExist:
  #  pass
  try:
    page = urllib.request.urlopen(url)
  except:
    print("ERROR")
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
  data = str(" ".join(data))
  try:
    new_page = Page.nodes.get(link=str(url))
    if new_page.page_text == data:
        print("already parsed: " + url)
        return
    else:
        new_page.delete()
  except Page.DoesNotExist:
    pass
  new_page = Page(link=str(url), page_text=data).save()
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
      w = Word(text=str(i)).save()
    except:
      w = Word.nodes.get(text=str(i))
    new_page.contained_word.connect(w)
  print("finished: " + url)

prev_seen = []

def search(url):
  if url in prev_seen:
    return []
  prev_seen.append(url)
  ret =set([])
  page = urllib.request.urlopen(url)
  soup = BeautifulSoup(page, "html.parser")
  result = soup.find("div", {"class":"mw-category"})
  result_sub = soup.find("div", {"class":"CategoryTreeItem"}) 
  result_pages = soup.find("div", {"id":"mw-pages"}) 
  list_links = []
  if result: list_links += [a['href'] for a in result.find_all('a', href=True)]
  if result_sub: list_links += [a['href'] for a in result_sub.find_all('a', href=True)]
  if result_pages: list_links += [a['href'] for a in result_pages.find_all('a', href=True)]
  for l in list_links:
    if l[0:6] == "/wiki/":
      if "/wiki/Category:" in l:
        ret = ret.union(search("https://en.wikipedia.org" + l))
      else:
        print("found link: " + l)
        scrape_page("https://en.wikipedia.org" + l)
        ret.add(l)
  return ret

search("https://en.wikipedia.org/wiki/Category:Trees")
#  scrape_page(l)
