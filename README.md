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

## Learning to tweet

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

With Markov chains, we're going to take a few words and use probability to come up with the word that comes next. In each 

