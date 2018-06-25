import nltk
from nltk.stem.snowball import SnowballStemmer
import re
import os
import glob
import json

CLUSTER_SIZE = 10

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def save_as_json(data,json_name):
	with open(json_name, 'w') as f:
		json.dump(data, f)
	print("save_as_json() completed")

def read_data_from_files(file_names, start_index):
	postings = dict()
	"""
	postings is likes this:
	{ term_a : { doc_id_x : [ pos1, pos2 ] ,
				 doc_id_y : [ pos3, pos4 ] }
	  term_b : { doc_id_y : [ pos5, pos6 ] ,
			     doc_id_z : [ pos7, pos8 ] } }
	"""

	for doc_id,file_name in enumerate(file_names):
		file = open(file_name,"r")
		content = file.read()
		#print(content)
		tokens = nltk.word_tokenize(content)
		#print(tokens)
		stemmer = SnowballStemmer("english")
		stemmed_tokens = [ stemmer.stem(token) for token in tokens ]
		#print(stemmed_tokens)
		result_tokens = []
		for token in stemmed_tokens:
			if re.search('(\D/|/\D)',token):
				for tk in re.split('(/)',token):
					result_tokens.append(tk)
			else:
				result_tokens.append(token)
		#print(result_tokens)
		print(doc_id+1,"/",len(file_names))

		for pos,token in enumerate(result_tokens):
			if token in postings:
				if doc_id in postings[token]:
					postings[token][doc_id].append(pos)
				else:
					postings[token][doc_id] = [pos]
			else:
				postings[token] = dict()
				postings[token][doc_id] = [pos]
	print(postings)

	tf_info = dict()
	"""
	tf_info is likes this:
	{ term_a : {    -1    : tf_a  ,
				 doc_id_x : tf_ax ,
				 doc_id_y : tf_ay }
	  term_b : {    -1    : tf_b  ,
	  			 doc_id_y : tf_by ,
			     doc_id_z : tf_bz } }
	"""

	for term,posting in postings.items():
		if term not in tf_info:
			tf_info[term] = dict()
		sum = 0
		for doc_id,pos_list in posting.items():
			length = len(pos_list)
			tf_info[term][doc_id] = length
			sum += length
		tf_info[term][-1] = sum #the doc_id of -1 means total tf
	print(tf_info)

	data = [postings, tf_info]
	"""
	data is like this:
	[postings, tf_info]
	"""
	return data

def read_data_from_path(src_path, dest_path):
	json_name = dest_path+"filenames.json"
	if os.path.exists(json_name):
		with open(json_name, 'r') as f:
			old_file_names = json.load(f)
	file_names = glob.glob(src_path+"*.html")
	save_as_json(file_names, json_name)
	new_file_names = list(set(file_names).difference(set(old_file_names)))
	print(new_file_names)
	data_file_names = glob.glob(dest_path+"data[0-9]*.json")
	indices = list()
	for name in data_file_names:
		str_id = re.search("data([0-9]*).json",name).group(1)
		indices.append(int(str_id))
	last_index = max(indices)
	print(last_index)

	length = len(new_file_names)
	start_index = last_index + 1
	for index,file_names_part in enumerate(chunks(new_file_names,CLUSTER_SIZE)):
		data = read_data_from_files(file_names_part,start_index)
		save_as_json(data, dest_path+"data"+str(index)+".json")
		start_index += CLUSTER_SIZE

###################################################################################
if __name__ == "__main__":
	source_path = "E:\\Jiaming\\Documents\\课程资料及作业\\信息检索\\src\\"
	destination_path = "../TermResource/"
	read_data_from_path(source_path, destination_path)