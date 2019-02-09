# DB-AnalysisOfTwitterData

#Assignment  Analysis of Twitter Data

Implement a small database application, which imports a dataset of Twitter tweets from the CSV file into database.

Application has to be able to answer queries corresponding to the following questions:

How many Twitter users are in the database?
Which Twitter users link the most to other Twitter users? (Provide the top ten.)
Who is are the most mentioned Twitter users? (Provide the top five.)
Who are the most active Twitter users (top ten)?
Who are the five most grumpy (most negative tweets) and the most happy (most positive tweets)?

# Import Data

In terminal in virtualmachine 

- $ docker run --rm -v $(pwd)/data:/data/db --publish=27017:27017 --name dbms -d mongo

- $ docker exec -it dbms bash

In root

- root@88385afac5fe:/$ apt-get update
- root@88385afac5fe:/$ apt-get install -y wget, unzip

Continue with downloading the data

- root@88385afac5fe:/$ wget http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip

In your VM the unzip package is not installed by default.

- root@88385afac5fe:/$ unzip trainingandtestdata.zip

To make use of the --headerline switch when importing the data with mongoimport, we add a headerline accordingly:

- root@88385afac5fe:/# sed -i '1s;^;polarity,id,date,query,user,text\n;' training.1600000.processed.noemoticon.csv
