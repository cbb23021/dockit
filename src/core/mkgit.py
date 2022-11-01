import os
import re
import subprocess
import sys
from getopt import getopt

import click
from colorama import Back, Fore, Style


class MkGit:
    _PATH_MAIN = os.popen('git rev-parse --show-toplevel').read().strip()
    _PATH_SUB_LS = os.popen(
        "git config --file .gitmodules --get-regexp path | awk '{ print $2 }'"
    ).read().splitlines()
    _PATH_SUB = list()
    _WT_ON_BK = Fore.WHITE + Back.LIGHTBLACK_EX
    _RESET = Style.RESET_ALL

    @classmethod
    def _get_submodules(cls):
        cls._PATH_SUB = [
            os.path.join(cls._PATH_MAIN, _) for _ in cls._PATH_SUB_LS
        ]

    @classmethod
    def add(cls, ignore):
        """ Auto add all files to git except submodules """
        cls._get_submodules()
        os.system('git add .')

        if cls._PATH_SUB:
            os.system(f'git restore --stage {" ".join(cls._PATH_SUB_LS)}')

        if ignore:
            os.system(f'git restore --stage {" ".join(ignore)}')

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

             - [deleted] (none) -> origin/feature/xxxx/add-advanced-task
             - [deleted] (none) -> origin/patch/michael/rename-success
        """
        pattern = re.compile(r'\[(.+)(\].+-> origin/)(.+)')
        info = pattern.sub(
            rf'[{Fore.CYAN}\1{Fore.RESET}\2{Fore.CYAN}\3{Fore.RESET}', info)
        return info

    @staticmethod
    def _re_branchs(msg):
        """ """
        pattern_remote = re.compile(r'(remotes[/\w]*)')
        pattern_now = re.compile(r'(\*)( )(.*)')
        msg = pattern_remote.sub(rf'{Fore.RED}\1{Fore.RESET}', msg)
        msg = pattern_now.sub(
            rf'{Fore.YELLOW}\1{Fore.RESET}\2{Fore.GREEN}\3{Fore.RESET}', msg)
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
            msg = cls._re_branchs(msg=subprocess.getoutput('git branch -a'))
            print(msg)

    @classmethod
    def _get_colored_repo(cls):
        repo = os.path.basename(os.getcwd())
        return (f'\n{Fore.LIGHTBLACK_EX}'
                f'{cls._WT_ON_BK}{repo}'
                f'{cls._RESET}'
                f'{Fore.LIGHTBLACK_EX}'
                f'{cls._RESET} ')

    @classmethod
    def _checkout(cls, branch):
        colored_repo = cls._get_colored_repo()
        info = subprocess.getoutput(f'git checkout {branch}')
        try:
            if 'Already on' in info:
                status = f'Already on {Fore.CYAN}{branch}{cls._RESET}'

            elif 'Switched to' in info:
                status = f'Switched to {Fore.YELLOW}{branch}{cls._RESET}'

            else:
                status = f'Error on {Fore.RED}{branch}{cls._RESET}\n{info}'

        except Exception:
            status = f'Error on {Fore.RED}{branch}{cls._RESET}\n{info}'

        print(f'{colored_repo}{status}')

    @classmethod
    def _current_branch(cls):
        colored_repo = cls._get_colored_repo()
        try:
            output = str(
                subprocess.check_output(['git', 'branch'],
                                        cwd=os.getcwd(),
                                        universal_newlines=True))
            branch = [a for a in output.split('\n') if a.find('*') >= 0][0]
            current_branch = branch[branch.find('*') + 2:]
            status = f'Stay on {Fore.GREEN}{current_branch}{cls._RESET}'

        except Exception:
            status = f'Error on {Fore.RED}info{cls._RESET}\n{output}'

        print(f'{colored_repo}{status}')

    @classmethod
    def swap(cls, ignore, branch_name):
        """s branch_name
        swap current branch to target branch
        """
        cls._checkout(branch=branch_name)

        cls._get_submodules()
        if not cls._PATH_SUB:
            return
        for path in cls._PATH_SUB:
            os.chdir(path)
            if branch_name in ignore:
                cls._current_branch()
            cls._checkout(branch=branch_name)

    @classmethod
    def pull(cls):
        """ pull all file from Git repo """


if __name__ == '__main__':
    MkGit.swap()
