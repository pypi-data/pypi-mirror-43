import sys
import argparse

from .test import test
from .core import run
from .file_mgr import truncated_files
from .update import update

# main argument parser, after pre-checking info
def parse():
    parser = argparse.ArgumentParser(prog="texnew",description='An automatic LaTeX template creator.')
    parser.add_argument('target', metavar='output', type=str, nargs=1,
                                help='the name of the file you want to create')
    parser.add_argument('template_type', metavar='template', type=str, nargs=1,
                                help='the name of the template to use')

    parser.add_argument('-l', "--list", action="store_true", default=False, dest="lst",help="list existing templates and root folder")
    parser.add_argument('-c', "--check", action="store_true", default=False, dest="lst",help="check for errors in existing templates")
    parser.add_argument('-u', "--update", action="store_true", default=False, dest="update",help="update the specified file with the desired template")

    args = parser.parse_args()
    return (args.target[0], args.template_type[0], args.update)

def main():
    if "-l" in sys.argv:
        print("\nRoot Folder: {}/".format(rpath()))
        print("Existing templates:\n"+ "\t".join(truncated_files("templates")))
    elif "-c" in sys.argv:
        test()
    else:
        target, template_type, update = parse()
        if update:
            update(target, template_type)
        else:
            if not target.endswith(".tex"):
                target = target + ".tex"
            run(target, template_type)

# entry point for script
if __name__ == "__main__":
    main()
