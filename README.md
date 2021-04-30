# KE_NSE_DATA
A crawler to get NSE data from https://mystocks.co.ke/ in json format



### Running it locally

```
git clone git@github.com:blackint/KE_NSE_DATA.git
```

```
cd KE_NSE_DATA/KE_NSE_stock_data_crawler/
```

For virtualenv and package management this project uses pipenv


[Install pipenv](https://pypi.org/project/pipenv/)


Run it in a virtualenv 

```
pipenv run scrapy crawl mystocks.co.ke
```

The data is stored in `stock_data` folder
