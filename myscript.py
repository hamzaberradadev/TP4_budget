import os
import json
## we will create a cash file to store the last good commit after each good push to the server
cash_file = 'last_good_commit.json'
good_commit = None
## we will open and read the cash file
with open(cash_file, 'r') as f:
    good_commit = json.load(f)['hash']

## we will get the current commit hash
last_commit = os.popen('git rev-parse HEAD').read().strip()

## we will run the git bisect command

print (last_commit+' '+good_commit)
os.system('git bisect start %s %s' % (last_commit, good_commit))
the_output_of_bisect = os.popen('git bisect run python manage.py test').read()
os.popen('git bisect bad').read()
os.popen('git bisect reset').read()

## we will check if the output of the bisect command is the bad commit
print('################################# \n %s' % the_output_of_bisect)
if the_output_of_bisect.find('is the first bad commit') != -1:
    ## then raise an error to stop the bisect
    raise Exception('Bisect found the bad commit')

with open(cash_file, 'w') as f:
    json.dump({'hash': last_commit}, f, indent=4)