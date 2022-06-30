
import pysolr
import urllib.parse

ratings_file_path = 'resources/ratings.csv'
movies_file_path = 'resources/movies.csv'
features_file_path = 'resources/FeaturesMovies.csv'
password = urllib.parse.quote('Solr@123', safe='')
solr_base_url = 'http://solr:{0}@81.28.53.10:9998/solr/'.format(password)


# Read ratings.csv file and save contents in the dectionary
def readRatingFile():
    result = {}
    with open(ratings_file_path, 'r') as f:
        lines = f.readlines()
        for row in lines:
            fields = row.split('*')
            if(fields[0] in result):
                movies = result.get(fields[0])
                movies[fields[1]] = fields[2].strip()
                result[fields[0]] = movies
            else:
                movies = {fields[1]: fields[2].strip()}
                result[fields[0]] = movies
    return result


# Read movies.csv file and save contents in the list
def readMoviesFile():
    movies = []
    with open(movies_file_path, 'r') as f:
        lines = f.readlines()
        for row in lines:
            fields = row.split('*')
            movies.append(fields[0])
    return movies


# Search tweets in Solr by movie_id value and get Sentiments features
def SolrSearchTweets(movie_id):
    solr = pysolr.Solr(solr_base_url+'english_tweets', timeout=30)
    stats = {
        'stats': 'on',
        'stats.field': ['like_count', 'retweet_count', 'polarity_neg', 'polarity_pos'],
        'facet': 'on',
        'facet.field': 'polarity_lable',
        'fl': 'user_id',
        'rows': 1200
    }
    response = solr.search('movie_id:{}'.format(movie_id), **stats)
    if response.hits < 1:
        return[]

    user_query = '{!terms f=user_id}'
    for doc in response.docs:
        user_query += str(doc['user_id']) + ','

    resp_stats = response.stats['stats_fields']
    like_mean = round(resp_stats['like_count']['mean'])
    # like_sum = resp_stats['like_count']['sum']
    retweet_mean = round(resp_stats['retweet_count']['mean'])
    # retweet_sum = resp_stats['retweet_count']['sum']

    pos_score = round(resp_stats['polarity_pos']['mean'], 2)
    neg_score = round(resp_stats['polarity_neg']['mean'], 2)
    tweet_count = resp_stats['polarity_pos']['count']
    polarity_lable = response.facets['facet_fields']['polarity_lable']
    scores = {}
    for key in polarity_lable:
        if type(key) is str:
            lable = key
        else:
            scores[lable] = round(key/tweet_count, 2)

    return [user_query, like_mean, retweet_mean, pos_score, neg_score, scores['very negative'], scores['negative'], scores['neutral'], scores['positive'], scores['very positive']]


# Search twitter users in Solr by user ids query and extract statistical features
def SolrSearchUsers(user_query):
    solr = pysolr.Solr(solr_base_url + 'twitter_user_english', timeout=30)
    stats_query = {
        'stats': 'on',
        'stats.field': ['follower_count', 'following_count', 'is_verified'],
        'rows': 0
    }
    response = solr.search(user_query[:-1], **stats_query)
    resp_stats = response.stats['stats_fields']
    follower_count = round(resp_stats['follower_count']['mean'])
    following_count = round(resp_stats['following_count']['mean'])
    is_verified = round(resp_stats['is_verified']['mean'], 3)

    return [follower_count, following_count, is_verified]


# This function writes all features movies to a file
# Any line of file is a movie features
def writeFileFeatures():
    file = open(features_file_path, "w")
    file.write('movie_id;features\n')
    movies = readMoviesFile()
    for movie_id in movies:
        try:
            features = SolrSearchTweets(movie_id)
            if len(features) > 0:
                features_2 = SolrSearchUsers(features[0])
                features.extend(features_2)
                file.write('{};{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(movie_id, *features[1:]))
                print('Movie ID: {}\t\tFeatures: {}'.format(movie_id, features[1:]))
            else:
                print('Movie ID: {}\t\tFeatures: []'.format(movie_id))
        except Exception as err:
            print('{}: Error => {}'.format(movie_id, err))
    file.close()



# This function reads FeaturesMovies.csv file and save its contents in the list
def readFeaturesFile():
    with open(features_file_path, 'r') as f:
        features = f.readlines()
    return features


# This function creates a file for any user.
# Each row of the file contains the features of an item and its rating.
def writeFileInputML(user_id, movies_rating):
    features = readFeaturesFile()[1:]
    file = open("resources/users_features/{}.csv".format(user_id), "w")
    file.write('likes,retweets,pos_score,neg_score,vn_lable,n_lable,nu_lable,p_lable,vp_lable,followers,followings,verifies,ratings\n')

    for line in features:
        fields = line.strip().split(';')
        movie_id = fields[0]
        feat_fl = fields[1].split(',')
        if movie_id in movies_rating:
            # rate = float(movies_rating[movie_id])
            # if rate < 2.5:
            #     rate = 0
            # else:
            rate = 1
            file.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(*feat_fl, rate))
            # print('Movie ID: {}\t\tFeatures: Yes {}'.format(movie_id, rate))
        else:
            file.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(*feat_fl, '0'))
            # print('Movie ID: {}\t\tFeatures: NO {}'.format(movie_id, 0))
    file.close()



# writeFileFeatures()
ratings = readRatingFile()
for user_id in ratings:
    if len(ratings[user_id]) > 100:
        writeFileInputML(user_id, ratings[user_id])
