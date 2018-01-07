import os
from twython import Twython
from twython import TwythonAuthError
from twython import TwythonRateLimitError
from twython import TwythonError
from warnings import warn
from time import time
from time import sleep
import math
from datetime import datetime

#Twitter API credentials
consumer_key = "lKNAlxQopd6077oSoMuh5gJWE"
consumer_secret = "w3uPQJc3LL0hFcOQhJI5OzKjSQPcbqpalZCMqaZxkIMykHyRgr"
access_token = "700526419168735232-Ts8k2NMLdF74Y6yY8pb1GPe8gJ4rdzU"
access_secret = "YOyF3FWQ4Ne5ZNAx03alQlCdfsBG4ibuxzY9uc6ZOj8t4"

def get_user_tweets(screen_name=None, user_id=None, num=0, include_rts=False):

    twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)

    tweets = None
    while(tweets == None):
        try:
            if screen_name == None:
                tweets = twitter.get_user_timeline(user_id = user_id, count = 200, trim_user = 1, include_rts = include_rts)
            else:
                tweets = twitter.get_user_timeline(screen_name = screen_name, count = 200, trim_user = 1, include_rts = include_rts)
        except TwythonRateLimitError:
            remainder = math.fabs(math.ceil(float(twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time()))
            print("Waiting for {} secs...".format(remainder))
            sleep(remainder)
            print("tweets Reconnecting...")
            continue
        except  TwythonAuthError:
            print ("tweets Bad Authentication")
            return []
        except TwythonError:
            print ("tweets 404 not found")
            continue

    totalTweets = tweets
    while len(tweets) >= 2:
        max_id = tweets[-1]["id"]
        try:
            if screen_name == None:
                tweets = twitter.get_user_timeline(user_id = user_id, max_id = max_id, count = 200, trim_user = 1, include_rts = include_rts )
            else:
                tweets = twitter.get_user_timeline(screen_name = screen_name, max_id = max_id, count = 200, trim_user = 1, include_rts = include_rts )

        except TwythonRateLimitError:
            remainder = math.fabs(math.ceil(float(twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time()))
            print("Waiting for {} secs...".format(remainder))
            sleep(remainder)
            print("tweets Reconnecting...")
            continue
        except TwythonError:
            print('tweets twythonerror')
            # return[]
            continue

        if len(tweets) > 1:
            totalTweets += tweets[1:]
        elif num > 0 and len(tweets) >= num:
            break

    for i in range(len(totalTweets)):
        date = totalTweets[i]["created_at"]
        totalTweets[i]["created_at"] = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')

    if num == 0:    # 'num' is used to decide getting all tweets or latest limited tweets
        return totalTweets
    else:
        return totalTweets[:num]

if __name__ == '__main__':

    save_folder = "tweet_users_with_gender"

    with open("available_users", "r") as input_file:
        for line in input_file.readlines():
            data = line.strip().split("\t")
            userID = data[0]
            screen_name = data[1]

            if os.path.exists(save_folder + '/' + userID):
                print('Duplicate user: ' + screen_name +'\n')
                continue

            print("Start to get "+ screen_name + "'s tweets...")
            output_list = get_user_tweets(screen_name, userID)

            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            output_content = ""
            with open(save_folder + '/' + userID,'a') as output_file:
                for item in output_list:
                    output_content += "{}\t{}\t{}\t{}\n".format(userID, screen_name, item["created_at"], " ".join(item["text"].split("\n")))
                output_file.write(output_content)
            print("Finish getting tweets...")
            print("\n")
