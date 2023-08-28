import configparser

config = configparser.ConfigParser()
config.read('dwh.cfg')

# staging tables:
staging_events_copy = ("""
        COPY staging_events_table from {}
        CREDENTIALS 'aws_iam_role={}' 
        JSON {}
        TIMEFORMAT 'epochmillisecs'
        REGION 'us-west-2';
""".format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])
                       )

staging_songs_copy = ("""
        COPY staging_songs_table from {}
        CREDENTIALS 'aws_iam_role={}' 
        FORMAT as json 'auto' 
        REGION 'us-west-2';
""".format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])
)

# schema tables:
songplay_table_insert = ("""INSERT INTO songplay(start_time, user_id, level, song_id,
 artist_id, session_id, location, user_agent)
SELECT e.ts AS start_time,
       e.user_id,
       e.level,
       s.song_id,
       s.artist_id,
       e.sessionId AS session_id,
       e.location,
       e.userAgent AS user_agent
FROM staging_events_table e
JOIN staging_songs_table s
ON s.title = e.song AND s.artist_name = e.artist
WHERE e.page = 'NextSong' AND e.user_id IS NOT NULL
""")

user_table_insert = ("""INSERT INTO "user"(user_id, first_name, last_name, gender, level)
SELECT DISTINCT(user_id),
       firstName AS first_name,
       lastName AS last_name,
       gender,
       level
FROM staging_events_table
WHERE user_id IS NOT NULL
""")

song_table_insert = ("""INSERT INTO song(song_id, title, artist_id, year, duration)
SELECT DISTINCT(song_id),
       title,
       artist_id,
       year,
       duration
FROM staging_songs_table
""")

artist_table_insert = ("""INSERT INTO artist(artist_id, name, location, latitude, longitude)
SELECT DISTINCT(s.artist_id),
       s.artist_name AS name,
       e.location,
       s.artist_latitude AS latitude,
       s.artist_longitude AS longitude
FROM staging_songs_table s
LEFT JOIN staging_events_table e ON s.artist_name = e.artist
""")

time_table_insert = ("""INSERT INTO time(start_time, hour, day, week, month, year, weekday) 
SELECT DISTINCT(ts) AS start_time,
        EXTRACT(hour FROM ts) AS hour,
        EXTRACT(day FROM ts) AS day,
        EXTRACT(week FROM ts) AS week,
        EXTRACT(month FROM ts) AS month,
        EXTRACT(year FROM ts) AS year,
        EXTRACT(weekday FROM ts) AS weekday
FROM staging_events_table
""")

copy_table_queries = [staging_songs_copy, staging_events_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert,
                        artist_table_insert, time_table_insert]
