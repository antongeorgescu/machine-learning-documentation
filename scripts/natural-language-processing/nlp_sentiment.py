from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random

def remove_noise(tweet_tokens, stop_words = ()):
    # following are the syntactic elements to be removed:
    # Hyperlinks - All hyperlinks in Twitter are converted to the URL shortener t.co. Therefore, keeping them in the text processing would not add any value to the analysis.
    # Twitter handles in replies - These Twitter usernames are preceded by a @ symbol, which does not convey any meaning.
    # Punctuation and special characters - While these often provide context to textual data, this context is often difficult to process. For simplicity, you will remove all punctuation and special characters from tweets.

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        # to remove hyperlinks, you need to first search for a substring that matches a URL starting with http:// or https://,
        # followed by letters, numbers, or special characters. 
        # Once a pattern is matched, the .sub() method replaces it with an empty string.
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        # Before running a lemmatizer, you need to determine the context for each word in your text. 
        # This is achieved by a tagging algorithm, which assesses the relative position of a word in a sentence
        
        # following are examples of extracted tags
        # NNP: Noun, proper, singular
        # NN: Noun, common, singular or mass
        # IN: Preposition or conjunction, subordinating
        # VBG: Verb, gerund or present participle
        # VBN: Verb, past participle
        # pos_refs = {'n': ['NN', 'NNS', 'NNP', 'NNPS'],
        #            'v': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
        #            'r': ['RB', 'RBR', 'RBS'],
        #            'a': ['JJ', 'JJR', 'JJS']}
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

if __name__ == "__main__":

    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    print(positive_cleaned_tokens_list[0])

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    # custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."
    # custom_tweet = "As violent protests continued for a fifth straight night over the death of an African-American man during an arrest by Minneapolis police, President Trump took advantage of the crisis to take a swipe at 'the Democrat Mayor' of Minneapolis for failing to control the protests."
    # custom_tweet = "The National Guard should have been used 2 days ago & there would not have been damage & Police Headquarters would not have been taken over & ruined."
    # custom_tweet = "Congratulations to NASA on the flawless Orion flight, as well as to program prime contractors Lockheed Martin and Boeing!"
    custom_tweet = "I was happy with Space-X launch becuase it shows a new development in space travel and human exploration"
    custom_tokens = remove_noise(word_tokenize(custom_tweet))

    print(custom_tweet, "TAG:",classifier.classify(dict([token, True] for token in custom_tokens)))