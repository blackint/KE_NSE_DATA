# KE_NSE_DATA
A crawler to get NSE data from https://mystocks.co.ke/



### Running it locally



[Install pipenv](https://pypi.org/project/pipenv/)

```
sudo apt install pipenv
```


Run it in a virtualenv 

```
pipenv run scrapy crawl mystocks.co.ke
```

The data is stored in `stock_data` folder
