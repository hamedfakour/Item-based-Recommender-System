import tweepy
import pysolr
import urllib


# setting Twitter API authentications parameters
# see this link for more info: https://developer.twitter.com/en
def TwitterAuthentication():
    API_KEY = 'U5BwOlOkXK2DsMYNmw23Kwn1t'
    API_SECRET = '2lbcFwi4HfyEr5NVnUgyoAuARVxpnwsBCreBUA5PhLw6NNdO4W'
    ACCESS_TOKEN = '884326388731432960-uqCitvAc0QqbyNUyCxfX3VewTnUnbca'
    ACCESS_TOKEN_SECRET = '9z6CeUDAd15zChiKRLmGa63NtUlb0oAeWPZzKda966kH7'
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


# Search movie name by twitter api (tweepy) and get response
def Search(auth, movie_name, max_tweets, movie_id):
    api = tweepy.API(auth)
    searched_tweets = []
    searched_users = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=movie_name, lang='en', count=count, max_id=str(last_id - 1))
            for status in new_tweets:
                tweet, user = StatusParser(status, movie_id)
                searched_tweets.append(tweet)
                searched_users.append(user)
            if not new_tweets:
                break
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print('Twitter API Error (Reason): ', e.reason)
            break
    return searched_tweets, searched_users


# Get tweet status and parse fields in tow dictionaries (tweet and user)
def StatusParser(status, movie_id):
    tweet = {
        'id': status.id,
        'user_id': status.author.id,
        'user_name': status.author.screen_name,
        'like_count': status.favorite_count,
        'retweet_count': status.retweet_count,
        'content': status.text,
        'date': status.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        'hashtags': status.entities['hashtags'],
        'movie_id': movie_id
    }
    user = {
        'user_id': status.author.id,
        'user_name': status.author.screen_name,
        'user_title': status.author.name,
        'description': status.author.description,
        'like_count': status.author.favourites_count,
        'creation_date': status.author.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        'follower_count': status.author.followers_count,
        'following_count': status.author.friends_count,
        'location': status.author.location,
        'is_verified': status.author.verified*1,
        'is_private': status.author.protected*1,
        'isGeoEnabled': status.author.geo_enabled,
        'list_count': status.author.listed_count,
        'profile_image_url': status.author.profile_image_url,
        'profileBackgroundImageUrl': status.author.profile_image_url_https,
        'tweet_count': status.author.statuses_count
    }
    return tweet, user


# Save tweets in Apache Solr
# documents: tweets or users information
# index_name: apache solr index name
def SolrCommit(documents, index_name):
    password = urllib.parse.quote('Solr@123', safe='')
    solr_address = 'http://solr:{0}@81.28.53.10:9998/solr/{}'.format(password, index_name)
    try:
        solr = pysolr.Solr(solr_address, timeout=30)
        solr.add(documents, commit=False, softCommit=True)
        print('Solr {} documents Commited'.format(solr_address))
    except Exception as err:
        print("SolrCommit Exception ({})".format(solr_address))
        print("Casuse: %s" % err)


# Read movies.csv file and save contents in the list
def readMoviesFile():
    movies_file_path = 'resources/movies.csv'
    movies = {}
    with open(movies_file_path, 'r') as f:
        lines = f.readlines()
        for row in lines:
            fields = row.strip().split('*')
            movies[fields[0]] = fields[1]
    return movies


# Main function for run another functions
# 1. Read Movies name and ID
# 2. Search movies in twitter and get response
# 3. Save tweets in apache solr
def RunTweetsSearch():
    movies = readMoviesFile()
    auth = TwitterAuthentication()
    max_tweets = 5
    for movie_id in movies:
        movie_name = movies[movie_id]
        tweets, users = Search(auth, movie_name, max_tweets, movie_id)
        print(len(tweets))
        SolrCommit(tweets, 'english_tweets')
        SolrCommit(users, 'twitter_user_english')


RunTweetsSearch()
