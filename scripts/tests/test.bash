#!bin/bash
set -e

# Set up
cd "$(dirname "$0")"
cp test.xyz ../../input/
mkdir ../../input/test/
cp test_dummy.xyz ../../input/test/

# Test proton_opt.py
cd ../..
python scripts/proton_opt.py test 1
if cmp -s input/test/test_dummy_protonopt.inp scripts/tests/answer_dummy_protonopt.inp
then
    echo "Proton_opt.py test passed."
else
    echo "Proton_opt.py test failed."
    fail=1
fi

# Test input_gen.py
cp scripts/tests/test_dummy_protonopt.out input/test/
python scripts/input_gen.py test 1
if cmp -s input/test/test_dummy.inp scripts/tests/answer_dummy.inp
then
    echo "Input_gen.py test passed."
else
    echo "Input_gen.py test failed."
    fail=1
fi

# Test StrainViz.py
mkdir -p output/test
cp scripts/tests/test_dummy.out input/test/
python scripts/StrainViz.py test
if cmp -s output/test/total_force.tcl scripts/tests/answer_total_force.tcl
then
    echo "StrainViz.py test passed."
else
    echo "StrainViz.py test failed."
    fail=1
fi

# Teardown
rm input/test.xyz
rm -r input/test/
rm -r output/test/

exit $fail