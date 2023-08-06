import click
from .commands.encoding import encoding
from .commands.esub import esub
from .commands.run import run, rune
from .commands.sdel import sdel
from .commands.which import which
from .commands.pn import pn
from .commands.flatten import flatten
from .commands.rename import rename
from .commands.duration import duration

@click.group()
def main():
    pass


main.add_command(encoding)
main.add_command(esub)
main.add_command(run)
main.add_command(rune)
main.add_command(sdel)
main.add_command(which)
main.add_command(pn)
main.add_command(flatten)
main.add_command(rename)
main.add_command(duration)

if __name__ == '__main__':
    main()
