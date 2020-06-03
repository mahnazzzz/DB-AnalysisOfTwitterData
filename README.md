

# Assignment  Analysis of Twitter Data

Implement a small database application, which imports a dataset of Twitter tweets from the CSV file into database.

You can find the assignment [here](https://github.com/datsoftlyngby/soft2019spring-databases/blob/master/assignments/assignment2.md)! 

# Program 

- Vagrant
- Docker
- MongoDB
- Regular expressions\aggregation


# Import Data

In Git Bash Here type:
- $ vagrant up
- $ vagrant ssh
- $ docker run --rm -v $(pwd)/data:/data/db --publish=27017:27017 --name dbms -d mongo
- $ docker exec -it dbms bash

In root

- root@88385afac5fe:/# apt-get update
- root@88385afac5fe:/# apt-get install -y wget
- root@88385afac5fe:/# apt-get install -y unzip

Continue with downloading the data

- root@88385afac5fe:/# wget http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip

In your VM the unzip package is not installed by default.

- root@88385afac5fe:/# unzip trainingandtestdata.zip
- root@88385afac5fe:/# mongoimport --drop --db social_net --collection tweets --type csv --headerline --file traning.1600000.processed.noemoticon.csv
- root@88385afac5fe:/# iconv -f ISO-8859-1 -t utf-8 training.1600000.processed.noemoticon.csv > converted-utf8.csv' (this converts it to utf8)

To make use of the --headerline switch when importing the data with mongoimport, we add a headerline accordingly:

- root@88385afac5fe:/# sed -i '1s;^;polarity,id,date,query,user,text\n;' training.1600000.processed.noemoticon.csv

he connect to Mongodb Compass Community both for localhost and host = 127.0.0.1 port 27017, but in both cases the data is stored in the local where i could not through run '.py' file get data from mongoDB

> ![image](https://user-images.githubusercontent.com/20173643/83579916-d9dc4880-a53a-11ea-82c3-9f56fedec95b.png)
![image](https://user-images.githubusercontent.com/20173643/83580201-b36add00-a53b-11ea-9c62-4fa623025f81.png)


Besides that through vagrant and docker I would connect into local mongoDB database, but I couldn't do it where it gives the error the whole time the gate 27017 is busy, then I will restart the port or through another port connect into the database but it was also not successful


# Solution

After I couldn't connected to the Mongo DB from either editor Jupyter notebook and Python to port where MongoDB was, though the data is imported. That's whyats inside the docker, I connected to the MongoDB and i got the data we should get from the CSV file using a regular expration and aggregation.

- root@88385afac5fe:/# mongo
- >show dbs

```sh
admin       0.000GB
config      0.000GB
local       0.000GB
social_net  0.217GB
```
 - use social_net
 - show collections
 
```sh
tweets
```
 - db.tweets.find()

```sh
{ "_id" : ObjectId("5ed7b475a22f7286db9e52ae"), "0" : 0, "1467810369" : 1467810672, "Mon Apr 06 22:19:45 PDT 2009" : "Mon Apr 06 22:19:49 PDT 2009", "NO_QUERY" : "NO_QUERY", "_TheSpecialOne_" : "scotthamilton", "@switchfoot http://twitpic" : { "com/2y1zl - Awww, that's a bummer" : { "  You shoulda got David Carr of Third Day to do it" : { " ;D" : "is upset that he can't update his Facebook by texting it... and might cry as a result  School today also. Blah!" } } } }
{ "_id" : ObjectId("5ed7b475a22f7286db9e52af"), "0" : 0, "1467810369" : 1467810917, "Mon Apr 06 22:19:45 PDT 2009" : "Mon Apr 06 22:19:53 PDT 2009", "NO_QUERY" : "NO_QUERY", "_TheSpecialOne_" : "mattycus", "@switchfoot http://twitpic" : { "com/2y1zl - Awww, that's a bummer" : { "  You shoulda got David Carr of Third Day to do it" : { " ;D" : "@Kenichan I dived many times for the ball. Managed to save 50%  The rest go out of bounds" } } } }
```


- How many Twitter users are in the database?



![image](https://user-images.githubusercontent.com/20173643/83680131-d69b9800-a5e0-11ea-83be-1fbb78e20333.png)
 


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









