import requests
import bs4
import csv

recent_activity = []
most_subscribed = []
most_growth = []

number_of_pages = 34

for page_number in range(1, number_of_pages+1):
    URL = f'http://redditlist.com/?page={page_number}'

    req = requests.get(URL)
    req.raise_for_status()

    soup = bs4.BeautifulSoup(req.text, 'html.parser')

    all_subreddits = soup.select('.listing-item')
    data_per_column = int(len(all_subreddits)/3)

    list_of_subreddits = []
    for subs in all_subreddits:
        list_of_subreddits.append(subs.attrs['data-target-subreddit'])

    recent_activity = recent_activity + list_of_subreddits[0:data_per_column*1]
    most_subscribed = most_subscribed + list_of_subreddits[data_per_column:data_per_column*2]
    most_growth = most_growth + list_of_subreddits[data_per_column*2:data_per_column*3]

output_filename = "/Users/Nehal/Dropbox/Programming/Reddit_Project/most_subscribed_subreddits.csv"

with open(output_filename, "w", newline='') as output:
    writer = csv.writer(output)
    for val in most_subscribed:
        writer.writerow([val])
