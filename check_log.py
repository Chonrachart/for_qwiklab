import re
import sys

""" log example

May 27 11:45:40 ubuntu.local ticky: INFO: Created ticket [#1234] (username)

Jun 1 11:06:48 ubuntu.local ticky: ERROR: Connection to DB failed (username)"""

def check_logs(log_file):

    users = {}
    error_type = {}

    pattern = r"[\w]* [\d]* [\d:]* [\w. ]+: ([\w]+) ([\w \[\]\#]*) \(([\w.]*)\)"

    with open(log_file, 'r') as file:
        #lines = file.readlines() not needed
        for line in file:
            match_check = re.search(pattern, line)
            # skip lines that don't match
            if not match_check:         
                continue  

            log_level = match_check[1]  # e.g., "ERROR" or "INFO"
            message = match_check[2]    # for ERROR log
            username = match_check[3]

            # ensure key exists
            users.setdefault(username, {"ERROR": 0, "INFO": 0})
            
            if log_level == "ERROR":
                error_type[message] = error_type.get(message, 0) + 1
                users[username]["ERROR"] += 1
            elif log_level == "INFO":
                users[username]["INFO"] += 1

    sorted_users = sorted(users.items())
    sorted_error_type = sorted(error_type.items(), key = lambda x:x[1], reverse=True)
        
    # return sorted_error_type, sorted_users

    # * Create CSV file user_statistics
    with open('user_statistics.csv', 'w', newline='') as user_csv:
        user_csv.write('Username,INFO,ERROR\n')
        for key, value in sorted_users:
            user_csv.write(str(key) + ',' + str(value['ERROR']) + ',' + str(value['INFO'])+'\n')

    # * Create CSV error_message
    with open('error_message.csv', 'w', newline='') as error_csv:
        error_csv.write('Error,Count\n')
        for key, value in sorted_error_type:
            error_csv.write(str(key) + ',' + str(value)+'\n')

    
if __name__ == "__main__":
    check_logs(sys.argv[1])





######## ANS ##########

# #!/usr/bin/env python3
# import sys
# import re
# import operator
# import csv

# # Dict: Count number of entries for each user
# per_user = {}  # Splitting between INFO and ERROR
# # Dict: Number of different error messages
# errors = {}

# # * Read file and create dictionaries
# with open('syslog.log') as file:
#     # read each line
#     for line in file.readlines():
#         # regex search
#         # * Sample Line of log file
#         # "May 27 11:45:40 ubuntu.local ticky: INFO: Created ticket [#1234] (username)"
#         match = re.search(
#             r"ticky: ([\w+]*):? ([\w' ]*)[\[[#0-9]*\]?]? ?\((.*)\)$", line)
#         code, error_msg, user = match.group(1), match.group(2), match.group(3)

#         # Populates error dict with ERROR messages from log file
#         if error_msg not in errors.keys():
#             errors[error_msg] = 1
#         else:
#             errors[error_msg] += 1
#         # Populates per_user dict with users and default values
#         if user not in per_user.keys():
#             per_user[user] = {}
#             per_user[user]['INFO'] = 0
#             per_user[user]['ERROR'] = 0
#         # Populates per_user dict with users logs entry
#         if code == 'INFO':
#             if user not in per_user.keys():
#                 per_user[user] = {}
#                 per_user[user]['INFO'] = 0
#             else:
#                 per_user[user]["INFO"] += 1
#         elif code == 'ERROR':
#             if user not in per_user.keys():
#                 per_user[user] = {}
#                 per_user[user]['INFO'] = 0
#             else:
#                 per_user[user]['ERROR'] += 1


# # Sorted by VALUE (Most common to least common)
# errors_list = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)

# # Sorted by USERNAME
# per_user_list = sorted(per_user.items(), key=operator.itemgetter(0))

# file.close()
# # Insert at the beginning of the list
# errors_list.insert(0, ('Error', 'Count'))

# # * Create CSV file user_statistics
# with open('user_statistics.csv', 'w', newline='') as user_csv:
#     for key, value in per_user_list:
#         user_csv.write(str(key) + ',' +
#                        str(value['INFO']) + ',' + str(value['ERROR'])+'\n')

# # * Create CSV error_message
# with open('error_message.csv', 'w', newline='') as error_csv:
#     for key, value in errors_list:
#         error_csv.write(str(key) + ' ' + str(value))/#
    
