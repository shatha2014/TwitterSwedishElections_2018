import os
#Get csv files contating the Tweets of parties.
if __name__ == '__main__':
    os.system('''mongoexport -d test -c "moderaterna_tweets_2" -fields textList --csv -o moderaterna.csv''')
    os.system('''mongoexport -d test -c "socialdemokraterna_tweets_2" -fields textList --csv -o socialdemokraterna.csv''')
    os.system('''mongoexport -d test -c "miljopartiet_tweets_2" -fields textList --csv -o miljopartiet.csv''')
    os.system('''mongoexport -d test -c "centerpartiet_tweets_2" -fields textList --csv -o centerpartiet.csv''')
    os.system('''mongoexport -d test -c "liberalerna_tweets_2" -fields textList --csv -o liberalerna.csv''')
    os.system('''mongoexport -d test -c "kristdemokraterna_tweets_2" -fields textList --csv -o kristdemokraterna.csv''')
    os.system('''mongoexport -d test -c "vansterpartiet_tweets_2" -fields textList --csv -o vansterpartiet.csv''')
    os.system('''mongoexport -d test -c "sverigedemokraterna_tweets_2" -fields textList --csv -o sverigedemokraterna.csv''')



