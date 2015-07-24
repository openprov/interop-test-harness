# Local configuration

PROV_TEST_CASES=$HOME/testcases
# Configure to use ProvPy source release
PROVPY_COMPARE="python $HOME/ProvPy/scripts/prov-compare"
PROVPY_CONVERT="python $HOME/ProvPy/scripts/prov-convert"
# Configure to use ProvToolbox source release
PROVTOOLBOX_CONVERT=$HOME/ProvToolbox/toolbox/target/appassembler/bin/provconvert
# Configure ProvStore
API_KEY="ApiKey you:12345qwert"

# Create local configuration directory with default name expected
# by tests.
CONFIG_DIR=localconfig
rm -rf $CONFIG_DIR
cp -r config/ $CONFIG_DIR

python prov_interop/set-yaml-value.py $CONFIG_DIR/harness.yaml test-cases="$PROV_TEST_CASES"
python prov_interop/set-yaml-value.py $CONFIG_DIR/harness.yaml comparators.ProvPyComparator.executable="$PROVPY_COMPARE"
python prov_interop/set-yaml-value.py $CONFIG_DIR/provpy.yaml ProvPy.executable="$PROVPY_CONVERT"
python prov_interop/set-yaml-value.py $CONFIG_DIR/provtoolbox.yaml ProvToolbox.executable="$PROVTOOLBOX_CONVERT"
python prov_interop/set-yaml-value.py $CONFIG_DIR/provstore.yaml ProvStore.authorization="$API_KEY"
