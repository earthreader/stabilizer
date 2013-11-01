import argparse
import os
import pkgutil


def export(output, package):
    namespace = package.__name__
    prefix = package.__name__ + '.'
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, prefix):
        try:
            module = __import__(modname, fromlist="dummy")
            name = module.__name__
            with open(os.path.join(output, name + '.cs'), 'w') as fp:
                fp.write('using Python.Runtime;')
                fp.write('namespace {0} {{\n'.format(namespace))
                fp.write('namespace {0} {{\n'.format(name))

                for attrname in dir(module):
                    if attrname.startswith('__') and attrname.endswith('__'):
                        continue
                    attr = getattr(module, attrname)
                    #TODO: write class, ETC.

                fp.write('}\n}')
        except:
            print('Cannot save module: {0}'.format(modname))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='stabler')
    parser.add_argument('-o', '--output', default='stabilized', help='output derectory')
    parser.add_argument('package', help='package to stabilize')

    args = parser.parse_args()
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    elif not os.path.isdir(args.output):
        print('{0} is already exist and not directory.')
        exit(1)

    package = __import__(args.package)
    export(args.output, package)
