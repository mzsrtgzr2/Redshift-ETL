import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# TABLES
SONGPLAYS = 'songplays'
USERS = 'users'
SONGS = 'songs'
ARTISTS = 'artists'
TIMES = 'time'
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

staging_events_table_create= ("""
""")

staging_songs_table_create = ("""
""")

songplay_table_create = ("""
""")

user_table_create = ("""
""")

song_table_create = ("""
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
