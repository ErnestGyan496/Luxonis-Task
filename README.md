This project involves scraping data from a website, saving it in a PostgreSQL database, and creating a Flask web application to display the scraped data, particularly image URLs.
Overview

This project consists of three main components:

    Web Scraping: Python script to scrape data from a website. This script retrieves relevant information, including image URLs, from the target website.

    PostgreSQL Database: Database to store the scraped data. We use PostgreSQL to persist the scraped data for future retrieval and use.

    Flask Web Application: Flask-based web application to interact with the scraped data. The Flask app provides endpoints to access the stored data, particularly the image URLs.
