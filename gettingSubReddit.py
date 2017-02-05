import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords #import the stopword list
from sklearn.ensemble import RandomForestClassifier

train = pd.read_csv("subreddits.csv")
vectorizer = CountVectorizer(analyzer="word", tokenizer = None, preprocessor= None, stop_words = None, max_features = 5000)

def review_to_words( raw_review ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(raw_review).get_text()
    #
    # 2. Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))
    #
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]
    #
    # 6. Join the words back into one string separated by space,
    # and return the result.
    return( " ".join( meaningful_words ))

def buildBagOfWords(reviews):

    #Initalize the "CountVectorizer" object, which is scikit-learn's
    #bag of words tool


    #fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform(clean_train_reviews) should be a list of strings
    train_data_features = vectorizer.fit_transform(reviews)

    train_data_features = train_data_features.toarray()

    return train_data_features
def trainForestModel(train_data_features, value):
    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = 100)

    # Fit the forest to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    forest = forest.fit( train_data_features, train[value] )

    return forest

def main():

    #Get the number of reviews based on the dataframe column size
    num_reviews = train["body"].size

    #initalize an empty list to hold our clean reviews

    clean_train_reviews = []

    #loop over each review; create an index i that goes from 0 to the length of the movie review list

    for i in xrange(0, num_reviews):
        #call our function for each one, and add the result to the list

        print "Review %d of %d\n" % ( i+1, num_reviews)
        clean_train_reviews.append(review_to_words(train["body"][i]))

    train_data_features = buildBagOfWords(clean_train_reviews)
    vocab = vectorizer.get_feature_names()
    print vocab

    import numpy as np

    # Sum up the counts of each vocabulary word
    dist = np.sum(train_data_features, axis=0)

    # For each, print the vocabulary word and the number of times it
    # appears in the training set
    for tag, count in zip(vocab, dist):
        print count, tag

    print "Training the random forest..."


    forest = trainForestModel(train_data_features, "score")

    forest2 = trainForestModel(train_data_features, "subreddit")

    # Read the test data
    test = pd.read_csv("subreddits.csv")

    # Verify that there are 25,000 rows and 2 columns
    print test.shape

    # Create an empty list and append the clean reviews one by one
    num_reviews = len(test["body"])
    clean_test_reviews = []
    test = "I love league of legends so much"
    clean_review = review_to_words(test)

    print(clean_review)
    clean_test_reviews.append(clean_review)
    ##print "Cleaning and parsing the test set movie reviews...\n"
    ##for i in xrange(0,num_reviews):
    ##    if( (i+1) % 1000 == 0 ):
    ##        print "Review %d of %d\n" % (i+1, num_reviews)
    ##    clean_review = review_to_words( test["body"][i] )
    ##    print(clean_review);
    ##    clean_test_reviews.append(clean_review )

    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()

    # Use the random forest to make sentiment label predictions
    result = forest.predict(test_data_features)
    result2 = forest2.predict(test_data_features)
    print(result2)
    print(result)
    # Copy the results to a pandas dataframe with an "id" column and
    # a "sentiment" column
    #output = pd.DataFrame( data={"subreddit":test["subreddit"], "score":result} )

    # Use pandas to write the comma-separated output file
    #output.to_csv( "Test.csv", index=False )

main()
