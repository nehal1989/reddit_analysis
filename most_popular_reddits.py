import re
import csv

with open('subreddit_list.txt') as file:
    my_regex = re.compile(r"/r/(.*) -")
    list_of_subreddits = []
    for lines in file.readlines():
        reg_results = my_regex.search(lines.strip())
        list_of_subreddits.append(reg_results.group(1))

output_filename = "/Users/Nehal/Dropbox/Programming/Reddit_Project/most_subscribed_cleaned_subreddits.csv"

with open(output_filename, "w", newline='') as output:
    writer = csv.writer(output)
    for val in list_of_subreddits:
        writer.writerow([val])

with open()