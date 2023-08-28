# drop tables
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"
user_table_drop = 'DROP TABLE IF EXISTS "user"'


staging_songs_table_create = ("""
      CREATE TABLE staging_songs_table (
            song_id VARCHAR(30) NOT NULL,
            artist_id VARCHAR(30) NOT NULL,
            artist_name VARCHAR NOT NULL,
            artist_location VARCHAR NOT NULL,
            artist_latitude DECIMAL,
            artist_longitude DECIMAL,
            num_songs INT NOT NULL,
            title VARCHAR,
            duration DECIMAL NOT NULL,
            year INT NOT NULL
        )""")

staging_events_table_create = ("""
      CREATE TABLE staging_events_table (
            artist VARCHAR,
            auth VARCHAR(15) NOT NULL,
            firstName VARCHAR(50),
            gender CHAR,
            itemInSession SMALLINT NOT NULL,
            lastName VARCHAR(50),
            length DECIMAL,
            level VARCHAR(10),
            location VARCHAR,
            method VARCHAR(10),
            page VARCHAR(20),
            registration DECIMAL,
            sessionId INT NOT NULL,
            song VARCHAR,
            status SMALLINT NOT NULL,
            ts TIMESTAMP NOT NULL,
            userAgent VARCHAR,
            user_id INT      
         )""")

songplay_table_create = ("""
    CREATE TABLE songplay(
        songplay_id INT IDENTITY(0,1) PRIMARY KEY,
        start_time TIMESTAMP NOT NULL REFERENCES time(start_time),
        user_id INT NOT NULL REFERENCES "user"(user_id) sortkey,
        level VARCHAR(10),
        song_id VARCHAR NOT NULL REFERENCES song(song_id) distkey,
        artist_id VARCHAR NOT NULL REFERENCES artist(artist_id),
        session_id INT NOT NULL,
        location VARCHAR,
        user_agent VARCHAR
)""")

user_table_create = ("""
     CREATE TABLE "user"(
        user_id INT NOT NULL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        gender CHAR,
        level VARCHAR(10)
) diststyle auto""")

song_table_create = ("""
    CREATE TABLE song(
        song_id VARCHAR(30) NOT NULL PRIMARY KEY,
        title VARCHAR NOT NULL,
        artist_id VARCHAR(30) NOT NULL,
        year INT NOT NULL,
        duration DECIMAL NOT NULL
)""")

artist_table_create = ("""
  CREATE TABLE artist(
        artist_id VARCHAR(30) NOT NULL PRIMARY KEY,
        name VARCHAR NOT NULL,
        location VARCHAR,
        latitude DECIMAL,
        longitude DECIMAL
)""")

time_table_create = ("""
    CREATE TABLE time(
        start_time TIMESTAMP NOT NULL PRIMARY KEY,
        hour SMALLINT NOT NULL,
        day SMALLINT NOT NULL,
        week SMALLINT NOT NULL,
        month SMALLINT NOT NULL,
        year SMALLINT NOT NULL,
        weekday SMALLINT NOT NULL
)""")

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create,
                        artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]