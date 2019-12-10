import evaluation_ex as eve
import numpy as np
import argparse, pickle, os
from sklearn.metrics import confusion_matrix

if __name__=='__main__':
	'''Take as input cv_slices.list dssp_path gor_path or svm_path outfile
		p=$(pwd)
		python3 evaluation_ex.py -l fake_id -d $p -p $p '''

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", dest="cv_set_list", help="insert file list of the protein to use for blind testing")
	parser.add_argument("-d", dest="dssp_path", help="insert the path of the dssp files to use as reference")
	parser.add_argument("-p", dest="pred_path", help="insert the path of the predicted ss")
	parser.add_argument("-o", dest="out_file", default='svm_stat.py', help="Dump here the computed statistics dictionary")
	parser.add_argument("-s", dest="stat", default='/home/um90/blank_stat.py', help="Insert non-blank stat file dump to grow")
	parser.add_argument("-blind", dest="blind", default=False, help="If True the pred_path is not altered", type=bool)
	args = parser.parse_args()

	##################### Set up for statistics ########################
	# Load the trained GOR model and extract window size
	with open(args.stat, 'rb') as f:
		stat_index = pickle.load(f)


	######################### File cycling #############################
	# For the blind test set all prediction files are in one folder
	if args.blind:
		print('Blind is ',args.blind,' initiating blind testing')
		eve.cv_slice_cycle(args.cv_set_list,args.dssp_path,args.pred_path,stat_index,args.blind)
	print(stat_index.keys(),stat_index['SOV'].keys(),stat_index['ss_sov'].keys())

	###################### Results ~hopefully~ #########################
	# Dump the statistics dictionary with pickle
	with open(args.out_file, 'wb') as f:
		pickle.dump(stat_index, f)

