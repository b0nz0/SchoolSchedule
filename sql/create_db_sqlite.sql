BEGIN TRANSACTION;
DROP TABLE IF EXISTS "school";
CREATE TABLE IF NOT EXISTS "school" (
	"name"	VARCHAR(30) NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "school_year";
CREATE TABLE IF NOT EXISTS "school_year" (
	"identifier"	VARCHAR NOT NULL,
	"school_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	FOREIGN KEY("school_id") REFERENCES "school"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "year";
CREATE TABLE IF NOT EXISTS "year" (
	"identifier"	VARCHAR NOT NULL,
	"school_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	FOREIGN KEY("school_id") REFERENCES "school"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "section";
CREATE TABLE IF NOT EXISTS "section" (
	"identifier"	VARCHAR NOT NULL,
	"school_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	FOREIGN KEY("school_id") REFERENCES "school"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "room";
CREATE TABLE IF NOT EXISTS "room" (
	"identifier"	VARCHAR NOT NULL,
	"room_type"	VARCHAR(11),
	"school_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	FOREIGN KEY("school_id") REFERENCES "school"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "person";
CREATE TABLE IF NOT EXISTS "person" (
	"fullname"	VARCHAR NOT NULL,
	"title"	VARCHAR,
	"is_impersonal"	BOOLEAN NOT NULL,
	"person_type"	VARCHAR(13),
	"school_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	FOREIGN KEY("school_id") REFERENCES "school"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "hour";
CREATE TABLE IF NOT EXISTS "hour" (
	"school_id"	INTEGER NOT NULL,
	"start"	TIME NOT NULL,
	"minutes"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	FOREIGN KEY("school_id") REFERENCES "school"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "plan";
CREATE TABLE IF NOT EXISTS "plan" (
	"school_id"	INTEGER NOT NULL,
	"identifier"	VARCHAR NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	FOREIGN KEY("school_id") REFERENCES "school"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "class_";
CREATE TABLE IF NOT EXISTS "class_" (
	"school_year_id"	INTEGER NOT NULL,
	"year_id"	INTEGER NOT NULL,
	"section_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("year_id") REFERENCES "year"("id"),
	FOREIGN KEY("section_id") REFERENCES "section"("id"),
	FOREIGN KEY("school_year_id") REFERENCES "school_year"("id")
);
DROP TABLE IF EXISTS "daily_hour";
CREATE TABLE IF NOT EXISTS "daily_hour" (
	"plan_id"	INTEGER NOT NULL,
	"week_day"	VARCHAR(9) NOT NULL,
	"ordinal"	INTEGER NOT NULL,
	"hour_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("hour_id") REFERENCES "hour"("id"),
	FOREIGN KEY("plan_id") REFERENCES "plan"("id")
);
DROP TABLE IF EXISTS "constraint";
CREATE TABLE IF NOT EXISTS "constraint" (
	"school_year_id"	INTEGER NOT NULL,
	"engine_id"	INTEGER,
	"identifier"	VARCHAR NOT NULL,
	"kind"	VARCHAR NOT NULL,
	"score"	INTEGER NOT NULL,
	"configuration"	VARCHAR NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("school_year_id") REFERENCES "school_year"("id")
);
DROP TABLE IF EXISTS "subject_in_class";
CREATE TABLE IF NOT EXISTS "subject_in_class" (
	"hours_total"	INTEGER NOT NULL,
	"max_hours_per_day"	INTEGER,
	"class_id"	INTEGER NOT NULL,
	"subject_id"	INTEGER NOT NULL,
	"room_id"	INTEGER,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("room_id") REFERENCES "room"("id"),
	FOREIGN KEY("subject_id") REFERENCES "subject"("id"),
	FOREIGN KEY("class_id") REFERENCES "class_"("id")
);
DROP TABLE IF EXISTS "class_plan";
CREATE TABLE IF NOT EXISTS "class_plan" (
	"plan_id"	INTEGER NOT NULL,
	"class_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("plan_id") REFERENCES "plan"("id"),
	FOREIGN KEY("class_id") REFERENCES "class_"("id")
);
DROP TABLE IF EXISTS "person_to_subject_in_class";
CREATE TABLE IF NOT EXISTS "person_to_subject_in_class" (
	"subject_in_class_id"	INTEGER NOT NULL,
	"person_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("subject_in_class_id") REFERENCES "subject_in_class"("id"),
	FOREIGN KEY("person_id") REFERENCES "person"("id")
);
DROP TABLE IF EXISTS "subject";
CREATE TABLE IF NOT EXISTS "subject" (
	"identifier"	VARCHAR NOT NULL,
	"default_hours"	INTEGER,
	"preferred_consecutive_hours"	INTEGER,
	"school_id"	INTEGER NOT NULL,
	"id"	INTEGER,
	"start_datetime"	DATETIME,
	"log_user"	VARCHAR,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("school_id") REFERENCES "school"("id")
);
COMMIT;
