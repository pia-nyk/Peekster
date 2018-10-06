import nltk
import re

'''
article_text = """
Artificial intelligence (AI), sometimes called machine intelligence, is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and other animals. In computer science AI research is defined as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.[1] Colloquially, the term "artificial intelligence" is applied when a machine mimics "cognitive" functions that humans associate with other human minds, such as "learning" and "problem solving".[2]

The scope of AI is disputed: as machines become increasingly capable, tasks considered as requiring "intelligence" are often removed from the definition, a phenomenon known as the AI effect, leading to the quip, "AI is whatever hasn't been done yet."[3] For instance, optical character recognition is frequently excluded from "artificial intelligence", having become a routine technology.[4] Modern machine capabilities generally classified as AI include successfully understanding human speech,[5] competing at the highest level in strategic game systems (such as chess and Go),[6] autonomously operating cars, and intelligent routing in content delivery networks and military simulations.

Artificial intelligence was founded as an academic discipline in 1956, and in the years since has experienced several waves of optimism,[7][8] followed by disappointment and the loss of funding (known as an "AI winter"),[9][10] followed by new approaches, success and renewed funding.[8][11] For most of its history, AI research has been divided into subfields that often fail to communicate with each other.[12] These sub-fields are based on technical considerations, such as particular goals (e.g. "robotics" or "machine learning"),[13] the use of particular tools ("logic" or artificial neural networks), or deep philosophical differences.[14][15][16] Subfields have also been based on social factors (particular institutions or the work of particular researchers).[12]

The traditional problems (or goals) of AI research include reasoning, knowledge representation, planning, learning, natural language processing, perception and the ability to move and manipulate objects.[13] General intelligence is among the field's long-term goals.[17] Approaches include statistical methods, computational intelligence, and traditional symbolic AI. Many tools are used in AI, including versions of search and mathematical optimization, artificial neural networks, and methods based on statistics, probability and economics. The AI field draws upon computer science, information engineering, mathematics, psychology, linguistics, philosophy, and many others.

The field was founded on the claim that human intelligence "can be so precisely described that a machine can be made to simulate it".[18] This raises philosophical arguments about the nature of the mind and the ethics of creating artificial beings endowed with human-like intelligence which are issues that have been explored by myth, fiction and philosophy since antiquity.[19] Some people also consider AI to be a danger to humanity if it progresses unabated.[20] Others believe that AI, unlike previous technological revolutions, will create a risk of mass unemployment.[21]

In the twenty-first century, AI techniques have experienced a resurgence following concurrent advances in computer power, large amounts of data, and theoretical understanding; and AI techniques have become an essential part of the technology industry, helping to solve many challenging problems in computer science, software engineering and operations research.[22][11]

A typical AI perceives its environment and takes actions that maximize its chance of successfully achieving its goals.[1] An AI's intended goal function can be simple ("1 if the AI wins a game of Go, 0 otherwise") or complex ("Do actions mathematically similar to the actions that got you rewards in the past"). Goals can be explicitly defined, or can be induced. If the AI is programmed for "reinforcement learning", goals can be implicitly induced by rewarding some types of behavior and punishing others.[a] Alternatively, an evolutionary system can induce goals by using a "fitness function" to mutate and preferentially replicate high-scoring AI systems; this is similar to how animals evolved to innately desire certain goals such as finding food, or how dogs can be bred via artificial selection to possess desired traits.[51] Some AI systems, such as nearest-neighbor, instead reason by analogy; these systems are not generally given goals, except to the degree that goals are somehow implicit in their training data.[52] Such systems can still be benchmarked if the non-goal system is framed as a system whose "goal" is to successfully accomplish its narrow classification task.[53]
"""
'''
def summarize(article_text):
	article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
	article_text = re.sub(r'\s+', ' ', article_text)

	formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
	formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
	sentence_list = nltk.sent_tokenize(article_text)
	stopwords = nltk.corpus.stopwords.words('english')

	word_frequencies = {}
	for word in nltk.word_tokenize(formatted_article_text):
		if word not in stopwords:
		    if word not in word_frequencies.keys():
		        word_frequencies[word] = 1
		    else:
		        word_frequencies[word] += 1

	maximum_frequncy = max(word_frequencies.values())

	for word in word_frequencies.keys():
		word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

	sentence_scores = {}
	for sent in sentence_list:
		for word in nltk.word_tokenize(sent.lower()):
		    if word in word_frequencies.keys():
		        if len(sent.split(' ')) < 30:
		            if sent not in sentence_scores.keys():
		                sentence_scores[sent] = word_frequencies[word]
		            else:
		                sentence_scores[sent] += word_frequencies[word]

	import heapq
	summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
	# print summary_sentences
	summary = ' '.join(summary_sentences)
	return(summary)
