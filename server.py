from flask import Flask, render_template, request, redirect, session
from bs4 import BeautifulSoup
import urlparse
import urllib2 #allows for urlopen function
import requests
import pprint #prints nicely if needed
import random #allows for random time interval later
import time #allows for time interval later
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
app = Flask(__name__)
app.secret_key = 'fig'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods = ['POST'])
def home():
    return redirect('/')

@app.route('/through_the_tubes', methods = ['POST'])
def search_url():
    errors = []
    if not request.form['url']:
        errors.append('You need a URL for this to work')
        return render_template('index.html', errors=errors)
    else:
        url = request.form['url'] #url you want to scrape/crawl through
        soup = getsoup(url)
        #converts object to a string
        tags = soup.split('\n')
        return render_template('success.html', tags=tags, url=url)

@app.route('/deeper_through_the_tubes', methods = ['POST'])
def search_deeper():
    tags = []
    url = request.form['url'] #url you want to scrape/crawl through
    search = request.form['search']#what you search for
    if not request.form['search']:
        tags.append('You have to give me something to search for')
        return render_template('success.html', tags=tags, url=url)
    else:
        soup = getsoup(url)
        code = soup.split('\n')
        idx = 0
        i = 0
        while i < len(code):
            if code[i].find(search) != -1:
                tags.insert(idx, code[i])
                idx+=1
                i+=1
            else:
                i+=1
        if len(tags) < 1:
            tags.insert(idx, 'Your Search Has Returned Nothing')
        # print (soup)
        return render_template('success.html', tags=tags, url=url)

@app.route('/matrix', methods = ['POST'])
def search_deepest():
    url = request.form['url'] #url you want to scrape/crawl through
    soup = getsoup(url)
    return render_template('matrix.html', soup=soup, url=url)

def getsoup(url):
    source_code = requests.get(url) # gets the code for the page. allowing the crawler to crawl through
    plain_text = source_code.text # turns code into text
    soup = str(BeautifulSoup(plain_text, 'html.parser')) #generates the text
    # soup = str(soup)
    return (soup)

app.run(debug=True)
