from bs4 import BeautifulSoup
from threading import Thread
from n4j import Page, Word
import tokenizer
import process_corpus as pc
import re
import urllib2
import time
wiki = "https://en.wikipedia.org/wiki/{page}"

def scrape_page(url):
  #print("starting: " + url)
  #try:
  #  Page.nodes.get(link=unicode(url, "utf-8"))
  #  return
  #except Page.DoesNotExist:
  #  pass
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
        print("already parsed: " + url)
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


#print("opening file")
#with open('./enwiki-latest-all-titles-in-ns0') as f:
#  print("opened file")
#  x = 0
#  t = []
#  for page in f:
#    count = 0
#    for c in page:
#      if c.isdigit():
#        count += 1
#    if count > 0:
#       continue
#    x+=1
#    if x<500000:
#        continue
#    if x%1000==1:
#      t.append(Thread(target=scrape_page, args=[wiki.format(page=page),]))
#      t[-1].start()
#    if len(t) > 50:
#       done = False
#       while not done:
#         time.sleep(0.1)
#         for i in t:
#           if not i.isAlive():
#             done=True
#             t.remove(i)
#             break
#orig_page = urllib2.urlopen("https://en.wikipedia.org/wiki/Category:Trees")
#result = soup.find("div", {"class":"mw-content-ltr"}).find_all('a', href=True)
#list_links = ['https://en.wikipedia.org/' + a['href'] for a in result]
#orig_page = urllib2.urlopen("https://en.wikipedia.org/wiki/Category:Trees")

prev_seen = []

def search(url):
  if url in prev_seen:
    return []
  prev_seen.append(url)
  ret =set([])
  page = urllib2.urlopen(url)
  soup = BeautifulSoup(page, "html.parser")
  result = soup.find("div", {"class":"mw-category"})
  result_sub = soup.find("div", {"class":"CategoryTreeItem"}) 
  result_pages = soup.find("div", {"id":"mw-pages"}) 
  list_links = []
  if result: list_links += [a['href'] for a in result.find_all('a', href=True)]
  if result_sub: list_links += [a['href'] for a in result_sub.find_all('a', href=True)]
  if result_pages: list_links += [a['href'] for a in result_pages.find_all('a', href=True)]
  if not list_links:
    print(url)
  for l in list_links:
    if l[0:6] == "/wiki/":
      if "/wiki/Category:" in l:
        ret = ret.union(search("https://en.wikipedia.org" + l))
      else:
        print("adding: " + l)
        ret.add(l)
  return ret

for l in search("https://en.wikipedia.org/wiki/Category:Trees"):
  scrape_page(l)
