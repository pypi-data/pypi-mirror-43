def make_doc():
    try:
        import doc_maker as doc
    except Exception:
        try:
            import os_sys.doc_maker as doc
        except Exception:
            try:
                from . import doc_maker as doc
            except Exception as x:
                raise Exception('docmaker not availeble try again later') from x
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
import sys


def main(args=None):
    help_msg = 'help for os_sys:\n\
commands:\n\
    make_doc\n\
    help\n\
help:\n\
    make_doc:\n\
        auto doc maker. generates a doc about a package or a module.\n\
    help:\n\
        shows this help screen'
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    if 'make_doc' == args[0]:
        make_doc()
    elif 'help' == args[0]:
        print(help_msg)
    else:
        print(help_msg)
        print('\n\n')
        print('error:', file=sys.stderr)
        print('    command %s is not a os_sys command' % args[0])
if __name__ == "__main__":
    main()
        
