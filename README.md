
# Program 

- Python
- MongoDB

# Import Data

In terminal in virtualmachine 

- $ docker run --rm -v $(pwd)/data:/data/db --publish=27017:27017 --name dbms -d mongo

- $ docker exec -it dbms bash

In root

- root@88385afac5fe:/$ apt-get update
- root@88385afac5fe:/$ apt-get install -y wget
- root@88385afac5fe:/$ apt-get install -y unzip

Continue with downloading the data

- root@88385afac5fe:/$ wget http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip

In your VM the unzip package is not installed by default.

- root@88385afac5fe:/$ unzip trainingandtestdata.zip
- root@da738e09730f:/# mongoimport --drop --db social_net --collection tweets --type csv --headerline --file traning.1600000.processed.noemoticon.csv

To make use of the --headerline switch when importing the data with mongoimport, we add a headerline accordingly:

- root@88385afac5fe:/# sed -i '1s;^;polarity,id,date,query,user,text\n;' training.1600000.processed.noemoticon.csv

# Problem

Through python I could not conceive to mongoDB which is in the local, even though the data is imported. So therefore through the docker made a container and have mongo db there, through mongodb i connected to the database and find data i should show

![image](https://user-images.githubusercontent.com/20173643/52914947-57406300-32ce-11e9-9e79-7a6601fc188e.png)

# Assignment  Analysis of Twitter Data

Implement a small database application, which imports a dataset of Twitter tweets from the CSV file into database.

Application has to be able to answer queries corresponding to the following questions:

- How many Twitter users are in the database?

> ![image](https://user-images.githubusercontent.com/20173643/52914916-219b7a00-32ce-11e9-86cc-ca0589f4dc0a.png)

- Which Twitter users link the most to other Twitter users? (Provide the top ten.)

 > db.tweets.aggregate([{'$match':{'text':{'$regex':"@\w+"}}},{'$addFields': {"mentions":1}},{'$group':{"_id":"$user", "mentions":{'$sum':1}}},{'$sort':{"mentions":-1}},{'$limit':10}])
 ![image](https://user-images.githubusercontent.com/20173643/52914760-8e157980-32cc-11e9-82d8-a2b2ebff7554.png)
 
- Who is are the most mentioned Twitter users? (Provide the top five.)
 
 > db.tweets.aggregate([{'$addFields': {'words':{'$split':['$text', ' ']}}},{'$unwind':"$words"},{'$match':{'words':{'$regex':"@\w+",'$options':'m'}}},{'$group':{'_id':"$words",'total':{'$sum':1}}},{'$sort':{'total':-1}}, {'$limit':5}])
![image](https://user-images.githubusercontent.com/20173643/52914769-9cfc2c00-32cc-11e9-9009-197718581f12.png)

- Who are the most active Twitter users (top ten)?
 
> db.tweets.aggregate([{'$group': {'_id': '$user', 'total': {'$sum':1}}},  {'$sort':{'total':-1}}, {'$limit':10} ])
![image](https://user-images.githubusercontent.com/20173643/52914783-b2715600-32cc-11e9-8c17-4b6ea767f349.png)

- Who are the five most grumpy (most negative tweets)

> db.tweets.aggregate([{'$match': {'text': {'$regex': "worst|wtf|damn|angry|pissed|mad"}}},{'$group':{'_id':"$user", 'emotion': {'$avg': "$polarity"}, 'total_negative_tweets': {'$sum': 1}}},{'$sort':{ 'emotion': 1, 'total_negative_tweets':-1}},
{'$limit': 5}])
![image](https://user-images.githubusercontent.com/20173643/52914786-c026db80-32cc-11e9-8e0b-49a9e6a93965.png)

- The most happy (most positive tweets)?

> db.tweets.aggregate([{'$match': {'text': {'$regex': "love|nice|good|great|amazing|happy"}}},{'$group':{'_id':"$user", 'emotion': {'$avg': "$polarity"}, 'total_positive_tweets': {'$sum': 1}}},{'$sort':{ 'emotion': -1, 'total_positive_tweets':-1
}}, {'$limit': 5}])
![image](https://user-images.githubusercontent.com/20173643/52914789-cd43ca80-32cc-11e9-8774-afc5d7805549.png)













