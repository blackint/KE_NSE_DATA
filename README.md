# KE_NSE_DATA
A crawler to get NSE data from https://mystocks.co.ke/ in json format



## Running it locally

### Clone

```
git clone git@github.com:blackint/KE_NSE_DATA.git
```

navigate to the project folder

```
cd KE_NSE_DATA/
```

### Install dependencies


For virtualenv and package management this project uses pipenv

[Install pipenv](https://pypi.org/project/pipenv/)


```
pipenv install
```

Run it in a virtualenv 

```
pipenv run scrapy crawl mystocks.co.ke
```

The data is stored in `stock_data` folder
