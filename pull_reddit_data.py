import praw

with open('reddit.config') as file:
    login_details = file.read().splitlines()

reddit = praw.Reddit(client_id=login_details[0],
                     client_secret=login_details[1],
                     password=login_details[2],
                     user_agent=login_details[3],
                     username=login_details[4])

print(reddit.user.me())

climbing_sr = reddit.subreddit('Climbing')

top_climbing = climbing_sr.top(limit=10)

for thing in top_climbing:
    print(thing.title)
