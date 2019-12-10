import argparse
import os
import numpy as np
import cv_prep as cv


def SVM_vectorisation(ofile,w,dssp,profile):
	'''Given a dssp and corresponding profile for each aa extraxct a feature vector'''
	# Correspondence between ss and SVM classes
	cl = {'H':1,'E':2,'-':3}

	# Initialise the window
	window = np.zeros((w//2+1,20))
	window = list(window)

	# Extract the secondary structure from file
	with open(dssp) as d:
		d.readline()
		ss = d.readline().rstrip()

	# Open the profile file & drop the header
	p = open(profile)
	p.readline()


	# Prep window for sliding: load the first w-1 lines
	while len(window)<w:
		# It's a bit cumbersome but it turns the string into float
		window.append(list(map(float,p.readline().split()[2:])))
	#~ print(len(window),window)


	# Window sliding + vectorisation
	for i in range(len(ss)):
		window = window[1:]
		line = list(map(float, p.readline().split()[2:]))
		if line==[]:
			window.append(list(np.zeros(20)))
		else:
			window.append(line)
		# Vectorisation
		k = 0
		v = str(cl[ss[i]])
		for h in range(w):
			for j in range(20):
				k += 1
				v += ' %r:%r'%(k,window[h][j])
		# Save vector to output
		ofile.write(v+'\n')

	p.close()

def ids_to_SVM_vectors(id_file,profile_path,dssp_path,window_size,outf):
	''' Given a id list of dssp+profiles cycles through it and vectorises each window. Saves each vector in outf'''

	# Open the output file
	outfile = open(args.outf,'w')

	#################### File cycling ########################
	with open(args.id_file,'r') as id_list:
		for ID in id_list:
			id_profile = os.path.join(args.profile_path, ID.rstrip()+'.profile')
			id_dssp = os.path.join(args.dssp_path, ID.rstrip()+'.dssp')
			SVM_vectorisation(outfile,args.window_size,id_dssp,id_profile)


	# Close output file to save progress
	outfile.close()




if __name__=='__main__':
	'''Take as input id_list dssp_path profile_path (dump_name window_size)
		p=$(pwd)
		python3 svm_prep.py -l fake_id -d $p -p $p -w 3 '''

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", dest="id_file", help="insert list of the file ids to build the SVM training set")
	parser.add_argument("-d", dest="dssp_path", help="insert the path of the dssp files to build the training set")
	parser.add_argument("-p", dest="profile_path", help="insert the path of the profile files to build the training set")
	parser.add_argument("-o", dest="outf", default='svm_test.txt', help="file to collect the feature vectors")
	parser.add_argument("-w", dest="window_size", default=5, help="insert window size to use in training", type=int)
	parser.add_argument("-training", dest="training", default=False, help="If True joins the different cv slices to make one file for SVM training", type=bool)
	args = parser.parse_args()

	if args.training:
		# Fuse the different vector cv slices to make the training files
		x = input('How many cv files have to be fused for training?\n')
		out_path = os.path.dirname(os.path.abspath(args.outf))
		cv.xfold_training(int(x),out_path,'.svm')
	else:
		# Convert into vectors for SVM each window form the id_file
		ids_to_SVM_vectors(args.id_file,args.profile_path,args.dssp_path,args.window_size,args.outf)

