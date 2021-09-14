import csv
import json
import sqlite3
import re

MOVIES_METADATA_TUPLES = []
NUM_MOVIES_COLS = 12
KEYWORDS_TUPLES = []
GENRES_TUPLES = []

IMDB_IDS = {}

def open_files():
    movies_csv_reader = csv.reader(open('movies_metadata.csv'), delimiter=',')
#     id, imdb_id, original_title, title, series, budget, original_language,
#     production_companies, production_countries, release_date, revenue, runtime,
#     spoken_languages
    for row in movies_csv_reader:
        if len(row) != 24:
            continue
        if row[0] == 'adult' or row[18] != 'Released':
            continue

        temp_tuple = [None] * NUM_MOVIES_COLS
        # row[5] = id
        id = row[5].strip()
        if len(id) == 0:
            continue
        temp_tuple[0] = row[6].strip() # imdb_id
        if len(temp_tuple[0]) != 9:
            continue
        IMDB_IDS[id] = temp_tuple[0] # connect id to imdb_id
        temp_tuple[1] = row[8].strip() # original_title
        if len(temp_tuple[1]) == 0:
            continue
        temp_tuple[2] = row[20].strip() # title
        if len(temp_tuple[2]) == 0:
            continue

        # determine whether the movie was in a series
        if len(row[1]) != 0: # yes if in series, no if not
            temp_tuple[3] = 'YES'
        else:
            temp_tuple[3] = 'NO'

        temp_tuple[4] = row[2].strip() # budget
        if len(temp_tuple[4]) == 0 or int(temp_tuple[4]) == 0:
            temp_tuple[4] = None

        # determine genre(s) of movie
        genres = json.loads(double_quotes(row[3]))
#         if len(genres) == 0:
#             continue
        for i in range(len(genres)):
            GENRES_TUPLES.append([temp_tuple[0], genres[i]['name'].strip()])

        temp_tuple[5] = row[7].strip() # original_language
        if len(temp_tuple[5]) == 0:
            temp_tuple[5] = None
        temp_tuple[6] = list_to_string(row[12]) # production_companies
        if len(temp_tuple[6]) == 0:
            temp_tuple[6] = None
        temp_tuple[7] = list_to_string(row[13]) # production_countries
        if len(temp_tuple[7]) == 0:
            temp_tuple[7] = None
        date = row[14].strip()
        date_parts = date.split('-')
        if len(date_parts) != 3:
            continue
        if len(date_parts[0]) != 4:
            continue
        temp_tuple[8] = row[14].strip() # release_date
        if len(temp_tuple[8]) != 10:
            continue
        temp_tuple[9] = row[15].strip() # revenue
        if len(temp_tuple[9]) == 0 or int(temp_tuple[9]) == 0:
            temp_tuple[9] = None
        temp_tuple[10] = row[16].strip() # runtime
        if len(temp_tuple[10]) == 0 or int(float(temp_tuple[10])) == 0:
            temp_tuple[10] = None
        temp_tuple[11] = lang_to_string(row[17]) # spoken languages
        if len(temp_tuple[11]) == 0:
            temp_tuple[11] = None

        MOVIES_METADATA_TUPLES.append(temp_tuple)
    print('Total number of movies: ', len(MOVIES_METADATA_TUPLES))
    print('Total number of tuples in genres: ', len(GENRES_TUPLES))

    kw_csv_reader = csv.reader(open('keywords.csv'), delimiter=',')
    for row in kw_csv_reader:
        movie_id = row[0].strip()
        if movie_id == 'id':
            continue
        if len(row) == 0:
            continue
        if len(row[1]) == 0:
            continue
        if movie_id in IMDB_IDS and IMDB_IDS[movie_id] != None:
            imdb_id = IMDB_IDS[movie_id]
        else:
            continue
        keywords = json.loads(double_quotes(row[1]))
        for kw in keywords:
            word = kw['name'].strip()
            word = check_keyword(word)
            temp = [imdb_id, word]
            KEYWORDS_TUPLES.append(temp)

def load_info():
    # create connection to database
    conn = sqlite3.connect('test0.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS "metadata";')
    c.execute('DROP TABLE IF EXISTS "keywords";')
    c.execute('DROP TABLE IF EXISTS "genres";')
    c.execute('DROP TABLE IF EXISTS "ratings";')

    conn.commit()

    # create tables
    c.execute('CREATE TABLE metadata ( \
        imdb_id CHAR(9) NOT NULL, \
        original_title VARCHAR(200) NOT NULL, \
        title VARCHAR(200) NOT NULL, \
        series VARCHAR(3) NOT NULL, \
        budget INTEGER, \
        original_language VARCHAR(50), \
        production_companies VARCHAR(250), \
        production_countries VARCHAR(250), \
        release_date CHAR(10) NOT NULL, \
        revenue INTEGER, \
        runtime INTEGER, \
        spoken_languages VARCHAR(50), \
        PRIMARY KEY(imdb_id));')
    conn.commit()

    c.execute('CREATE TABLE genres ( \
        movie_id CHAR(9) NOT NULL, \
        genre VARCHAR(100) NOT NULL, \
        PRIMARY KEY (movie_id, genre), \
        FOREIGN KEY (movie_id) REFERENCES metadata(imdb_id));')
    conn.commit()

    c.execute('CREATE TABLE keywords ( \
        movie_id CHAR(9) NOT NULL, \
        word VARCHAR(100) NOT NULL, \
        PRIMARY KEY(movie_id, word), \
        FOREIGN KEY (movie_id) REFERENCES metadata(imdb_id));')
    conn.commit()

    # insert each tuple into the table
    for tuple in MOVIES_METADATA_TUPLES:
        c.execute('INSERT OR IGNORE INTO metadata VALUES (?,?,?,?,?,?,?,?,?,?,?,?);', \
            (tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], \
            tuple[6], tuple[7], tuple[8], tuple[9], tuple[10], tuple[11]))
        conn.commit()

    for tuple in GENRES_TUPLES:
        c.execute('INSERT OR IGNORE INTO genres VALUES (?, ?);', (tuple[0], tuple[1]))
        conn.commit()

    for tuple in KEYWORDS_TUPLES:
        c.execute('INSERT OR IGNORE INTO keywords VALUES (?, ?);', (tuple[0], tuple[1]))
        conn.commit()

def double_quotes(json_string):
    new_string = json_string.replace("'", "\"")
    for i in range(len(new_string)):
        if new_string[i] == '"':
            if new_string[i-1] != '{' and new_string[i-1] != ' ':
                if new_string[i+1] != ':' and new_string[i+1] != '}' and new_string[i+1] != ',':
                    new_string = new_string[:i] + '\'' + new_string[(i+1):]
            elif new_string[i-1] == ' ':
                if new_string[i-2] != ':' and new_string[i-2] != ',' and new_string[i+1] != '}':
                    new_string = new_string[:i] + '\'' + new_string[(i+1):]
        elif new_string[i] == "\\":
            new_string = new_string[:i] + '/' + new_string[(i+1):]
        elif new_string[(i-7):i] == 'rlenok"':
            new_string = new_string[:(i-1)] + '\'' + new_string[i:]
    return new_string

def check_keyword(word_string):
    new_string = word_string
    if new_string[:4] == '/xa0':
        new_string = new_string[4:]
    return new_string

def list_to_string(att):
    json_ob = json.loads(double_quotes(att))
    str = ""
    first = True
    for ele in json_ob:
        if first:
            str = ele['name'].strip()
            first = False
        else:
            str = str + ', ' + ele['name'].strip()
    return str

def lang_to_string(ob):
    json_ob = json.loads(double_quotes(ob))
    str = ""
    first = True
    for ele in json_ob:
        if first:
            str = ele['iso_639_1'].strip()
            first = False
        else:
            str = str + ', ' + ele['iso_639_1'].strip()
    return str

if __name__ == "__main__":
    print('we are in the main function')
    open_files()
    load_info()
    print('we are just about to exit the main function')
