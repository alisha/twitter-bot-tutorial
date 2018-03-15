# Twitter Bot Tutorial

This is a tutorial on how to make Twitter bots in Python. It was developed by Alisha Ukani for MAHacks 2018.

## Getting started

### Installing Tweepy

We're going to use [Tweepy](https://github.com/tweepy/tweepy), a tool that lets us easily connect to the Twitter API using Python. Run the following code in your command line to install it:

```
pip install tweepy
```

### Create a .gitignore file

We're going to be using some API keys and secret keys, which you don't want to release to the world because then other people can make API calls as if you were making them. For example, someone could tweet to your Twitter account! To stop that, create a new file called `.gitignore` (no file extension) and enter the following
```
secret.py
*.pyc
```

Make sure you commit this change before continuing.

### Setting up Twitter

An optional, but helpful, step is to create a new Twitter account for your bot. For the time being, you can use your personal Twitter, but you'll eventually want to create a separate account for the bot so you can share this with others. Make sure you're logged in to the account you want to tweet from.

Now, we're going to create an application so we can connect Tweepy to our account:
1. Go to [apps.twitter.com](https://apps.twitter.com/) and click "Create New App"
2. Give your app a name, description, and placeholder URL (I used my personal website).
3. Make sure your app's "Access level" is "Read and write". If not, click "modify app permissions"
4. Click "manage keys and access tokens" to see your API client and secret keys, as well as your access token and access token secret.
5. Create a file in your project directory called "secret.py" and put in the following:
```
TWITTER_CLIENT = "" # enter your Consumer Key (API Key) in the quotes
TWITTER_SECRET = "" # enter your Consumer Secret (API Secret) in the quotes
TWITTER_ACCESS = "" # enter your access token in the quotes
TWITTER_ACCESS_SECRET = "" # enter your access token secret in the quotes
```

### Learning to tweet

Before doing anything fancy, we're going to learn how to tweet from our programs. Create a file named `main.py` and enter the code below. Note that this code is found in the `tweet.py` file in this repo.

```
import secret   # this has our API keys
import tweepy

auth = tweepy.OAuthHandler(secret.TWITTER_CLIENT, secret.TWITTER_SECRET)
auth.set_access_token(secret.TWITTER_ACCESS, secret.TWITTER_ACCESS_SECRET)

api = tweepy.API(auth)

try:
    api.update_status("Hello, world!")
except TweepyError:
    print "Could not tweet"
```

Congrats! You can now tweet from your code. Feel free to stop here. We're going to continue and learn about how we can use Markov chains to generate text, and then tweet the messages that we generate.

## Intro to Markov Chains

We're going to learn how to generate messages to tweet. Instead of coming up with phrases all on our own, we're going to write code that can emulate another text. This tutorial will recreate my [PoliticsBot](https://github.com/alisha/PoliticsBot), so we'll try to generate political statements based on historical speeches.

Let's say we want to generate some messages that sound like the text below:
```
I am happy
I am a programmer
I am a college student
I am teaching a workshop
```

With Markov chains, we're going to take a few words and use probability to come up with the word that comes next. Let's say we want to generate a statement that starts with the phrase "I am". What should come next? Based on the text above, we can say there's a 50% chance the next word should be "a", a 25% chance the next word should be "happy", and a 25% chance the next word should be "teaching". We can use a random number generator and pick the next word according to these probabilities. We continue doing this process until our reference text (called our **corpus**) can't give us any more words to say.

We're going to break up this project now into 3 steps: creating a word map to identify those patterns of words, generating messages using our word map, and then tweeting those messages.

You can use a new file if you'd like, or continue in the same file. If you create a new file, make sure to later add in your Twitter functionality. If you continue in the same file, it's best to comment out your function that tweets "Hello, world!" while we work on the Markov chains part.

### Generating a word map

All of the code for this section is in `gen-word-map.py`.

First, download the file `simple-corpus.txt` from this repository and put it in the folder with your code. Add the following code to your python file so we can access the text in your corpus file: 

```
def main():
  # Open and read corpus
  corpus = open("simple-corpus.txt", "r")
  word_lines = corpus.readlines()
  corpus.close()

if __name__ == '__main__':
  main()
```

You can now open your corpus file and read the lines in the file into an array (called `word_lines`).

Given our corpus text, we want to store every pair of words with a word that should come next. From the corpus above, that means we want to store the following mappings: `I am => happy`, `I am => a`, `I am => a`, and `I am => teaching`.

To do this, we're going to use a data structure called a **dictionary** (abbreviated as a `dict`). A dict lets you map things to other things — in our case, it lets us map a pair of words to a list of words that should follow. Copy and past the following code into your file, before the `main()` function:

```
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
```

We're now going to go through this code, line by line. If you think you understand this code, go ahead and copy the contents of `gen-word-map.py` into your file, and then skip to the next section.

In addition to creating a word map, we're going to keep track of a list of sentence starters (`sentence_starters = []`). When we generate messages later, we'll use this to pick the first 2 words of our tweet. Then, we can build on that tweet using the word map we just coded.

The first thing we do is create a new dict called `word_map` with the line `word_map = dict()`. Then, we have a for loop that goes through each line in `word_lines`, aka each line of text in our corpus file.

We then split the corpus line into a list of words by calling `words = line.split()`. We also set up a variable called `end_of_sentence` that is true when we've reached the end of a sentence, or false if we haven't. This will be useful in a little bit.

Now, we go through the list of words that we just created. If we're at the end of a sentence, we add the next 2 words to our list of sentence starters, and then continue. Then, we check if we're at the end of a sentence by checking for punctuation (we can have multiple sentences in a given line). Then, we map the current word and the word that follows it to the next word. This builds our dictionary with things like `{("I", "am"), "happy"}`.

When we're done building all of these mappings, we return our word map.

### Generating Messages

All of the code for this section is in `gen-message.py`. It contains code from `gen-word-map.py`.

Add the following code to your file, after the `create_word_map()` function but before the `main()` function:

```
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
```

Let's go through the `gen_message` function. It takes in a `word_map` parameter, which is a dictionary mapping a pair of strings to another string -- this is what we just created in the last step.

First, we generate a random start to our sentence by picking a random element in the `senence_starters` array. We can retrieve the first and second words from this, and we add this to an array of strings that will make up our tweet.

Now, we want to add words to our tweet until we've reached the character limit. We can check this with the `under_limit` function. This function takes an array of strings, joins all the elements into one string (separating each element with a space, as signifed by the `' '`), and then checking the length of this string.

While we're under the character limit, we want to add words to our tweet. The way to do this is to check the last two words in our tweet, and looking them up in our dictionary to find what word should come next. We find the last two words in our tweet with the line `last_words = [tweet_array[end_index-2], tweet_array[end_index-1]]`. 

Then, we check if we've stored this pair of words in our `word_map` by checking the `word_map`'s `keys`. If it's in there, we pick a random third word. If it's not there, we stop building our tweet and just return it.

### Tweeting our Messages

All of the code for this section is in `markov.py`. It contains code from `gen-word-map.py` and `gen-message.py`.

Now, we're going to add back in the ability to tweet our message. First, if you started working on a new file for this part of the tutorial, add your import statements back in:
```
import secret   # this has our API keys
import tweepy
```

Then, modify the `main()` function to tweet the message we generated:
```
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
```

You've now written code to read a file, generate word mappings, create a message based on those word mappings, and tweet that message. That's a lot! Congrats on coming this far.

The rest of this tutorial covers where to find a corpus, and how to make your program run automatically so you can tweet at regular intervals witout manually running your code.

### Where to find a corpus

There are 3 sample texts in this repo: `simple-corpus.txt`, which we've been using so far, as well as `historical-speeches.txt`, which I compiled manually for [@PoliticianBot](https://twitter.com/politicianbot), and `jane-austen.txt`, which contains Jane Austen's novels *Emma* and *Pride and Prejudice* and was used for [@AustenBot](https://twitter.com/austenbot). You can find a lot of old novels online at [Project Gutenberg](https://www.gutenberg.org/).

You can use web scraping to get other corpuses (though please don't try to scrape the same website too many times, since that can overwhelm the site's server). You can also use APIs to collect information -- what if you used the Twitter API to read a ton of tweets, and then use that as your corpus?

### Tweeting regulary (or, how to cron)

**Section TBD**
