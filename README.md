# solidity_testgen

Test generation for Solidity 

### Dependincies / Setup
* Aeval TestGen (TDB: how to)
* SMT Encoder set up 
```
git clone https://github.com/leonardoalt/cav_2022_artifact
cd cav_2022_artifact
echo "RUN sed -i 's/let solverOutput;/console.log(query); let solverOutput;/g' /home/solc-js/smtsolver.ts" >> Dockerfile-solcmc
docker build -f Dockerfile-solcmc . --rm -t leoalt/cav
```
example of command
`./docker_solcmc examples smoke_safe.sol Smoke 30 z3`
* ADT 
```
git clone https://github.com/leonardoalt/adt_transform
cd adt_transform 
cargo build
```
location of executable file and example of command
`./target/debug/adt_transform adt_free.smt2`

#### build project
`forge build`

#### run all tests
`forge test`

#### run specificied tests
`forge test --match Loop*`

#### run Python 
`python3 ./scripts/SolidityTestGen.py -i ./src/Loop_1.sol`