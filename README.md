This is a Goodreads data scraper.

The form of the project is a Docker Container that will run Python code.
The python code is wrapped in a Flask application that will keep the web server available for requests. The error handling in the code should ensure 0 downtime.

The only route available is /book with the parameters url(of the book in goodreads) and depth(how many layers of recommended should it go down into), URL encoded.
*****More to follow.

The output of the program is in the form of a JSON string containing book entries. These are the goodreads recommended books of the initial book that was provided with the selected depth.

Example curl request:

curl -X GET "http://127.0.0.1:5000/book?url=https://www.goodreads.com/book/show/929.Memoirs_of_a_Geisha&depth=1" > books.json
