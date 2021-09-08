# Redshift ETL project

## Overview
The Project is to build an ETL Pipeline that extracts music streaming startup data from S3, staging it in Redshift and then transforming data into a set of Dimensional and Fact Tables for their Analytics Team to continue finding Insights to what songs their users are listening to.

## Description

Application of Data warehouse and AWS to build an ETL Pipeline for a database hosted on Redshift Will need to load data from S3 to staging tables on Redshift and execute SQL Statements that create fact and dimension tables from these staging tables to create analytics

## Datasets

- Song Data Path: s3://udacity-dend/song_data

The first dataset is a subset of real data from the Million Song Dataset(https://labrosa.ee.columbia.edu/millionsong/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. 
For example:

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}


- Log Data Path: s3://udacity-dend/log_data

The second dataset consists of log files in JSON format. The log files in the dataset with are partitioned by year and month.
For example:

log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json

And below is an example of what a single log file, 2018-11-13-events.json, looks like.

{"artist":"Pavement", "auth":"Logged In", "firstName":"Sylvie", "gender", "F", "itemInSession":0, "lastName":"Cruz", "length":99.16036, "level":"free", "location":"Klamath Falls, OR", "method":"PUT", "page":"NextSong", "registration":"1.541078e+12", "sessionId":345, "song":"Mercy:The Laundromat", "status":200, "ts":1541990258796, "userAgent":"Mozilla/5.0(Macintosh; Intel Mac OS X 10_9_4...)", "userId":10}

- Log Data JSON Path: s3://udacity-dend/log_json_path.json

## Fact Table

songplays - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

## Dimension Tables

<b>users</b> - users in the app
user_id, first_name, last_name, gender, level

<b>songs</b> - songs in music database
song_id, title, artist_id, year, duration

<b>artists</b> - artists in music database
artist_id, name, location, lattitude, longitude

<b>time</b> - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday


## Schema for Song Play Analysis

#### Fact Table
songplays - records in event data associated with song plays. Columns for the table:

    songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

#### Dimension Tables 
##### users

    user_id, first_name, last_name, gender, level
##### songs

    song_id, title, artist_id, year, duration

##### artists

    artist_id, name, location, lattitude, longitude

##### time

    start_time, hour, day, week, month, year, weekday



## Running the Code

### Setup Python Environment with Conda

run the following command to create python environment:
```
conda env create -f environment.yml
```
### Create AWS Infrastrucuture
We will use [Pulumi](https://www.pulumi.com/) to scaffold the infrastructure:
- Redshift cluster
- IAM role the cluster assumes when doing COPY INTO the staging tables

```
cd infra
pulumi up
```
From the outputs of the last command update
the configuration file dwh.cfg

the ARN and HOST should be changed to what was just created by pulumi command.

### Run the code

```
python create_tables.py
python etl.py
python test.py
```

if there are errors from Redshift, can see them with
```
python rs_logs.py
```

### Destroy Infra
```
cd infra
pulumi destroy
```