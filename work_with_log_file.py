#!/usr/bin/env python3

#qwiklabs_work_with_log_file

import sys
import os
import re

# check if word in log

def error_search(log_file):
  error = input("what is the error? ") #example in put "disk full error"
  returned_errors = []
  with open(log_file, mode = 'r', encoding = 'UTF-8') as file:
    for log in file.readlines(): # read log line by line 
      error_patterns = ["error"]
      for i in range(len(error.split(' '))): # iterate 0, 1, 2 dis, full, error
        error_patterns.append(fr"{error.split(' ')[i].lower()}")
      if all(re.search(error_pattern, log.lower()) for error_pattern in error_patterns):
        returned_errors.append(log) # if that log have word "disk", "full", "error" then collect to returned_errors
  return returned_errors

def file_output(retruned_errors):
  with open(os.path.expanduser('~') + '/data/errors_found.log', mode = 'w') as file:
    for error in returned_errors:
      file.write(error)

if __name__ == "__main__":
  log_file = sys.argv[1]
  returned_errors = error_search(log_file)
  file_output(returned_errors)
  sys.exit(0)
