import click
import sys
sys.path.append('..')
from GetOdds import getresults


@click.command(name='give-me-the-odds')
@click.argument('millenium', nargs=1)
@click.argument('empire', nargs=1)
def result(millenium, empire):
   print(int(getresults(millenium, empire)[0]))


if __name__ == "__main__":
    result()