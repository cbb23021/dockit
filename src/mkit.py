import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

from core.mkgit import MkGit

class Mkit(click.MultiCommand):

    @click.group(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green',
    )
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
    def gitadd():
        MkGit.add()

if __name__ == '__main__':
    Mkit.cli()


