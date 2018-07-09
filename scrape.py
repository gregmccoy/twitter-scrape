import twitter
from twython import Twython
import json
import pprint
import argparse
import os
from auth_keys import *

parser = argparse.ArgumentParser()
parser.add_argument("--output", dest="output", help="File to save to")
parser.add_argument("--geo", dest='geo', help="Use only tweets with geo available")
parser.add_argument("--popular", action='store_true', help="Sort by popular")
parser.add_argument("search", help="Search")
args = parser.parse_args()


class TwitterSearch():
    def __init__(self, args):
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        twitter = Twython(APP_KEY, APP_SECRET)
        self.twitter = twitter
        self.tweet_mode = "extended"
        if args.output:
            self.filename = args.output

        if args.geo:
            self.geo = args.geo
        else:
            self.geo = False

        if args.popular:
            self.result_type = 'popular'
        else:
            self.result_type = 'mixed'

        if args.search:
            self.search = args.search
        else:
            print("Please provide a search term")
            raise Exeception


    def run_search(self):
        try:
            personal = ["I ", "I'm ", " me", " mine", "I've "]
            query = '{} exclude:retweets'.format(self.search)


            if self.geo:
                print("Using GEO {}".format(self.geo))
                search_results = self.twitter.search(q=query, count=50, lang="en", is_quote_status=False, geocode=self.geo, result_type=self.result_type, tweet_mode=self.tweet_mode)
            else:
                search_results = self.twitter.search(q=query, count=50, lang="en", is_quote_status=False, tweet_mode=self.tweet_mode)

            with open(self.filename, 'w') as f:
                json_data = "["
                for tweet in search_results['statuses']:
                    #for i in personal:
                    #    if i in tweet["text"]:
                    #print(i)
                    print("User: {}".format(tweet["user"]["name"].encode("utf-8")))
                    print("Tweet: {}".format(tweet["full_text"].encode("utf-8")))
                    print("Location: {}".format(tweet["user"]["location"]))
                    print("Date: {}".format(tweet["created_at"]))
                    print("Retweets: {}".format(tweet["retweet_count"]))
                    print("Favourites: {}".format(tweet["favorite_count"]))
                    print("---")
                            #continue
                    data = {
                        "name": tweet["user"]["screen_name"],
                        "text": tweet["full_text"],
                        "created_at": tweet["created_at"],
                        "favorite_count": tweet["favorite_count"],
                        "retweet_count": tweet["retweet_count"],
                        "location": tweet["user"]["location"],
                    }
                    json_data = json_data + json.dumps(data) + ","
                json_data = json_data[:-1] + "]"
                f.write(json_data)
        except Exception as e:
            print(e)
            return None

tw_search = TwitterSearch(args)
tw_search.run_search()
