ssh fmfsu@grigory1.cs.fsu.edu 'rm -rf /home/fmfsu/soltestgen/testgen_output.zip'
ssh fmfsu@grigory1.cs.fsu.edu 'cd /home/fmfsu/soltestgen; zip -r testgen_output.zip testgen_output'
rm ~/Downloads/sandbox.zip
scp fmfsu@grigory1.cs.fsu.edu:~/soltestgen/testgen_output.zip ~/Downloads/.
cd ~/Downloads
unzip testgen_output.zip
