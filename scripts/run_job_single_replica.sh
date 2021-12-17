#!/bin/bash

rep=$1
num_taxa=$2
cwd=`pwd`
out_apple="$cwd/result_apple_$rep.txt"
out_pplacer="$cwd/result_pplacer_$rep.txt"
out_epang="$cwd/result_epang_$rep.txt"
out_sepp="$cwd/result_sepp_$rep.txt"

#compare_path="/mnt/home/alaminmd/research/metagenomics/placement"
spliting_path="/mnt/home/alaminmd/research/scripts"
scripts="/mnt/home/alaminmd/research/scripts"

tree_file="$num_taxa.txt"
echo "$tree_file" 
#cd $taxa
cd $rep
head -$rep ../$tree_file|tail -1 > true_topo.tree  

rm *.REF
raxmlHPC-PTHREADS-AVX2 -f e -t reference_rax.tree -m GTRGAMMA -p 88 -n REF -s aln.fa -T 4
python ~/research/scripts/fasta_phylip.py aln.fa aln.phy
fastme -dJ -i aln.phy -u RAxML_result.REF -o reference_rax_me.tree -T 1
for ((i=1;i<=$num_taxa;i++))
do
cd $i

nw_prune ../reference_rax_me.tree $i > backbone_rax_me.tree
nw_prune ../RAxML_result.REF $i > backbone_rax.tree

#python $spliting_path/ref_query_split.py ../aln.fa $i query.fa ref.fa

echo "apple_running"
time run_apples.py -q query.fa -s ref.fa -t backbone_rax_me.tree -o placement_apple.jplace
guppy tog -o placement_apple.tree placement_apple.jplace

echo "q_$i" >> $out_apple
python  $scripts/compareTrees.py ../true_topo.tree placement_apple.tree >> $out_apple
python  $scripts/compareTrees.py ../true_topo.tree backbone_rax_me.tree >> $out_apple


cd ..
done
cd ..
cd ..


