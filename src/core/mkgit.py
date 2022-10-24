import os
import sys
from getopt import getopt


class MkGit:
    _PATH_MAIN = os.popen('git rev-parse --show-toplevel').read().strip()
    _PATH_SUB_LS = os.popen("git config --file .gitmodules --get-regexp path | awk '{ print $2 }'").read().splitlines()
    _PATH_SUB = list()

    @classmethod
    def _get_submodules(cls):
        cls._PATH_SUB = [os.path.join(cls._PATH_MAIN, _) for _ in cls._PATH_SUB_LS]

    @classmethod
    def add(cls):
        """ Auto add all files to git except submodules """
        cls._get_submodules()
        os.system('git add .')

        if cls._PATH_SUB:
            os.system(f'git restore --stage {" ".join(cls._PATH_SUB_LS)}')

        if len(sys.argv) > 1 and sys.argv[1] == '-i':
            args = sys.argv[2:]
            os.system(f'git restore --stage {" ".join(args)}')

        os.system('git status')

if __name__ == '__main__':
    MkGit.add()
