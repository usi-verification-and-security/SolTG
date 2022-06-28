import argparse
import os
import random
import shutil
import subprocess
import time
from datetime import datetime
from sys import platform

from SolParser import SolParser

""" Init SetUp 
"""


def init():
    global ADT_DIR, SOLCMC, DOCKER_SOLCMC, ADT_DIR, TIMEOUT, SANDBOX_DIR, SOLVER_TYPE, TG_PATH, TG_TIMEOUT, FORGE_PATH
    # Dockerfile-solcmc
    SANDBOX_DIR = "../sandbox"
    if platform == "darwin":
        SOLCMC = "/Users/ilyazlatkin/CLionProjects/cav_2022_artifact"
        ADT_DIR = "/Users/ilyazlatkin/CLionProjects/adt_transform/target/debug/adt_transform"
        TG_PATH = "/Users/ilyazlatkin/CLionProjects/aeval/cmake-build-debug/tools/nonlin/tgnonlin"
        FORGE_PATH = "/Users/ilyazlatkin/.cargo/bin/forge"
    if platform == "linux" or platform == "linux2":
        SOLCMC = "/home/fmfsu/Dev/blockchain/cav_2022_artifact"
        ADT_DIR = "/home/fmfsu/Dev/blockchain/adt_transform/target/debug/adt_transform"
        TG_PATH = "/home/fmfsu/Dev/blockchain/aeval/build/tools/nonlin/tgnonlin"
        FORGE_PATH = "/home/fmfsu/.cargo/bin/forge" # "/home/fmfsu/.foundry/bin/forge"
    DOCKER_SOLCMC = SOLCMC + "/docker_solcmc"
    TIMEOUT = 900
    TG_TIMEOUT = 60
    SOLVER_TYPE = "z3"  # "eld" # "z3"


def clean_dir(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def prepare_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    else:
        print('clear output directory {}'.format(dir))
        # remove dir
        os_info = os.uname()
        if (os_info.sysname != 'Darwin'):
            clean_dir(dir)
        else:
            shutil.rmtree(dir)
            os.mkdir(dir)


def move_to_sandbox(files, add_h, was_cleaned):
    print("========move_to_sandbox===========")


""" write content to the file"""


def logger(file, content):
    f = open(file, 'a')
    now = datetime.now()
    time = now.strftime("%H:%M:%S:%f")
    t = str('[{}]'.format(time))
    if type(content) is list:
        f.writelines([t] + ['\n'])
        for c in content:
            if type(c) is list:
                f.writelines([' '.join(c)] + ['\n'])
            elif type(c) is bytes:
                cs = str(c)
                list_to_print = [f + '\n' for f in cs.split('\\n')]
                f.writelines(list_to_print + ['\n'])
            else:
                f.writelines([str(c)] + ['\n'])
    elif type(content) is str:
        f.write(t + '\n' + content + '\n')
    f.close()


""" converts list ot string with spaces"""


def list_to_string(lst):
    return ' '.join([str(e) for e in lst])


def command_executer(command, timeout, log_file, output_file):
    print("command: {}".format(str(command)))
    f = open(output_file, "a")
    logger(log_file, list_to_string(command))
    with subprocess.Popen(command, stdout=f, stderr=subprocess.PIPE) as process:
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            mesage = 'command: {} has been killed after timeout {}'.format(list_to_string(command), timeout)
            print(mesage)
            stdout, stderr = process.communicate()
            #logger(log_file, str(stdout))
            #logger(log_file, str(stderr))
        except Exception:
            process.kill()
            process.wait()
            mesage = 'command: {} has been killed after timeout {}'.format(list_to_string(command), timeout)
            print(mesage)
            logger(log_file, mesage)
            raise
        retcode = process.poll()
        logger(log_file, [process.args, retcode, stdout, stderr])
        if retcode and retcode != 254:
            return False
        else:
            return True


def command_executer_docker_solcmc(command, timeout, file):
    print("command: {}".format(str(command)))
    logger(file, list_to_string(command))
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            mesage = 'command: {} has been killed after timeout {}'.format(list_to_string(command), timeout)
            print(mesage)
            stdout, stderr = process.communicate()
            # logger(file, str(stdout))
            # logger(file, str(stderr))
        except Exception:
            process.kill()
            process.wait()
            mesage = 'command: {} has been killed after timeout {}'.format(list_to_string(command), timeout)
            print(mesage)
            logger(file, mesage)
            raise
        retcode = process.poll()
        # logger(file, str(subprocess.CompletedProcess(process.args, retcode, stdout, stderr)))
        logger(file, [process.args, retcode, stdout, stderr])
        if retcode and retcode != 254:
            return False
        else:
            # start with "Running with solver" and terminate with "Entire output"
            start = False
            out = []
            to_ckeck = str(stdout).split("\\n")
            number_of_set_logic_HORN = 0
            for s in to_ckeck:
                if "(set-logic HORN)" in str(s):
                    number_of_set_logic_HORN += 1
                if "Entire output" in str(s) or number_of_set_logic_HORN > 1:
                    break
                if start:
                    out.append(s + "\n")
                if "Running with solver" in str(s):
                    start = True
            # add "(set-option :produce-proofs true)"
            # add "(get-proof)"
            # out.insert(1, "(set-option :produce-proofs true)\n")
            # out.append("(get-proof)\n")
            return out


def run_solcmc(updated_file_name, contract_name):
    # ./docker_solcmc examples smoke_safe.sol Smoke 30 z3
    save = os.getcwd()
    os.chdir(SOLCMC)
    basename = os.path.basename(updated_file_name)
    smt_name = os.path.splitext(basename)[0] + '.smt2'
    command = ["./docker_solcmc_updated", "tmp", basename,
               contract_name, str(10), SOLVER_TYPE]  # , '>', smt_name]
    smt2_list = command_executer_docker_solcmc(command, TIMEOUT, "tmp/log.txt")
    os.chdir(save)
    return smt2_list


def run_adt_transform(smt2_file, smt2_wo_adt):
    print("run adt_transform script")
    save = os.getcwd()
    os.chdir(SANDBOX_DIR)
    command = [ADT_DIR, smt2_file]  # , ">", smt2_wo_adt]
    command_executer(command, 60, SANDBOX_DIR + "/log.txt", smt2_wo_adt)
    os.chdir(save)


def get_fun_signature(line):
    start = line.index("function") + len("function")
    if line.find(")") < 0:
        # not supported case regression/types/array_aliasing_memory_1.sol,
        # when function declared in multiple lines
        return []
    end = line.index(")", start + 1)
    function_all = line[start:end + 1].strip()
    function_name = function_all[:function_all.index("(")]
    out = [function_name]
    inside = function_all[function_all.index("(") + 1: function_all.index(")")]
    if inside:
        raw_paramentes = inside.split(',')
        for p in raw_paramentes:
            out.append(p.split()[0])
    # ToDo: add types of parameters
    return out


def is_in_contract_type(line):
    tockens = line.split()
    for e in ['interface', 'contract', 'library']:
        if e in tockens:
            return True
    return False


def get_contrac_type(line):
    if 'interface' in line:
        return 'interface'
    if 'contract' in line:
        return 'contract'
    if 'library' in line:
        return 'library'
    return "NaN"


def update_file(file, name):
    print("update file: {}".format(file))
    contract_name = name
    f = open(file, "r", encoding='ISO-8859-1')
    lines_to_check = f.readlines()
    out = []
    for tmp_l in lines_to_check: # ToDo: check if needed later when Excel feature will be ready
        if tmp_l.strip().startswith("//"):
            continue
        index_of_comments = tmp_l.find("//")
        if index_of_comments > 1:
            l = tmp_l[:index_of_comments]
        else:
            l = tmp_l
        if "pragma solidity" in l:
            print("pragma solidity is found")
        else:
            out.append(l)

    basename = os.path.basename(file)
    updated_file_name = os.path.dirname(file) + "/" + os.path.splitext(basename)[0] + \
                        "_updated" + os.path.splitext(basename)[1]
    f_updated = open(updated_file_name, 'a')
    f_updated.writelines(out)
    f_updated.close()
    f.close()
    print(updated_file_name)
    print(contract_name)
    smt2_list = run_solcmc(updated_file_name, contract_name)
    # move to sanbox
    source = SOLCMC + "/tmp"
    destination = os.path.abspath(SANDBOX_DIR)
    allfiles = os.listdir(source)
    for e in allfiles:
        if e == "log.txt":
            shutil.move(source + "/" + e, destination + "/log_encoding.txt")
        else:
            shutil.move(source + "/" + e, destination + "/" + e)

    if smt2_list:
        smt2_file = SANDBOX_DIR + "/" + os.path.splitext(basename)[0] + ".smt2"
        f_smt = open(smt2_file, 'a')
        f_smt.writelines(smt2_list)
        f_smt.close()
        smt2_wo_adt = SANDBOX_DIR + "/" + os.path.splitext(basename)[0] + "_wo_adt.smt2"
        run_adt_transform(smt2_file, smt2_wo_adt)


def move_for_encoding(file, contract_name):
    print("move_for_encoding")
    # check tmp folder in SOLCMC/tmp
    tmp_dir = SOLCMC + "/tmp"
    prepare_dir(tmp_dir)
    new_file = tmp_dir + "/" + os.path.basename(file)
    shutil.copyfile(file, new_file)
    update_file(new_file, contract_name)


def run_tg(file):
    basename = os.path.basename(file)
    smt_name = os.path.splitext(basename)[0] + "_wo_adt.smt2"
    new_smt_file_name = SANDBOX_DIR + "/" + smt_name
    print("run TG with".format(new_smt_file_name))
    logger(SANDBOX_DIR + '/log.txt', "run TG with".format(new_smt_file_name))
    to_print = "{} {} {}".format(TG_PATH, "--keys <keys_valus_to_be_define> ", new_smt_file_name)
    print(to_print)
    log_file = SANDBOX_DIR + "/log.txt"
    logger(log_file, to_print)
    command_tg = [TG_PATH, '--inv-mode', '0', '--no-term' '--keys', '4271,13242',
                  new_smt_file_name]
    command_executer(command_tg, TG_TIMEOUT, log_file, log_file)


def is_fun_supported(fun_signature):
    # currently only int formate is supported
    for f in fun_signature:
        #if f != "uint":
        if "uint" not in f:
            return False
    return True


def generate_stub(file_name, signature):
    name_wo_extension = os.path.splitext(file_name)[0]
    test_name = name_wo_extension + ".t.sol"
    test_file_full_path = "../test/" + test_name
    test_file = open(test_file_full_path, 'w')
    out = ["//Generated Test by TG\n", "//{}\n".format(str(signature)),
           "pragma solidity ^0.8.13;\n\n",
           "import \"forge-std/Test.sol\";\n",
           "import \"../src/{}.sol\";\n\n".format(name_wo_extension),
           f'contract {name_wo_extension}_Test is Test' + ' {\n']

    # contracts declaration
    for i, c in enumerate(signature):
        if c[0][1] in ['contract', 'library']:  # skip interphases
            out.append("\t{} {};\n".format(c[0][0], "c" + str(i)))

    # generate setUp function
    out.append("\n")
    out.append("\tfunction setUp() public {\n")
    for i, c in enumerate(signature):
        if c[0][1] in ['contract', 'library']: # skip interphases
            out.append("\t\t{} = new {}();\n".format("c" + str(i), c[0][0]))
    out.append("\t}\n")

    # generate Tests : one test for each function for each contract
    index = 0
    out.append("\n")
    for i, c in enumerate(signature):
        if len(c) > 1 and c[0][1] in ['contract', 'library']: # skip interphases
            for j, funcs in enumerate(c[1:]):
                check = is_fun_supported(funcs[1:])
                if check:
                    #generate random content
                    content = ','.join([str(random.randint(1, 30)) for e in funcs[1:]])
                    out.append(f'\tfunction test_{name_wo_extension}_{index}() public ' + '{\n')
                    out.append("\t\t{}.{}({});\n".format("c" + str(i), funcs[0], content))
                    out.append("\t\tassertTrue(true);\n\t}\n")
                    index += 1

    out.append("}\n")
    test_file.writelines(out)
    test_file.close()


def run_test(file, signature):
    global  SANDBOX_DIR
    basename = os.path.basename(file)
    new_name = SANDBOX_DIR + "/" + basename
    print("Run tests for: {} ".format(new_name))
    save = os.getcwd()
    print(save)
    generate_stub(basename, signature)
    # copy source file to "scr"
    shutil.copyfile(file, "../src/" + basename)
    #run command:  forge test --match name
    SANDBOX_DIR = os.path.abspath(SANDBOX_DIR)
    logger(SANDBOX_DIR + "/log.txt", "new signature" + str(signature))
    os.chdir("../")
    command_executer([FORGE_PATH, 'clean'], 60, SANDBOX_DIR + "/log.txt", SANDBOX_DIR + "/log.txt")
    command = [FORGE_PATH, 'test', '--match', str(os.path.splitext(basename)[0])]
    command_executer(command, 60, SANDBOX_DIR + "/log.txt", SANDBOX_DIR + "/test_results.txt")
    command = [FORGE_PATH, 'coverage', '--match', str(os.path.splitext(basename)[0]), '--report', 'lcov']
    command_executer(command, 60, SANDBOX_DIR + "/log.txt", SANDBOX_DIR + "/test_results.txt")
    command = [FORGE_PATH, 'coverage', '--match', str(os.path.splitext(basename)[0]), '--report', 'summary']
    command_executer(command, 60, SANDBOX_DIR + "/log.txt", SANDBOX_DIR + "/test_results.txt")
    #copy lcov file
    if os.path.isfile("lcov.info"):
        shutil.move("lcov.info", SANDBOX_DIR + "/lcov.info")
        genhtml_report_command = ['genhtml', '--branch-coverage', '--output', SANDBOX_DIR + '/generated-coverage', SANDBOX_DIR + "/lcov.info"]
        command_executer(genhtml_report_command, 60, SANDBOX_DIR + "/log.txt", SANDBOX_DIR + "/log.txt")
    os.chdir(save)
    #os.remove("../src/" + basename)
    clean_dir("../src")
    shutil.move("../test/" + os.path.splitext(basename)[0] + ".t.sol",
                SANDBOX_DIR + "/" + os.path.splitext(basename)[0] + ".t.sol")
    clean_dir("../test")


def find_contract_name(signature):
    for s in signature:
        if s[0][1] == 'contract':
            return s[0][0]
    return 0



def main(filename):
    start_time = time.time()
    init()
    global ADT_DIR, SOLCMC, DOCKER_SOLCMC, ADT_DIR, TIMEOUT, SOLVER_TYPE, SANDBOX_DIR, TG_PATH, TG_TIMEOUT, FORGE_PATH
    if not filename:
        parser = argparse.ArgumentParser(description='python script for Solidity Test Generation')
        insourse = ['-i', '--input_source']
        kwsourse = {'type': str, 'help': 'Input .c-file. or directory'}
        parser.add_argument(*insourse, **kwsourse)

        args = parser.parse_args()
        print(args)
        file = ""
        if args.input_source is not None:
            if os.path.isfile(args.input_source):
                file = args.input_source
                print('solidity input file was set to {}'.format(file))
            elif os.path.isdir(args.input_source):
                print('TBD'.format(args.input_source))
                exit(1)
        else:
            print('invalid input_source: {}'.format(args.input_source))
            exit(1)
    else:
        file = filename

    clean_dir(SANDBOX_DIR)

    signature = SolParser.get_signature(file)
    contract_name = find_contract_name(signature)
    if contract_name:
        move_for_encoding(file, contract_name)

        run_tg(file)
        run_test(file, signature)

    tt = time.time() - start_time
    to_print_var = 'total time: {} seconds'.format(tt)
    print(to_print_var)
    logger(SANDBOX_DIR + '/log.txt', to_print_var)


if __name__ == "__main__":
    main("")
