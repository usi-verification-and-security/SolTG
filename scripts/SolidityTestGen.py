import argparse
import os
import shutil
import glob
import subprocess
import time
from datetime import datetime
import random

""" Init SetUp 
"""

def init():
    global SOLCMC, DOCKER_SOLCMC, ADT_DIR, TIMEOUT, SANDBOX_DIR
    #Dockerfile-solcmc
    SANDBOX_DIR = "../sandbox"
    SOLCMC = "/Users/ilyazlatkin/CLionProjects/cav_2022_artifact"
    DOCKER_SOLCMC = SOLCMC + "/docker_solcmc"
    ADT_DIR = "/Users/ilyazlatkin/CLionProjects/adt_transform/target/debug/adt_transform"
    TIMEOUT = 30


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


def command_executer(command, timeout, file):
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
            logger(file, str(stdout))
            logger(file, str(stderr))
            # raise subprocess.TimeoutExpired(
            #     process.args, timeout, output=stdout, stderr=stderr,
            # )
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
            return True

def run_solcmc(updated_file_name, contract_name):
    # ./docker_solcmc examples smoke_safe.sol Smoke 30 z3
    save = os.getcwd()
    os.chdir(SOLCMC)
    basename = os.path.basename(updated_file_name)
    smt_name = os.path.splitext(basename)[0] + '.smt2'
    command = [DOCKER_SOLCMC, "tmp", basename,
               contract_name, str(30), 'z3', '>', smt_name]
    command_executer(command, 60, "tmp/log.txt")
    os.chdir(save)


def update_file(file):
    print("update file: {}".format(file))
    contract_name = ""
    f = open(file, "r", encoding='ISO-8859-1')
    lines_to_check = f.readlines()
    out = []
    for l in lines_to_check:
        if "contract" in l:
            print("contract found")
            tockens = l.split()
            next = False
            out.append(l)
            for t in tockens:
                if next:
                    contract_name = t
                    break
                if t == "contract":
                    next = True
        elif "pragma solidity" in l:
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
    run_solcmc(updated_file_name, contract_name)


def move_for_encoding(file):
    print("move_for_encoding")
    # check tmp folder in SOLCMC/tmp
    tmp_dir = SOLCMC + "/tmp"
    prepare_dir(tmp_dir)
    new_file = tmp_dir + "/" + os.path.basename(file)
    shutil.copyfile(file, new_file)
    update_file(new_file)


def main():
    start_time = time.time()
    init()
    global SOLCMC, DOCKER_SOLCMC, ADT_DIR, TIMEOUT
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

    move_for_encoding(file)

    tt = time.time() - start_time
    print('TG total time: {} seconds or {} hours'.format(tt, tt / 3600))


if __name__ == "__main__":
    main()