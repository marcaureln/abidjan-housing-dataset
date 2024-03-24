# Abidjan Housing Dataset

Equivalent to the [California housing dataset](https://inria.github.io/scikit-learn-mooc/python_scripts/datasets_california_housing.html). 
This dataset is based on data scraped from [Jumia Deals](https://web.archive.org/web/20231208193801/https://deals.jumia.ci/) (now shut down).

## Getting started

### Environment setup

This project requires [Python 3.8 or later](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/) to manage dependencies.

```bash

Python 3 and [Poetry](https://python-poetry.org/docs/).

```bash
# Clone the repository:
git clone https://github.com/marcaureln/abidjan-housing-dataset.git
# Install dependencies:
poetry install
# Activate the virtual environment:
poetry shell
# To leave the virtual environment, run:
exit
```

### Folder structure

- `scraper/`: [Scrapy](https://scrapy.org/) project to scrape data.
- `notebooks/`: Jupyter notebooks to explore and clean the data.
- `input/`: Raw and unprocessed from the scraper.

## Contributors

- [Alex N'Guessan](https://github.com/marcaureln)
- [Abdel Beugre](https://github.com/iAbdelRahim)
