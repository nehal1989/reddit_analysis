import sqlite3
import os
import praw
import csv
from collections import namedtuple


with open('most_subbed.csv') as file:
    reader = csv.reader(file)
    most_subbed_list = [row[0] for row in reader]

# Make SQLite database file
current_directory = os.path.dirname(os.path.realpath(__file__))
targer_folder = 'data'
database_name = 'post_database.db'
complete_path = os.path.join(current_directory, targer_folder, database_name)

db_exist = os.path.isfile(complete_path)

if db_exist:
    pass
else:
    db = sqlite3.connect(complete_path)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE submissionInfo (
                    id INTEGER PRIMARY KEY,
                    title text,
                    upvotes int,
                    post_id text,
                    url text,
                    num_comments int,
                    timestamp real,
                    upvoteratio real,
                    subreddit_name text
    )""")
    db.close()


# Load reddit login details and log into api
with open('reddit.config') as file:
    login_details = file.read().splitlines()

reddit = praw.Reddit(client_id=login_details[0],
                     client_secret=login_details[1],
                     password=login_details[2],
                     user_agent=login_details[3],
                     username=login_details[4])

print(reddit.user.me())


# Get subreddit

number_of_subreddits = 50

for i in range(number_of_subreddits):
    subreddit_name = most_subbed_list[i]
    subreddit_instance = reddit.subreddit(subreddit_name)
    submissions = subreddit_instance.hot(limit=1000)

    # Organise data
    submission_data = namedtuple('submission_data', 'title score post_id url num_comments timestamp '
                                                    'upvoteratio subreddit_name')

    list_of_submissions = []


    for idx, sub in enumerate(submissions, 1):
        if sub.stickied is False:
            print(f"Getting submission {idx} from {subreddit_name}")
            list_of_submissions.append(submission_data(title=sub.title,
                                                score=sub.score,
                                                post_id=sub.id,
                                                url=sub.url,
                                                num_comments=sub.num_comments,
                                                timestamp=sub.created,
                                                upvoteratio=sub.upvote_ratio,
                                                subreddit_name=subreddit_name))


    db = sqlite3.connect(complete_path)
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO
                        submissionInfo(title, upvotes, post_id, url, num_comments, timestamp, upvoteratio, subreddit_name)
                        VALUES(?,?,?,?,?,?,?,?)""", list_of_submissions)
    # remove duplicates
    cursor.execute("""
    DELETE FROM submissionInfo WHERE rowid NOT IN (SELECT min(rowid) FROM submissionInfo GROUP BY post_id, id)
    """)

    db.commit()  # Commit changes to the DB
    db.close()
