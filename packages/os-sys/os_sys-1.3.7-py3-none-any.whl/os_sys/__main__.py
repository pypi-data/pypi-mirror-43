def make_doc():
    import os_sys.doc_maker as doc
    docmaker = input('do you want to make a doc about a module or a package(typ: module or package):\n')
    if docmaker.lower() == 'module':
        path = input('module:\n')
        doc.doc_maker.make_doc(path)
    elif docmaker.lower() == 'package':
        path = input('path to package folder:\n')
        doc.helper.HTMLdoc(path)
    else:
        class ArgumentError(Exception):
            '''argument error'''
        raise ArgumentError('expected input module or package get input: %s' % docmaker)

        
