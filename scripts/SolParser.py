import argparse
import json
import os
import subprocess


def is_supported_type(identifier):
    not_supported = ['array', 'contract', 'enum', 'function_external', 'struct', 'userDefinedValue']
    return not True in [n in identifier for n in not_supported]


class SolParser:
    @classmethod
    def read(self, file):
        if os.path.splitext(file)[1] == ".json":
            f = open(file, "r")
            data = json.load(f)
            #print(data)
            return data
        if os.path.splitext(file)[1] == ".sol":
            command = ['solc', file, '--ast-compact-json']
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                try:
                    stdout, stderr = process.communicate(input, timeout=20)
                    stdout_results = stdout.decode("utf-8")
                    stdout_results = stdout_results.replace("\'", "\"")
                    #print(stdout_results)
                    next_line = False
                    index = 0
                    for i, line in enumerate(stdout_results.split('\n')):
                        if next_line:
                            break
                        if file in line:
                            next_line = True
                            index = i
                    cut_result = '\n'.join(stdout_results.split('\n')[index + 1:])
                    data = json.loads(cut_result)
                    # print(data)
                    return data
                except subprocess.TimeoutExpired:
                    process.kill()
                    mesage = 'command: {} has been killed after timeout {}'.format("solc", 20)
                    print(mesage)
                    return []

    @classmethod
    def parse_data(self, data):
        n_of_contracts = len(data['nodes'])
        print("number of contracts: {}".format(n_of_contracts))
        out = []
        for n in data['nodes']:
            if n['nodeType'] != "ContractDefinition":
                continue
            for_one_contract = []
            name = n['name']
            print("name: {}".format(name))
            contractKind = n['contractKind']
            print("contractKind: {}".format(contractKind))
            for_one_contract.append([name, contractKind])
            f_c = n['nodes']
            for fc in f_c:
                if 'kind' not in fc:
                    continue
                f_name = fc['name']
                f_kind = fc['kind']
                if f_kind == 'constructor':
                    parameters = fc['parameters']['parameters']
                    constructor_parameters = []
                    for p in parameters:
                        identifier = p["typeDescriptions"]["typeIdentifier"]
                        if is_supported_type(identifier):
                            constructor_parameters.append(p['typeName']['name'])
                            constructor_parameters.append(p['name'])
                    # find [name, contractKind] and add constructor_parameters
                    for el in for_one_contract:
                        if len(el) == 2:
                            if el[0] == name and el[1] == constructor_parameters:
                                el += constructor_parameters
                    continue
                if f_kind == 'function' and fc['visibility'] == 'public':
                    tmp_f = [f_name]
                    print("kind: {} name: {}".format(f_kind, f_name))
                    params = fc['parameters']['parameters']
                    print("# of parameters: {}".format(len(params)))
                    for p in params:
                        identifier = p["typeDescriptions"]["typeIdentifier"]
                        if is_supported_type(identifier):
                            p_type = p['typeName']['name']
                            p_name = p['name']
                            tmp_f.append(p_type)
                            tmp_f.append(p_name)
                        elif 'contract' in identifier:
                            tmp = p['typeDescriptions']['typeString']
                            if 'contract' in tmp:
                                p_type = tmp.split()[1]
                                p_name = p['name']
                            else:
                                continue  # unkown ow type
                        elif not is_supported_type(identifier):
                            tmp_f = []  # enum case or function_external or struct : skip
                        else:
                            if 'name' in p['typeName']['baseType']:
                                p_type = p['typeName']['baseType']['name']
                                p_name = p['name']
                                tmp_f.append(p_type + "[]")
                                tmp_f.append(p_name)
                            else:
                                tmp_f = []  # case of array[][] not supported currently
                                continue
                        # print("type: {}".format(p_type))
                        # print("name: {}".format(p_name))
                    if tmp_f:
                        for_one_contract.append(tmp_f)
            out.append(for_one_contract)
        return out

    @classmethod
    def get_signature(self, file):
        d = SolParser.read(file)
        if d:
            return SolParser.parse_data(d)
        else:
            return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='python script for sol file parse')
    insourse = ['-i', '--input_file']
    kwsourse = {'type': str, 'help': 'path: location of the file'}
    parser.add_argument(*insourse, **kwsourse)
    args = parser.parse_args()

    if args.input_file is not None and os.path.isfile(args.input_file):
        f = args.input_file
        print('input file {}'.format(f))
    else:
        exit(1)

    d = SolParser.read(f)
    if d:
        print(SolParser.parse_data(d))
