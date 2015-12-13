import nltk
#import re
import xlwt
from nytdata4 import Data
from operator import itemgetter

def main():
	book = xlwt.Workbook(encoding="utf-8")
	sheet1 = book.add_sheet("Sheet 1")
	sheet1.write(0, 0, "Year")
	sheet1.write(0, 1, "Average Wordcount")
	sheet1.write(0, 2, "Average Headline Relevance to Content")

	d = Data()
	avg_wordcounts = d.article_data[0]
	headlines = d.article_data[1]

	i = 1
	for year in avg_wordcounts:
		print(year)
		sheet1.write(i, 0, year)
		sheet1.write(i, 1, avg_wordcounts[year])
		avg_rel = avg_relevance(headlines[year])
		sheet1.write(i, 2, avg_rel)
		i += 1

	book.save("NYT_data5.xls")



def avg_relevance(headlines):
	avg_rel = 0
	num_abstracts = 0
	relevance = list()
	for headline, abstract in headlines:
		if (len(abstract) != 0):
			num_abstracts += 1
		rel = determine_relevance(headline, abstract)
		avg_rel += rel
		relevance.append((rel, headline, abstract))
	print(min(relevance, key=itemgetter(0)))

	print("number of articles " + str(len(headlines)))
	print("number of abstracts " + str(num_abstracts))
	return avg_rel / num_abstracts

def determine_relevance(headline, abstract):
	noun_types = ('NN', 'NNS', 'NNP', 'DT', 'POS', 'IN')
	#list of tuples with (topic, importance of presence)
	topics = list()
	noun_phrase = list()
	headline_pos = classify_pos(headline)
	headline_lower_pos = dict(classify_pos(headline.lower()))
	for (w, pos) in headline_pos:
		#print(w, pos)
		#print(classify_pos(w.lower()))
		try:
			w_lower = headline_lower_pos[w.lower()]
		except:
			w_lower = classify_pos(w)
		if pos == "NNP" and w_lower in noun_types:
			#verbs sometimes mis-classified to proper nouns
			#because of headline capitalization
			topics.append((w, 1))

		elif pos in noun_types and w_lower in noun_types:
			noun_phrase.append((w, pos))
		else:
			#not a noun
			if len(noun_phrase) > 2:
				phrase_str = ""
				for n, pos in noun_phrase:
					if pos == "POS":
						phrase_str = phrase_str[:-1]
					phrase_str += str(n + " ")
				phrase_str = phrase_str[:-1]
				topics.append((phrase_str, 0.5))
			noun_phrase = list()
	#abstract_len = len(re.findall(r'\w+', abstract))
	#remove duplicates
	topics = list(set(topics))
	relevance = 0
	if len(abstract) != 0:
		for t, i in topics:
			occurrences = count_word(abstract, t)
			relevance += (occurrences / (len(topics) * i))

	if len(topics) == 0:
		return 0
	else:
		return relevance / len(topics)



def count_word(text, word):
	start = 0
	index = word_index(text, word, start)
	if index != -1:
		occurrences = 1
	else:
		return 0
	while index != -1:
		occurrences += 1
		start = index + len(word)
		index = word_index(text, word, start)
	return occurrences

def word_index(text, word, start):
	w = 0
	endings = [" ", ".", "-", ","]
	for t in range(start, len(text)):
		if text[t].lower() == word[w].lower():
			if w == len(word) - 1 and (t == len(text) - 1 or t - w == 0 or (text[t - w - 1] in endings and text[t + 1] in endings)):
				return t - w
			elif w == len(word) - 1:
				w = 0
			else:
				w += 1
		else:
			w = 0
	return -1

def classify_pos(txt):
	"""
		PENN TREEBANK PART OF SPEECH TAG
		1.	CC	Coordinating conjunction
		2.	CD	Cardinal number
		3.	DT	Determiner
		4.	EX	Existential there
		5.	FW	Foreign word
		6.	IN	Preposition or subordinating conjunction
		7.	JJ	Adjective
		8.	JJR	Adjective, comparative
		9.	JJS	Adjective, superlative
		10.	LS	List item marker
		11.	MD	Modal
		12.	NN	Noun, singular or mass
		13.	NNS	Noun, plural
		14.	NNP	Proper noun, singular
		15.	NNPS	Proper noun, plural
		16.	PDT	Predeterminer
		17.	POS	Possessive ending
		18.	PRP	Personal pronoun
		19.	PRP$	Possessive pronoun
		20.	RB	Adverb
		21.	RBR	Adverb, comparative
		22.	RBS	Adverb, superlative
		23.	RP	Particle
		24.	SYM	Symbol
		25.	TO	to
		26.	UH	Interjection
		27.	VB	Verb, base form
		28.	VBD	Verb, past tense
		29.	VBG	Verb, gerund or present participle
		30.	VBN	Verb, past participle
		31.	VBP	Verb, non-3rd person singular present
		32.	VBZ	Verb, 3rd person singular present
		33.	WDT	Wh-determiner
		34.	WP	Wh-pronoun
		35.	WP$	Possessive wh-pronoun
		36.	WRB	Wh-adverb
	"""
	return nltk.pos_tag(nltk.word_tokenize(txt))

if __name__ == '__main__':
	main()