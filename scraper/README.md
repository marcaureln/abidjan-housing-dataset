# Scraper

This is a [Scrapy](https://scrapy.org/) project to scrape data from listing websites.
It is configurable and can be used to scrape data from any website.
Scraped data is saved in a MySQL database.

## Getting started

### MySQL (optional)

We provide a `compose.yml` file to start a MySQL server in a Docker container. Make sure you have [Docker](https://docs.docker.com/get-docker/) installed on your machine.

```bash
# Start the MySQL server
docker compose up -d
```

### Scraper

```bash
# Copy the example configuration file:
cp scraper.toml.example scraper.toml
# Edit the configuration file with your favorite editor (e.g. vim):
vim scraper.toml
# Gather posts links
scrapy crawl links
# Gather posts details 
scrapy crawl posts
```
