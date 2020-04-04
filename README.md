# CORD-19 database
 A SQLite database for CORD-19

There are two tables in this database.

papers
```sql
CREATE TABLE "papers" (
	"paper_id"	TEXT,
	"title"	TEXT,
	"abstract"	TEXT,
	"subset_type"	TEXT,
	PRIMARY KEY("paper_id")
);
```

body_text
```sql
CREATE TABLE "body_text" (
	"paper_id"	TEXT NOT NULL,
	"paragraph_id"	INTEGER NOT NULL,
	"section"	TEXT,
	"text"	TEXT,
	PRIMARY KEY("paragraph_id","paper_id")
);
```