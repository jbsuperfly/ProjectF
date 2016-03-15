from flask import Flask, render_template, request, redirect, session
from bs4 import BeautifulSoup
from datetime import datetime
import urlparse
import urllib2 #allows for urlopen function
import requests
import pprint #prints nicely
import random #allows for random time interval
import time #allows for time interval
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
    return render_template('index.html')
@app.route('/through_the_tubes', methods = ['POST'])
def search_url():
    errors = []
    if not request.form['url']:
        errors.append('You need a URL for this to work')
        return render_template('index.html', errors=errors)
    else:
        url = request.form['url'] #url you want to scrape/crawl through
        try:
            urllib2.urlopen(url)
        except:
            print 'ERROR: '+url+' does not exist'
        else:
            source_code = requests.get(url) # gets the code for the page. allowing the crawler to crawl through
            plain_text = source_code.text # turns code into text
            soup = BeautifulSoup(plain_text) #generates the text
            soup = str(soup)
            #converts object to a string
            # print (soup)
            tags = []
            idx = 0
            i = 0
            line = ""
            while i < len(soup):
                if soup[i] == '\n':
                    line+=soup[i]
                    tags.insert(idx, line)
                    line = ""
                    idx+=1
                    i+=1
                elif soup[i] == ' ':
                    i+=1
                else:
                    line+=soup[i]
                    i+=1
            # print (soup)
            return render_template('success.html', tags=tags, url=url)
@app.route('/deeper_through_the_tubes', methods = ['POST'])
def search_deeper():
    errors = []
    if not request.form['search']:
        errors.append('You have to give me something to search for')
        return render_template('index.html', errors=errors)
    else:
        url = request.form['url'] #url you want to scrape/crawl through
        search = request.form['search']#what you search for
        source_code = requests.get(url) # gets the code for the page. allowing the crawler to crawl through
        plain_text = source_code.text # turns code into text
        soup = BeautifulSoup(plain_text) #generates the text
        soup = str(soup)
        tags = []
        idx = 0
        i = 0
        line = ""
        while i < len(soup):
            if soup[i] == '\n':
                line+=soup[i]
                if line.find(search) != -1:
                    tags.insert(idx, line)
                    line = ""
                    idx+=1
                    i+=1
                else:
                    line = ""
                    i+=1
            elif soup[i] == ' ':
                i+=1
            else:
                line+=soup[i]
                i+=1
        if len(tags) < 1:
            tags.insert(idx, 'Your Search Has Returned Nothing')
        # print (soup)
        return render_template('success.html', tags=tags, url=url)
@app.route('/matrix', methods = ['POST'])
def search_deepest():
    url = request.form['url'] #url you want to scrape/crawl through
    source_code = requests.get(url) # gets the code for the page. allowing the crawler to crawl through
    plain_text = source_code.text # turns code into text
    soup = BeautifulSoup(plain_text) #generates the text
    soup = str(soup)
    return render_template('matrix.html', soup=soup, url=url)
app.run(debug=True)
