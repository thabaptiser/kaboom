from n4j import Page, Word
from neomodel import db
import py2neo
import re
import urllib2
from flask import Flask, render_template, request
app = Flask(__name__)

search_home = """<!DOCTYPE html>
<html>
<body>

<input name="txtSearch" size="25" type="text" class="field" id="txtSearch" />
<button type="button" onclick='window.location.href="http://45.55.95.111/query/" + document.getElementById("txtSearch").value;'>
Submit
</button>

</body>
</html>

"""


@app.route('/')
def home():
  if request.args.get('search'):
    return search(request.args.get('search'))
  return render_template('index.html')

@app.route('/?search=<query>')
def search(query):
  query = query.lower()
  a = ''
  #for i in query.split():
  #  a += 'MATCH (p:Page)<-[:CONTAINS]-(Word {text:"' + i + '"})\n'
  #a+='\nRETURN p'
  cyph = ('MATCH (p:Page)<-[:CONTAINS]-(w:Word) '
         'WITH p, collect(w.text) as wKeys '
         'WHERE ALL (v IN {values} WHERE v IN wKeys) '
         'RETURN p')
  cyph = cyph.format(values = ['{i}'.format(i=i) for i in query.split()])
  print(cyph)
  query_results = db.cypher_query(cyph)
  link_list = []
  for i in query_results:
    for j in i[:1000]:
        print(type(j))
        try:
          link_list.append([j.p["link"], j.p["page_text"]])
        except AttributeError:
          pass
          #print(j.p["link"])
  return render_template('search.html', results=link_list)
  for i in link_list:
    ret += '<p>' + i[0] + '</p>\n<p>' + i[1][:50] + '...</p>'
  return ret
