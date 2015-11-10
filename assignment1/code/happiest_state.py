import string # for string.punctuation in 'to_list' function
import json, sys


                        # ANSI codes and names of states
                        
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

                                #time zones
                        # (some states use 2 zones, so it counts for both!)

zones = {'AKST':
                 {
                  'Name': {'Alaska','AKST'},
                  'States':{'AK'}
                 },
         'AST':
                 {
                  'Name': {'AST','Atlantic'},
                  'States': {'PR','VI'}
                  },
         'CST':
                 {
                  'Name': {'CST','Central'},
                  'States': {'AL','AR','FL','IA','IL','IN','KS','KY','LA','MI','MN','MO','MS','NE','ND','OK','SD','TN','TX','WI'}
                  },
         'ChST':
                 {
                  'Name': {'ChST','Chamorro'},
                  'States': {'GU','MP'}
                  },
         'EST':
                 {
                  'Name': {'EST','Eastern'},
                  'States':{'AL','CT','DC','DE','FL','GA','IN','KY','MD','ME','MI','MA','NC','NH','NJ','NY','OH','PA','RI','SC','TN','VA','VT','WV'}
                  },
         'HAST':
                 {
                  'Name': {'HAST','HST','Hawaii','Hawaii-Aleutian','Aleutian'},
                  'States': {'AK','HI'}
                  },
         'MST':
                 {
                  'Name': {'MST','Mountain'},
                  'States': {'AZ','CO','ID','KS','MT','ND','NE','NM','NV','OR','SD','TX','UT','WY'}
                  },
         'PST':
                 {
                  'Name': {'PST','Pacific'},
                  'States': {'CA','ID','NV','OR','WA'}
                  },
         'SST':
                 {
                  'Name': {'SST','Samoa'},
                  'States': {'AS'}
                  }
}

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


#-------------------------------------------------------------

def check_place(tweet):

        state = None                            # main variables
        country = None
        time_zone = None


        #-----------------------inner function--------------------------------------
        
        def in_states(dic,text,ctr):        # verify if there's a 'state' in: text.
                                            # ctr - country, does not change
                                            # if 'state' is not found

                st = None                   # state' variable

                for k,v in dic.items():

                                # 2 possible assertions for the presence
                                # of 'state'-sentence/word:
                                
                        assert1 = v in text
                        assert2 = text.rstrip()[-3:].isupper() and text[-2:] == k
                        
                                #  drop all spaces from the end
                                # ' TX' , ',TX' , '/TX' is upper (from -3 index)

                        if assert1 or assert2:
                                                
                                st = k
                                if st != None:
                                        ctr = 'United States'
                                        
                return ctr, st
                        
        #-------------------------------------------------------------------------


        if tweet['place'] != None:

                                # let's check values from different geographical keys

                t_name = tweet['place']['full_name']
                t_country = tweet['place']['country']
                
                country = t_country
                country, state = in_states(states,t_name,country)
                
                
                

        if tweet['user'] != None and state == None:

                                # !only if no result yet for 'state'
                
                t_timezone = tweet['user']['time_zone']
                t_location = tweet['user']['location']  # values from geographical keys

                if t_location != None:
                              
                        country, state = in_states(states,t_location,country)
                        


                if state == None and t_timezone != None:

                                # no 'state' yet? the last option is 'time_zone'
                        
                        country, state = in_states(states,t_timezone,country)


                                # to calculate time zone use 'time zones dict'

                        for k,z in zones.items():
                                if any(name in t_timezone for name in z['Name']):
                                        time_zone = k


                                # return 3 vars (may be None - empty)
               
        return country, state, time_zone
                        


#----------------------------------------__main__--------------------------------------------------                

def main():

        
        #--------------------pre-computed scores-----------------------

        afinnfile = open(sys.argv[1],'r')
        
        scores = {} # initialize an empty dictionaries
        specials={} # 'specials' is one with compound keys(i.e. 'dont walk', 'fed up')

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
                        #if filter_lang(JSON_tweet):
                                
                                # append tweet to main list only if lang = 'en' (English)
                                # it's OPTIONAL, because lots of nationalities are in the US,
                                # so I've commented it

                        tweets_json.append(JSON_tweet)
                        
        tweets.close()

        #---------------------------------------------------------------------
                
        output_list={} # dict with sentiments

        for t in tweets_json: 

                text = t['text'].lower()   # all to lowercase
                id_t = t['id']
                Sum = 0

                text, sentiment1 = specials_sum(text,specials)
                sentiment2 = scores_sum(to_list(text),scores)
                Sum = sentiment1 + sentiment2           # total score of tweet
                

                output_list[id_t] = Sum


        #-------------------------------------------------------------------------------

        scores_states={}        # a dict with sentiment scores of states
                                # next we'll create for each 'state'-key an empty list
                                
        for keys in states.keys():
                scores_states[keys]=[]     

        for tweet in tweets_json:

                id_tweet = tweet['id']

                c,s,t = check_place(tweet)     

                                        # c,s,t = country, state, time_zone
                                        # append each score if s (state) is non-Nil
                                        # scores are in 'output_list'

                if s != None:
                        scores_states[s].append(output_list[id_tweet])

                else:

                                        # here the most interesting thing is:
                                        # the time zone verification
                                        # if all else fails in detecting the state
                                        
                        asrt1 = (t != None)
                        asrt2 = (c == None or c == 'United States')

                                        # country should be None or US only
                                        # (and not Canada, in particular!)

                        if asrt1 and asrt2:

                                weight = 1/len(zones[t]['States'])

                                        # since there are lots of states
                                        # in each time zone, a proper weighting
                                        # must be used (1/m, where m - number of states
                                        # in time zone)
                                
                                for s_zone in zones[t]['States']:
                                        scores_states[s_zone].append(weight*output_list[id_tweet])



        
        #------------------------------------------------------------------------------

        for x_keys in scores_states.keys():
                if len(scores_states[x_keys])>0:
                        scores_states[x_keys]=(sum(scores_states[x_keys])/len(scores_states[x_keys]))

                                        # calculate mean score if list is non-empty
                                        # update 'scores_states' as one value per state
                else:
                        scores_states[x_keys] = 0  # 0 score for empty lists


        happiest_value = max(scores_states.values())
        happiest_state = [x for x in scores_states.keys() if scores_states[x] == happiest_value]

                        # a list, not a single value, because
                        # the happiest score could be the same for a few states

        size = len(happiest_state)
        

        #-------OUTPUT-------------------------
        for i in range(size):
        	      print(happiest_state[i])

        	     
        	      

##----------------alternative-OUTPUT-------------------------------
##
##        if size == 1:
##                print('...And the happiest ('+str(happiest_value)+') state is:\n\n\t\t\t', happiest_state[0])
##        else:
##                print('...And the happiest ('+str(happiest_value)+') states are:\n\n')
##                for i in range(size):
##                      print("\t\t\t",happiest_state[i])

#--------------------------------------------------------------------------


if __name__ == '__main__':
        main()

