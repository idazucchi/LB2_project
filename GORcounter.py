import numpy as np


def max_list_position(l):
	max_val = l[0]
	pos = 0
	for i in range(len(l)):
		if l[i]> max_val:
			max_val = l[i]
			pos = i
	# [max_val,pos]
	return pos

class GorCounter:

	# Attributes and methods to compute GOR method

	# Set up dict with window counters for coil Helix strand and aa
	# + list of profile header (aa)
	# + dict of ss type counter and total n° aa
	def __init__(self,w):
		window = np.zeros((w,20))
		self.ss_windows = {'-':window,'H':window,'E':window,'aa_freq':window}
		self.aa = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
		self.ss_prop = {'-':0,'H':0,'E':0,'tot':0}
		self.window_size = w
		self.info = False

	# Counters update with data from a profile window
	def update_counter(self,profile_w,ss):
		# Update window counter: summing the profile window to the counter for the right ss and overall
		self.ss_windows['aa_freq'] = profile_w + self.ss_windows['aa_freq']
		self.ss_windows[ss] = profile_w + self.ss_windows[ss]
		# Update the ss counters
		self.ss_prop[ss] += 1
		self.ss_prop['tot'] += 1

	# Normalise counter for tot number of aa evaluated --> ss_prop[tot]
	def normalize_counter(self):
		# Normalize window counter: summing the profile window to the counter for the right ss and overall
		for key in self.ss_windows.keys():
			self.ss_windows[key] = self.ss_windows[key]/self.ss_prop['tot']
		# Normalize the ss counters
		for key in ['-','E','H','tot']:
			self.ss_prop[key] = self.ss_prop[key]/self.ss_prop['tot']

	# Compute the I(ss,residue R in position d) -> k is the aa index, d is the position in the window
	def extract_pSRk(self,ss_type,d,k):
		p_RS = self.ss_windows[key][d,k]
		p_R = self.ss_windows['aa_freq'][d,k]
		p_S = self.ss_prop[key]
		# Compute I(S,Rk) for position d --> mind the LOG
		p_SRk = np.log(p_RS/(p_R*p_S))
		return p_SRk

	# Convert the counters to windows of precomputed Information function -> I(S,Rk)
	def counter_to_info(self):
		ss_type = ['-','E','H']
		for key in ss_type:
			p_RS = self.ss_windows[key]
			p_R = self.ss_windows['aa_freq']
			p_S = self.ss_prop[key]
			# Compute I(S,Rk) for position d --> mind the LOG
			p_SRk = np.log(p_RS/(p_R*p_S))
			self.ss_windows[key] = p_SRk
		self.info = True

	# Assign ss to the central residue of the profile window
	def assign_SS(self,profile_w):
		# If the counter has been converted to information function matrices
		if self.info:
			ss_type = ['-','E','H']
			info_list = []
			# For each ss compute the information --> sum[I(S,Rk)*aa_frequency]
			for key in ss_type:
				info_M = self.ss_windows[key]*profile_w
				info_list.append(np.sum(info_M))
			ss_i = max_list_position(info_list)
		return ss_type[ss_i]

