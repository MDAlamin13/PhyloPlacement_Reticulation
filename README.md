# PhyloPlacement_Reticulation

Placement_data_simulate.py --> Simulate sequence data and generate the reference tree
run_data_simulation_all_replica.sh --> Run the Placement_data_simulate.py script for all the replicas 
process_per_taxon.py --> Used in the Placement_data_simulate.py script to perform the simulation for a single taxon
run_job_single_replica.sh -- > Run the placement methods for all the plaement queries for a single replica
run_all_replica.sh --> Run the run_job_single_replica.sh script for all the replicas
placement_result_process.py -- > Process the placement tree and calculate the delta errors
analysis_genetrees.py --> Calculate pariwise distances of the set of gene trees generated from ms 

