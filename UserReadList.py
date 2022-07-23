from bs4 import BeautifulSoup#, SoupStrainer

class UserBookRating():
    def __init__(self,bookUrl,title,rating):
        if("goodreads" in bookUrl):
            self.bookUrl = bookUrl
        else:
            self.bookUrl = "http://goodreads.com"+bookUrl
        self.rating = rating
        self.title = title

    def dictionaryForJson(self):
        return {
            "BookUrl": self.bookUrl,
            "Rating": self.rating,
            "Title": self.title
        }


class User():
    def __init__(self):
        self.name=''
        self.userId=''
        self.ratings = []



    def populateUserRatings(self,urlOfReadShelf,browser):
        browser.get(urlOfReadShelf)
        html = browser.page_source

        #Strain HTML page to increase speed
        #strainer = SoupStrainer('table', attrs={'id': 'books'})

        readBooksSoup = BeautifulSoup(html, 'lxml')
        #Get pages of user reviews
        reviewPagesEntries = readBooksSoup.find("div", {"id": "reviewPagination"})
        pagesNumberElements = reviewPagesEntries.find_all('a')
        pagesNumber=[element.get_text() for element in pagesNumberElements]
        finalPageWithURL={}
        finalPageWithURL["finalPage"] = pagesNumber[-2]
        finalPageWithURL["finalURL"] = pagesNumberElements[-2]["href"]

        for index in range(2, int(finalPageWithURL["finalPage"])):
            try:
                print("Page"+str(index)+"of"+finalPageWithURL["finalPage"])
                readBooksTableEntries = readBooksSoup.find_all("tr", {"class": "bookalike review"})
                for bookEntry in readBooksTableEntries:
                    bookTitle = bookEntry.find("td", {"class": "field title"}).find('a')['title']
                    bookUrl = bookEntry.find("td", {"class": "field title"}).find('a')['href']
                    bookRating = len(bookEntry.find("td", {"class": "field rating"}).find_all("span",{"class" : "staticStar p10" }))
                    ratedBook = UserBookRating(bookUrl,bookTitle,bookRating)
                    self.ratings.append(ratedBook)
                newURL = "http://goodreads.com"+str(finalPageWithURL["finalURL"]).replace("page="+finalPageWithURL["finalPage"],"page="+str(index))
                browser.get(newURL)
                html = browser.page_source
                readBooksSoup = BeautifulSoup(html, 'lxml')
            except:
                continue
