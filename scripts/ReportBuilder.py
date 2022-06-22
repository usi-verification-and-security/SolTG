import argparse
import os
import re


class html_report:

    def create_header(table):
        header_line = "No., Sourse dir, Sourse code, Links (smt2 logs reports) , Tests, Coverage, Time"
        header = header_line.split(",")
        table += "  <tr>\n"
        for column in header:
            table += "    <th>{0}</th>\n".format(column.strip())
        table += "  </tr>\n"
        return table


    def create_hyperlinnk_to_file(text):
        if not text:
            return "NaN"
        name = os.path.basename(text)
        if os.path.exists(text):
            return "<a href=\"{0}\">{1} </a>\n".format(text, name)
        else:
            return "NaN"

    def create_hyperlinnk_to_test_file(text):
        if not text:
            return "NaN"
        if os.path.exists(text):
            return "<a href=\"{0}\">{1} </a>\n".format(text, "test")
        else:
            return "NaN"

    def smt2_status(ll):
        if "smt2" not in ll:
            return "-"
        else:
            return ll[13]

    def smt2_number_of_lines(smt2file):
        if os.path.exists(smt2file):
            return len(open(smt2file).readlines())
        else:
            return "-"

    def link_to_log(p):
        name = os.path.dirname(p) + "/log.txt"
        return "<a href=\"{0}\">{1}</a>\n".format(name, "log")

    def get_z3_results(p):
        if "z3_error" in p:
            return "timeout"
        if len(p) > 15:
            if ('sat' in p[16] and 'unsat' not in p[16]):
                return 'sat'
            if ('unsat' in p[16]):
                return 'unsat'
        else:
            return "-"

    def parse_result_line(line):
        tmp = line.split(';')
        tmp_1 = tmp[0].split()
        out = ''
        if tmp_1[-2].isnumeric():
            if int(tmp_1[-2]) > 0:
               out += "<br/><font color=green>{}</font> ".format(tmp_1[-2] + " " + tmp_1[-1])
        tmp_2 = tmp[1].split()
        if tmp_2[-2].isnumeric():
            if int(tmp_2[-2]) > 0:
                out += "<br/><font color=red>{}</font> ".format(tmp[1])
        return out

    @classmethod
    def get_extra_info_from_log(cls, dir):
        log = [f.path for f in os.scandir(dir) if f.is_file() and os.path.basename(f) == 'log.txt']
        out = ''
        if len(log) >= 1:
            what_to_check = ["Multiple queries are not supported",
                             "Assertion failed",
                             "Done with TG",
                             "array operation requires one sort parameter",
                             "ALL Branches are covered: DONE",
                             "FOUND", 'unrolling sat', 'unrolling unsat', 'WOW!']
            filein = open(log[0], "r", encoding='ISO-8859-1')
            lines = filein.readlines()
            for w in what_to_check:
                for line in lines:
                    if re.search(w, line):
                        out += "<br/>" + "<font color=8B008B>{}</font>\n".format(w)
                        break
        return out



    @classmethod
    def clear_benchmarkdir(self, dir, nonlinear):
        for n in nonlinear:
            tmp = dir + "/" + n + ".c"
            if os.path.isfile(tmp):
                # remove dir
                os.remove(tmp)


    @classmethod
    def get_tests_info(cls, dir):
        test_results = [f.path for f in os.scandir(dir) if f.is_file() and os.path.basename(f) == 'test_results.txt']
        out = ''
        if len(test_results) >= 1:
            what_to_check = ["No tests match",
                             "Unnamed return variable",
                             "Done with TG",
                             "array operation requires one sort parameter"]
            filein = open(test_results[0], "r", encoding='ISO-8859-1')
            lines = filein.readlines()
            for line in lines:
                if "Test result:" in line:
                    out += "<br/>" + cls.parse_result_line(line)
            for w in what_to_check:
                for line in lines:
                    if re.search(w, line):
                        out += "<br/>" + "<font color=8B008B>{}</font>\n".format(w)
                        break
            return out
        else:
            return "No info"

    @classmethod
    def get_coverage_data(cls, line):
        return "No info"


    @classmethod
    def buildReport(self, dir):
        fileout = open("{}/1_html_report.html".format(dir), "w+")

        table = "<table border=\"1\" cellspacing=\"0\" cellpadding=\"4\">\n"
        table = html_report.create_header(table)

        i = 1
        subdirs = [f.path for f in os.scandir(dir) if f.is_dir() and os.path.basename(f)]
        out = []
        for s in subdirs:
            out += [(s, f.path) for f in os.scandir(s) if f.is_dir() and os.path.basename(f)]
        for o in sorted(out):
            (subd, line) = o
            print(line)
            table += "  <tr>\n"
            table += "    <td>{0}</td>\n".format(i)
            table += "    <td>{0}<br/>\n".format(
                html_report.create_hyperlinnk_to_file(subd))
            table += "    <td>{0}<br/>\n".format(
                html_report.create_hyperlinnk_to_file(line + '/' + os.path.basename(line) + '.sol'))
            table += "    <td>{0}<br/>{1}<br/>{2}<br/>{3}<br/></td>\n".format(html_report.get_smt2_file(line),
                                                            html_report.get_log_file(line, "log.txt"),
                                                            html_report.get_log_file(line, "log_encoding.txt"),
                                                            html_report.get_extra_info_from_log(line))
            table += "    <td>{0}<br/>{1}</br>{2}</td>\n".format(html_report.create_hyperlinnk_to_test_file(line + '/' + os.path.basename(line) + '.t.sol'),
                                                         html_report.get_log_file(line, "test_results.txt"),
                                                        html_report.get_tests_info(line))
            table += "    <td>{0}</td>\n".format(html_report.get_coverage_data(line))
            table += "    <td>{0}</td>\n".format(str(html_report.get_time_consumed(line)) + ' seconds')
            table += "  </tr>\n"
            i += 1
        table += "</table>"
        # table = table.replace("../{}".format(dir), ".")
        table = table.replace(dir, ".")
        fileout.writelines(table)
        fileout.close()



    @classmethod
    def get_smt2_file(cls, dir):
        smt2files = [f.path for f in os.scandir(dir) if f.is_file() and os.path.splitext(f)[1] == '.smt2']
        if len(smt2files) >= 1:
            out = ""
            for f in sorted(smt2files):
                if "wo_adt" not in f:
                    out += "<font color=\"black\">[original smt]<br/> {}</font><br/>\n".format(html_report.create_hyperlinnk_to_file(f))
                else:
                    out += "<font color=\"black\">[adt free smt]<br/> {}</font><br/>\n".format(
                        html_report.create_hyperlinnk_to_file(f))
            return out
        else:
            return "<font color=\"red\">{}</font>\n".format('no smt')

    @classmethod
    def get_log_file(cls, dir, log_file_name):
        log = [f.path for f in os.scandir(dir) if f.is_file() and os.path.basename(f) == log_file_name]
        if len(log) >= 1:
            return html_report.create_hyperlinnk_to_file(log[0])
        else:
            return "<font color=\"red\">{}</font>\n".format('no log')


    @classmethod
    def get_time_consumed(cls, dir):
        log = [f.path for f in os.scandir(dir) if f.is_file() and os.path.basename(f) == 'log.txt']
        if len(log) >= 1:
            with open(log[0], 'rb') as f:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
                last_line = f.readline().decode()
                time_con = last_line.split()
                if len(time_con) > 3 and ("total time" in last_line):
                    return "%8.2f" % (float(time_con[2]))
                else:
                    "<font color=\"red\">{}</font>\n".format('no available')
        else:
            return "<font color=\"red\">{}</font>\n".format('no available')



    def is_nonlinear(name):
        filein = open(name, "r", encoding='ISO-8859-1')
        lines = filein.readlines()
        for l in lines:
            if "Nonlinear CHC is currently unsupported" in l:
                return False
        return True



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='python script for Report Builder')
    insourse = ['-i', '--input_dir']
    kwsourse = {'type': str, 'help': 'dir: where TG run is located'}
    parser.add_argument(*insourse, **kwsourse)
    args = parser.parse_args()

    if args.input_dir is not None:
        if os.path.isdir(args.input_dir):
            dir = args.input_dir
            print('report dir set to {}'.format(dir))
    else:
        dir = "/Users/ilyazlatkin/CLionProjects/blockchain_exp/hello_foundry/testgen_output"

    html_report.buildReport(dir)

