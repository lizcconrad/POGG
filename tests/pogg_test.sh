# script to call the test commands because hatch is broken...
# run from pogg/tests

TEST_DATA_DIR="test_data"
#TEST_FILES="pogg_config/*"
#TEST_FILES="pogg_routine/*"
#TEST_FILES="my_delphin/*"
#TEST_FILES="data_handling/*"
#TEST_FILES="lexicon/*"
#TEST_FILES="graph_to_SEMENT/*"
#TEST_FILES="semantic_composition/*"
#TEST_FILES="semantic_composition/test_sement_util.py"
#TEST_FILES="evaluation/*"
TEST_FILES="pogg_config/* pogg_routine/* my_delphin/* data_handling/* lexicon/* graph_to_SEMENT/* evaluation/* semantic_composition/*"
#TEST_FILES="pogg_config/* pogg_routine/* my_delphin/* data_handling/* lexicon/* graph_to_SEMENT/* evaluation/* semantic_composition/*"




# add files in tests to PYTHONPATH to enable discovering modules that contain test case classes
#export PYTHONPATH="${PYTHONPATH}:."


GRAMMAR_PATH="/Users/lizcconrad/Documents/PhD/POGG/ERG/ERG_2023/erg-2023.dat"
SEMI_PATH="/Users/lizcconrad/Documents/PhD/POGG/ERG/ERG_2023/trunk/etc/erg.smi"

COVERAGE_CONFIG_FILE="/Users/lizcconrad/Documents/PhD/POGG/pogg/pyproject.toml"

coverage run -m --branch --rcfile=$COVERAGE_CONFIG_FILE --data-file=".coverage" pytest -vv $TEST_FILES --test_data_dir=$TEST_DATA_DIR --grammar_path=$GRAMMAR_PATH --semi_path=$SEMI_PATH

#Get the last version
coverage_file="$(ls  .coverage* | sort -V | tail -n1)"
mv $coverage_file .coverage

coverage report -m --rcfile=$COVERAGE_CONFIG_FILE --data-file=".coverage"

# remove coverage file
rm .coverage
