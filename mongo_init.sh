# Shell script used in order to set up a mongo db and import initial flights data
# Author : Guillaume Pouilloux
# Version : 1.0

MONGO_PORT=27017
MONGO_NAME=mongo-flights
MONGO_VERSION=3.0.3

echo Running mongo container listening on port $MONGO_PORT
docker run --name $MONGO_NAME -p 27017:27017 -d mongo:$MONGO_VERSION

echo Waiting for database $MONGO_NAME to start
secs=60
while [ $secs -gt 0 ]; do
   echo -ne "$secs\033[0K\r"
   sleep 1
   : $((secs--))
done

MONGO_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' $MONGO_NAME)
echo Importing dataset into MongoDB at $MONGO_IP:$MONGO_PORT
mongoimport --host $MONGO_IP:$MONGO_PORT --db test --collection flights --type json --file init.json --jsonArray
