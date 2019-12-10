import evaluation_ex as eve
import argparse, pickle, os
import numpy as np
from sklearn.metrics import confusion_matrix

def cv_slice_cycle(cv_slice,dssp_path,pred_file,stat_dic):
	'''This function takes in input a list of files used for testing a predictor, the path of the reference dssp,
		the prediction file and the dictionary that stores the statistical indexes.
		For each file the Sov is computed, both for total and for each ss type,
		as well as the ConfusionMatrix, from which are extracted MCC, Q3, TPR and PPV'''

	# Open the file that lists the test files and the svm_prediction
	id_list = open(cv_slice,'r')
	pr = open(pred_file,'r')

	# Initialise the confusion M,  initialise the stat dictionary and set the ss types
	cm = 0
	ss_types = ['H','E','-']
	stat_dic['SOV'][cv_slice] = []
	stat_dic['ss_sov'][cv_slice] = {'H':[],'E':[],'-':[]}

	# Cycle through the cv slice and process each file
	for seq_id in id_list:
		# Get dssp
		dssp = eve.get_fasta(os.path.join(dssp_path, seq_id.rstrip()+'.dssp'))
		# Get corresponding predicted ss
		pred = ''
		for i in range(len(dssp)):
			pred += pr.readline().rstrip()
		pred = pred.replace('1','H').replace('2','E').replace('3','-')
		# Compute confusion matrix
		cm += confusion_matrix(np.array(list(dssp)),np.array(list(pred)), labels=ss_types)
		# Update SOV list !! ss_sov is updated inside the sov() --> only need the corresponding dict
		stat_dic['SOV'][cv_slice].append(eve.sov(pred,dssp,stat_dic['ss_sov'][cv_slice]))

	# Now that the confusion M is complete compute stat indezes
	Q3 = sum(np.diag(cm))/sum(sum(cm))
	stat_dic['Q3'].append(Q3)
	# For each ss type compute the One.vs.All CM
	for q in range(3):
		ss = ss_types[q]
		indexes = [0,1,2]
		indexes.pop(q)
		i,j = indexes[0],indexes[1]
		a = np.array([cm[i]+cm[j],cm[q]])
		b = np.array((list([a[0][i]+a[0][j],a[0][q]]),list([a[1][i]+a[1][j],a[1][q]])))
		# Assign TN, FP, FN, TP  and derive MCC, TPR and PPV
		TN, FP, FN, TP = b[0][0], b[0][1], b[1][0], b[1][1]
		d = ((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))**(1/2)
		stat_dic['MCC'][ss].append(((TP*TN)-(FP*FN))/d)
		stat_dic['TPR'][ss].append((TP)/(TP+FN))
		stat_dic['PPV'][ss].append(TP/(TP+FP))    # precision
	print(cm,Q3)
	id_list.close()
	pr.close()



if __name__=='__main__':
	'''Take as input cv_slices.list dssp_path gor_path or svm_path outfile
		p=$(pwd)
		python3 evaluation_ex.py -l fake_id -d $p -p $p '''

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", dest="cv_set_list", help="insert a list of the file name for the different cv slices used for testing")
	parser.add_argument("-d", dest="dssp_path", help="insert the path of the dssp files to use as reference")
	parser.add_argument("-p", dest="pred_file", help="insert the file with the predicted ss")
	parser.add_argument("-o", dest="out_file", default='svm_stat.py', help="Dump for the statistics dictionary")
	parser.add_argument("-s", dest="stat", default='/home/um90/blank_stat.py', help="Insert stat file dump to add information to a given dataset")

	args = parser.parse_args()

	##################### Set up for statistics ########################
	# Load the trained GOR model and extract window size
	with open(args.stat, 'rb') as f:
		stat_index = pickle.load(f)


	######################### File cycling #############################
	# For each cv slice listed in the cv_list perform the stat evaluation
	#~ with open(args.cv_set_list,'r') as cv_list:
		#~ for cv_slice in cv_list:

	# One slice at a time, one parameter set at a time
	cv_slice_cycle(args.cv_set_list,args.dssp_path,args.pred_file,stat_index)
	#~ print(stat_index)
	print(stat_index.keys(),stat_index['SOV'].keys(),stat_index['ss_sov'].keys())

	###################### Results ~hopefully~ #########################
	# Dump the statistics dictionary with pickle
	with open(args.out_file, 'wb') as f:
		pickle.dump(stat_index, f)


