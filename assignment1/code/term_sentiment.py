import string # for string.punctuation in 'to_list' function
import json, sys


#--------------------------functions---------------------------------

def filter_lang(tweet):         # English language
                                # returns true

        return tweet['lang'] == 'en'


#----------------------------------------------------------------------

def specials_sum(ini_tweet,specials_dict):

        Sum=0
        for k in specials_dict.keys():
                if k in ini_tweet:

                                # it's time to count every particular sentiment
                                
                        sentiment_count = specials_dict[k]*ini_tweet.count(k)

                                # add to main sum
                                # and later remove 'em from tweet
                                
                        Sum += sentiment_count 
                        ini_tweet = ini_tweet.replace(k,"")

                                # return an updated tweet with provisional sum
                
        return ini_tweet, Sum        
        

def to_list(ini_tweet):
        
        list_tweet = [s.strip(string.punctuation) for s in ini_tweet.split()]
        return [s for s in list_tweet if s != '']

                                # omit empty elements like ''
        



def scores_sum(ini_list,scores_dict):

                # here is a LIST, NOT STRING(!) on the input

        Sum=0
        scores_l=list(scores_dict.keys())

                        # create a list from AFINN-111 dict

        for z in ini_list:
                if z in scores_l:
                        Sum += scores_dict[z]

        out_list = [x for x in ini_list if x not in scores_l]

                        #remove 'em from tweet
                       
        return out_list, Sum



#----------------------------------------__main__--------------------------------------------------                

def main():


        #--------------------pre-computed scores-----------------------

        afinnfile = open(sys.argv[1],'r')
        afinn_length = len(afinnfile.readlines())

             
        scores = {}     # initialize an empty dictionaries
        specials = {}   # 'specials' is one with compound keys(i.e. 'dont walk', 'fed up')

        afinnfile.seek(0)
        for line in afinnfile:
            
                term, score = line.split("\t") # The file is tab-delimited. "\t" means "tab character"
                if ' ' in term:
                        specials[term] = int(score) # Convert the score to an integer.
                else:
                        scores[term] = int(score) 

                                # Put every (term, score) pair in the dictionary

        afinnfile.close()




        #----------------------MAIN CODE------------------------------

        tweets = open(sys.argv[2],'r')
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

        output_list={}          # dict with pre-calculated sentiments  
        words_set = set()       # ini set for words not in AFINN-111

        for t in tweets_json:

                text = t['text'].lower()   # all to lowercase
                id_t = t['id']
                Sum = 0

                text, sentiment1 = specials_sum(text,specials)
                text_cut, sentiment2 = scores_sum(to_list(text),scores)
                Sum = sentiment1 + sentiment2           # total score of tweet


                #-- now we'll create a set with words not in AFINN-111 ------

                for word in text_cut:

                        if word not in words_set:    
                                words_set = words_set | {word}  # append new words

                #------------------------------------------------------------

                output_list[id_t] = Sum         # output sentiment scores

                #---------------------------------------------------------             


        #---Assignment_3---now it's time to calculate the rest of words' sentiments----

        sent_scores = {}   # a dict with sentiment scores

        for w in words_set:

                sentiment=0     # default score should be 0
                n=0             # number of occurencies

                for tweet in tweets_json:
                        
                        if w in tweet['text'].lower():

                                        # if a word is in tweet,
                                        # increase n of occurencies by 1
                                        # and score by the corresponding one
                                        # from output_list
                                        # (will be divided by n)
                                
                                sentiment += output_list[tweet['id']]
                                n+=1


                if n != 0:
                        sentiment = sentiment/n

                                        # mean value if many occurencies
                                        
                sent_scores[w] = sentiment



        for k in sorted(sent_scores.keys()):
                
                                        # try to avoid encoding problems:

                term = k.encode('ascii','xmlcharrefreplace').decode()
                print(term,str("%.3f" % sent_scores[k])) 
                

              
#--------------------------------------------------------------------------


if __name__ == '__main__':
        main()

