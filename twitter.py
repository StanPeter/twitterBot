#twitter Bot
import tweepy, os, time
from dotenv import load_dotenv

load_dotenv()


consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

#authorization for tweeter account, need to open a developer account there to get keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#if you have many tweets its better to put some restrictions
def get_published_tweets():
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

def limit_handler(cursor):  #if sent too many get requests sleep()
    try:
        while True:
            yield cursor.next() 
    except tweepy.RateLimitError:
        time.sleep(1000)

def follower_bot(name_to_follow): #Bot to follow people filtered by name
    for follower in limit_handler(tweepy.Cursor(api.followers).items()):
        if follower.name == name_to_follow:
            follower.follow()
            break

#phrase/word you want to search for + number of tweets you want to like(set as favourite) containing the phrase/word
def liking_bot(searched_phrase, num_of_tweets): 
    for tweet in limit_handler(tweepy.Cursor(api.search, searched_phrase).items(num_of_tweets)):
        try:
            tweet.favorite()    #Tweet was liked
        except tweepy.TweepyError as e:
            print(e.reason)
        except StopIteration:
            break
