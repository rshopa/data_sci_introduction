import string # for string.punctuation in 'to_list' function
import json, sys


#--------------------------functions---------------------------------

def filter_lang(tweet):         # English language
                                # returns true

        return tweet['lang'] == 'en'


#----------------------------------------------------------------------

def specials_sum(ini_tweet,specials_dict):

                # 'specials' are compound terms (i.e. 'dont walk', 'fed up')
                # this function calculates the sentiment score of ini_tweet
                # using dictionary, made of 'specials' - specials_dict
                # and returns initial tweet without these terms,
                # along with the overall score (Sum)
                

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

                # convert tweet to list of words omitting empty elements like ''
        



def scores_sum(ini_list,scores_dict):

                # here is a LIST, NOT STRING(!) on the input
                # overall sentiment score (Sum) is calculated
                # using dictionary formed of single words "scores_dict"

        Sum=0
        scores_l=list(scores_dict.keys())

                        # create a list from AFINN-111 dict

        for z in ini_list:
                if z in scores_l:
                        Sum += scores_dict[z]
                       
        return Sum



#----------------------------------------__main__--------------------------------------------------                

def main():

        
        #--------------------pre-computed scores-----------------------

        afinnfile = open(sys.argv[1],'r')
        afinn_length = len(afinnfile.readlines())

             
        scores = {} # initialize an empty dictionaries
        specials = {} # 'specials' is one with compound keys(i.e. 'dont walk', 'fed up')
        
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
                
        for t in tweets_json:

                text = t['text'].lower()   # all to lowercase
                id_t = t['id']
                Sum = 0

                text, sentiment1 = specials_sum(text,specials)
                sentiment2 = scores_sum(to_list(text),scores)
                Sum = sentiment1 + sentiment2           # total score of tweet
   
        
##              here and ID and a sentiment score of every tweet
##              are printed instead of just the sentiment of each tweet,
##              as it is required in the assignment.
##              There a simpler output should be used in the next command: 
##              print(str(float(Sum)))
                         
                print('id: '+str(id_t)+', score: '+str(float(Sum)))
      

               
#--------------------------------------------------------------------------


if __name__ == '__main__':
        main()

