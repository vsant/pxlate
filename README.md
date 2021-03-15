![picture](logos/logo.png)

# pxlate - Reverse Image Search (2009)
Upload an image and the program will display similar appearing images.

* **pxlate/** has backend python code to scrape the web to create an image database, and to search an input image against this database
* **web/** has frontend PHP code to take input images and display the results

In order to get the crawler program running:
* Copy pxlate/crawler/settings.py.sample as settings.py and update API_KEY with a Google Image Search AJAX API key of your own.
