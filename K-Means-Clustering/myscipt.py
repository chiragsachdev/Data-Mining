#!/usr/bin/python3
import os, pickle, re
import pandas as pd
from sklearn.cluster import KMeans

path = os.path.join(".","DataSet")
os.system("mkdir Outputs")

# return list of tokens from given string
def ft_tokenize(text):
	text = text + " "
	tokens = []
	token = ""
	for ch in text:
		if re.match("[a-zA-Z0-9]", str(ch)) != None or ch == "\'":
			token += ch
		else:
			if token != "":
				tokens.append(token)
				token = ""

	return tokens

# count words in all reviews and return dictionary of {word: count}
def ft_getWordCount(data):
	wordCount = {}
	review_tokens=[]
	for review in data:
		entry = []
		for word in ft_tokenize(review):
			# not adding single character words
			if word in wordCount:
				wordCount[word] += 1
			else:
				wordCount[word] = 1
			entry.append(word)
		review_tokens.append(entry)
	return wordCount, review_tokens

# returns all words from text parsed to calculate wordcount
def ft_getWordList(wordCount):	return [word for word in wordCount]

# removes stopwords from wordlist
def ft_rmStopWordsList(data):
	fp = open(os.path.join(path,"long_stopwords.txt"), "r")
	stopwords = fp.read().split("\n")
	for i in stopwords:
		if i in data:
			t = data.pop(data.index(i))
	return data

# removes stopwords from wordcount
def ft_rmStopWordsCount(data):
	fp = open(os.path.join(path,"long_stopwords.txt"), "r")
	stopwords = fp.read().split("\n")
	for i in stopwords:
		if i in data:
			t = data.pop(i)
	return data

# parse raw data to a list of review/text
def ft_getReviews():
	reviews = []
	# read from text file into raw data
	fp = open(os.path.join(path,"foods.txt"),"r",encoding = "cp850")
	raw_data = fp.readlines()
	fp.close()
	i = 0
	# no of entries per review
	offset = raw_data.index("\n")

	while (i < len(raw_data)):
		# isolate an entry
		entry = raw_data[i:i+offset]
		# append review to data
		reviews.append(entry[-1][13:-1].lower())
		# increment counter to next entry
		i+=offset+1
	return reviews

# refining the top 500 most occuring words 
def ft_refinetop500(wordcount):
	top = {}
	data = "Word,count,\n"
	i = 0
	wordcount = sorted(wordcount.items(),key = lambda k:k[1],reverse=True)
	for word in wordcount:
		if i == 500:
			break
		top[word[0]]= word[1]
		data = data + "\"" + word[0] + "\"" + "," + str(word[1]) + ",\n"
		i += 1
	fp = open(os.path.join("Outputs","top_words.csv"),"w")
	fp.write(data)
	fp.close()
	return top

# vectorize a given review
def ft_vectorize(entry, top):
	vector = []
	for word in top:
		if word in entry:
			vector.append(entry.count(word))
		else:
			vector.append(0)
	return vector

# vectorize all reviews of the dataset
def ft_getFeatureVectors(review_tokens, top):
	feature_vectors = []
	for entry in review_tokens:
		vector = ft_vectorize(entry, top)
		feature_vectors.append(vector)
	return feature_vectors

# preprocess the raw dataset into feature vectors
def ft_PreProcess():
	print("Preprocessing data\n")
	print("reading reviews from datatset")
	reviews = ft_getReviews()
	print("getting wordcount from reviews")
	wordcount, review_tokens = ft_getWordCount(reviews)
	print("getting unique wordlist as L")
	L = ft_getWordList(wordcount)
	print("removing stopwords from L")
	W = ft_rmStopWordsList(L)
	print("removing stopwords from wordcount to match words from L")
	wordcount = ft_rmStopWordsCount(wordcount)
	print("refining top 500 entries")
	top = ft_refinetop500(wordcount)
	print("building feature vectors")
	feature_vectors = ft_getFeatureVectors(review_tokens, top)
	print("Preprocessing done\n\n")

	return feature_vectors, top

# function to perform kmeans clustering and store the clusters in a bin file
def ft_kmeans(feature_vectors):
	km = KMeans(n_clusters = 10)
	km = km.fit(feature_vectors)
	return km


# main
def main():

	feature_vectors, top = ft_PreProcess()
	print("Beginning clustering")
	km = ft_kmeans(feature_vectors)
	print("Clustering done\n")

	# print("Saving clusters and feture vectors to csv file")
	labels = ["\""+x+"\"" for x in top]
	df = pd.DataFrame(feature_vectors, columns=labels)
	df["Clusters"] = km.labels_
	# df.to_csv(os.path.join("Outputs","clusters.csv"))

	print("Beginning cluster analysis") 
	cluster_analysis = []
	for i in range(10):
		top_5_words = [labels[x] for x in km.cluster_centers_.argsort()[:,::-1][i, :5]]
		cluster_analysis.append("Cluster {} : {} \n".format(i, " ".join(top_5_words)))
	print("Saving top 5 words per cluster in a text file")
	fp = open(os.path.join("Outputs","cluster_analysis.txt"),"w")
	fp.writelines(cluster_analysis)
	fp.close()
	print("\nDone!")

	return

if __name__=="__main__":
	main()
