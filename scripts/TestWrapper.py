import os.path


class TestWrapper:

    def __init__(self, testgen_file, signature):
        self.testgen_file = testgen_file
        self.signature = signature

    def read(self, file):
        f = open(file, "r")
        inside_test = False
        raw_tests = []
        a_test = []
        for line in f.readlines():
            if "END TEST" in line:
                inside_test = False
                if a_test:
                    raw_tests.append(a_test)
                a_test = []
            if inside_test:
                if line:
                    a_test.append(line)
            if "NEW TEST" in line:
                inside_test = True
        return raw_tests

    def is_int(self, string):
        try:
            string_integer = int(string)
            return 1
        except ValueError:
            return 0

    def get_values(cls, raw_list):
        test = {}
        for item in raw_list:
            tokens = item.strip().split()
            if len(tokens) < 2:
                print("Error: check!")
                continue
            chc_name = tokens[0]
            var_value = tokens[2][1:-1]
            tmp = var_value.split('=')
            var = int(tmp[0][len("_tg_"):])
            value = -1
            if "array" in tmp[1] or "store" in tmp[1]:
                continue
            else:
                value = int(tmp[1])
            if "contract" in chc_name:
                if "contract" in test:
                    if var in test["contract"]:
                        test["contract"][var].append(value)
                    else:
                        test["contract"][var] = [value]
                else:
                    tmp_dict = {}
                    tmp_dict[var] = [value]
                    test["contract"] = tmp_dict
            if "block" in chc_name and "function" in chc_name and "summary" not in chc_name and "return" not in chc_name:
                start = chc_name.index("_function_")
                end = chc_name.index("__")
                if start < 0 or end < 0:
                    print("Error2: check!")
                    continue
                function_name = chc_name[start + len("_function_"): end]
                if function_name in test:
                    if var in test[function_name]:
                        test[function_name][var].append(value)
                    else:
                        test[function_name][var] = [value]
                else:
                    tmp_dict = {}
                    tmp_dict[var] = [value]
                    test[function_name] = tmp_dict

        return test

    def wrap(self, log_file, signature):
        raw_tests = self.read(log_file)
        clean_test = [self.get_values(test) for test in raw_tests]
        return clean_test


    def wrap(self):
        if os.path.isfile(self.testgen_file):
            raw_tests = self.read(self.testgen_file)
            clean_test = [self.get_values(test) for test in raw_tests]
            return clean_test
        else:
            return False


if __name__ == '__main__':
    tw = TestWrapper("../sandbox/testgen.txt",[])
    [print(e) for e in tw.wrap()]
    # python script to generate Solidity Tests from Raw log and signature of Sol file
