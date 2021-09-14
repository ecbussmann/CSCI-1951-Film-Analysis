# Tech Report
Please visit this link for the full tech report, with graphics:
https://docs.google.com/document/d/1BiBXqb6uRFJ-gQ88uAlz9ZVdRWZPZ4vR8HAV41zB4tE/edit?usp=sharing

### Data sources ###
We collected the data Kaggle, a subsidiary of Google that allows data scientists to collect and share datasets. We used two different sets. The first set, titled “The Movies Dataset,” was published by Rounak Banik, a data scientist at the reputable Fractal Analytics. Banik extracted the information from TMDB, a movie rating website, using TMDB’s open API. Banik also gained information from GroupLens, which is a research group that publishes public data from MovieLens, a movie recommendation website. The second set, titled “IMDB Movies Extensive Dataset,” was published by Stefano Leone, a postGraduate student in Data Analytics at National College of Ireland. This public domain information was scraped from IMDB, another movie review website.

We used Java and Python to extract the data from the CSV files. We then used SQL to compile the data into tables.

### Is the source reputable? ###
We believe the source is reputable. All three sets have been downloaded and viewed many times, with “The Movies Dataset” being downloaded as many as 133,000 times. This fact means that many people have used and thus trusted this data. Additionally, the information all originated from trusted sources. TMDB, MovieLens, Rotten Tomatoes, and IMDB are all well-known movie sources. While users can post their reviews of movies, official workers at these sites must post the specific movie details, making the information more trustworthy. Furthermore, many of these data sets share movie details; across the sets, the shared details match for each movie. It would be questionable if TMDB, Rotten Tomatoes, and IMDB had different runtimes for the same movie. But, if all three sites had the same runtime, then we essentially have three checkpoints to verify that this runtime is correct. As a result of having multiple datasets with similar schemas, we can check multiple times that the information in the tables is accurate.

### Sample Generation ###
How did you generate the sample? Is it comparably small or large? Is it representative or is it likely to exhibit some kind of sampling bias?

The sample was generated using the RANDOM() function in SQL. It is comparably small. The sample contains 100 tuples from the all_movies table and 100 tuples from the keywords table, which are 0.296 % and 0.064 % of the total data points from the tables, respectively. These samples are random and thus believed to be representative of the overall dataset.

Are there any other considerations you took into account when collecting your data? This is open-ended based on your data; feel free to leave this blank. (Example: If it's user data, is it public/are they consenting to have their data used? Is the data potentially skewed in any direction?)

Users who post on these websites consent to having their review published on these public websites. To post a review, one has to make an account and agree to the terms in conditions. All websites have explicit terms and conditions that uses’ published reviews are public, and the websites have the right to use these reviews freely. For example, the IMDB terms and conditions states: “Your License to IMDb: If you do post content or submit material, and unless we indicate otherwise, you grant IMDb a nonexclusive, royalty-free, perpetual, irrevocable, and fully sublicensable right to use, reproduce, modify, adapt, publish, translate, create derivative works from, distribute, and display such content throughout the world in any media.” Lastly, users are not identifiable from just their numerical review and the average over all reviews for a given movie.

The data could potentially be skewed. This form of data is on a volunteer basis: to review, one would have to decide on their own to create an account and provide feedback for the movie. Those neutral to the movie, may decide that taking the time to write this review is not worth it. As a result, reviews could be generated from those who have significantly positive or significantly negative feelings towards the movie. This type of bias is called volunteer bias because it is common in volunteer-generated data sets. To check if bias exists, we will use a few other indicators of success, including movie revenue and critic reviews. Additionally, we found that reviews written by people over the age of 45 years old only comprise 12.7 percent of the votes in our IMDB dataset and reviews written by women only comprise 16.5 percent of the votes in our IMDB dataset. Thus, the data is also skewed by the opinions of younger, male reviewers.


### Data cleanliness ###
The data is relatively clean, as we made sure that all values of a single attribute were in the same format and joined the primary tables from the IMDb dataset and The Movies Dataset based on movies’ IMDb ID, a unique movie identifier which was common across both datasets. The data contains a plethora of information on each movie, such as languages, keywords, production companies, countries, and user ratings. We believe that this data contains what we need in order to complete our project because there are many attributes on which to analyze how users rate movies.


There are 33,748 movies in the all_movies table and 155,991 (movie, keyword) combinations in the keywords table. Over half of the movies have an original language of English (as evidenced by the pie chart below). We believe that this is a fairly high number of movies and that it is enough data to perform our analyses on.

We allowed for null values in almost all attributes of our all_movies table unless the attribute was 1) the IMDb ID (primary key), 2) related to movie ratings (e.g., vote/rating statistics like mean and median and vote counts), or 3) the month and year of release. Even so, however, null values were relatively rare; all attributes have less than 4% of its values as null. Thus, even though there are some null values for most attributes, our dataset is so large that the null values make up a very small percentage of the total values for each attribute.

In the all_movies table, there are no duplicates, as each row represents a unique movie and because of the primary key of the movie, each movie should be represented exactly one time in the table. In the keywords table, there are multiple rows for a single movie if the movie has multiple keywords associated with it. This, however, is helpful, in case we want to analyze how many movies are associated with a single keyword.

### Data distribution ###
The frequency of ratings per each rating-level is graphed below. As shown, the data is slightly right-skewed; this skew means that people tend to rate movies higher on average on IMDB. In fact, the average rating on IMDB is 7.2067 and the median rating on IMDB is 7. The maximum frequency per movie rating is 164028558, which occurs for a rating of 7. The minimum frequency of a movie rating is 9191558, which occurs for a rating of 2.

We also graphed the distribution of original movie languages. The most common original language was English, with 67.7 percent of movies being made in English.

Lastly, we found that about 10.4 percent of the movies in our dataset were part of a series.

### Data types ###
Are there any data type issues? Where are these coming from? How will you fix them?
We are changing the format of some of the data. For example, the original movie dataset had a category with a list of actors. We wanted to be able to quantify and better use this list. As a result, we counted the number of movies in the dataset for each actor. We then picked a threshold (a certain number of movies) on what qualifies a popular actor. Next, we changed the actor column to be the number of popular actors who are in the movie. Thus, instead of having a list of names, we have one clear number on how  many popular actors were featured in the movie. This singular digit is much easier when comparing the movies to each other.

From The Movies Dataset, we removed movies if the movies were only rumored to be released to the public rather than confirmed. The reason for this is that information (e.g., ratings) associated with movies which are only rumored to be released may be biased because only a select few may have had access to the movie. We also removed movies that were categorized as “adult” because we wanted to focus on movies that were accessible and appropriate for people of all ages. Lastly, we excluded movies which were missing values for at least one of the attributes included in our final all_movies table. This is because we wanted to avoid any null values in our table.

### Challenges and observations ###

One challenge we noticed while collecting our data is just how biased our reviews are. As mentioned above, we found that reviews written by people over the age of 45 years old only comprise 12.7 percent of the votes in our IMDB dataset and reviews written by women only comprise 16.5 percent of the votes in our IMDB dataset. Unfortunately, a more equal set of movie reviews does not exist due to the lower rates of tech use for older generations and the lack of female film critics. This biased data will impact our analysis because we will know that the results are not representative of the whole population. We might try to conduct comparative analysis in which we see how results compare when we give greater weight to reviews conducted by females or older people (so that the portion of reviews for each population is more equal). We will also write a discretion on how our results should be interpreted given the biased nature of our data.
