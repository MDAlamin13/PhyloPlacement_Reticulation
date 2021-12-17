# PhyloPlacement_Reticulation

Placement_data_simulate.py --> Simulates sequence data and generates the reference tree
run_data_simulation_all_replica.sh --> Runs the Placement_data_simulate.py script for all the replicas 
process_per_taxon.py --> Used in the Placement_data_simulate.py script to perform the simulation for a single taxon
run_job_single_replica.sh -- > Runs the placement methods for all the plaement queries for a single replica
run_all_replica.sh --> Runs the run_job_single_replica.sh script for all the replicas
placement_result_process.py -- > Processes the placement tree and calculate the delta errors
analysis_genetrees.py --> Calculates pariwise distances of the set of gene trees generated from ms 

