ssh fmfsu@grigory1.cs.fsu.edu 'rm -rf /home/fmfsu/soltestgen/testgen_output.zip'
ssh fmfsu@grigory1.cs.fsu.edu 'cd /home/fmfsu/soltestgen; zip -r testgen_output.zip testgen_output'
rm ~/Downloads/sandbox.zip
scp fmfsu@grigory1.cs.fsu.edu:~/soltestgen/testgen_output.zip ~/Downloads/.
cd ~/Downloads
unzip testgen_output.zip


#(=>
#(and
#  (and (interface_0_C_49_0 this_0 abi_0 crypto_0 state_0 x_2_0) true)
#  (and (summary_4_function_test__48_49_0 error_0 this_0 abi_0 crypto_0 tx_0 state_0 x_2_0 state_1 x_2_1) (= error_0 0))
#) (interface_0_C_49_0 this_0 abi_0 crypto_0 state_1 x_2_1))))