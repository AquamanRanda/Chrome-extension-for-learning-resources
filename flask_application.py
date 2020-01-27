from flask import Flask,jsonify,request
import cloudscraper
from bs4 import BeautifulSoup
import requests
import re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def get(URL):
    """
    returns the website data html content
    """
    return requests.get(url=URL).content


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
    contents = get(urls)
    soup = BeautifulSoup(contents, "lxml")
    feat = soup.find('span',{'id', 'tutorial-title-txt'}).get_text()
    for link in soup.findAll('a', {'id','js-tutorial-title marginright-sm'}):
        if link.get('href').startswith("/"):
            links.append(link.get('href'))
            continue
        links.append(link.get('href'))
    return {feat :links[0]}


def get_paid3(title):
    links = []
    URL = "https://hackr.io/tutorials/learn-"+title+"?sort=upvotes&type_tags%5B%5D=2&languages%5B%5D=en"
    courses = []
    top=[]
    soup = BeautifulSoup(get(URL),"lxml")
    for link in soup.findAll("a", {'id','js-tutorial-title marginright-sm'}):
        if link.get('href').startswith("/"):
            links.append(link.get('href'))
            continue
        links.append(link.get('href'))
    top=soup.find_all('span',{'id', 'tutorial-title-txt'})
    for i in range(0,3):
        clean = remove_tags(str(top[i]))
        courses.append(clean)
    res = {} 
    for key in courses: 
        for value in links: 
            res[key] = value
            links.remove(value) 
            break  
    return res
    
def get_free3(title):
    links = []
    URL = "https://hackr.io/tutorials/learn-"+title+"?sort=upvotes&type_tags%5B%5D=1&languages%5B%5D=en"
    courses = []
    top=[]
    soup = BeautifulSoup(get(URL),"lxml")
    for link in soup.findAll("a", {'id','js-tutorial-title marginright-sm'}):
        if link.get('href').startswith("/"):
            links.append(link.get('href'))
            continue
        links.append(link.get('href'))
    top=soup.find_all('span',{'id', 'tutorial-title-txt'})
    for i in range(0,3):
        clean = remove_tags(str(top[i]))
        courses.append(clean)
    res = {} 
    for key in courses: 
        for value in links: 
            res[key] = value
            links.remove(value) 
            break  
    return res

'''if __name__ == '__main__':
    titl = input("Enter the course: ")
    title = titl.replace(" ","-")
    Main_URL = "https://hackr.io/tutorials/learn-"+title
    course = input("Free/Paid ?")
    if(course == 1):
        URL = "https://hackr.io/tutorials/learn-"+title+"?sort=upvotes&type_tags%5B%5D=1&languages%5B%5D=en"
    else:
        URL = "https://hackr.io/tutorials/learn-"+title+"?sort=upvotes&type_tags%5B%5D=2&languages%5B%5D=en"
    url = get_url(URL)
    content = get(URL)
    get_featured(title)
    get_top3(url,content)'''
def Merge(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res 

app = Flask(__name__)

#languages = [{'name' : 'python'} , {'name' : 'javascript'}, {'name' : 'android-development'}, {'name' : 'java'} , {'name' : 'data-structures-algorithms'} , {'name': 'c-plus-plus'}, {'name': 'react'} , {'name': 'angular'} ,{'name': 'html-5'},{'name':'css'} ,{'name':'c'},{'name':'git'},{'name':'bootstrap'} ,{'name': 'c-sharp'} ,{'name': 'information-security-ethical-hacking'} , {'name': 'blockchain-programming'} ,{'name': 'django'}, {'name': 'mysql'},{'name': 'sql'} , {'name': 'arduino'}, {'name': 'unity'}, {'name' : 'react-native'} , {'name': 'jquery'} , {'name' :'intro-to-programming'}, {'name':'vue-js'},{'name': 'bitcoin'} , {'name': 'go'}, {'name' :'flutter'}, {'name' :'ios-swift'}, {'name' :'asp-net'} ,{'name' :'kotlin'} , {'name': 'typescript'}]

@app.route('/', methods=['GET'])
def test():
    if request.method == 'GET':
        course = input("Enter a course: ")
        feat = get_featured(course)
        paid = get_paid3(course)
        free = get_free3(course)
        return jsonify({'program': {course : {'featured': feat,'paid_top3' : paid,'free_top3': free}}})

if __name__ == '__main__':
    app.run(debug=True, port=8080)