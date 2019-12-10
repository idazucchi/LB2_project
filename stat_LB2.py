import numpy as np
import pickle, argparse

def stat(d,s,t,k):
	#~ print(d,'>>>><<<',k)
	#~ print(k)
	mean = np.nanmean(d[k])
	s[k].append(mean)
	err = np.nanstd(d[k])
	s[k].append(err)
	t[k] += '& %r $\\pm$ %r '%(round(mean,2),round(err,2))

def print_d(d): 
	for k in d.keys():
		if type(d[k])==dict:
			print(k)
			print_d(d[k])
		else:
			print(' & %s  %s \\\\'%(str(k),d[k]))  

def average(d,s,t,comm=stat):
	for k in d.keys():
		if type(d[k])==dict:
			print(k)
			average(d[k],s[k],t[k],comm)
			#~ average(d[k],s,t,comm)
		else:
			print(k)
			comm(d,s,t,k)
			#~ comm

def dic_cy(d,s):
	for k in d.keys():
		print(d.keys(),s.keys())
		if type(d[k])==dict:
			print(k)
			dic_cy(d[k],s[k])
		else:
			print(k,len(d[k]))

def stat_elab(stat):
	# Load the statistics file 
	with open(stat, 'rb') as f:
		stat_index = pickle.load(f)
	
	new_Sov = []
	for i in stat_index['SOV'].keys():
		print(len(stat_index['SOV'][i]))
		new_Sov.append(np.nanmean(stat_index['SOV'][i]))
	#~ print(len(new_Sov['SOV']))
	stat_index['SOV'] = new_Sov
	
	print(stat_index['SOV'],np.nanmean(stat_index['SOV']))
	new_ss_sov = {'H':[],'E':[],'-':[]}
	for ss in new_ss_sov.keys():
		for i in stat_index['ss_sov'].keys():
			new_ss_sov[ss] += stat_index['ss_sov'][i][ss]			
			#~ print(len(new_ss_sov[ss]))
	stat_index['ss_sov'] = new_ss_sov
	return stat_index


if __name__=='__main__':
	'''Take as input cv_slices.list dssp_path gor_path or svm_path outfile
		p=$(pwd)
		python3 evaluation_ex.py -l fake_id -d $p -p $p '''
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", dest="input_file", help="insert a list of the file name for the stat files to print out")
	args = parser.parse_args()
	
	##################### Set up for statistics ########################
	
	# Load a blank dictionary for the table and one for the numbers
	with open('../blank_stat.py', 'rb') as w:
		recap = pickle.load(w)
	recap['SOV'] = []
	recap['ss_sov'] = {'-':[], 'H':[], 'E':[]}
	tab = {'ss_sov': {'-':'', 'H':'', 'E':''}, 'TPR': {'-':'', 'H':'', 'E':''}, 'PPV': {'-':'', 'H':'', 'E':''}, \
		'SOV':'', 'Q3':'', 'MCC': {'-':'', 'H':'', 'E':''}}
	#~ print(recap)
	
	ida = stat_elab(args.input_file)
	svmb = stat_elab('blind_svm.py')
	gorb = stat_elab('blind_gor.py')
	vi = stat_elab('stat_svm_g2_c4.py')
	msm = stat_elab('stat_svm_g2_c2.py')
	maria = stat_elab('stat_svm_g05_c2.py')
	#~ dic_cy(stat_dic,tab)
	
	average(svmb,recap,tab)
	average(gorb,recap,tab)
	
	print_d(tab)
	
