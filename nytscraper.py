from nytimesarticle import articleAPI
import time


def main():    
    headlines_wordcounts = get_range_headlines_and_wordcount(1980, 2015)
    f = open('nytdata4.py', 'w')
    f.write('class Data:\n    def __init__(self):\n        self.article_data = ' + str(headlines_wordcounts))
    f.close()

def get_range_headlines_and_wordcount(start, end):
    '''
    Returns a tuple of a dictionary mapping a year to all headlines from that year
    and a second dictionary mapping year to average wordcount
    for all years from start to end (dates)
    '''
    headlines = list()
    avg_wordcounts = list()
    for i in range(start, end + 1):
        print i
        #tuple with avg_wordcount and headlines from a year i
        headline_wordcount = get_headlines_and_wordcount(str(i))
        avg_wordcounts.append((i, headline_wordcount[0]))
        headlines.append((i, headline_wordcount[1]))
    #dictionary with year -> dict of headline -> abstract
    headlines = dict(headlines)
    #dictionary with year -> avg wordcount
    avg_wordcounts = dict(avg_wordcounts)
    return (avg_wordcounts, headlines)

def parse_wordcount(articles):
    '''
    Parses query result for word count from each article
    Returns a list of word counts
    '''
    wordcounts = list()
    for i in articles['response']['docs']:
        wordcounts.append(i['word_count'])
    return wordcounts

def parse_headlines(articles):
    '''
    Parses query result for headlines from each article
    Returns a list of headlines
    '''
    headlines = list()
    for i in articles['response']['docs']:
        if i['lead_paragraph'] is not None:
            headlines.append(((i['headline']['main'].encode('ascii', 'ignore')), i['lead_paragraph'].encode('ascii', 'ignore'))) 
        elif i['abstract'] is not None:
            headlines.append(((i['headline']['main'].encode('ascii', 'ignore')), i['abstract'].encode('ascii', 'ignore')))
        elif i['snippet'] is not None:
            #no abstract
            headlines.append(((i['headline']['main'].encode('ascii', 'ignore')), i['snippet'].encode('ascii', 'ignore')))
        else:
        	headlines.append(((i['headline']['main'].encode('ascii', 'ignore')), ""))
    return headlines

def get_headlines_and_wordcount(date):
    '''
    This function accepts a year in string format (e.g.'1980')
    and it will return a tuple of average wordcount and a list headlines
    for that year.
    '''
    #please dont use my key :)
    api = articleAPI('fad6d61d6d69a16df4ef1e0f38ec9c00:10:73444277')
    headlines = []
    wordcounts = []
    for i in range(0,100):
        articles = api.search(fq = {'source':['The New York Times']},
               begin_date = date + '0101',
               end_date = date + '1231',
               sort='oldest',
               page = str(i))
        headlines += parse_headlines(articles)
        wordcounts += parse_wordcount(articles)
        time.sleep(1) #10 requests per second (10 items on a page)
    #find the average wordcount for this year
    num_wordcounts = len(wordcounts)
    avg_wordcount = 0
    for i in wordcounts:
        if i != None:
            try:
    	        avg_wordcount += int(i)
            except:
                print i
        else:
            num_wordcounts -= 1
    avg_wordcount = avg_wordcount / num_wordcounts
    return (avg_wordcount, headlines)

if __name__ == '__main__':
    main()
