
import sys
import os
import random
import urllib

AN_ARBITRARY_LARGE_NUMBER = 4242424242421337424242
FILE_TYPE = '.txt'
TARGET_URL = 'localhost'

URL_SUCCESS_CODE = 200

SUCCESS_STATE = "YES"
FAILURE_STATE = "NO"

TEST_DELIMITER = '\t'
TEST_DATA = 'Bob\tJack\tbob@gmail.com\t\ty\t2015-02-18\t1993-02-13\tmale\ttypeI autism\t2000-03-12\t\ty\tnice tool\tPalo Alto\tCA\tUSA\t34000\t1.1234\t11.9884\tR1,R2,R5,R5\tgout,AIDS,flu'

def process_info():
    raw_data, delimiter = get_params(sys.argv)
    out_file_name = str(random.randint(0, AN_ARBITRARY_LARGE_NUMBER)) + FILE_TYPE
    out_file = open(out_file_name, 'w')
    out_file.write(delimiter + '\n')
    out_file.write(raw_data)
    out_file.close()
    # TODO: Change this to used actual host & file name (Currently in testing mode)
    code = urllib.urlopen('http://localhost:5000/processFile?file=scp_test.txt').getcode()
    os.remove(out_file_name)
    if code == URL_SUCCESS_CODE:
        print SUCCESS_STATE
    print FAILURE_STATE

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