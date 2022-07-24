from sphinx.util import requests
from bs4 import BeautifulSoup#, SoupStrainer
import sys
import re

def cleanText(text):
    text = text.replace('\n', '')
    text = text.strip()
    return text

class Book():
    def __init__(self, url, depth, log, browser):
        self.log = log
        self.URL = ""
        self.Title = ""
        self.Series = ""
        self.NoInSeries = 0.0
        self.Author = []
        self.Rating = 0.0
        self.NoRaters = 0
        self.NoReviewers = 0
        self.Synopsys = ""
        self.Depth = 0
        self.RecommendedLinks = []
        self.BookID = ""
        self.Status = "Unread"
        self.Genres = []
        self.URL = url

        browser.get(url)
        html = browser.page_source

        page = requests.get(url)

        if url.find("-") > url.rfind("."):
            self.BookID = url[url.rfind("/") + 1:url.find("-")]
        else:
            self.BookID = url[url.rfind("/") + 1:url.rfind(".")]
        #{
        # This could speed up the process if it can be done correctly
        # strainer = SoupStrainer('div', attrs={'class': 'mainContentFloat '})
        #}

        self.soup = BeautifulSoup(html, 'lxml')
        self.populate_all_Book_fields()

    def __iter__(self):
        return iter(
            [self.URL, self.BookID, self.Depth, self.Title, self.NoInSeries, self.Series, self.Author, self.Status,
             self.Rating, self.NoRaters, self.NoReviewers, self.Genres, self.Synopsys])
    def getLog(self):
        return self.log.getLog()
    def dictionaryForJson(self):
        return {
            "URL": self.URL,
            "BookId": self.BookID,
            "Title": self.Title,
            "Number in Series": self.NoInSeries,
            "Series": self.Series,
            "Authors": self.Author,
            "Rating": self.Rating,
            "Number of Raters": self.NoRaters,
            "Number of Reviewers": self.NoReviewers,
            "Genres": self.Genres,
            "Synopsis": self.Synopsys
        }
    def __eq__(self, other):
        return self.BookID == other.BookID \
               and self.Title == other.Title

    def __hash__(self):
        return hash(('BookID', self.BookID,
                     'title', self.Title))

    def find_recommended(self):
        results = self.soup.find_all("li", {"class": "cover"})
        for li in results:
            self.RecommendedLinks.extend([str(li.find('a')['href'])])

    def populate_all_Book_fields(self):
        # Get Book title
        try:
            divTitle = self.soup.find("div", {"id": "metacol"})
            self.Title = cleanText(divTitle.find("h1", {"id": "bookTitle"}).get_text())
        except:
            e = sys.exc_info()[0]
            self.log.log("Title could not be read. Error:" + str(e) + "\n")
        # Get Book series
        try:
            FullSeries = cleanText(divTitle.find("h2", {"id": "bookSeries"}).get_text())
            index = FullSeries.find('#')
            self.Series = FullSeries[1:index - 1]
            self.NoInSeries = FullSeries[index:len(FullSeries) - 1]
        except:
            e = sys.exc_info()[0]
            self.log.log("BookSeries could not be read for Book " + self.Title + ". Error:" + str(e) + "\n")
        # Get Book author
        try:
            [self.Author.append(cleanText(i.get_text())) for i in
             self.soup.find("div", {"id": "bookAuthors"}).find_all("span", itemprop="name")]
        except:
            e = sys.exc_info()[0]
            self.log.log("Author could not be read for Book " + self.Title + ". Error:" + str(e) + "\n")
        # Get Book rating and no. of raters and reviewers
        try:
            self.Rating = float(
                re.sub("[a-zA-Z]+", "", cleanText(self.soup.find("span", itemprop="ratingValue").get_text())))
            self.NoRaters = int(re.sub("[a-zA-Z,]+", "", cleanText(self.soup.find(itemprop="ratingCount").attrs["content"])))
            self.NoReviewers = int(
                re.sub("[a-zA-Z,]+", "", cleanText(self.soup.find(itemprop="reviewCount").attrs["content"])))
        except:
            e = sys.exc_info()[0]
            self.log.log(
                " Book Rating and Rating and Reviewers could not be read for Book " + self.Title + ". Error:" + str(
                    e) + "\n")
        # Get Book synopsis
        try:
            self.Synopsys = cleanText(
                self.soup.find("div", {"id": "descriptionContainer"}).find("div", {"id": "description"}).find("span", {
                    "style": "display:none"}).get_text())
        except:
            e = sys.exc_info()[0]
            self.log.log("Synopsis could not be read for Book " + self.Title + ". Error:" + str(e) + "\n")

        # Get Book recommended links
        try:
            self.find_recommended()
        except:
            e = sys.exc_info()[0]
            self.log.log("Recommended Books could not be read for Book " + self.Title + ". Error:" + str(e) + "\n")
        try:
            shelvesContainer = self.soup.find('div', class_='rightContainer').find_all('a',
                                                                                       class_='actionLinkLite bookPageGenreLink')
            for cont in shelvesContainer:
                self.Genres.append(cont.text)
        except:
            e = sys.exc_info()[0]
            self.log.log("Genres could not be read for Book " + self.Title + ". Error:" + str(e) + "\n")