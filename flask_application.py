from flask import Flask,jsonify,request
import cloudscraper
from bs4 import BeautifulSoup
import requests
import re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def get_url(url):
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url)
    if (scraper.get(url).status_code < 400):
        return resp.text
    else:
        print('Server refused to connect')

def get_featured(course):
    links =[]
    urls = "https://hackr.io/tutorials/learn-"+course
    contents = get_url(urls)
    soup = BeautifulSoup(contents, "lxml")
    feat = soup.find('span',{'id', 'tutorial-title-txt'}).get_text()
    for link in soup.findAll('a', {'id','js-tutorial-title marginright-sm'}):
        if link.get('href').startswith("/"):
            links.append(link.get('href'))
            continue
        links.append(link.get('href'))
    return {feat :links[0]}
def create_dict(courses,links):
    res = {} 
    for key in courses: 
        for value in links: 
            res[key] = value
            links.remove(value) 
            break  
    return res

def get_paid3(title):
    links = []
    URL = "https://hackr.io/tutorials/learn-"+title+"?sort=upvotes&type_tags%5B%5D=2&languages%5B%5D=en"
    courses = []
    top=[]
    soup = BeautifulSoup(get_url(URL),"lxml")
    for link in soup.findAll("a", {'id','js-tutorial-title marginright-sm'}):
        if link.get('href').startswith("/"):
            links.append(link.get('href'))
            continue
        links.append(link.get('href'))
    top=soup.find_all('span',{'id', 'tutorial-title-txt'})
    for i in range(0,3):
        clean = remove_tags(str(top[i]))
        courses.append(clean)
    return create_dict(courses,links)
    
def get_free3(title):
    links = []
    URL = "https://hackr.io/tutorials/learn-"+title+"?sort=upvotes&type_tags%5B%5D=1&languages%5B%5D=en"
    courses = []
    top=[]
    soup = BeautifulSoup(get_url(URL),"lxml")
    for link in soup.findAll("a", {'id','js-tutorial-title marginright-sm'}):
        if link.get('href').startswith("/"):
            links.append(link.get('href'))
            continue
        links.append(link.get('href'))
    top=soup.find_all('span',{'id', 'tutorial-title-txt'})
    for i in range(0,3):
        clean = remove_tags(str(top[i]))
        courses.append(clean)
    return create_dict(courses,links)
    
def get_list():
    names = []
    links = []
    URL = "https://hackr.io"
    soup = BeautifulSoup(get_url(URL),"lxml")
    for link in soup.findAll('a',{'id','topic-grid-item js-topic-grid-item'}):
        if link.get('href').startswith("/"):
            links.append(link.get('href'))
            continue
        links.append(link.get('href'))
    for i in range(len(links)):
        a = links[i]
        names.append(a[33:])
    return names

def Merge(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res 

app = Flask(__name__)
a = get_list()
languages = []
for i in range(len(a)):
    languages.append({'name': a[i]})

@app.route('/', methods=['GET'])
def lists():
    return jsonify({'programs': languages})
@app.route('/<string:name>', methods=['GET'])
def test(name):
    if request.method == 'GET':
        feat = get_featured(name)
        paid = get_paid3(name)
        free = get_free3(name)
        return jsonify({'program': {name : {'featured': feat,'paid_top3' : paid,'free_top3': free}}})

if __name__ == '__main__':
    app.run(debug=True)