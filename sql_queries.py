import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# GLOBAL VARIABLES
LOG_DATA = config.get("S3","LOG_DATA")
LOG_PATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")
IAM_ROLE = config.get("IAM_ROLE","ARN")

# TABLES
SONGPLAYS = 'fact_songplays'
USERS = 'dim_users'
SONGS = 'dim_songs'
ARTISTS = 'dim_artists'
TIMES = 'dim_time'
STAGING_EVENTS = 'staging_events'
STAGING_SONGS = 'staging_songs'

# DROP TABLES

_DROP_FORMAT = 'DROP TABLE IF EXISTS {};'

staging_events_table_drop = _DROP_FORMAT.format(STAGING_EVENTS)
staging_songs_table_drop = _DROP_FORMAT.format(STAGING_SONGS)
songplay_table_drop = _DROP_FORMAT.format(SONGPLAYS)
user_table_drop = _DROP_FORMAT.format(USERS)
song_table_drop = _DROP_FORMAT.format(SONGS)
artist_table_drop = _DROP_FORMAT.format(ARTISTS)
time_table_drop = _DROP_FORMAT.format(TIMES)

# CREATE TABLES

staging_events_table_create= (f"""
CREATE TABLE IF NOT EXISTS {STAGING_EVENTS}
(
    artist VARCHAR NOT NULL,
    auth VARCHAR,
    firstName VARCHAR,
    gender CHAR,
    itemInSession INTEGER NOT NULL,
    lastName VARCHAR,
    length float NOT NULL,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration TIMESTAMP NOT NULL,
    sessionId INTEGER NOT NULL,
    song VARCHAR NOT NULL,
    status INTEGER NOT NULL,
    ts TIMESTAMP NOT NULL,
    userAgent VARCHAR,
    userId INTEGER NOT NULL
)
""")

staging_songs_table_create = (f"""
CREATE TABLE IF NOT EXISTS {STAGING_SONGS}
(
    song_id VARCHAR NOT NULL ,
    num_songs INTEGER,
    title VARCHAR NOT NULL,
    artist_name VARCHAR NOT NULL,
    artist_latitude FLOAT,
    year INTEGER,
    duration FLOAT NOT NULL,
    artist_id VARCHAR NOT NULL,
    artist_longitude FLOAT,
    artist_location VARCHAR
)
""")

songplay_table_create = (f"""
CREATE TABLE IF NOT EXISTS {SONGPLAYS}
(
    songplay_id integer IDENTITY(0,1),
    start_time timestamp NOT NULL,
    user_id varchar NOT NULL,
    level varchar,
    song_id varchar,
    artist_id varchar,
    session_id varchar NOT NULL,
    location varchar,
    user_agent varchar
)
""")

user_table_create = (f"""
CREATE TABLE IF NOT EXISTS {USERS}
(
    user_id varchar NOT NULL PRIMARY KEY,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    gender char,
    level varchar
)
""")

song_table_create = (f"""
CREATE TABLE IF NOT EXISTS {SONGS}
(
    song_id varchar NOT NULL PRIMARY KEY, 
    title varchar NOT NULL,
    artist_id varchar NOT NULL, 
    year integer, 
    duration float
)
""")

artist_table_create = (f"""
CREATE TABLE IF NOT EXISTS {ARTISTS}
(
    artist_id varchar NOT NULL PRIMARY KEY,
    name varchar NOT NULL,
    location varchar, 
    latitude float, 
    longitude float
)
""")

time_table_create = (f"""
CREATE TABLE IF NOT EXISTS {TIMES}
(
    start_time timestamp NOT NULL PRIMARY KEY,
    hour integer, 
    day integer,
    week integer, 
    month integer, 
    year integer, 
    weekday integer
)
""")

# STAGING TABLES

staging_events_copy = ("""
copy {db} 
from {json_data}
iam_role {iam_role}
json {json_path}
""").format(
    db=STAGING_EVENTS,
    json_data=LOG_DATA,
    json_path=LOG_PATH,
    IAM_ROLE=IAM_ROLE
)

staging_songs_copy = ("""
copy {db} 
from {json_data}
iam_role {iam_role}
""").format(
    db=STAGING_SONGS,
    json_data=LOG_DATA,
    IAM_ROLE=IAM_ROLE
)

# FINAL TABLES

songplay_table_insert = (f"""
INSERT INTO {SONGPLAYS}
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT e.ts, e.userId, e.level, s.song_id, s.artist_id, e.sessionId, e.location, e.userAgent 
FROM {STAGING_EVENTS} as e
JOIN {STAGING_SONGS} as s ON e.song=s.title
""")

user_table_insert = (f"""
INSERT INTO {USERS}
(user_id, first_name, last_name, gender, level)
SELECT e.userId, e.firstName, e.lastName, e.gender, e.level
FROM {STAGING_EVENTS} as e
""")

song_table_insert = (f"""
INSERT INTO {SONGS}
(song_id, title, artist_id, year, duration)
SELECT song_id, title, artist_id, year, duration
FROM {STAGING_SONGS}
""")

artist_table_insert = (f"""
INSERT INTO {ARTISTS}
(artist_id, name, location, latitude, longitude)
SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM {STAGING_SONGS}
""")

time_table_insert = (f"""
INSERT INTO {TIMES}
(start_time, hour, day, week, month, year, weekday)
SELECT 
    ts,
    extract(hour from time_val),
    extract(day from time_val),
    extract(week from time_val),
    extract(month from time_val),
    extract(year from time_val),
    extract(weekday from time_val)
FROM {STAGING_EVENTS}
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
