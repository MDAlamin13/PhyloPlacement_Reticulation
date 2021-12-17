import sys
import os
from ete3 import Tree
from Bio import SeqIO
import subprocess
import random



def create_camifiles(rep,query_file,out_dir,sample_size):
    cwd = os.getcwd()
    cami_loc='/mnt/home/alaminmd/research/metagenomics/simulation/camisim/CAMISIM-master/'
    out1='genome_to_id_'+str(rep)+'.tsv'
    out2='metadata_'+str(rep)+'.tsv'
    out3='default_config_'+str(rep)
    cami_default_config=cami_loc+'defaults_1/default_config.ini'

    with open(out1,'w') as o1:
        genome_name='Genome1'
        file_loc=cwd+'/'+query_file
        o1.write('%s\t%s\n'%(genome_name,file_loc))
    with open(out2,'w') as o2:
        o2.write('genome_ID\tOTU\tNCBI_ID\tnovelty_category')
        o2.write('\n')
        genome_name='Genome1'
        otu=str(rep)
        o2.write('%s\t%s\t2\tnew_species\n' % (genome_name,otu))
    with open(out3,'w') as o3:
        with open(cami_default_config,'r') as cmf:
            for line in cmf:
                if line.startswith('output_directory'):
                    l='output_directory='+out_dir+'\n'
                    o3.write(l)

                elif line.startswith('samtools=tools/samtools-1.3/samtools'):
                    l='samtools='+cami_loc+'tools/samtools-1.3/samtools\n'
                    o3.write(l)
                elif line.startswith('readsim=tools/art_illumina-2.3.6/art_illumina'):
                    l='readsim='+cami_loc+'tools/art_illumina-2.3.6/art_illumina\n'
                    o3.write(l)
                elif line.startswith('error_profiles=tools/art_illumina-2.3.6/profiles/'):
                    l='error_profiles='+cami_loc+'tools/art_illumina-2.3.6/profiles/\n'
                    o3.write(l)
                elif line.startswith('size='):
                    l='size='+sample_size+'\n'
                    o3.write(l)                
                elif line.startswith('ncbi_taxdump=tools/ncbi-taxonomy_20170222.tar.gz'):
                    l='ncbi_taxdump='+cami_loc+'tools/ncbi-taxonomy_20170222.tar.gz\n'
                    o3.write(l)
                elif line.startswith('strain_simulation_template=scripts/StrainSimulationWrapper/sgEvolver/simulation_dir/'):
                    l='strain_simulation_template='+cami_loc+'scripts/StrainSimulationWrapper/sgEvolver/simulation_dir/\n'
                    o3.write(l)
                elif line.startswith('metadata=defaults_1/metadata.tsv'):
                    l='metadata='+out2+'\n'
                    o3.write(l) 
                elif line.startswith('id_to_genome_file=defaults_1/genome_to_id.tsv'):
                    l='id_to_genome_file='+out1+'\n'
                    o3.write(l)
                else:
                    o3.write(line)                                   
    cami_run_cmd='python '+cami_loc+'metagenomesimulation.py '+out3
    env_change_run='source activate camisim_bear && '+cami_run_cmd+' && conda deactivate'
    subprocess.run(env_change_run, shell=True)

taxon=sys.argv[1]
sample_size=sys.argv[2]
replica_path=sys.argv[3]

os.chdir(replica_path)

script_path="/mnt/home/alaminmd/research/scripts"

i=int(taxon)

taxa_folder=str(i)
cmd='mkdir '+taxa_folder
os.system(cmd)
cwd=os.getcwd()
os.chdir(taxa_folder)
cmd='python '+script_path+'/split_ref_query.py ../aln.fa '+str(i)+' query.fa ref.fa'
os.system(cmd)
'''
### camisim and asssembly ####
q_file='query_seq.fa'
ref_file='ref.fa' 
out_dir='camiout_'+str(i)
out_dir_cmd='mkdir '+out_dir
os.system(out_dir)
create_camifiles(i,q_file,out_dir,sample_size)
assembl_folder='assembly_'+str(i)
#assembly_cmd='megahit -m 0.8 -o '+assembl_folder+' --12 '+out_dir+'/2021*/reads/anonymous_reads.fq.gz'
#os.system(assembly_cmd)

assembly_cmd='metaspades.py -o '+assembl_folder+' --12 '+out_dir+'/2021*/reads/anonymous_reads.fq.gz -m 750'
os.system(assembly_cmd)

## Change the name scaffolds.fasta accordign to the assembler used ##

cmd='perl '+script_path+'/filter_mags.pl 200 '+assembl_folder+'/scaffolds.fasta > filtered_contigs.fasta'
os.system(cmd)

cmd='grep ">" filtered_contigs.fasta > contig_list.txt'
os.system(cmd)


with open('contig_list.txt','r') as conf:
    count=0
    for line in conf:
        contig=line.split('\n')[0].split('>')[1]
        cmd='python '+script_path+'/separate_query_alignments.py filtered_contigs.fasta '+contig+' temp_q.fasta'
        os.system(cmd)

        temp_aln='temp_aln.fasta'
        mafft_cmd='mafft --auto --addfragments temp_q.fasta --thread -1 '+ref_file+' > '+temp_aln
        os.system(mafft_cmd)

        cmd='python '+script_path+'/separate_query_alignments.py temp_aln.fasta '+contig+' temp_q_alingned.fasta'
        os.system(cmd)

        cmd='cat temp_q_alingned.fasta >> queries.fa'
        os.system(cmd)
        count+=1
        if(count==30):
            break
'''
