import re
import os
import sys
import subprocess
import click
from getopt import getopt

from colorama import Fore, Back, Style


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

    @staticmethod
    def _re_words(info):
        """
        e.q.
            From https://xxx.net/xxx/xx
             - [
               group1: (deleted)
               group2: (]         (none)     -> origin/)
               group3: (feature/michael/xxxx)

             - [deleted]         (none)     -> origin/feature/xxxx/add-advanced-task
             - [deleted]         (none)     -> origin/patch/michael/rename-success-to-completed
        """
        # return re.sub(r'\[(.+)(\].+-> origin/)(.+)', rf'[{Fore.CYAN}\1{Fore.RESET}\2{Fore.CYAN}\3{Fore.RESET}', info)
        pattern = re.compile(r'\[(.+)(\].+-> origin/)(.+)')
        info = pattern.sub(rf'[{Fore.CYAN}\1{Fore.RESET}\2{Fore.CYAN}\3{Fore.RESET}', info)
        return info

    @staticmethod
    def _re_branchs(msg):
        """ """
        pattern_remote = re.compile(r'(remotes[/\w]*)')
        pattern_now = re.compile(r'(\*)( )(.*)')
        msg = pattern_remote.sub(rf'{Fore.RED}\1{Fore.RESET}', msg)
        msg = pattern_now.sub(rf'{Fore.YELLOW}\1{Fore.RESET}\2{Fore.GREEN}\3{Fore.RESET}', msg)
        return msg

    @classmethod
    def fetch(cls):
        """ sort out current branchs """
        try:
            info = subprocess.getoutput('git fetch --prune')
        except:
            print('No Git detect!')
            return

        if not info:
            info = 'Nothing To Update.'
        if 'deleted' in info:
            info = MkGit._re_words(info=info)
        print(info)

        # display branches
        click.echo('show branchs [y/N]: \n')
        show = click.getchar()
        if show == 'y':
            msg  = cls._re_branchs(msg=subprocess.getoutput('git branch -a'))
            print(msg)

    @classmethod
    def swap(cls):
        """ swap current branch to target branch """

    @classmethod
    def pull(cls):
        """ pull all file from Git repo """


if __name__ == '__main__':
    MkGit.swap()
