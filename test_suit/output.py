import os
import re


def outputFile(src, dst):
    dst_file = open(dst, "w")
    reg = r"\w+[\+-]\w+"
    with open(src, "r") as src_file:
        lines = src_file.readlines()
        i = 0
        for line in lines:
            comment = str(line)

            if i >= 1:  # skip the first line
                _list = re.findall(reg, comment)
                comment = ""
                for item in _list:

                    comment += item + ","
                comment = comment[0: len(comment)-1]  # skip the fin ","
                comment += "\n"
                dst_file.write(comment)
            else:
                _list = re.findall(r"\w", comment)
                if len(_list) != 2:
                    dst_file.write(comment)
                else:
                    comment = _list[0] + "           ,          " + _list[1]

                    # comment = comment[0: len(comment)-1]  # skip the fin ","
                    comment += "\n"
                    dst_file.write(comment)
            i += 1
            # if(comment.)
            # print line


if __name__ == "__main__":
    outputFile(src="10-1500-kt.txt", dst="out_file-kt.txt")