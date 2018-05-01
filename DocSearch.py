from pathlib import Path
import textract, re, argparse
import configparser
import os, sys

#command line argument parser
parser = argparse.ArgumentParser(description='Search the CV database')
parser.add_argument('search_list', metavar='N', type=str, nargs='+', help='search terms seperated by a space')
parser.add_argument('-i', dest='case_option_sensitive', action='store_true', help='if option is specified, the search is case sensitive')
parser.add_argument('-w', dest='case_option_whole_words', action='store_true', help='if option is specified, whole-words only are searched')
args = parser.parse_args()

#Set antiword HOME path for windows build
os.environ["HOME"] = "./"

#import config file
config = configparser.ConfigParser()
config.read('init.ini')

#specify the path to the documents directory
doc_path = Path(config['OPTIONS']['Path'])
doc_list = list(doc_path.glob('**/*.*'))

search_results = {}

#initialize dictionary
for j in args.search_list:
    search_results[j] = []

#case sensitve option
if (args.case_option_sensitive):
    option_arg = 0
else:
    option_arg = re.I

#whole words option
if (args.case_option_whole_words):
    first_white_space = '\s'
    end_white_space = '(\s|\n)'
else:
    first_white_space = ''
    end_white_space =''

#textract is awesome - all in one solution for all file types, crazy - loop through list of files and match search terms with specified options
for i in doc_list:
    try:
        text = textract.process(str(i)).decode('utf-8')
        for j in args.search_list:
            if (re.search(first_white_space + j + end_white_space, text, option_arg)):
                search_results[j].append('found ' + j + ' in ' + str(i))
    except:
        print("unable to decode file - some weird charcter encoding in that file :" + str(i))

#write results to log file
with open('search_results.txt', 'w') as log:
    for j in args.search_list:
        log.write('Results for ' + j + ' :\n')
        for i in search_results[j]:
            log.write(i + '\n')
        log.write('\n')