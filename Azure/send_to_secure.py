
import sys
import random

DELIMITER_INDEX = 0
DATA_INDEX = 1
AN_ARBITRARY_LARGE_NUMBER = 4242424242421337424242
FILE_TYPE = '.txt'

TEST_DELIMITER = '\t'
TEST_DATA = 'Joe\t\tjoe@gmail.com\tyes\t\t2015-02-18'

def process_info():
    raw_data, delimiter = get_params(sys.argv)
    out_file_name = str(random.randint(0, AN_ARBITRARY_LARGE_NUMBER)) + FILE_TYPE
    out_file = open(out_file_name, 'w')
    out_file.write(delimiter + '\n')
    out_file.write(raw_data)
    out_file.close()

def get_params(args):
    num_args = len(args)
    if num_args > 2:
        raw_data, delimiter = args[1:]
    elif num_args == 2:
        raw_data = args[1]
        delimiter = TEST_DELIMITER
    else:
        raw_data = TEST_DATA
        delimiter = TEST_DELIMITER
    return (raw_data, delimiter)

process_info()