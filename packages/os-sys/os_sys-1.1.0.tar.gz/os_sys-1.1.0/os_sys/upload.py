import os, sys, requests
def all_dict(dictory, exceptions=None, file_types=None, maps=True, files=False, print_data=False):
    import os
    data = []
    string_data = ''
    e = exceptions
    if 'list' in str(type(e)) or e == None:
        pass
    else:
        raise TypeError('expected a list but got a %s' % type(e))
    e = file_types
    if 'list' in str(type(e)) or e == None:
        pass
    else:
        raise TypeError('expected a list but got a %s' % type(e))
    
    print_ = print_data
    
    for dirname, dirnames, filenames in os.walk(dictory):
        # print path to all subdirectories first.
        if maps:
            for subdirname in dirnames:
                dat = os.path.join(dirname, subdirname)
                data.append(dat)
                string_data = string_data + '\n' + dat
                if print_:
                    print(dat)

        # print path to all filenames.
        if files:
            for filename in filenames:
                s = False
                fname_path = filename
                file = fname_path.split('.')
                no = int(len(file) - 1)
                file_type = file[no]
                if not e == None:
                    for b in range(0, len(e)):
                        if e[b] == file_type:
                            s = True
                            
                if e == None:
                    s = True
                if s:
                    s = False   
                            
                    dat = os.path.join(dirname, filename)
                    data.append(dat)
                    string_data = string_data + '\n' + dat
                    if print_:
                        
                        print(dat)
        

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if not exceptions == None:
            
            for ip in range(0, int(len(exceptions))):
                exception = exceptions[ip]
                
                if exception in dirnames:
                    # don't go into any .git directories.
                    dirnames.remove(exception)
    
    return [data, string_data]
def upload(file, link='http://httpbin.org/post'):
    with open(str(file), 'rb') as f:
        r = requests.post(link, files={str(file): f})
    return str(r.text)
def upload_tree(dictory, link='http://httpbin.org/post'):
    files = all_dict(dictory, None, None, False, True, False)[0]
    for k in range(0, len(files)):
        try:
            k.replace(str(str(dictory)), '')
        except:
            pass
    response = []
    for i in range(0, len(files)):
        try:
            response.append(upload(str(files[i]), link))
        except Exception as ex:
            response.append('''error: %s by uploading file''' % ex)
    return response
print(upload_tree('C:/mattie/own lib/own lib/dist', link='https://upload.pypi.org/legacy'))
