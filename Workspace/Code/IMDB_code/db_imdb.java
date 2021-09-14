import java.io.FileReader;
//import com.opencsv.CSVReader;
import java.io.BufferedReader;
import java.sql.*; //(for JDBC)
// import java.util.Objects; //(for various useful Java functions)
//import org.sqlite.JDBC;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Date;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.lang.Integer;
import java.util.Map;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class db_imdb
{

	private static int POP_THRESHOLD = 10;

	/**
	 * You are only provided with a main method, but you may create as many
	 * new methods, other classes, etc as you want: just be sure that your
	 * application is runnable using the correct shell scripts.
	 */
	public static void main(String[] args) throws Exception
	{


		System.out.println("hi");
		String imdb_movies = "IMDB/IMDb movies.csv";
		String imdb_ratings = "IMDB/IMDb ratings.csv";

		BufferedReader alReader = new BufferedReader(new FileReader(imdb_movies));
		ArrayList<String[]> movies = new ArrayList<String[]>();
		String line;
		String[] alTuple;
		Map<String, Integer> actor_pop = new HashMap<>();

		String regex = ",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)";

		alReader.readLine();
		//alReader.readLine();
		while ((line = alReader.readLine()) != null) {
			alTuple = line.split(regex, -1);
			if(alTuple[3].equals("1894")){
				alTuple[4] = "10/9/94";
			}

			if(alTuple[0].equals("tt0002199")){
				alTuple[4] = "1/1/13";
			}

			alTuple[5] = alTuple[5].replaceAll("\"", "");
			alTuple[7] = alTuple[7].replaceAll("\"", "");
			alTuple[9] = alTuple[9].replaceAll("\"", "");
			alTuple[10] = alTuple[10].replaceAll("\"", "");
			movies.add(alTuple);
			String actors = alTuple[12];
			actors = actors.replaceAll("\"", "");
			String[] actor_list = actors.split(",");
			for (String actor : actor_list) {
				if(!actor.equals("")){
				if(actor_pop.containsKey(actor)) {
					actor_pop.replace(actor, actor_pop.get(actor) + 1);
				} else {
					actor_pop.put(actor, 1);
				}
			}
			}
		}


		//create data for movie --> number of popular actors
		List<Integer> movieActorPop = new ArrayList<>();
		for (String[] movie: movies) {

			int countPopActors = 0;

			String actors = movie[12];
			actors = actors.replaceAll("\"", "");
			String[] actor_list = actors.split(",");

			if(actor_list.length > 0){
				for(String actor: actor_list) {
					if(!actor.equals("")){
					if(actor_pop.get(actor) >= POP_THRESHOLD){
						countPopActors += 1;
					}
				}
			}
		}

			movieActorPop.add(countPopActors);
		}


		BufferedReader apReader = new BufferedReader(new FileReader(imdb_ratings));

		apReader.readLine();
		ArrayList<String[]> ratings = new ArrayList<String[]>();
		String[] tempTuple; // temporary tuple to receive information from csv
		while ((line = apReader.readLine()) != null) {
			tempTuple = line.split(regex, -1);
			ratings.add(tempTuple);
		}

		// initialize the connection to the database
		Class.forName("org.sqlite.JDBC");
		String DB_FILE = "movies.db";
		Connection conn = DriverManager.getConnection("jdbc:sqlite:" + DB_FILE);

		// enable FOREIGN KEY constraint checking
		Statement stat = conn.createStatement();
		stat.executeUpdate("PRAGMA foreign_keys = OFF;");

		// speed up INSERTs
		stat.executeUpdate("PRAGMA synchronous = OFF;");
		stat.executeUpdate("PRAGMA journal_mode = MEMORY;");

		// DELETE statement to overwrite any existing data in the database
		stat.executeUpdate("DROP TABLE IF EXISTS movies;");
		stat.executeUpdate("DROP TABLE IF EXISTS ratings;");
		stat.executeUpdate("DROP TABLE IF EXISTS actors;");

		stat.executeUpdate("PRAGMA foreign_keys = ON;");

		// CREATE the mvoies table with the schema:
		stat.executeUpdate("CREATE TABLE movies "
				+ "(id CHAR(9) NOT NULL PRIMARY KEY,"
				+ "title VARCHAR(150) NOT NULL,"
				+ "original_title VARCHAR NOT NULL,"
				+ "year INTEGER NOT NULL,"
				+ "month_published INTEGER NOT NULL,"
			  + "genre VARCHAR(150) NOT NULL,"
			  + "duration INTEGER NOT NULL,"
				+ "country VARCHAR(200) NOT NULL,"
				+ "language VARCHAR(200) NOT NULL,"
				+ "director VARCHAR(200) NOT NULL,"
				+ "writer VARCHAR(200) NOT NULL,"
				+ "production_company VARCHAR(200) NOT NULL, "
				+ "popular_actors INTEGER NOT NULL);");

		// CREATE the actors table with the schema:
		stat.executeUpdate("CREATE TABLE actors "
				+ "(actor_name VARCHAR(150) PRIMARY KEY NOT NULL, "
				+ "num_movies INTEGER NOT NULL);");

		// CREATE the ratings table with the schema
		stat.executeUpdate("CREATE TABLE ratings "
				+ "(id CHAR(9) NOT NULL,"
				+ "weighted_avg_vote REAL NOT NULL, "
				+ "total_votes INTEGER NOT NULL, "
			  + "mean_vote REAL NOT NULL, "
				+ "median_vote INTEGER NOT NULL, "
				+ "votes_10 INTEGER NOT NULL, "
			  + "votes_9 INTEGER NOT NULL, "
			  + "votes_8 INTEGER NOT NULL, "
		  	+ "votes_7 INTEGER NOT NULL, "
		  	+ "votes_6 INTEGER NOT NULL, "
		  	+ "votes_5 INTEGER NOT NULL, "
			  + "votes_4 INTEGER NOT NULL, "
		  	+ "votes_3 INTEGER NOT NULL, "
		  	+ "votes_2 INTEGER NOT NULL, "
		  	+ "votes_1 INTEGER NOT NULL, "
		  	+ "us_voter_rating REAL NOT NULL, "
		  	+ "us_voter_count INTEGER NOT NULL, "
				+ "foreign_voter_rating REAL NOT NULL, "
				+ "foreign_voter_count INTEGER NOT NULL, "
				+ "male_avg_vote REAL NOT NULL,"
				+ "male_votes INTEGER NOT NULL,"
				+ "female_avg_vote REAL NOT NULL,"
				+ "female_votes INTEGER NOT NULL,"
				+ "PRIMARY KEY (id),"
				+ "FOREIGN KEY (id) references movies(id) ON DELETE CASCADE);");

		PreparedStatement prepAl = conn.prepareStatement("INSERT OR IGNORE INTO "
				+ "movies (id, title, original_title, year, month_published, genre, duration, country, language, " +
			"director, writer, production_company, popular_actors) VALUES (?,?, ?,?, ?,?, ?,?, ?,?, ?,?, ?)");

		int count = 0;
		for (String[] tuple : movies) {
				prepAl.setString(1, tuple[0]); //id
				prepAl.setString(2, tuple[1]); //title
				prepAl.setString(3, tuple[2]); //original_title

				prepAl.setInt(4, Integer.parseInt(tuple[3])); //year

				//month published
				Pattern pattern = Pattern.compile(".+?(?=/)");
				Matcher matcher = pattern.matcher(tuple[4]);
				String month;
				if(matcher.find() == false) {
					month = "0";
				} else{
					month = matcher.group();
				}

				prepAl.setInt(5, Integer.parseInt(month)); //month
				prepAl.setString(6, tuple[5]); //genre
				prepAl.setInt(7, Integer.parseInt(tuple[6])); //duration
				prepAl.setString(8, tuple[7]); //country
				if(tuple[8].equals("")){
					tuple[8] = "None";
				}
				prepAl.setString(9, tuple[8]); //language
				prepAl.setString(10, tuple[9]); //director
				prepAl.setString(11, tuple[10]); //writer
				prepAl.setString(12, tuple[11]);
				prepAl.setInt(13, movieActorPop.get(count));
				prepAl.addBatch();
				count += 1;
		}

		conn.setAutoCommit(false);
		prepAl.executeBatch();
		conn.setAutoCommit(true);

		PreparedStatement prepAp = conn.prepareStatement("INSERT OR IGNORE INTO "
				+ "actors (actor_name, num_movies) VALUES (?,?)");
		for (String tuple : actor_pop.keySet()) {

				prepAp.setString(1, tuple);
				prepAp.setInt(2, actor_pop.get(tuple));
				prepAp.addBatch();

		}

		conn.setAutoCommit(false);
		prepAp.executeBatch();
		conn.setAutoCommit(true);

		// populate flights
		PreparedStatement prepFl = conn.prepareStatement("INSERT OR IGNORE INTO ratings (id, weighted_avg_vote, " +
			"total_votes, mean_vote, median_vote, votes_10, votes_9, votes_8, votes_7, votes_6, "
			+ "votes_5, votes_4, votes_3, votes_2, votes_1, male_avg_vote, male_votes, female_avg_vote, female_votes, us_voter_rating, us_voter_count, foreign_voter_rating," +
			"foreign_voter_count) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?)");
		for (String[] tuple : ratings) {

			// only after all constraints have been checked and passed: add the tuple's info
			// into the relation
			prepFl.setString(1, tuple[0]); // id
			prepFl.setDouble(2, Double.parseDouble(tuple[1])); //weighted ag
			prepFl.setInt(3, Integer.parseInt(tuple[2])); // total_votes
			prepFl.setDouble(4, Double.parseDouble(tuple[3])); // mean_vote
			try {
				prepFl.setInt(5, Integer.parseInt(tuple[4])); // median vote
			} catch(Exception e) {
				prepFl.setInt(5, (int) Double.parseDouble(tuple[4])); // median vote
			}

			prepFl.setInt(6, Integer.parseInt(tuple[5]));
			prepFl.setInt(7, Integer.parseInt(tuple[6]));
			prepFl.setInt(8, Integer.parseInt(tuple[7]));
			prepFl.setInt(9, Integer.parseInt(tuple[8]));
			prepFl.setInt(10, Integer.parseInt(tuple[9]));
			prepFl.setInt(11, Integer.parseInt(tuple[10]));
			prepFl.setInt(12, Integer.parseInt(tuple[11]));
			prepFl.setInt(13, Integer.parseInt(tuple[12]));
			prepFl.setInt(14, Integer.parseInt(tuple[13]));
			prepFl.setInt(15, Integer.parseInt(tuple[14]));


			// avg male vote
			try {
				prepFl.setDouble(16, Double.parseDouble(tuple[23]));
			} catch(Exception e) {
				if(tuple[23].equals("")){
					continue;
				} else{
					prepFl.setDouble(16, (double)Integer.parseInt(tuple[23]));
				}
			}

			try{
				prepFl.setInt(17, Integer.parseInt(tuple[24]));
			} catch(Exception e) {
				if(tuple[24].equals("")){
					continue;
				}
			}



			// avg female vote
			try{
				prepFl.setDouble(18, Double.parseDouble(tuple[33]));
			} catch(Exception e) {
				if(tuple[33].equals("")){
					continue;
				} else{
					prepFl.setDouble(18, (double)Integer.parseInt(tuple[33]));
				}
			}

			try{
				prepFl.setInt(19, Integer.parseInt(tuple[34]));
			} catch(Exception e){
				if (tuple[34].equals("")){
					continue;
				}
			}

			// us/foreign
			try {
				prepFl.setDouble(20, Double.parseDouble(tuple[45]));
			} catch(Exception e) {
				if(tuple[45].equals("")){
					continue;
				} else {
					prepFl.setDouble(20, (double)Integer.parseInt(tuple[45]));
				}
			}

			try {
				prepFl.setInt(21, Integer.parseInt(tuple[46]));
			} catch (Exception e) {
				if(tuple[46].equals("")){
					continue;
				} else{
					prepFl.setInt(21, (int)Double.parseDouble(tuple[46]));
				}
			}
			try {
				prepFl.setDouble(22, Double.parseDouble(tuple[47]));
			} catch(Exception e) {
				if(tuple[47].equals("")){
					continue;
				} else {
					prepFl.setDouble(22, (double)Integer.parseInt(tuple[47]));
				}
			}

			try{
				prepFl.setInt(23, Integer.parseInt(tuple[48]));
			} catch(Exception e){
				continue;
			}

			// add the batch
			prepFl.addBatch();

		}

		conn.setAutoCommit(false);
		prepFl.executeBatch();
		conn.setAutoCommit(true);

	}
}
