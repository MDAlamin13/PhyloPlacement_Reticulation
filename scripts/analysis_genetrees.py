import os,sys
from ete3 import Tree
import glob



species_tree_file=sys.argv[1]
gene_tree_file=sys.argv[2]
#rep =int(sys.argv[3])

species_trees=[]
with open(species_tree_file,'r') as stf:
    for line in stf:
        tree=line.split('\n')[0]
        species_trees.append(tree)

cwd=os.getcwd()
fileexp=gene_tree_file+'*.txt'

num_rep=len(species_trees)
dist_avg_values=[0 for i in range(num_rep)]
total_paritions=[0 for i in range(num_rep)]
unique_trees=[0 for i in range(num_rep)]

for gene_tree_f in glob.glob(fileexp):
	rep=int(gene_tree_f.split('_')[-1].split('.')[0])
	#print("Analysis of gene tree file : %s"%gene_tree_f)
	gene_trees=[]
	with open(gene_tree_f,'r') as f:
		for line in f:
			if line.startswith('['):
				tree=line.split(']')[1].split('\n')[0]
				gene_trees.append(tree)

	if(len(gene_trees)!=0):
		tree_indexes=[]
		for i in range(len(gene_trees)):
			tree_indexes.append(i)

			dist_mat=[]
			dist_species_tree=[]
		same_pairs=[]
		st=Tree(species_trees[rep-1])
		for i in range(len(gene_trees)):
			t1=Tree(gene_trees[i])
			robinson= st.robinson_foulds(t1,unrooted_trees=True)
			dist_species_tree.append(robinson[0]/robinson[1])
			temp_dist=[]
			for j in range(i+1,len(gene_trees)):
				t2=Tree(gene_trees[j])
				robinson= t1.robinson_foulds(t2,unrooted_trees=True)
				if(robinson[0]==0):
					same_pairs.append([i,j])
				temp_dist.append(robinson[0]/robinson[1])
			dist_mat.append(temp_dist)
		#print('Number of gene trees: %s'%str(len(gene_trees)))
		#print('Distances with the species tree: ')
		#print(dist_species_tree)
		avg=sum(dist_species_tree)/len(dist_species_tree)
		dist_avg_values[rep-1]=avg
		total_paritions[rep-1]=len(gene_trees)
		#print('Average dist with species tree: %s'%str(avg))
		#print("Gene tree diatances: ")
		#for row in dist_mat:
		#	print(row)     

		all_sets=[]

		for pair in same_pairs:
			t1=pair[0]
			t2=pair[1]

			found=False
			for s in all_sets:
				if(t1 in s or t2 in s):
					s.add(t1)
					s.add(t2)
					found=True
					break
			if(found==False):
				new_set=set(pair)
				all_sets.append(new_set) 

		for i in range(len(gene_trees)):
			found=False
			for s in all_sets:
				if(i in s):
					found=True
					break
			if(found==False):
				new_set=set([i])
				all_sets.append(new_set)     

		#print(all_sets)
		#print('Number of uniqe gene tree topology: %s\n'%str(len(all_sets)))
		unique_trees[rep-1]=len(all_sets)
                

	else: 
		st=Tree(species_trees[rep-1])
		with open(gene_tree_f,'r') as gtf:
			for line in gtf:
				gene_tree=line.split('\n')[0]
				t1=Tree(gene_tree)
				robinson= st.robinson_foulds(t1,unrooted_trees=True)
				print("Singele gene tree. Distance with species tree: ")
				print('%s \n'%(str(robinson[0]/robinson[1])))

				dist_avg_values[rep-1]=robinson[0]/robinson[1]

X=[x for x in range(1,num_rep+1)]
print(X)
print("Distances")
print(dist_avg_values)
print("Number of gene trees")
print(total_paritions)
print("Number of Unique trees")
print(unique_trees)
