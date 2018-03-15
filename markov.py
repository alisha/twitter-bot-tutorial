import secret   # this has our API keys
import tweepy
from random import randrange

sentence_starters = []

# Create map of words
# word_lines is a list of strings that represents our file
def create_word_map(word_lines):
  word_map = dict()

  # Go through each line in our corpus
  for line in word_lines:
    
    # Split each line into a list of words
    words = line.split()

    end_of_sentence = True
    
    # Go through each word in our corpus line
    for index in range(0,len(words)-2):
      
      # If we're at the end of a sentence, add the start of the next sentence
      # to our array of sentence starters
      if end_of_sentence:
        sentence_starters.append((words[index], words[index + 1]))
        end_of_sentence = False

      # Check if at the end of sentence
      if words[index + 1] == "?" or words[index + 1] == "." or words[index + 1] == "!":
        end_of_sentence = True

      # Add word pairings to our word_map
      if (words[index], words[index + 1]) in word_map.keys():
        word_map[(words[index], words[index + 1])].append(words[index + 2])
      else:
        word_map[(words[index], words[index + 1])] = [words[index + 2]]

  return word_map


# Returns true if the contents of the array is under Twitter's character limit
def under_limit(array):
  return len(' '.join(array)) < 280


# Generate tweet
def gen_message(word_map):
  # Find a random starting point for our tweet
  index = randrange(len(sentence_starters) - 1)

  # Figure out the first 2 words in our tweet
  first_word = sentence_starters[index][0]
  second_word = sentence_starters[index][1]
  
  # Holds an array of all words in the tweet
  tweet_array = [first_word, second_word]

  while under_limit(tweet_array) is True:
    # Figure out the last 2 words in our tweet
    end_index = len(tweet_array)
    last_words = [tweet_array[end_index-2], tweet_array[end_index-1]]

    # Try to add more words to our tweet
    if (last_words[0], last_words[1]) in word_map.keys():
      possible_third_words = word_map[(last_words[0], last_words[1])]
      third_word_index = randrange(len(possible_third_words))
      random_third_word = possible_third_words[third_word_index]
      tweet_array.append(random_third_word)
    else:
      # We can't add any more words so just return the tweet
      return tweet_array

    # Make sure we're not over 280 characters
    if under_limit(tweet_array) is False:
      return tweet_array


def main():
  # Open and read corpus
  corpus = open("simple-corpus.txt", "r")
  word_lines = corpus.readlines()
  corpus.close()

  # Create word map
  word_map = create_word_map(word_lines)
  tweet_array = gen_message(word_map)
  tweet = ' '.join(tweet_array)

  # Twitter authentication
  auth = tweepy.OAuthHandler(secret.TWITTER_CLIENT, secret.TWITTER_SECRET)
  auth.set_access_token(secret.TWITTER_ACCESS, secret.TWITTER_ACCESS_SECRET)
  api = tweepy.API(auth)

  # Try to tweet
  try:
    api.update_status(tweet)
  except TweepyError:
    print "Could not tweet"

if __name__ == '__main__':
  main()
