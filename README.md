# log_analysis
---
The log_analysis tool, a reporting tool used to draw business conclusions, from data captured in a backend database. The reporting tool prints out reports in plain text.
# Design
---
The business logic is implemented within the backend database, in the way of:
- Joins 
- Use of aggregations 
- Views

This is to simplify the extraction of needed reporting information by leveraging the Python DB-API, issuing the execution of single database queries within Python code.

# How to Run Tool
---
#### Prerequisites
psycopg2 module
PostgreSQL Database
**Database Tables:**
- authors
- articles
- log

**Database Views:**
- **author_article_view**
**-Create View Command:**

```sql
CREATE OR REPLACE VIEW AUTHOR_ARTICLE_VIEW AS
SELECT A.NAME,
       AE.TITLE,
       L.TIME,
       to_char(L.TIME::date, 'MonthDD, YYYY') AS DAY,
       COUNT(AE.TITLE) AS VIEWED_ARTICLES,
       L.STATUS
FROM AUTHORS A
INNER JOIN ARTICLES AE ON A.ID = AE.AUTHOR
RIGHT JOIN LOG L ON AE.SLUG = SUBSTRING(L.PATH FROM 10)

GROUP BY A.NAME,
         AE.TITLE,
         L.TIME,
         L.STATUS
ORDER BY A.NAME ASC;
```


- **top_articles_view**
-**Create View Command:**

```sql
CREATE OR REPLACE VIEW TOP_ARTICLES_VIEW AS
SELECT NAME,
       TITLE,
       SUM(VIEWED_ARTICLES) AS TOTAL_VIEWED_ARTICLES
FROM AUTHOR_ARTICLE_VIEW
WHERE NAME IS NOT NULL
  AND STATUS = '200 OK'
GROUP BY NAME,
         TITLE
ORDER BY SUM(VIEWED_ARTICLES) DESC
LIMIT 3;
```


- **authors_all_times_view**
-**Create View Command:**

```sql
CREATE OR REPLACE VIEW AUTHORS_ALL_TIMES_VIEW AS
SELECT NAME,
       SUM(TOTAL_VIEWED_ARTICLES)
FROM
  ( SELECT NAME,
           TITLE,
           SUM(VIEWED_ARTICLES) AS TOTAL_VIEWED_ARTICLES
   FROM AUTHOR_ARTICLE_VIEW
   WHERE NAME IS NOT NULL
     AND STATUS = '200 OK'
   GROUP BY NAME,
            TITLE
   ORDER BY SUM(VIEWED_ARTICLES) DESC) AS TOP_ARTICLES
GROUP BY NAME
ORDER BY SUM(TOTAL_VIEWED_ARTICLES) DESC;
```


- **visits_per_day_view**
-**Create View Command:**

```sql
CREATE OR REPLACE VIEW VISITS_PER_DAY_VIEW AS
SELECT DAY,
       TOTAL_ACCESS_COUNT,
       SUCCESS,
       FAILURE,
       ROUND((FAILURE::decimal * 100) / TOTAL_ACCESS_COUNT, 1) AS PERCENTAGE_FAILURE
FROM
  ( SELECT DAY,
           COUNT(AA.STATUS) AS TOTAL_ACCESS_COUNT,

     ( SELECT COUNT(AB.STATUS)
      FROM AUTHOR_ARTICLE_VIEW AB
      WHERE AB.STATUS = '200 OK'
        AND AB.DAY = AA.DAY ) AS SUCCESS,

     ( SELECT COUNT(AC.STATUS)
      FROM AUTHOR_ARTICLE_VIEW AC
      WHERE AC.STATUS <> '200 OK'
        AND AC.DAY = AA.DAY ) AS FAILURE
   FROM AUTHOR_ARTICLE_VIEW AA
   GROUP BY DAY) VISITS
ORDER BY ROUND((FAILURE::decimal * 100) / TOTAL_ACCESS_COUNT, 1) DESC;
```

#### Run Tool:
***Command Line:***
python log_analysis.py










