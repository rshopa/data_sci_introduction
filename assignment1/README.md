# Twitter Sentiment Analysis in Python

This assignment originally required Python 2.7 environment (exactly 2.7.3 version), but in my case all issues were made using Python 3.3. I did not include here rewritten _twitterstream.py_ code in order to get twitter data from the stream, as well as all the initial documents, except _AFINN-111.txt_ and assignment instructions (_instructions.pdf_). I also put here the lighter _test_output_tweets.txt_ output file (**Problem 1**) instead of 80+ Mb file containing data from the full 10-minute long live stream session.

The _/code_ dir include the next files (**Problems 2-6**):
* _tweet_sentiment.py_
* _term_sentiment.py_
* _frequency.py_
* _happiest_state.py_
* _top_ten.py_

All the scripts run an output as required in the assignment, except _tweet_sentiment.py_, which prints the sentiment of each tweet in the file, one sentiment per line, in the following form:

__id: (term id), score: (sentiment:float)__

Personally speaking, the most interesting problem was to determine the happiest state (#5). Generally, "place" and "user" fields are used to determine the location. But when providing exploratory analysis of tweet objects, I have noticed a lot of "special cases": names of US cities with missing state, but obvious to determine (Philadelphia, Indianapolis), typos like "Houston, tx ", not mentioning lots of tweets from US, written in Spanish. So it appears to be a tricky problem to write a script that covers all exceptions (as well as to create a comprehensive set of test cases, which is also an interesting issue).

I proposed here an option by considering user's "time_zone" field as an additional contribution to the sentiment score. This contribution is weighted by the number of states in particular time zone. Of course, all the fields related to "country" are verified not to be non-US ones (like Canada, for example).
