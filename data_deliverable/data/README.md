# Data Spec

### Data description ###
The data in our set was used for the Spring 2021 CSCI 1951A Final Project by Emily Belt, Erika Bussmann, and Mandy Chang.
-------------------------------------------------------------------------------------------------------------------------------
The data was collected from Kaggle, a subsidiary of Google that allows data scientists to collect and share datasets. Two different sets were used. The first set, titled “The Movies Dataset,” was published by Rounak Banik, a data scientist at the reputable Fractal Analytics. Banik extracted the information from TMDB, a movie rating website, using TMDB’s open API. Banik also gained information from GroupLens, which is a research group that publishes public data from MovieLens, a movie recommendation website. The second dataset, titled “IMDB Movies Extensive Dataset,” was published by Stefano Leone. This public domain information was scraped from IMDB, another movie review website. Datasets were combined and cleaned using Java and Python.

Link to full dataset: https://drive.google.com/file/d/1UbFeHyQpfXozqvgRNG8nHcPBogvZiY5Z/view?usp=sharing

#### Data format ####

#### all_movies table####
all_movies - this table contains all of the movies we will be using for our project’s prediction. Each tuple in this table refers to a single movie and has the following attributes:

id - CHAR(9) -- the unique 9-character IMDb identifier of the movie starting with “tt”; this attribute was the primary key of this table (its value is thus not allowed to be null).

title - VARCHAR(150) -- the title of the movie; this value is not allowed to be null.

original_title - VARCHAR -- the original title of the movie; in most cases, a movie’s original title is the same as its title, but in cases where they differ, it is usually because original_title is in the original language of the movie, while title is in English; this value is not allowed to be null.

year - INTEGER -- the year in which the movie was released.

month_published - INTEGER -- the month in which the movie was released, in numerical format (eg. 1 = January, 2 = February, etc.)

genre - VARCHAR(150) -- the genre(s) of the movie; if there are multiple, the genres are all in a single string, separated by commas.

country - VARCHAR(200) -- the country(ies) from which the movie originated; if there are multiple, the countries are all in a single string, separated by commas.

director - VARCHAR(200) -- the name(s) of the director(s) of the movie, in the format of “<first name> <last name>”; if there are multiple, the directors’ names are all in a single string, separated by commas.

writer - VARCHAR(200) -- the name(s) of the writer(s) of the movie, in the format of “<first name> <last name>”; if there are multiple, the writers’ names are all in a single string, separated by commas.

production_company - VARCHAR(200) -- the name of the primary production company of the movie.
popular_actors - INTEGER -- the number of popular actors who are in the movie; a popular actor is defined as an actor from the IMDb dataset who has been in more than 10 movies from the IMDb dataset.

weighted_avg_vote - REAL -- the weighted average of the IMDb votes for the movie.
total_votes - INTEGER -- the total number of IMDb votes the movie has from users.

mean_vote - REAL -- the average IMDb vote of the movie.

median_vote - INTEGER -- the median IMDb vote of the movie.

votes_10 - INTEGER -- the number of votes the movie received on IMDb that were a 10.
votes_9 - INTEGER -- the number of votes the movie received on IMDb that were a 9.
votes_8 - INTEGER -- the number of votes the movie received on IMDb that were a 8.
votes_7 - INTEGER -- the number of votes the movie received on IMDb that were a 7.
votes_6 - INTEGER -- the number of votes the movie received on IMDb that were a 6.
votes_5 - INTEGER -- the number of votes the movie received on IMDb that were a 5.
votes_4 - INTEGER -- the number of votes the movie received on IMDb that were a 4.
votes_3 - INTEGER -- the number of votes the movie received on IMDb that were a 3.
votes_2 - INTEGER -- the number of votes the movie received on IMDb that were a 2.
votes_1 - INTEGER -- the number of votes the movie received on IMDb that were a 1.

us_voter_rating - REAL -- the average vote the movie received from IMDb users who are from the United States of America.

us_voter_count - INTEGER -- the number of votes the movie received on IMDb from users who are from the United States of America.

foreign_voter_rating - REAL -- the average vote the movie received from IMDb users who are not from the United States of America.

foreign_voter_count -  INTEGER -- the number of votes the movie received on IMDb from users who are not from the United States of America.

male_avg_vote - REAL - the average rating of the movie by all male-identifying individuals who rated it

male_total_votes - INTEGER - the total number of male-identifying individuals who rated this movie

female_avg_vote - REAL - the average rating of the movie by all female-identifying individuals who rated it

female_total_votes - INTEGER - the total number of female-identifying individuals who rated this movie

series - VARCHAR(3) -- “YES” if the movie is in a series, “NO” if otherwise

budget - INTEGER -- the budget of the movie, in US dollars; this value is allowed to be null.
original_language - CHAR(2) -- the original language of the movie in two-letter ISO 639-1 standard language codes (e.g., “en” = English, “fr” = French); this value is allowed to be null.

revenue - INTEGER -- the revenue of the movie, in US dollars; this value is allowed to be null.

runtime - INTEGER -- the runtime of the movie, in minutes; this value is allowed to be null.

spoken_languages VARCHAR -- the language(s) spoken in the movie; if there are multiple languages, they are all in a single string, separated by commas; this value is allowed to be null.

Primary key = id

#### Keywords table ####
keywords - this table contains links between movies and keywords associated with those movies. Each tuple in this table refers to a single (movie, keyword) pair and has the following attributes:

movie_id - CHAR(9) -- the unique 9-character IMDb identifier of a movie starting with “tt”; this attribute is a foreign key, which references the “id” attribute of the all_movies table.

word - VARCHAR(100) -- the keyword associated with the movie whose IMDb ID is movie_id.

Primary key = (movie_id, word); since there can be multiple keywords associated with a single movie, the only way to uniquely identify a tuple is to make both the movie’s IMDb ID and the keyword the primary key.
