#/bin/bash

# Load DO and human doa and extracts stats
fastsemsim --ontology_type DiseaseOntology --ac_species human  -vv --task stats

# Load GO and human goa and extracts stats
fastsemsim --ontology_type GeneOntology --ac_species human  -vv --task stats

# The file example_cmdline_params.txt was automatically built by fastSemSim by running this line adding the parameter  --save_params example_cmdline_params.txt:
fastsemsim -vvv --task SS -o GeneOntology --ac_species fly  --query_input file --query_mode pairs --query_ss_type obj  --ontology_ignore positively_regulates --ontology_ignore negatively_regulates --ontology_ignore regulates --cut 0.9 --query_file data/GO_fly_pairs_query.txt  --tss Resnik --tmix BMA --root biological_process --ignore_EC TAS --query_file_sep "\t" --save_params example_cmdline_params.txt

# The file example_cmdline_params.txt was automatically built by fastSemSim by running this line adding the parameter  --save_params example_cmdline_params.txt:
fastsemsim -vvv --task SS -o GeneOntology --ac_species fly  --query_input file --query_mode pairs --query_ss_type obj  --ontology_ignore positively_regulates --ontology_ignore negatively_regulates --ontology_ignore regulates --query_file data/GO_fly_pairs_query.txt  --tss Resnik --tmix BMA --root biological_process --ignore_EC TAS --query_file_sep "\t" --save_params example_cmdline_params.txt

# This command line runs fastsemsim comman-line with the parameters in file example_cmdline_params.
fastsemsim --load_params example_cmdline_params.txt
# equivalent
fastsemsim -c example_cmdline_params.txt

# Calculate all pairwsie sem sim between all the proteins in the GO human GOA
fastsemsim --ontology_type GeneOntology --query_ss_type obj --tss Resnik --mix BMA --query_input ac --ac_species human  -vv --root molecular_function
fastsemsim --ontology_type GeneOntology --query_ss_type obj --tss Resnik --mix BMA --query_input ac --ac_species human  -vv --root molecular_function --remove_nan

# Calculate all pairwsie sem sim between all the proteins in the DO human GOA
fastsemsim --ontology_type DiseaseOntology --query_ss_type obj --tss Resnik --mix BMA --query_input ac --ac_species human  -vv --output_file temp.txt --remove_nan

# Calculate all pairwsie sem sim between all the ontological terms  in the DO (using the human DOA to calculate the IC)
fastsemsim --ontology_type DiseaseOntology --query_ss_type term --tss Resnik --mix BMA --query_input ontology --ac_species human  -vv --output_file temp.txt --remove_nan


# Load DO and human doa and extracts stats - save config file
fastsemsim --ontology_type DiseaseOntology --ac_species human  -vv --task stats --save_params example_cmdline_params.txt

fastsemsim  --load_params example_cmdline_params.txt