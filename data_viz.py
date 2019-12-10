import matplotlib.pyplot as plt
import palettable as pal
import counters as c
import math
import numpy as np

def adjust_lightness(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

#~ from palettable.colorbrewer.qualitative import Pastel1_7

def fig_A(axes):
	# create data
	names = ['Coil','Strand','Helix']
	size=[c.c,c.e,c.h]
	#~ size=[10,10,10,10,10,10,10,10,20]
	
	
	colors = {'purple':'#b372e6','blue':'#4a82cd','green':'#5aa347','red':'#ff5757','orange':'#ffb32f','yellow':'#ffeb68','turquoise':'#27c9be','pink':'#f687ba','grey':'#b1adac'}
	col = (0.179, 0.114, 0.230, 0.5)
	# Create a circle for the center of the plot
	my_circle=plt.Circle( (0,0), 0.7, color='white')
	
	#~ plt.figure(figsize=(6,5))
	axes.pie(size, labels=names, autopct='%1.1f%%', wedgeprops=dict(width=0.4, edgecolor='w'), pctdistance=0.75, labeldistance=1.1,colors=[colors['blue'],colors['red'],colors['green']])
	
	#~ plt.legend()
	
	'''Fix the dimensions of the canvas'''

def fig_B(ax):
	colors = {'purple':'#b372e6','blue':'#4a82cd','green':'#5aa347','red':'#ff5757','orange':'#ffb32f','yellow':'#ffeb68','turquoise':'#27c9be','pink':'#f687ba','grey':'#b1adac'}
	aa_h_dic={'L': 9536, 'E': 7450, 'R': 4815, 'P': 1509, 'S': 3458, 'H': 1516, 'T': 3271, 'K': 5332, 'V': 5112, 'I': 4821, 'G': 2520, 'Q': 3838, 'D': 3592, 'F': 3066, 'A': 9118, 'W': 1086, 'Y': 2509, 'N': 2309, 'M': 2073, 'C': 811}
	aa_e_dic={'G': 2414, 'L': 4841, 'V': 6494, 'T': 3226, 'Q': 1401, 'E': 2321, 'R': 2406, 'K': 2437, 'P': 1092, 'A': 3131, 'H': 1105, 'C': 822, 'S': 2438, 'Y': 2410, 'F': 2649, 'W': 888, 'D': 1598, 'I': 4634, 'M': 1019, 'N': 1262}
	aa_c_dic={'K': 5336, 'V': 4039, 'S': 6680, 'H': 2276, 'R': 4209, 'T': 5405, 'E': 5768, 'P': 7250, 'G': 10884, 'D': 7488, 'Q': 3114, 'L': 6096, 'N': 5204, 'M': 1598, 'I': 2979, 'C': 1275, 'A': 6138, 'F': 2870, 'Y': 2470, 'W': 1009, 'X': 3}
	
	aa_tot = {}
	for key in aa_h_dic.keys():
		aa_tot[key] = aa_h_dic[key]+aa_e_dic[key]+aa_c_dic[key]
	
	N = []
	for dic in [aa_h_dic,aa_e_dic,aa_c_dic,aa_tot]:
		t = 0
		for k in dic.keys():
			t += dic[k] 
		N.append(t)
	for dic in [aa_h_dic,aa_e_dic,aa_c_dic,aa_tot]:
		i = [aa_h_dic,aa_e_dic,aa_c_dic,aa_tot].index(dic)
		for k in dic.keys():
			dic[k] = float(dic[k])/float(N[i])
	
	aa = ['A',  'E',  'G', 'F', 'I',  'K', 'M', 'L', 'P', 'S', 'R', 'T', 'W', 'V', 'Y','H','N', 'D', 'Q','C',]
	
	ss = ['H','E','C','tot']
	conv = {'H':aa_h_dic,'E':aa_e_dic,'C':aa_c_dic,'tot':aa_tot}
	con = {'H':colors['blue'],'E':colors['red'],'C':colors['green'],'tot':colors['yellow']}
	barWidth = 0.6
	
	
	# Create bars
	for i in ss:
		dic = conv[i]
		heights = [int(math.ceil(dic[key]*100)) for key in aa]
		#~ print len(heights)
		pos = [j-ss.index(i) for j in range(1,len(aa)*4,4)]
		ax.bar(pos, heights, width = barWidth, color = con[i], label=i)
	
	# Create legend
	plt.legend()
	 
	#~ # Text below each barplot with a rotation at 90
	ax.set_xticks( [i for i in range(1,80,4)])
	ax.set_xticklabels(aa)
	ax.set_ylabel('Residue frequency (%)')
	
	 
	# Show graphic
	#~ plt.show()

def fig_CD(axes):
	colors = {'purple':'#b372e6','blue':'#4a82cd','green':'#5aa347','red':'#ff5757','orange':'#ffb32f','yellow':'#ffeb68','turquoise':'#27c9be','pink':'#f687ba','grey':'#b1adac'}
	species={'Homo sapiens (Human)': 245, 'Escherichia coli': 146, 'Bos taurus (Bovine)': 48, 'Thermus thermophilus': 41, 'Salmonella enterica (Salmonella choleraesuis)': 13, 'Bacillus cereus': 6, 'Murine leukemia virus': 1, 'Bacillus subtilis': 34, 'Pyrococcus furiosus': 7, 'Mastigocladus laminosus (Fischerella sp.)': 3, 'Mus musculus (Mouse)': 35, "Saccharomyces cerevisiae (Baker's yeast)": 46, 'Sphingobium sp. (strain NBRC 103272 / SYK-6)': 2, 'Hirudo medicinalis (Medicinal leech)': 2, 'Escherichia phage lambda (Bacteriophage lambda)': 1, 'Clostridium cochlearium': 2, 'Rattus norvegicus (Rat)': 14, 'Bacillus thuringiensis': 1, 'Cowpox virus (CPV)': 1, 'Acinetobacter calcoaceticus': 1, 'Rous sarcoma virus': 3, 'Geobacillus stearothermophilus (Bacillus stearothermophilus)': 14, 'Methanocaldococcus jannaschii': 10, 'Thermotoga maritima': 33, 'Streptomyces clavuligerus': 2, 'Enterobacteria phage T4 (Bacteriophage T4)': 9, 'Aspergillus oryzae (Yellow koji mold)': 1, 'Simian immunodeficiency virus (SIV)': 1, 'Klebsiella oxytoca': 4, 'Ochrobactrum anthropi': 1, 'Tobacco mosaic virus': 1, 'Rhodobacter sphaeroides (Rhodopseudomonas sphaeroides)': 5, 'Tenebrio molitor (Yellow mealworm beetle)': 1, 'Corynephage beta': 1, 'Methanopyrus kandleri': 4, 'Borreliella burgdorferi (Lyme disease spirochete) (Borrelia burgdorferi)': 2, 'Mammalian orthoreovirus': 1, 'Toxoplasma gondii': 2, 'Trypanosoma brucei': 2, 'Methanothermobacter thermautotrophicus (Methanobacterium thermoformicicum)': 11, 'Streptococcus pneumoniae': 5, 'Enterobacteria phage M13 (Bacteriophage M13)': 1, 'Bacillus lentus': 1, 'Klebsiella aerogenes (Enterobacter aerogenes)': 1, 'Cellvibrio japonicus (Pseudomonas fluorescens subsp. cellulosa)': 2, 'Sus scrofa (Pig)': 6, 'Micrococcus luteus (Micrococcus lysodeikticus)': 1, 'Zaire ebolavirus': 1, 'Lysinibacillus sphaericus (Bacillus sphaericus)': 1, 'Methanothermobacter marburgensis': 4, 'Pseudomonas aeruginosa': 21, 'Desulfovibrio vulgaris': 5, 'Thermoascus aurantiacus': 1, 'Haemophilus influenzae': 10, 'Gallus gallus (Chicken)': 14, 'Bacillus thermoproteolyticus': 1, 'Streptococcus pyogenes': 2, 'Bacillus circulans': 1, 'Thermosynechococcus elongatus': 15, 'Fusarium oxysporum (Fusarium vascular wilt)': 1, 'Amaranthus caudatus (Love-lies-bleeding) (Inca-wheat)': 1, 'Archaeoglobus fulgidus': 13, 'Neurospora crassa': 1, 'Enteroctopus dofleini (North Pacific giant octopus) (Octopus dofleini)': 1, 'Saccharolobus solfataricus (Sulfolobus solfataricus)': 10, 'Thermoplasma acidophilum': 5, 'Gibberella zeae (Wheat head blight fungus) (Fusarium graminearum)': 1, 'Magnaporthe oryzae (Rice blast fungus) (Pyricularia oryzae)': 2, 'Chondrostereum purpureum': 1, 'Human immunodeficiency virus 1': 3, 'Aspergillus aculeatus': 1, 'Helicobacter pylori (Campylobacter pylori)': 6, 'Streptomyces lividans': 1, 'Rotavirus A': 1, 'Staphylococcus xylosus': 1, 'Ustilago maydis P6 virus (UmV6) (UmV-P6)': 1, 'Ustilago maydis P4 virus (UmV4) (UmV-P4)': 1, 'Clostridium thermocellum (Ruminiclostridium thermocellum)': 5, 'Methanosarcina mazei (Methanosarcina frisia)': 3, 'Choristoneura fumiferana (Spruce budworm moth) (Archips fumiferana)': 1, 'Rhizobium radiobacter (Agrobacterium tumefaciens) (Agrobacterium radiobacter)': 3, 'Phleum pratense (Common timothy)': 1, 'Aquifex aeolicus': 13, 'Indiana vesiculovirus': 2, 'Limulus polyphemus (Atlantic horseshoe crab)': 2, 'Mycobacterium tuberculosis': 21, 'Lactococcus lactis': 5, 'Thermus aquaticus': 2, 'Ichthyomyzon unicuspis (Silver lamprey)': 1, 'Halobacterium salinarum (Halobacterium halobium)': 5, 'Stenotrophomonas maltophilia (Pseudomonas maltophilia) (Xanthomonas maltophilia)': 1, 'Adeno-associated dependoparvovirus B': 1, 'Deinagkistrodon acutus (Hundred-pace snake) (Agkistrodon acutus)': 1, 'Murid herpesvirus 4 (MuHV-4) (Murine gammaherpesvirus 68)': 2, 'Thermobifida fusca (Thermomonospora fusca)': 2, 'Methylococcus capsulatus': 3, 'Streptomyces olivochromogenes': 1, 'Streptomyces sp. (strain SA-COO)': 1, 'Oligotropha carboxidovorans (Pseudomonas carboxydovorans)': 3, 'Plasmodium falciparum': 3, 'Mamestra brassicae (Cabbage moth)': 1, 'Mammalian 1 orthobornavirus': 1, 'Pseudomonas savastanoi (Pseudomonas syringae pv. savastanoi)': 1, 'Rhodoblastus acidophilus (Rhodopseudomonas acidophila)': 2, 'Drosophila melanogaster (Fruit fly)': 13, 'Bacillus phage SPP1 (Bacteriophage SPP1)': 1, 'Hathewaya histolytica (Clostridium histolyticum)': 1, 'Methanosarcina barkeri': 1, 'Staphylococcus aureus': 18, 'Halorhodospira halophila (Ectothiorhodospira halophila)': 1, 'Spinacia oleracea (Spinach)': 2, 'Treponema pallidum': 1, 'Dickeya chrysanthemi (Pectobacterium chrysanthemi) (Erwinia chrysanthemi)': 1, 'Enterococcus faecalis (Streptococcus faecalis)': 10, 'Synechocystis sp. PCC 6803': 6, 'Aleuria aurantia (Orange peel mushroom)': 1, 'Talaromyces minioluteus (Filamentous fungus) (Penicillium minioluteum)': 1, 'Nostoc sp. (strain PCC 7120 / SAG 25.82 / UTEX 2576)': 3, 'Streptomyces tendae': 1, 'Measles morbillivirus': 1, 'Flammulina velutipes (Agaricus velutipes)': 1, 'Vibrio cholerae': 9, 'Synechococcus elongatus': 2, 'Azotobacter vinelandii': 3, 'Eucommia ulmoides (Hardy rubber tree)': 1, 'Paracoccus denitrificans': 8, 'Clostridium perfringens': 1, 'Yersinia pseudotuberculosis': 1, 'Volvariella volvacea': 1, 'Amphidinium carterae (Dinoflagellate)': 1, 'Schizosaccharomyces pombe (Fission yeast)': 3, 'Aedes aegypti (Yellowfever mosquito) (Culex aegypti)': 1, 'Pseudomonas putida (Arthrobacter siderocapsulatus)': 5, 'Trichomonas vaginalis': 1, 'Geobacillus kaustophilus': 4, 'Paracoccus pantotrophus (Thiosphaera pantotropha)': 1, 'Foot-and-mouth disease virus': 1, 'Deinococcus radiodurans': 5, 'Bacillus licheniformis': 1, 'Meleagris gallopavo (Wild turkey)': 1, 'Tomato bushy stunt virus': 1, 'Trimeresurus stejnegeri (Chinese green tree viper) (Viridovipera stejnegeri)': 1, 'Pyrobaculum aerophilum': 4, 'Vibrio proteolyticus (Aeromonas proteolytica)': 1, 'Paenarthrobacter aurescens (Arthrobacter aurescens)': 1, 'Dictyostelium discoideum (Slime mold)': 1, 'Escherichia virus T7': 1, 'Caenorhabditis elegans': 5, 'Tick-borne encephalitis virus': 1, 'Bacillus sp. MN-32': 1, 'Streptomyces coelicolor': 2, 'Chlamydomonas reinhardtii (Chlamydomonas smithii)': 1, 'Mycoplasma pneumoniae': 2, 'Tachypleus tridentatus (Japanese horseshoe crab)': 1, 'Triticum aestivum (Wheat)': 1, 'Autographa californica multiple nucleopolyhedrovirus': 1, 'Momordica charantia (Bitter gourd) (Balsam pear)': 2, 'Lycodichthys dearborni (Antarctic eelpout) (Rhigophila dearborni)': 1, 'Bacillus phage PBS2 (Bacteriophage PBS2)': 1, 'Penicillium brevicompactum': 1, 'Arabidopsis thaliana (Mouse-ear cress)': 11, 'Oryctolagus cuniculus (Rabbit)': 3, 'Bluetongue virus': 1, 'Pyrococcus horikoshii': 18, 'Naja atra (Chinese cobra)': 1, 'Vaccinia virus': 1, 'Cucumaria echinata (Sea cucumber)': 1, 'Clostridium acetobutylicum': 2, 'Bordetella pertussis': 1, 'Bacteroides thetaiotaomicron': 7, 'Haloarcula marismortui': 29, 'Enterobacter cloacae': 1, 'Argyrosomus regius (Meagre)': 1, 'Paenibacillus polymyxa (Bacillus polymyxa)': 1, 'Bacillus alcalophilus': 1, 'Methylobacterium extorquens (Methylobacterium dichloromethanicum) (Methylorubrum extorquens)': 2, 'Komagataella pastoris (Yeast) (Pichia pastoris)': 1, 'Aspergillus kawachii (White koji mold) (Aspergillus awamori var. kawachi)': 1, 'Oryza sativa (Rice)': 2, 'Pseudomonas syringae group genomosp. 3': 3, 'Sulfurisphaera tokodaii': 2, 'Hordeum vulgare (Barley)': 2, 'Leishmania braziliensis': 1, 'Rhodnius prolixus (Triatomid bug)': 1, 'Human SARS coronavirus (SARS-CoV) (Severe acute respiratory syndrome coronavirus)': 5, 'Rhodomonas sp. (strain CS 24) (Chroomonas sp. (strain CS24))': 3, 'Yersinia pestis': 9, 'Legionella pneumophila': 3, 'Pseudomonas fluorescens': 2, 'Shewanella frigidimarina': 1, 'Listeria monocytogenes': 1, 'Pyrococcus abyssi': 1, 'Bordetella phage BPP-1': 1, 'Xenopus laevis (African clawed frog)': 3, 'Shigella flexneri': 7, 'Enterococcus faecium (Streptococcus faecium)': 2, 'Vibrio parahaemolyticus': 3, 'Agrobacterium fabrum': 6, 'Klebsiella pneumoniae': 3, 'Phytophthora cinnamomi (Cinnamon fungus)': 1, 'Bacillus halodurans': 6, 'Porphyromonas gingivalis': 3, 'Nitrosomonas europaea': 3, 'Hypocrea jecorina (Trichoderma reesei)': 2, 'Ascaris suum (Pig roundworm) (Ascaris lumbricoides)': 1, 'Bovine papillomavirus type 1': 1, 'Yersinia enterocolitica': 1, 'Chromobacterium violaceum': 4, 'Musca domestica (House fly)': 2, 'Helix pomatia (Roman snail) (Edible snail)': 1, 'Leptoxyphium fumago (Caldariomyces fumago)': 1, 'Aeropyrum pernix': 1, 'Thermococcus kodakarensis': 1, 'Klebsiella michiganensis': 1, 'Luciola cruciata (Japanese firefly) (Genji firefly)': 1, 'Xanthomonas campestris': 1, 'Molineria latifolia (Lumbah) (Curculigo latifolia)': 1, 'Pasteurella multocida': 1, 'Geotrichum sp. (strain M128)': 1, 'White spot syndrome virus': 1, 'Euplotes raikovi': 1, 'Burkholderia glumae (Pseudomonas glumae)': 2, 'Streptomyces avidinii': 1, 'Thermococcus litoralis': 1, 'Delftia acidovorans (Pseudomonas acidovorans) (Comamonas acidovorans)': 1, 'Neisseria meningitidis': 2, 'Avian coronavirus': 1, 'Myxococcus xanthus': 1, 'Shewanella loihica': 1, 'Murine coronavirus': 2, 'Griffithsia sp. (strain Q66D336) (Red alga)': 1, 'Listeria innocua': 1, 'Allochromatium vinosum (Chromatium vinosum)': 3, 'Psychrobacter arcticus': 1, 'Staphylococcus epidermidis': 2, 'Geobacter sulfurreducens': 1, 'Lactobacillus plantarum': 1, 'Mycoplasma arthritidis': 1, 'Escherichia phage P1 (Bacteriophage P1)': 1, 'Achromobacter cycloclastes': 1, 'Plasmodium vivax': 1, 'Finegoldia magna (Peptostreptococcus magnus)': 1, 'Streptococcus virus Cp1': 1, 'Human coronavirus 229E (HCoV-229E)': 1, 'Influenza A virus': 4, 'Mycobacterium smegmatis': 2, 'Equus caballus (Horse)': 1, 'Streptomyces macromomyceticus': 1, 'Themiste hennahi (Peanut worm) (Themiste zostericola)': 1, 'Anabaena variabilis': 2, 'Alphapapillomavirus 9': 1, 'Shewanella oneidensis': 2, 'Dioscoreophyllum cumminsii (Serendipity berry) (Rhopalandria cumminsii)': 1, 'Brevundimonas diminuta (Pseudomonas diminuta)': 1, 'Alcaligenes faecalis': 2, 'Bacillus anthracis': 2, 'Colwellia psychrerythraea (Vibrio psychroerythus)': 1, 'Rhodococcus jostii': 1, 'Paraburkholderia xenovorans': 1, 'Corynebacterium glutamicum (Brevibacterium saccharolyticum)': 1, "Human herpesvirus 8 (HHV-8) (Kaposi's sarcoma-associated herpesvirus)": 1, 'Shewanella amazonensis': 1, 'Esox lucius (Northern pike)': 1, 'Bacillus clausii': 1, 'Jannaschia sp. (strain CCS1)': 2, 'Cryptosporidium parvum': 1, 'Salinispora tropica': 1, 'Caldanaerobacter subterraneus': 2, 'Pseudomonas phage PP7 (Bacteriophage PP7)': 2, 'Histophilus somni (Haemophilus somnus)': 1, 'Novosphingobium aromaticivorans (Sphingomonas aromaticivorans)': 1, 'Bacillus amyloliquefaciens (Bacillus velezensis)': 3, 'Streptomyces albogriseolus': 1, 'Thaumatococcus daniellii (Katemfe) (Phrynium daniellii)': 1, 'Ruminiclostridium cellulolyticum': 2, 'Clostridium botulinum': 1, 'Leishmania mexicana': 1, 'Human immunodeficiency virus 2': 1, 'Aplysia californica (California sea hare)': 1, 'Rhodospirillum rubrum': 1, 'Aequorea victoria (Jellyfish)': 1, 'Thermotoga neapolitana': 1, 'Thermus sp. GH5': 1, 'Alcaligenes xylosoxydans xylosoxydans (Achromobacter xylosoxidans)': 1, 'Thermochromatium tepidum (Chromatium tepidum)': 1, 'Aeribacillus pallidus': 1, 'Ustilago sphaerogena (Smut fungus)': 1, 'Streptomyces castaneoglobisporus': 2, 'Nicotiana tabacum (Common tobacco)': 1, 'Leishmania major': 1, 'Bordetella bronchiseptica (Alcaligenes bronchisepticus)': 1, 'Clostridium pasteurianum': 1, 'Lactobacillus reuteri': 1, 'Nostoc ellipsosporum': 1, 'Caulobacter vibrioides (Caulobacter crescentus)': 1, 'Prosthecochloris aestuarii': 1, 'Trypanosoma vivax (Duttonella vivax)': 1, 'Burkholderia pseudomallei (Pseudomonas pseudomallei)': 2, 'Streptococcus sp. group G': 1, 'Alcanivorax borkumensis': 1, 'Pseudomonas mendocina': 4, 'Streptococcus agalactiae': 1, 'Bacillus sp. RAPc8': 2, 'Cupriavidus pinatubonensis': 1, 'Enterobacteria phage K1F (Bacteriophage K1F)': 1, 'Desulfitobacterium hafniense (Desulfitobacterium frappieri)': 1, 'Aspergillus flavus': 1, 'Streptococcus mutans': 2, 'Phanerochaete chrysosporium (White-rot fungus) (Sporotrichum pruinosum)': 1, 'Brucella abortus': 1, 'Chlamydia trachomatis': 1, 'Sphingosinicella xenopeptidilytica': 1, 'Crambe hispanica': 1, 'Loligo vulgaris (Common European squid)': 1, 'Campylobacter jejuni': 1, 'Xenorhabdus nematophila (Achromobacter nematophilus)': 1, 'Danio rerio (Zebrafish) (Brachydanio rerio)': 1, 'Elizabethkingia meningoseptica (Chryseobacterium meningosepticum)': 1, 'Lysobacter enzymogenes': 1, 'Pachyrhizus erosus': 1, 'Glycine max (Soybean) (Glycine hispida)': 1, 'Thermococcus thioreducens': 1, 'Thunnus atlanticus (blackfin tuna)': 1, 'Nectria haematococca': 1, 'Photobacterium profundum': 1, 'Schistocerca gregaria (Desert locust) (Gryllus gregarius)': 1, 'Calloselasma rhodostoma (Malayan pit viper) (Agkistrodon rhodostoma)': 1, 'Xenopus tropicalis (Western clawed frog) (Silurana tropicalis)': 1, 'Cyanidioschyzon merolae (Red alga)': 1, 'Hungateiclostridium cellulolyticum': 1, 'Anas platyrhynchos (Mallard) (Anas boschas)': 1, 'Betula pendula (European white birch) (Betula verrucosa)': 1, 'Sporosarcina pasteurii (Bacillus pasteurii)': 3, 'Rhodobacter capsulatus (Rhodopseudomonas capsulata)': 1, 'Clostridioides difficile (Peptoclostridium difficile)': 2, 'Acinetobacter baumannii': 1, 'Phaseolus vulgaris (Kidney bean) (French bean)': 1, 'Zymomonas mobilis': 1, 'Serratia marcescens': 1, 'Streptomyces cinnamonensis': 1, 'Arachis hypogaea (Peanut)': 1, 'Methanobrevibacter ruminantium': 1, 'Medicago truncatula (Barrel medic) (Medicago tribuloides)': 1, 'Rhizobium meliloti (Ensifer meliloti) (Sinorhizobium meliloti)': 2, 'Physcomitrella patens subsp. patens (Moss)': 1, 'Sporomusa ovata': 2, 'Pseudomonas mevalonii': 1, 'Geodia cydonium (Sponge)': 1, 'Carica papaya (Papaya)': 1, 'Bacteroides vulgatus': 1, 'Thermomonospora curvata': 2}
	superk={'Eukaryota': 556, 'Bacteria': 719, 'Viruses': 67, 'Archaea': 132}
	superk_labels = []
	superk_sizes = []
	for k in superk.keys():
		superk_labels.append(k)
		superk_sizes.append(superk[k])
	# Data to plot
	sp_labels = ['Homo sapiens','M. musculus',"S. cerevisiae",'B. taurus',' ',' ',' ','E. coli','T. thermophilus','B. subtilis',' ']
	sp_size = [245, 35, 46, 48, 182,132, 67, 146, 41, 34, 498]
	
	col = [colors['blue'],colors['red'],colors['yellow'],colors['green']]
	sp_col = [adjust_lightness(colors['blue'],1.15),adjust_lightness(colors['blue'],1.25),adjust_lightness(colors['blue'],1.35),\
		adjust_lightness(colors['blue'],1.45),adjust_lightness(colors['blue'],1.55),adjust_lightness(colors['red'],1.15),\
		adjust_lightness(colors['yellow'],1.15),adjust_lightness(colors['green'],1.15),adjust_lightness(colors['green'],1.25)\
		,adjust_lightness(colors['green'],1.35),adjust_lightness(colors['green'],1.45)]
	 
	# Plot
	axes.pie(superk_sizes, labels=superk_labels, autopct='%1.1f%%', pctdistance=0.98,  colors=col, wedgeprops=dict(width=0.3, edgecolor='w'), startangle=330,frame=True)
	axes.pie(sp_size, labels=sp_labels, colors=sp_col, wedgeprops=dict(width=0.3, edgecolor='w'), labeldistance=0.8,radius=0.75,startangle=330) #
	centre_circle = plt.Circle((0,0),0.5,color='black', fc='white',linewidth=0)
	fig = plt.gcf()
	fig.gca().add_artist(centre_circle)
	 
	plt.axis('equal')
	plt.tight_layout()
	#~ plt.show()

def fig_E(axes):
	colors = {'purple':'#b372e6','blue':'#4a82cd','green':'#5aa347','red':'#ff5757','orange':'#ffb32f','yellow':'#ffeb68','turquoise':'#27c9be','pink':'#f687ba','grey':'#b1adac'}
	scop_classes={'low-resolution': 0, 'All alpha': 325, 'Alpha/eta': 173,  'Alpha + beta': 347,\
		 'Membrane\n proteins': 51,'All beta': 223, 'k': 0, 'i': 0,  'l': 0, 'Multi-domain': 34,'Small proteins': 52, 'h': 0}
	size = []
	labels = []
	for k in scop_classes.keys():
		if scop_classes[k]!=0:
			size.append(scop_classes[k])
			labels.append(k)
	con = [colors['blue'],colors['red'],colors['green'],colors['yellow'],colors['orange'],colors['turquoise'],colors['purple'],colors['pink']]
	#~ plt.figure(figsize=(6,5))
	axes.pie(size, labels=labels, autopct='%1.1f%%', pctdistance=0.75, wedgeprops=dict(width=1, edgecolor='w'),labeldistance=1.1,colors=con)
	#~ axes.tightlayout
	#~ plt.show()

# create the entire figure where our subplots will go
fig = plt.figure(figsize=(9,12))
# tell the figure how the subplots should be laid out
# in the example below we will have
# 2 row of plots, each row will have 2 plots
# subplot has 2 rows and 2 columns, plot location 1
axesl = fig.add_subplot(2 , 2, 1)
axesl.set_title('A')
# subplot has 2 rows and 2 columns, plot location 2
axes2 = fig.add_subplot(2 , 2, 2)
axes2.set_title('B')
# subplot has 2 rows and 2 columns, plot location 3
axes3 = fig.add_subplot(2 , 2, 3)
axes3.set_title('C')
# subplot has 2 rows and 2 columns, plot location 4
axes4 = fig.add_subplot(2 , 2, 4)
axes4.set_title('D')

fig_A(axesl)
fig_B(axes2)
fig_CD(axes3)
fig_E(axes4)
#~ fig.tight_layout()
plt.show()
fig.savefig('fig1.eps', format='eps')
