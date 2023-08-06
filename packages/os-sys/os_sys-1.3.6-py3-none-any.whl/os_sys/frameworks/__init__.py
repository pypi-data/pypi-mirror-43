import os
import inspect

# find all python files below a certain folder
files = []
for (dirpath, dirnames, filenames) in os.walk('C:\\Users\\matthijs\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\os_sys'):
    for filename in filenames:
        if filename.endswith('.py'):
            files.append(os.sep.join([dirpath, filename]))

for f in files:
    # turn the files into code objects and find declared constants
    functions = []
    code_obj = compile(open(f).read(), f, 'exec')
    members = dict(inspect.getmembers(code_obj))
    for idx in range(len(members['co_consts'])//2):
        val = members['co_consts'][idx * 2]
        name = members['co_consts'][idx * 2 + 1]
        # this also matches lambdas and classes... 
        if repr(type(val)) == "<class 'code'>":
            functions.append(name)
    print(f'{f}: {functions}')
