"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import twitter


api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]

    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    new_tweet = (" ".join(words))
    n = 140
    if len(new_tweet) > n:
        while True:
            if new_tweet[n] == " ":
                return new_tweet[:n]
            else:
                n -= 1
    else: 
        return new_tweet


def tweet(chain):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    # print api.VerifyCredentials()

    #send a tweet
    status = api.PostUpdate(chain)

    print status.text

    user_input = raw_input("Enter/Return to tweet again [q to quit] >  ")

    if user_input != "q":
        new_chains = make_chains(text)
        new_chain = make_text(chains)
        tweet(new_chain)


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

chain = make_text(chains)

tweet(chain)

# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)
