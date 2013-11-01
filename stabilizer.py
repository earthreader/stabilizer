import argparse
import inspect
import os
import pkgutil


TEMPLATE_CS = """using Python.Runtime;

namespace {0} {{
{1}
}}
"""

TEMPLATE_CLASS = """public class {0} {{
}}
"""

TEMPLATE_FUNCTION = """public PyObj {0}({1}) {{
}}
"""

TEMPLATE_STR = """public String {0} {{get{{}} set{{}}}}
"""

TEMPLATE_BOOL = """public Boolean {0} {{get{{}} set{{}}}}
"""

IGNORE_LIST = { '__all__', '__builtins__', '__doc__', '__file__', '__name__',
               '__package__'}

def export(output, package):
    prefix = package.__name__ + '.'
    for imp, modname, ispkg in pkgutil.walk_packages(package.__path__, prefix):
        try:
            module = __import__(modname, fromlist="dummy")
            name = module.__name__
            with open(os.path.join(output, name + '.cs'), 'w') as fp:
                contents = []
                try:
                    all = module.__all__
                except:
                    all = dir(module)
                for attrname in all:
                    if attrname in IGNORE_LIST:
                        continue
                    attr = getattr(module, attrname)
                    #TODO: write class, ETC.
                    if inspect.ismodule(attr):
                        continue
                    elif inspect.isclass(attr):
                        contents.append(TEMPLATE_CLASS.format(attrname))
                    elif inspect.isfunction(attr):
                        spec = inspect.getargspec(attr)
                        args = []
                        for arg in spec.args:
                            args.append('PyObject {0}'.format(arg))
                        contents.append(
                            TEMPLATE_FUNCTION.format(attrname, ', '.join(args))
                        )
                    elif isinstance(attr, str):
                        contents.append(TEMPLATE_STR.format(attrname))
                    elif isinstance(attr, bool):
                        contents.append(TEMPLATE_BOOL.format(attrname))
                    else:
                        print type(attr), attrname

                fp.write(
                    TEMPLATE_CS.format(name, ''.join(contents))
                )
        except Exception as e:
            print e
            print('Cannot save module: {0}'.format(modname))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='stabler')
    parser.add_argument('-o', '--output', default='stabilized',
                        help='output derectory')
    parser.add_argument('package', help='package to stabilize')

    args = parser.parse_args()
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    elif not os.path.isdir(args.output):
        print('{0} is already exist and not directory.')
        exit(1)

    package = __import__(args.package)
    export(args.output, package)
