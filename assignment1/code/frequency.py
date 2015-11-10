import string # for string.punctuation in 'to_list' function 
import json, sys


#--------------------------functions---------------------------------

def filter_lang(tweet):         # English language
                                # returns true

        return tweet['lang'] == 'en'


def to_list(ini_tweet):
        list_tweet = [s.strip(string.punctuation) for s in ini_tweet.split()]
        return [s for s in list_tweet if s != '']

                        # parse ini_tweet string to list of single words
                        # omit empty elements like ''



#----------------------------------------__main__--------------------------------------------------                

def main():


        #----------------------MAIN CODE------------------------------

        tweets = open(sys.argv[1],'r')
        input_length = len(tweets.readlines())

        tweets_json = []        # THE MAIN LIST OF json-TWEETS!

        # now let's create a list of dictionaries

        tweets.seek(0)
        while 1:
                text=tweets.readline()
                
                if text == '':
                        break
                if text[-1] != '\n':
                        text+='\n'      # last tweet won't have '\n' at the end, so
                                        # it should be appended
                        
                if 'b\'{"created_at":' in text:
                        
                                # now it's time to use json
                                
                        text_modified = bytearray(text[2:-2],encoding='ascii').decode('unicode_escape')

                                # what exact encoding to use (maybe not ascii), I don't know...
                                # here I've used bytearray and 'unicode_escape' option

                        JSON_tweet = json.loads(text_modified)
                        if filter_lang(JSON_tweet):
                                
                                # append tweet to main list only if lang = 'en' (English)
                                # it's OPTIONAL,
                                
                                tweets_json.append(JSON_tweet)
                        
        tweets.close()

        #---------------------------------------------------------------------

        words_freq = {}       # ini dict for words and their frequency

        for t in tweets_json:

                text = to_list(t['text'].lower())
                                #--------------------------
                                # all to lowercase and to list
                                # of single words
                
                for word in text:
                        if word not in words_freq.keys():    
                                words_freq[word] = 0
                                        #-----------------------
                                        # append new words
                                        # and n of occurencies (default - 0)
                

        #-------Assignment_4-------------words freqs---------------------------------

        total_words = 0         # total sum of words in all tweets

        for t in tweets_json:
                
                tweet = t['text'].lower()       # lowercase all words
                
                l_tweet = to_list(tweet)        # parse to list of single words
                total_words += len(l_tweet)     # count them and add to total_words

                for z in words_freq.keys():

                                                # count words

                        if z in l_tweet:
                                words_freq[z] += l_tweet.count(z)

        #--now transform counts of words to frequencies in the same dict 'words'--

        for w in sorted(words_freq.keys()):

                words_freq[w] = words_freq[w]/total_words
                print(w.encode('ascii','xmlcharrefreplace').decode(),"{0:.4g}".format(words_freq[w]))

                                # avoid encoding problems
                                # and output up to 4th digits


        
        #--------------------------------------------------------------------------


if __name__ == '__main__':
        main()

