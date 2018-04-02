#!/usr/bin/python

import re
import sys

report_only_final_class_label = True
verbose = False
if len(sys.argv) == 2 and sys.argv[1] == "--fuzzy_scores":
    report_only_final_class_label = False
elif len(sys.argv) == 2 and sys.argv[1] == "--verbose":
    verbose = True
elif len(sys.argv) == 3:
    if "--verbose" in sys.argv and "--fuzzy_scores" in sys.argv:
        report_only_final_class_label = False
        verbose = True
elif len(sys.argv) == 1:
    pass

hashtag_handle_removal = re.compile("[&#@]\\S*")
url_removal = re.compile("http\\S*")
email_removal = re.compile("\\S*@\\S*\\.\\S*")
RT_removal = re.compile("RT\\W")
word_extractor = re.compile("([a-zA-Z']+)")

first_line = False
prev_data = ""

# Data format:
# {seq},{count},{hate_score},{offensive_score},{neither_score},{class},{tweet}
# seq: sequence number
# count: total number of scorers for this tweet
# hate_score: number of scorers who classified the tweet as hate speech
# offensive_score: number of scorers who classified the tweet as offensive speech
# neither_score: number of scorers who classified the tweet as neither offensive nor hate speech
# class: the final class label: 0,1,2 (hate, offensive, neither)
# tweet: the raw text of the tweet
for line in sys.stdin:
    if not first_line:
        prev_data = line
        first_line = True
        continue
    else:
        # fails if next line is continuation of this one
        try:
            seq,count,h_s,o_s,n_s,class_id,tweet = line.split(',',6)
        except ValueError:
            # haven't finished the previous line
            prev_data += line
            continue
        else:
            seq,count,h_s,o_s,n_s,class_id,tweet = prev_data.split(',',6)
            prev_data = line
    # split on the first six commas to get the seven values
    #print(line.split(',',6))
    #seq,count,h_s,o_s,n_s,class_id,tweet = line.split(',',6)
    if not seq.isdigit():
        continue
    # convert to correct data types
    seq = int(seq)
    count = int(count)
    h_s = int(h_s)
    o_s = int(o_s)
    n_s = int(n_s)
    class_id = int(class_id)

    # remove hashtags and twitter handles
    filt_tweet = hashtag_handle_removal.sub("", tweet)
    # remove "RT" occurrences
    filt_tweet = RT_removal.sub("",filt_tweet)
    # remove urls
    filt_tweet = url_removal.sub("",filt_tweet)
    # remove email addresses
    filt_tweet = email_removal.sub("",filt_tweet)
    # make lowercase
    filt_tweet = filt_tweet.lower()
    # extract words
    words = word_extractor.findall(filt_tweet)
    # report scores with word
    if verbose:
        print(tweet)
        print(filt_tweet)
    if report_only_final_class_label:
        for word in words:
            print("{}\t{} {} {}".format(word,int(class_id==0),int(class_id==1),int(class_id==2)))
    else:
        for word in words:
            print("{}\t{} {} {}".format(word,h_s,o_s,n_s))
