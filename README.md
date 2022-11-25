# Abidjan Housing Dataset

Kinda equivalent to the _California Housing dataset_ (you can find it on [scikit-learn](https://inria.github.io/scikit-learn-mooc/python_scripts/datasets_california_housing.html)). This dataset is resulting from data scraped from the popular listing website [Jumia Deals](https://deals.jumia.ci/). The raw data is already available (see [releases](https://github.com/marcaureln/abidjan-housing-dataset/releases)). The next step is to extract as much information as we can from it (longitude, latitude, etc., see [California Housing data description](https://github.com/ageron/handson-ml/tree/master/datasets/housing#data-description) and [Ames (Iowa) housing dataset](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data)).

## To-do:

- [x] Collect data
- [ ] Clean and augment the dataset
- [ ] Vizualize data

## What's next?

- **Make spiders configurable**: it'll make scraping other websites easier and without having to modify the code or write multiple spiders.
-

## Getting started and contributing

1. Clone the repository
2. Create a virtual environment: `python3 -m venv <my_venv>`
3. Activate the virtual environment: `source ./<my_venv>/bin/activate`
4. Install dependencies: `pip3 install -r ./requirements.txt`
5. When you want to leave virtual environment, run: `deactivate`

**Run spiders:**

1. While in the project directory, move to _scraper_ folder (Scrapy project): `cd ./scraper`
2. Gather posts links: `scrapy crawl links -o links.csv` # links will be output to a `links.csv` file
3. Gather posts details: `scrapy crawl posts -a links=links.csv -o posts.csv` # the links file should be relative to the scraper root folder i.e. `<repository>/scraper`

**Track project dependencies:**

1. While in the virtual environment, install your package, e.g. `pip install pandas`
2. `pip freeze > requirements.txt`
3. `git commit -am requirements.txt`
4. Push to the repository.
