#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def top_articles():
    """Retrieve most popular three articles of all time"""
    try:
        conn = psycopg2.connect(database=DBNAME)
        cursor = conn.cursor()
        cursor.execute("select title, total_viewed_articles from \
                       top_articles_view")
        articles = cursor.fetchall()
        print("The following are the most popular three articles of all time:")
        print("=" * 75)
        print("\n")

        for row in articles:

            print('. "{}" - {} views'.format(row[0], row[1]))

            cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()


def authors_all_times():
    """Retrieve most popular article authors of all time"""
    try:
        conn = psycopg2.connect(database=DBNAME)
        cursor = conn.cursor()
        cursor.execute("select name, sum from authors_all_times_view")
        authors = cursor.fetchall()
        print("\n")
        print("The following are the most popular article authors \
              of all time:")
        print("=" * 75)
        print("\n")
        for row in authors:
            print('. {} - {} views'.format(row[0], row[1]))
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        conn.close()


def visits_per_day():
    """Retrieve days with greater than a percent request error """
    try:
        conn = psycopg2.connect(database=DBNAME)
        cursor = conn.cursor()
        cursor.execute("select day, percentage_failure from visits_per_day_view \
                       where percentage_failure > 1.0")
        days = cursor.fetchall()
        print("\n")
        print("Following are days which more than 1 percent of requests \
              lead to errors:")
        print("=" * 75)
        print("\n")

        for row in days:
            print('. {} - {}% errors'.format(row[0], row[1]))
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        conn.close()


if __name__ == '__main__':
    top_articles()
    authors_all_times()
    visits_per_day()
