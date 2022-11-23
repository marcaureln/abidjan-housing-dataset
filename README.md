# Abidjan Housing Dataset - Scraper

## Getting started and contributing

1. Clone the repository
2. Create a virtual environment: `python3 -m venv <my_venv>`
3. Activate the virtual environment: `source ./<my_venv>/bin/activate`
4. Install dependencies: `pip3 install -r ./requirements.txt`
5. When you want to leave virtual environment, run: `deactivate`

**Run spiders:**

1. While in the project directory, move to _scraper_ folder (Scrapy project): `cd ./scraper`
2. Gather posts links: `scrapy crawl links -o links.csv` # links will be output to a `links.csv` file

**Track project dependencies:**

1. While in the virtual environment, install your package, e.g. `pip install pandas`
2. `pip freeze > requirements.txt`
3. `git commit -am requirements.txt`
4. Push to the repository.
