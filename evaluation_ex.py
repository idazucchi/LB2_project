import argparse, re, os, pickle
import numpy as np
from sklearn.metrics import confusion_matrix

'''Decide on the output format, Fucking comment this shit
	MAYBE include dict structure in the def of cv_slice_cycle and then sum them in the script main'''

def getOverlap(a, b):
	'''Returns 0 if no overlap between the ranges is found,
		otherwise returns the range of the overlap'''
	return max(0, min(a[1], b[1]) - max(a[0], b[0]))

def get_fasta(fasta_like):
	'''Given the path to a fasta-like file, it returns the fasta string'''
	with open(fasta_like,'r') as f:
		f.readline()
		return f.readline().rstrip()

'''Improve with flags?? So to stop if there is no more match :)??
		only doing this if it is suuuper slow! '''
def ss_type_sov(p,d,ss):
	'''Given a reference and predicted ss sequence, and a ss type,
		this function returns the ss type sov, N and partial SOV '''
	# Find ss segments in dssp and predicted ss seq
	ss_re = re.compile(ss)
	ss_iter = ss_re.finditer(d)
	pred_ss_spans = [i.span() for i in ss_re.finditer(p)]

	# Initialise the N --> normalisation
	N = 0
	sov_ss = 0

	# Loop through the ss segments in the dssp seq
	for segment in ss_iter:
		# Flag to include the segments with no match in the N factor
		has_overl = False
		len_seg = segment.end()-segment.start()
		# Loop over the segments found in the predicted ss
		for i in pred_ss_spans:
			minov = getOverlap(segment.span(),i)
			# If overlap is present add the term to the growing sov
			if minov!=0:
				has_overl = True
				N += len_seg
				maxov = max(segment.end(), i[1]) - min(segment.start(), i[0])
				delta = min(maxov-minov, minov, int(len_seg/2), int((i[1] -i[0])/2))
				#~ print(maxov-minov, minov, int(len_seg/2), int((i[1] -i[0])/2))
				#~ print(minov,maxov,segment.span(),segment.group(),i, len_seg, delta)
				sov_ss += ((minov+delta)/maxov)*len_seg
		# If the segment had no match add the segment to N
		if not has_overl:
			N += len_seg
	if N==0:
		# return nan instead of 0 because the ss is completel missing and it would skew the averages later on
		return N, sov_ss, np.nan
	ss_type_sov = sov_ss*100/N
	return N, sov_ss, ss_type_sov

def sov(p,d,ss_sov_dic):
	'''This function returns the SOV, given a reference and predicted ss sequence.
		It also stores the ss_sov for each ss type in a dictionary --> {'H':[],'E':[],'-':[]}'''
	# Initialise the N --> normalisation
	N_tot = 0
	sov = 0

	# for each type of ss compute partial sov
	for ss_type in ['H*H','E*E','-*-']:
		N,partial_sov_ss,x = ss_type_sov(p,d,ss_type)
		N_tot += N
		sov += partial_sov_ss
		# Update dictionary with ss_sov
		ss_sov_dic[ss_type[0]].append(x)
	return sov*100/N_tot



def cv_slice_cycle(cv_slice,dssp_path,pred_path,stat_dic,blind=False):
	'''This function takes in input a list of files used for testing a predictor, the path of the reference dssp
		and that of the predictions, and the dictionary that stores the statistical indexes.
		For each file the Sov is computed, both for total and for each ss type,
		as well as the ConfusionMatrix, from which are extracted MCC, Q3, TPR and PPV'''
	# Open the file that lists the test files (cv slice)
	id_list = open(cv_slice,'r')

	# Initialise the confusion M,  initialise the stat dictionary and set the ss types
	cm = 0
	ss_types = ['H','E','-']
	stat_dic['SOV'][cv_slice] = []
	stat_dic['ss_sov'][cv_slice] = {'H':[],'E':[],'-':[]}
	if  not blind:
		pred_path = pred_path + cv_slice[-6]

	# Cycle through the cv slice and process each file
	for seq_id in id_list:
		# Get dssp and predicted ss
		pred = get_fasta(os.path.join(pred_path, seq_id.rstrip()+'.gor'))
		dssp = get_fasta(os.path.join(dssp_path, seq_id.rstrip()+'.dssp'))
		#print(pred)
		#print(seq_id)
		# Compute confusion matrix
		cm += confusion_matrix(np.array(list(dssp)),np.array(list(pred)), labels=ss_types)
		# Update SOV list !! ss_sov is updated inside the sov() --> only need the corresponding dict
		stat_dic['SOV'][cv_slice].append(sov(pred,dssp,stat_dic['ss_sov'][cv_slice]))

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



if __name__=='__main__':
	'''Take as input cv_slices.list dssp_path gor_path or svm_path outfile
		p=$(pwd)
		python3 evaluation_ex.py -l fake_id -d $p -p $p '''

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", dest="cv_set_list", help="insert a list of the file name for the different cv slices used for testing")
	parser.add_argument("-d", dest="dssp_path", help="insert the path of the dssp files to use as reference")
	parser.add_argument("-p", dest="pred_path", help="insert the path of the predicted ss sequences")
	parser.add_argument("-o", dest="out_file", default='ex_stat.py', help="Dump for the statistics dictionary")
	args = parser.parse_args()

	####################### Set up for statistics ######################
	# Dictioray structured to collect all stat indexes for each cv slice
	stat_index = { 'TPR':{'H':[],'E':[],'-':[]}, 'PPV':{'H':[],'E':[],'-':[]}, 'MCC':{'H':[],'E':[],'-':[]},\
					'ss_sov':{}, 'Q3':[], 'SOV':{}}

	######################### File cycling #############################
	# For each cv slice listed in the cv_list perform the stat evaluation
	with open(args.cv_set_list,'r') as cv_list:
		for cv_slice in cv_list:
			cv_slice_cycle(cv_slice.rstrip(),args.dssp_path,args.pred_path,stat_index)
	#~ print(stat_index)
	print(stat_index.keys(),stat_index['SOV'].keys(),stat_index['ss_sov'].keys())

	###################### Results ~hopefully~ #########################
	# Dump the statistics dictionary with pickle
	with open(args.out_file, 'wb') as f:
		pickle.dump(stat_index, f)





	########################## SOV Benchmark ###########################
	#~ d = 'CHHHHHHHHHHC'
	#~ p = 'CHCHCHCHCHCC' #12.5
	#~ p = 'CCCHHHHHCCCC' 63.2
	#~ p = 'CHHHCHHHCHHC' 40.6
	#~ p = 'CHHCCHHHHHCC' 52.3
	#~ p = 'CCCHHHHHHCCC' 80.5
	#~ print(sov(p,d))



