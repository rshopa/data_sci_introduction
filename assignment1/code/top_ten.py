import sys, json


#--------------------------functions---------------------------------

def filter_lang(tweet):         # English or unknown language
                                # returns true

        return tweet['lang'] == 'en' or tweet['lang'] == None




def filter_tweet(tweet):      # if there's any hashtags

                        # I've explored that the next keys
                        # are always in the tweet:
                        #       "tweet['entities']['hashtags']"
                        #       "tweet['user']"
                        # should be also "tweet['user']['hashtags']"
                        # but it's not true here

        statement1 = len(tweet['entities']['hashtags'])>0
        statement2 = 'entities' in tweet['user'].keys() and len(tweet['user']['entities']['hashtags'])>0

        return  statement1, statement2
        
#---------------------------------------------------------------------

def main():

        tweets = open(sys.argv[1],'r') 
        
        rank = {}               # an empty dict for hashtags and their ranking

        # now let's look through our tweets' file

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

                        J_tweet = json.loads(text_modified)

                        s1,s2 = filter_tweet(J_tweet)
                        s_lang = filter_lang(J_tweet)

                        if s1 and s_lang:     # look in tweet['entities']['hashtags']

                              for tag in J_tweet['entities']['hashtags']:

                                              #----------------------------------
                                              # every new hashtag will be stored
                                              # in 'rank' dictionary,
                                              # otherwise its number
                                              # of occurencies will increase

                                      if tag['text'] not in rank.keys():
                                              rank[tag['text']] = 1
                                                      #---------------
                                                      # 1st occurence                                              
                                      else:
                                              rank[tag['text']] += 1
                                                      #--------------------------------
                                                      # increase number of occurencies

                        elif s2 and s_lang:   # in ['user']['hashtags']

                                for tag in J_tweet['user']['hashtags']:

                                      if tag['text'] not in rank.keys():
                                              rank[tag['text']] = 1
                                      else:
                                              rank[tag['text']] += 1
                     
                   
        tweets.close()

        #---------------------------------------------------------------------

        output_list = []        # here top ten hashtags will be stored

        sorted_keys_10th = sorted(rank.values())[-10]
                                #-------------------------------
                                # 10th position of top ten values (occurencies)

        for hashtag in rank.keys():
                if rank[hashtag] >= sorted_keys_10th:
                        output_list.append([hashtag,rank[hashtag]])

        output_list.sort(key = lambda x: x[1],reverse = True)
                                #---------------------------------------
                                # sort by second argument (value) descending

                                                   #-----------------------
        for x in output_list[:10]:                 # only 10 results [:10]
                                                   # for final output.
                                                   # (same scores may occur
                                                   # for different hashtags)

                                # try to avoid encoding problems:
                                
                tag = x[0].encode('ascii','xmlcharrefreplace').decode()
                print(tag,str(float(x[1])))   

        

#--------------------------------------------------------------------------


if __name__ == '__main__':
        main()
