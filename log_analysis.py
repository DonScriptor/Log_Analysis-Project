#!/usr/bin/env python2.7

# Modules Imports
# importing psycopg2 for adapting posrgesql to python
import psycopg2


def get_popular_articles():
    """ First Function: getting the most popular 3 articles """
    DBNAME = "news"  # news DataBase constant
    # connecting to the news PostgreSQL database using psycopg2 adapter
    db_conn = psycopg2.connect(database=DBNAME)
    cursor = db_conn.cursor()  # creating a cursor
    db_query = '''
    CREATE VIEW rawPath as SELECT '/article/' || slug
    as path, title from articles;
    CREATE VIEW viewsCount as  SELECT title, count(log.id)
    as views from rawPath left join log on rawPath.path = log.path
     group by title;
    select * from viewsCount order by views desc limit(3);
               '''  # multi-line query
    cursor.execute(db_query)  # executing the postgresql query
    # fetching all the result and storing them in a variable
    popular_articles = cursor.fetchall()
    print "\n* The most popular three articles of all time:"
    for article in popular_articles:
        articleViews = ' - '.join(map(str, (article)))
        print(articleViews + ' views')
    db_conn.close()

get_popular_articles()


def get_top_authors():
    DBNAME = "news"  # news DataBase constant
    # connecting to the news PostgreSQL database using psycopg2 adapter
    db_conn = psycopg2.connect(database=DBNAME)
    cursor = db_conn.cursor()  # creating a cursor
    db_query = '''
    CREATE VIEW Pathwithauthor as SELECT '/article/' || slug as
     rawPath, author, title from articles;
    CREATE VIEW articlescount as SELECT author, title, id, COUNT(log.id) as
     views from pathwithauthor
    left join log on pathwithauthor.rawPath = log.path group by title,
     author, id order by views desc;
    select name, sum(views) as viewscount from articlescount
     join authors on author = authors.id
     group by name order by viewscount desc limit(3);
               '''  # storing our quey in a variable for convenience
    cursor.execute(db_query)  # executing the postgresql query
    top_authors = cursor.fetchall()  # fetching all the result
    print "\n* The most popular article authors of all time:"
    for author in top_authors:
        topAuthrors = ' - '.join(map(str, (author)))
        print(topAuthrors + ' views')
    db_conn.close()

get_top_authors()


def network_errors():
    DBNAME = "news"  # news DataBase constant
    # connecting to the news PostgreSQL database using psycopg2 adapter
    db_conn = psycopg2.connect(database=DBNAME)
    cursor = db_conn.cursor()  # creating a cursor
    db_query = '''
    create view total_count as select date(time) as dateDays,
    count(*) as total from log group by dateDays order by total desc;
    create view error_count as select count(*) as total_errors,
    date(time) as dateDays from log where status <> '200 OK'
    group by dateDays order by total_errors desc;
    create view error_percentage as select total_count.dateDays,
    (error_count.total_errors :: float/total_count.total)*100 as
    fail_percent from error_count join total_count on
    error_count.dateDays = total_count.dateDays;
    select dateDays, fail_percent from error_percentage
    where fail_percent > 1.0;
               '''
    cursor.execute(db_query)  # executing the postgresql query
    errors_percentage = cursor.fetchall()  # fetching all the result
    print "\n* error messages percentage more than 1 %"
    for error in errors_percentage:
        print(error[0], error[1])
        print" --------------------------------- "
    db_conn.close()


network_errors()
