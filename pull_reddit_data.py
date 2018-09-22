import pandas
import praw
import datetime as dt

with open('reddit.config') as file:
    login_details = file.read().splitlines()

reddit = praw.Reddit(client_id=login_details[0], \
                     client_secret=login_details[1], \
                     user_agent=login_details[2], \
                     username=login_details[3], \
                     password=login_details[4])

