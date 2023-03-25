# import os
# import json
# ## we will create a cash file to store the last good commit after each good push to the server
# cash_file = 'last_good_commit.json'
# good_commit = None
# ## we will open and read the cash file
# with open(cash_file, 'r') as f:
#     good_commit = json.load(f)['hash']

# ## we will get the current commit hash
# last_commit = os.popen('git rev-parse HEAD').read().strip()

# ## we will run the git bisect command

# print (last_commit+' '+good_commit)
# os.system('git bisect start %s %s' % (last_commit, good_commit))
# the_output_of_bisect = os.popen('git bisect run python manage.py test').read()
# os.popen('git bisect bad').read()
# os.popen('git bisect reset').read()

# ## we will check if the output of the bisect command is the bad commit
# print('################################# \n %s' % the_output_of_bisect)
# if the_output_of_bisect.find('is the first bad commit') != -1:
#     ## then raise an error to stop the bisect
#     raise Exception('Bisect found the bad commit')

# with open(cash_file, 'w') as f:
#     json.dump({'hash': last_commit}, f, indent=4)

import os 
import sys
import subprocess

result = subprocess.run(['python', 'manage.py', 'test'], capture_output=True, text=True)

if result.returncode == 0:
    print("Tous les tests ont réussi !")
    exit(0)
else:
    print("Des erreurs ont été trouvées lors de l'exécution des tests :\n")
    print(result.stdout)
    print(result.stderr)
    bad_commit = subprocess.run(['git', 'log', '-1', '--pretty=format:%H'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    good_commit = subprocess.run(['git', 'log','--skip=19', '-n', '1', '--pretty=format:%H'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    print('bad_commit: %s' % bad_commit)
    print('good_commit: %s' % good_commit)

    print(subprocess.run(['git', 'bisect', 'good', good_commit],capture_output=True, text=True).stdout.strip()) 
    print(subprocess.run(['git', 'bisect', 'bad', bad_commit],capture_output=True, text=True).stdout.strip()) 
    
    while(True):
        result = subprocess.run(['python', 'manage.py', 'test'], capture_output=True, text=True)
        this_commit = subprocess.run(['git', 'log', '-1', '--pretty=format:%H'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        print('this_commit: %s' % this_commit)
        if result.returncode == 0:
            print('good')
            r = subprocess.run(['git', 'bisect', 'good', this_commit],capture_output=True, text=True).stdout
        else:
            print('bad')
            r = subprocess.run(['git', 'bisect', 'bad', this_commit],capture_output=True, text=True).stdout
        print(r)
        if r.find('is the first bad commit') != -1:
            print('is the first bad commit')
            bad_commit = r.split(' ')[1].strip()
            print('bad_commit: %s' % bad_commit)
            print(subprocess.run(['git', 'bisect', 'reset'],capture_output=True, text=True).stdout.strip())
            exit(1)


