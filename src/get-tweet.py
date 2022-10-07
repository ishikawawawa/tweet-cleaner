import tweepy

# bearer_token (Optional[str]) – Twitter API Bearer Token

# consumer_key (Optional[str]) – Twitter API Consumer Key

# consumer_secret (Optional[str]) – Twitter API Consumer Secret

# access_token (Optional[str]) – Twitter API Access Token

# access_token_secret (Optional[str]) – Twitter API Access Token Secr

tw_client = tweepy.Client(
    bearer_token='',
    consumer_key='',
    consumer_secret='',
    access_token='',
    access_token_secret='',
)

tw_client.get_tweet