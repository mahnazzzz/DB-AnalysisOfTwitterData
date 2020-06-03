

# Assignment  Analysis of Twitter Data

Implement a small database application, which imports a dataset of Twitter tweets from the CSV file into database.

You can find the assignment [here](https://github.com/datsoftlyngby/soft2019spring-databases/blob/master/assignments/assignment2.md)! 

# Program 

- MongoDB
- Pycharm(Terminal)

# Import Data

In Pycharm in terminal 

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

Through python I could not get data from mongoDB which is in the local, even though the data is imported. So therefore through the docker made a container and have mongo db there, into the docker through mongodb i connected to the database and find data i should get

![image](https://user-images.githubusercontent.com/20173643/83579720-53c00200-a53a-11ea-8fe5-3ea7f7fde6da.png)

I got the connect to Mongodb Compass Community both for localhost and host = 127.0.0.1 port 27017, but in both cases the data is stored in the local where i could not through run '.py' file get data from mongoDB

> ![image](https://user-images.githubusercontent.com/20173643/83579916-d9dc4880-a53a-11ea-82c3-9f56fedec95b.png)
![image](https://user-images.githubusercontent.com/20173643/83580201-b36add00-a53b-11ea-9c62-4fa623025f81.png)


Besides that through vagrant and docker I would connect into local mongoDB database, but I couldn't do it where it gives the error the whole time the gate 27017 is busy, then I will restart the port or through another port connect into the database but it was also not successful



# Løsning

Application has to be able to answer queries corresponding to the following questions:

- How many Twitter users are in the database?

> ![image](https://user-images.githubusercontent.com/20173643/83580019-3ccddf80-a53b-11ea-8049-0eb88ce2b500.png)

- Which Twitter users link the most to other Twitter users? (Provide the top ten.)

![image](https://user-images.githubusercontent.com/20173643/83580398-528fd480-a53c-11ea-9887-537699e417fb.png)
```sh
db.tweets.aggregate([{'$match':{'text':{'$regex':"@\w+"}}},
                        {'$addFields': {"mentions":1}},
                        {'$group':{"_id":"$user", "mentions":{'$sum':1}}},
                        {'$sort':{"mentions":-1}},
                        {'$limit':10}])
 
```
 
 
 
- Who is are the most mentioned Twitter users? (Provide the top five.)

 ![image](https://user-images.githubusercontent.com/20173643/83580540-97b40680-a53c-11ea-8a1d-55789300986c.png)
 ```sh
db.tweets.aggregate([{'$addFields': {'words':{'$split':['$text', ' ']}}},
                         {'$unwind':"$words"},
                         {'$match':{'words':{'$regex':"@\w+",'$options':'m'}}},
                         {'$group':{'_id':"$words",'total':{'$sum':1}}},
                         {'$sort':{'total':-1}},
                         {'$limit':5}])
 ```


- Who are the most active Twitter users (top ten)?

 ![image](https://user-images.githubusercontent.com/20173643/83580745-19a42f80-a53d-11ea-89ed-f749e19234e7.png)
 
 ```sh
 db.tweets.aggregate([{'$group': {'_id': '$user', 'total': {'$sum':1}}},
                         {'$sort':{'total':-1}},
                         {'$limit':10}
                         ])

 ```
- Who are the five most grumpy (most negative tweets)

![image](https://user-images.githubusercontent.com/20173643/83580847-65ef6f80-a53d-11ea-9bc0-7688669f20b0.png)
 ```sh
db.tweets.aggregate([{'$match': {'text': {'$regex': "worst|wtf|damn|angry|pissed|mad"}}},
                                    {'$group':{'_id':"$user", 'emotion': {'$avg': "$polarity"}, 'total_negative_tweets': {'$sum': 1}}},
                                    {'$sort':{ 'emotion': 1, 'total_negative_tweets':-1}},
                                    {'$limit': 5}
                                    ])
 ```

- The most happy (most positive tweets)?

![image](https://user-images.githubusercontent.com/20173643/83580968-ca123380-a53d-11ea-9de0-e32a16231a6b.png)
```sh
db.tweets.aggregate([{'$match': {'text': {'$regex': "love|nice|good|great|amazing|happy"}}},
                         {'$group':{'_id':"$user", 'emotion': {'$avg': "$polarity"}, 'total_positive_tweets': {'$sum': 1}}},
                         {'$sort':{ 'emotion': -1, 'total_positive_tweets':-1}}, 
                         {'$limit': 5}
                         ])

```









