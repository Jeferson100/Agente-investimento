import snscrape.modules.twitter as sntwitter

maxTweets = 10
i = 0
tweets_list = []
for tweet in sntwitter.TwitterSearchScraper('petr4').get_items():
    if i > maxTweets:
        break
    print(tweet)
    tweets_list.append([tweet.date, tweet.url, tweet.username, tweet.content])
    i = i + 1

with open('twitter.txt', 'w') as arquivo:
    for tweet in tweets_list:
        arquivo.write(f"{tweet[0]} - {tweet[1]} - {tweet[2]} - {tweet[3]}\n")
    
