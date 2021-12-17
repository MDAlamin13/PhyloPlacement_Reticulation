import sys
import os
from ete3 import Tree
from Bio import SeqIO
import subprocess
import random

script_path="/mnt/home/alaminmd/research/scripts"
parent_fold=os.getcwd()


ms_command_file=sys.argv[1]
model_tree_file=sys.argv[2]
rep=int(sys.argv[3])
num_taxa=sys.argv[4]
sample_size=sys.argv[5]
num_ret=int(sys.argv[6])

outgrp=int(num_taxa)+1
#ms_command=''
model_trees=[]

ms_commands=[]
with open(ms_command_file,'r') as mscf:
    for line in mscf:
        ms_command=line.split('\n')[0]
        ms_commands.append(ms_command)
        
with open(model_tree_file,'r') as mtf:
    for line in mtf:
        model_tree=line.split('\n')[0]
        model_trees.append(model_tree)    


### running ms and seq-gen for a single replica

cmd=ms_commands[rep-1]
#os.system(cmd)

output_file=cmd.split('> ')[1] ##contains the file prefix infos

seq_gen_tree=output_file
#cmd='tail -n +4 '+output_file+' | grep -v // > '+seq_gen_tree
#os.system(cmd)
num_tree=0
with open(output_file,'r') as outf:
    for line in outf:
        num_tree+=1
print('%s\n'%str(num_tree))

genetrees_file='genetrees_'+str(rep)+'.txt'
cmd='head -1 '+genetrees_file+' > '+seq_gen_tree
os.system(cmd)
seq_file=output_file.split('.txt')[0]+'.fasta'
rd=random.randrange(12345, 999999, 15)
print(seq_gen_tree)
if(num_ret==0):
    seq_cmd='seq-gen -mHKY -l 1000 -s 0.5 '+seq_gen_tree+' > '+seq_file
else:
    seq_cmd='seq-gen -mHKY -l 1000 -p '+str(num_tree)+' -s 0.5 -z '+str(rd)+' '+seq_gen_tree+' > '+seq_file
os.system(seq_cmd)


msa_file=output_file.split('.txt')[0]+'_all_aln.fasta'

msa_file_outgroup=output_file.split('.txt')[0]+'_all_aln_outgrp.fasta'
concat_cmd='python '+script_path+'/concat_all_loci.py '+seq_file+' '+msa_file
os.system(concat_cmd)

### removing the outgrp sequence
#cmd='python '+script_path+'/split_ref_query.py '+msa_file_outgroup+' '+str(outgrp)+' qtemp.fasta '+msa_file
#os.system(cmd)

#cmd='rm qtemp.fasta '+msa_file_outgroup
#os.system(cmd)

replica_folder=str(rep)
cmd='mkdir '+replica_folder
os.system(cmd)

cmd='mv '+msa_file+' '+replica_folder
os.system(cmd)

os.chdir(replica_folder)

unique_id=str(num_taxa)+'_'+str(rep)
rd=random.randrange(12345, 999999, 15)
cmd='raxmlHPC-PTHREADS-AVX2 -s '+msa_file+' -n '+unique_id+' -p '+str(rd)+' -m GTRGAMMA -T 6'
os.system(cmd)

cmd='mv '+msa_file+' aln.fa'
os.system(cmd)

rax_tree='RAxML_bestTree.'+unique_id
cmd='mv '+rax_tree+' reference_rax.tree'
os.system(cmd)

count=0
for i in range(1,int(num_taxa)+1):
    curr_path=os.getcwd()
    #cmd='sbatch -A liulab '+parent_fold+'/batch.sh '+ str(i)+' '+str(sample_size)+' '+curr_path+' '+parent_fold
    cmd=parent_fold+'/batch.sh '+ str(i)+' '+str(sample_size)+' '+curr_path+' '+parent_fold
    os.system(cmd) 
    count+=1
