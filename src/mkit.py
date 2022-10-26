"""
    | ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
    | ┗┳        ┗━┓
    |  ┃          ┣┓
    |  ┃          ┏┛
    |  ┗┓┓┏━━━━┳┓┏┛
    |   ┃┫┫    ┃┫┫
    |   ┗┻┛    ┗┻┛
    God Bless,Never Bug.
"""
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

from core.mkgit import MkGit

class Mkit(click.MultiCommand):

    @click.group(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green',
    )
    # @click.command(context_settings=dict(help_option_names=['-h', '--help']))
    @click.version_option(version='0.0.1', prog_name='mkit')
    def cli():
        """
        \b
                        __   _ __
             ____ ___  / /__(_) /_
            / __ `__ \/ //_/ / __/
           / / / / / / ,< / / /_
          /_/ /_/ /_/_/|_/_/\__/

        FILENAME is the name of the file to check.
        """
        pass

    @cli.command()
    @click.option('-i', '--igore', 'ignore', help='ignore files')
    def gitadd(ignore):
        """ Auto add all files to git and ignore submodules """
        MkGit.add()

    @cli.command()
    def gitfetch():
        """ sort out current branchs """
        MkGit.fetch()

if __name__ == '__main__':
    Mkit.cli()


