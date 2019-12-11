from sklearn.utils import murmurhash3_32 as mmh
from fnvhash import fnv1a_32 as fnvh
from pyhashxx import hashxx
from bitarray import bitarray
import os, glob, statistics, pickle, math, pyhash

m = 300_000
bit_array = None

def ft_readFile(fname):
	fp = open(fname,'r',encoding='cp850')
	while(True):
		data = fp.readline().strip('\n') #reading 1 username at a time
		if not data:
			break

		yield data

def ft_mmh(text):
	global m
	hash_value = mmh(text, positive = True)
	return (hash_value % m)

def ft_fnvh(text):
	global m
	hash_value = fnvh(text.encode())
	return (hash_value % m)

def ft_hashxx(text):
	global m
	hash_value = hashxx(text.encode())
	return (hash_value % m)

def ft_superfasthash(text):
	global m
	hash_value = pyhash.super_fast_hash()(text)
	return (hash_value % m)

def ft_spooky_32(text):
	global m
	hash_value = pyhash.spooky_32()(text)
	return (hash_value % m)

def ft_farmhash(text):
	global m
	hash_value = pyhash.farm_32()(text)
	return (hash_value % m)


def ft_process():
	global bit_array

	f_name = "Data/listed_username_30.txt"
	data = ft_readFile(f_name)
	flag = True
	while (flag):
		try:
			uname = next(data)
		except StopIteration:
			flag = False
		
		i = ft_mmh(uname)
		j = ft_fnvh(uname)
		k = ft_hashxx(uname)
		l = ft_superfasthash(uname)
		m = ft_spooky_32(uname)
		n = ft_farmhash(uname)
		bit_array[i] = True
		bit_array[j] = True
		bit_array[k] = True
		bit_array[l] = True
		bit_array[m] = True
		bit_array[n] = True
	return

def ft_train():
	global bit_array
	global m


	# creting empty bit array 
	bit_array = bitarray(m) 

	# setting all bits to 0
	bit_array.setall(False) 

	# filling bit strings with training data 
	ft_process()

	return

def ft_evaluate():
	global bit_array

	f_name = "Data/listed_username_365.txt"
	data = ft_readFile(f_name)
	flag = True
	spam_count = {'spam' : 0, 'not_spam' : 0}
	while (flag):
		try:
			uname = next(data)
		except StopIteration:
			flag = False
		count = {True : 0, False : 0}
		i = ft_mmh(uname)
		j = ft_fnvh(uname)
		k = ft_hashxx(uname)
		l = ft_superfasthash(uname)
		m = ft_spooky_32(uname)
		n = ft_farmhash(uname)
		count[bit_array[i]] += 1
		count[bit_array[j]] += 1
		count[bit_array[k]] += 1
		count[bit_array[l]] += 1
		count[bit_array[m]] += 1
		count[bit_array[n]] += 1

		if count[True] > count[False]:	spam_count['spam'] += 1
		else:	spam_count['not_spam'] +=1
	return (spam_count)

def ft_fpp(n):
	global m
	val = 1 - math.e**(-3*(m/n))
	val = val**3

	return (val)
def main():
	# training data
	print("Training Bloom filter on listed_username_30.txt")
	ft_train()
	# evaluating bloom filter
	print("Evaluating Bloom filter on listed_username_365.txt as data stream")
	spam_counter = ft_evaluate()

	# Writing output file
	print("Writing output file")
	outtext = "The data has been processed line by line (1 username at a time)\n"
	outtext += "Size of data stream (m) = 2,642,941\n"
	outtext += "Size of bit array (n) =\t610,649\n"
	outtext += "Optimal hash functions acc (m/n)ln2 = 3\n"
	outtext += "Bloom filter has been implemented using fnvhash1A_32, murmur3_32, hashxx hash, superfasthash, spooky_32 hash and farm_32 hash functions\n"
	outtext += "Theoretical FPR according to data is :\t{:.4f}\n\n".format(ft_fpp((spam_counter['not_spam']+spam_counter['spam'])))
	outtext += "Spam Count =\t{}\n".format(spam_counter['spam'])
	outtext += "False Positives =\t{}\n".format(spam_counter['not_spam'])
	outtext += "Actual False Positive Rate = \t{:.4f}\n".format(spam_counter['not_spam']/(spam_counter['not_spam']+spam_counter['spam']))

	with open("Output.txt",'w') as fp:
		fp.write(outtext)
	print("Output written")

if __name__ == "__main__":
	main()