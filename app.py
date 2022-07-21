# run pip freeze > requirements.txt in terminal to save requirements
from Book import Book
from Log import Log
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
from flask import Flask, request
import jsonpickle

app = Flask(__name__)

@app.route('/book')
def get_book_recommendations():
    #Request parameters
    urlOfBook = request.args.get('url')
    depth = request.args.get('depth')
    print(urlOfBook)
    print(depth)
    #Variable setup
    CollectionRead = []
    CollectionToRead = []
    VisitedLinks = set()
    index = 0
    log = Log()
    #Browser setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background
    with Chrome(ChromeDriverManager().install(), options=chrome_options) as browser:
        root = Book(urlOfBook, 0, log,  browser)
        List = []
        List.append(root)
        ToVisit = root.RecommendedLinks
        while (index < int(depth)):
            NewList = []
            for enum, i in enumerate(ToVisit):
                if not i in VisitedLinks:
                    #print("At depth " + str(index + 1) + " current Book " + str(enum) + " of " + str(len(ToVisit)) + "URL:"+i)
                    try:
                        new = Book(i, index, log, browser)
                        message = "At depth " + str(index + 1) + " current Book is " + str(
                            new.Title) + " number " + str(enum + 1) + " of " + str(
                            len(ToVisit)) + ". Continuing to next Book...\n"
                        log.log(message)
                        List.append(new)
                        VisitedLinks.add(i)
                        NewList.extend(new.RecommendedLinks)
                    except:
                        e = sys.exc_info()[0]
                        message = "At depth " + str(index) + " Book number " + str(enum) + " of " + str(
                            len(ToVisit)) + " abandoned due to problems with HTML. Error was " + str(e) + "\n"
                        log.log(message)
            index += 1
            ToVisit = NewList
    json_string=""
    for book in List:
        dictionary=book.dictionaryForJson()
        dictionary["log"]=log.getLog()
        json_string +=jsonpickle.encode(dictionary)
    return (json_string)

#if __name__ == '__main__':
    # run app in debug mode on port 5000
#    app.run(port=5000)