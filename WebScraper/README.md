# WebScraper

This script take two parameters from the user input: the number of pages (an integer) and the type of articles (a string). 

The integer with the number of pages specifies the number of pages on which the program should look for the articles.

The script goes to the https://www.nature.com/nature/articles?sort=PubDate&year=2020 website and navigate between the pages with the requests module changing the URL.

Then it creates a directory named Page_N (where N is the page number corresponding to the number input by the user) for each page. 

Search and collect all articles page by page; filter all the articles by the article type and put all the articles that are found on the page with the matched type to the directory Page_N. 

Mind that when the user enters some number, for example, 4, the program should search all pages up to that number and the respective folders (Folder 1, Folder 2, Folder 3, Folder 4) should be created.

It saves the articles to separate *.txt files and named them based on the article name and convention. 

If there's no articles on the page, the program should still create a folder, but in this case the folder would be empty.
