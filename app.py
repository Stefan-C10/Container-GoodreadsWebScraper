# run pip freeze > requirements.txt in terminal to save requirements
from Book import Book
from Log import Log
from UserReadList import User
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
from flask import Flask, request
import jsonpickle

app = Flask(__name__)

@app.route('/user')
def get_user_read_books():
    try:
        urlOfUserReadBooks = request.args.get('profile')
    except:
        return "Please check your input parameters in the URL. Should be profile={Goodreads user read list URL link}"
    if("?shelf=read" not in urlOfUserReadBooks):
        urlOfUserReadBooks += "?shelf=read"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background
    with Chrome(ChromeDriverManager().install(), options=chrome_options) as browser:
        userReadShelf = User()
        userReadShelf.populateUserRatings(urlOfUserReadBooks, browser)

    json_string = "["
    for rating in userReadShelf.ratings:
        dictionary = rating.dictionaryForJson()
        json_string += jsonpickle.encode(dictionary) + ","
    json_string += "]"
    return json_string

@app.route('/book')
def get_book_recommendations():
    #Request parameters
    try:
        urlOfBook = request.args.get('url')
        depth = request.args.get('depth')
    except:
        return "Please check your input parameters in the URL. Should be an url={value}&depth={number}"
    #Variable setup
    visitedLinks = set()
    index = 0
    log = Log()
    List = []
    #Browser setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background
    with Chrome(ChromeDriverManager().install(), options=chrome_options) as browser:
        root = Book(urlOfBook, 0, log,  browser)
        List.append(root)
        ToVisit = root.RecommendedLinks
        while (index < int(depth)):
            NewList = []
            for enum, i in enumerate(ToVisit):
                if not i in visitedLinks:
                    try:
                        log = Log()
                        new = Book(i, index, log, browser)
                        List.append(new)
                        visitedLinks.add(i)
                        NewList.extend(new.RecommendedLinks)
                    except:
                        e = sys.exc_info()[0]
            index += 1
            ToVisit = NewList
    json_string="["
    for book in List:
        dictionary = book.dictionaryForJson()
        dictionary["log"] = book.getLog()
        json_string += jsonpickle.encode(dictionary)+","
    json_string += "]"
    return json_string

#FOR DEBUGGING PURPOSES
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(port=5000)