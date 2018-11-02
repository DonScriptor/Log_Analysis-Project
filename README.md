# Installation

Here is the [news data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

To run that code you need to have to have vagrant installed and the udacity VM installed,
then go to vagrant subfolder in that VM and run vagrant up, after it finishes run vagrant ssh,
then go to shared directory cd /vagrant where yo should have newsdata.sql file with my **log.py** file.
**OR**
install [python]( https://www.python.org/downloads/ ) and [postgresql]( https://www.postgresql.org/download/ ) then in the go to direcory where **log.py** and **newsdata.sql** exist.

# Usage

# Project goals:
-- Using the (news) database we are required to obtain the following information;
  1. What are the most popular three articles of all time?
  2. Who are the most popular article authors of all time?
  3. On which days did more than 1% of requests lead to errors?

# Installation:
To run that code you need to have to have vagrant installed and the udacity VM installed,
then go to vagrant subfolder in that VM and run `vagrant up`, after it finishes run `vagrant ssh`,
then go to shared directory `cd /vagrant` where yo should have `newsdata.sql`.

# Usage

Run in bash the following command to build the database: `psql -d news -f newsdata.sql`
then execute the program by running: `python log_analysis.py` , then press enter to view results.


# Project breakdown:
-- The Log Analysis project consists of 3 file;
  1. log_analysis.py witch includes the python code for the purpose of the project.
  2. putput.txt witch holds the output of the python code.
  3. README.md witch is the readme file for the project.

# PostgreSQL code approach:
-- the (news) database contains 3 tables:
1. The (authors) table includes information about the authors of articles.
2. The (articles) table includes the articles themselves.
3. The (log) table includes one entry for each time a user has accessed the site.
4. Since the (articles) table holds the articles titles and the (log) table holds the view count, we need to find a column match between the two articles to be able to perform a join and a count aggregation.
4. The (slug) column in the (articles) table can seems to match the (path) column from the (log) table.
5. I tried to use the REPLACE function to remove the '/article/' string from the (path) column in the log table but was unsuccessful to match the result with the (slug) column from the (articles) table due to the (log.path) column containing some empty entries.
6. I used the concatenation operator (||) instead to add the string '/article/' to the (articles.slug) column.

# Online Resources:
1.[http://www.postgresqltutorial.com/postgresql-replace/]
2.[https://www.postgresql.org/docs/6.3/static/c09.htm]
3.[https://stackoverflow.com/questions/9477651/sql-remove-sub-string-from-a-columns-text]
4.[https://www.tutorialspoint.com/postgresql/postgresql_views.htm]
5.[https://www.postgresql.org/docs/9.1/static/functions-datetime.html]
6.[https://www.tutorialspoint.com/postgresql/postgresql_using_joins.htm]
7.[https://developers.google.com/edu/python/strings]
8.[https://www.postgresql.org/docs/current/static/datatype-numeric.html]

# python code approach:
-- the log_analysis.py file contain the code for executing the needed PostgreSQL queries and can be refactored in different ways:
  1. There can be 3 functions to execute the 3 different queries, in each function we connect to the news database, create a cursor, execute the query using the cursor, than printing the output.
  2. There can be 3 functions as step 1, but we can define the connection variable and the cursor
  as global variable and use them throughout the project instead of defining them every time inside each function. (this is the approach I prefer)
  3. There can be only one function that executes all the required queries.
  4. There also can be a class that takes in the database name, query and action to be executed on the query and returns the result.[like Movie_Trailer Project!!]




# Code breakdown:
-- Since this is a PostgreSQL database, the psycopg2 module needs to be imported to adapt the database and python.
-- A global variable for connecting to the news database has been declared and initialized.
-- A global variable for creating a cursor method on the connection has been declared and initialized.
1. First function get_popular_articles().
  * this function returns the top 3 most popular article from the database.
  * inside this function a variable holds the database query is used and passed to the execute methode.
  * fetchall method is then used to capture all the output of the execute method and passed the result to a local variable for further processing.
  * the query



2. Second function get_popular_articles().

* I have created a view slugtopath to make a relatioon between log and articles tables.
* created another view by joining theview we made with log table.
'''
  CREATE VIEW rawPath as SELECT '/article/' || slug
  as path, title from articles;
  CREATE VIEW viewsCount as  SELECT title, count(log.id)
  as views from rawPath left join log on rawPath.path = log.path
   group by title;
  select * from viewsCount order by views desc limit(3);
  '''
2. Third function network_errors().

* I have created a view status to get date(time) and format it , also count total requests per day from log.
* then i created couple of other views to get the fail attempts per day from the log table by actually getting all the statuses that doesn't equal 200 ok.
* then selected the fail rate an divided it over the over all attempts per day count to get the percentage > 1%
   
