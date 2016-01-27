# Mines .NET - Flights API

This project exposes an API that allows to query a flight database.

## Start the REST API

This API is built using Python and Flask.

To run the app, just run :

``` bash
pip install -r requirements.txt
python run.py
```

## MongoDB database

To set up a mongo database in local, please run :
``` bash
./mongo_init.sh
```

If you want to use Heroku as a db host, you will need to manually import the initial dataset :
``` bash
mongoimport --host ds051635.mongolab.com:51635 --db heroku_x9vv876g --username heroku_x9vv876g --password im9uv9qf6rni1hm406h5trl9ig --collection flights --type json --file init.json --jsonArray
```
