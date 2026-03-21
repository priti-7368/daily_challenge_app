import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Users
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT UNIQUE,
password TEXT
)
""")

# Categories
cur.execute("""
CREATE TABLE IF NOT EXISTS categories(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT
)
""")

# Challenges
cur.execute("""
CREATE TABLE IF NOT EXISTS challenges(
id INTEGER PRIMARY KEY AUTOINCREMENT,
category_id INTEGER,
challenge_text TEXT
)
""")

# User challenge tracking
cur.execute("""
CREATE TABLE IF NOT EXISTS user_challenges(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
challenge_id INTEGER,
date TEXT,
status TEXT
)
""")

# Reflections
cur.execute("""
CREATE TABLE IF NOT EXISTS reflections(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
date TEXT,
note TEXT
)
""")

# Insert categories
cur.execute("INSERT INTO categories(name) VALUES ('Health')")
cur.execute("INSERT INTO categories(name) VALUES ('Learning')")
cur.execute("INSERT INTO categories(name) VALUES (Productivity')")
cur.execute("INSERT INTO categories(name) VALUES ('Creativity')")

# Insert challenges

cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Walk for 15 minutes')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Eat one fruit today')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Take a 10 minute walk outside')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Sleep at least 7 hours tonight')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Do 5 minutes of deep breathing')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Avoid junk food for the day')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Stretch your body for 5 minutes')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Drink a glass of warm water in morning')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Eat a healthy breakfast')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Avoid sugary drinks today')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Relax your eyes for 5 minutes')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (1,'Drink 8 glasses of water')")

cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Read 5 pages of a book')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Learn a new English word')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Read 10 pages of a book')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Watch an educational video')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Learn 3 new English words')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Write a short summary of what you learned')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Practice coding for 20 minutes')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Search and learn one new concept online')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Write one paragraph in English')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Read a motivational article')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Learn one new shortcut in computer')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (2,'Revise something you learned yesterday')")

cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Clean your workspace')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Plan tomorrow tasks')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Do 10 push ups')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Walk 5000 steps today')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Do 20 squats')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Stretch for 10 minutes')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Do a 10 minute workout')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Try 5 minutes of yoga')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Climb stairs for 5 minutes')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Jog in place for 3 minutes')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Do 15 jumping jacks')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (3,'Stretch your legs for 5 minutes')")

cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Write 3 lines of a poem')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Draw a simple sketch')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Write your goals for today')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Complete one pending task')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Organize your study table')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Avoid social media for 1 hour')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Make a to do list')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Focus on one task for 25 minutes')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Clean one folder in your computer')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Delete unnecessary files')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Plan your tasks for tomorrow')")
cur.execute("INSERT INTO challenges(category_id,challenge_text) VALUES (4,'Write down one achievement of today')")

conn.commit()
conn.close()

print("Database created successfully")