#!/usr/bin/python3

import os, glob, statistics, random, pyhash

max_0 = [-1 for i in range(30)]
# function to readfile in chunks of 64 mb as a generator object
def ft_readFile(fname):
	fp = open(fname,'r',encoding='cp850')
	while(True):
		data = fp.read(64_000_000) #reading approx 64 mb
		if not data:
			break

		yield data

# split data into complete lines and partial last line 
def ft_processChunk(text):
	n = text.rfind("\n") + 1
	data = text[:n-1]
	residue = text[n:]

	return data, residue

# function to calculate max of tailing 0's of hash values (murmur, fnv and xxhash) 
def ft_process(text):
	# splitting on lines
	lines = text.split('\n')
	# assigning max lowest to all possible hash values
	global max_0
	for line in lines:
		# skipping blank entries
		if len(line) == 0:	continue
		# skipping lines that don't begin with 'Q'
		if line[0] =="Q":
			quote = line[2:]

			for i in range(10):
				# calculating # of tailing 0's for murmurhash
				hash_value = pyhash.super_fast_hash(seed = i)(quote)
				tail_0 = len(bin(hash_value)[2:]) - (bin(hash_value)[2:].rfind('1') + 1)
				# assigning # of tailing 0's as 0 if no 1's found in bin string
				if tail_0 == len(bin(hash_value)[2:]):	tail_0 = 0
				if tail_0 > max_0[i]:	max_0[i] = tail_0
			for i in range(10,20):
				# calculating # of tailing 0's for murmurhash
				hash_value = pyhash.murmur3_32(seed = i)(quote)
				tail_0 = len(bin(hash_value)[2:]) - (bin(hash_value)[2:].rfind('1') + 1)
				# assigning # of tailing 0's as 0 if no 1's found in bin string
				if tail_0 == len(bin(hash_value)[2:]):	tail_0 = 0
				if tail_0 > max_0[i]:	max_0[i] = tail_0
			for i in range(20,30):
				# calculating # of tailing 0's for murmurhash
				hash_value = pyhash.xx_32(seed = i)(quote)
				tail_0 = len(bin(hash_value)[2:]) - (bin(hash_value)[2:].rfind('1') + 1)
				# assigning # of tailing 0's as 0 if no 1's found in bin string
				if tail_0 == len(bin(hash_value)[2:]):	tail_0 = 0
				if tail_0 > max_0[i]:	max_0[i] = tail_0

	return

def main():
	global max_0
	# getting list of files to be read
	files = glob.glob("./Data/*.txt")
	residue = ""
	# maintaining list of average of tailing 0's from chunks
	ctr = 1
	# processing 1 file at a time
	for fname in files:
		print("Processing : {} {}".format(fname,ctr))
		# get generator object of data chunks
		data = ft_readFile(fname)
		# processing generator object over all values
		flag = True
		mb_processed = 0
		while (flag):
			# get next item of generator object till next item does not exist
			try:
				text = residue + next(data)
			except StopIteration:
				text = residue 
				flag = False
			text, residue = ft_processChunk(text)
			if len(text) == 0:	continue
			mb = len(text) / 1_000_000
			mb_processed += mb
			print("Processing {:.2f} MB block".format(mb))
			# get average tailing 0 count for current data chunk
			ft_process(text)
			# group_avg.append(g_avg)
			print("Processed {:.2f} MB from file #{}".format(mb_processed, ctr))
		residue = ""
		ctr += 1

	random.shuffle(max_0) 
	group_avg = [sum(max_0[i:i+5])/5 for i in range(0,30,5)]
	print("File done")

	print("Writing output file")
	# take value of R as median of averages of tailing 0's
	med_g_avg = statistics.median(group_avg)
	outtext = "The data has been processed in chunks of approx. 64 MB\n"
	outtext += "The hashing function used is 30 superfasthash, murmurhash and hashxx functions with seed in range(0,30) mapping to 32 bit unsigned integers\n"
	outtext += "The tailing 0's was calculated for Quotes in these chunks of 64 MB\n"
	outtext += "The medians of averages of groups is :\t{}\n".format(med_g_avg)
	outtext += "Estimate of Unique Quotes from the Flajolet-Martin algorithm"
	outtext += " :\t{}\n".format(int(2**med_g_avg))
	# estimated number of unique entries = 2^R
	with open("Output.txt",'w') as fp:
		fp.write(outtext)
	print("Output written")

if __name__ == "__main__":
	main()