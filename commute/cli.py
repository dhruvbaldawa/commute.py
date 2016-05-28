#!/usr/bin/env python
"""
The MIT License (MIT)

Copyright (c) 2016 Dhruv Baldawa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import commute
import click
import time
from parsedatetime import Calendar


@click.command()
@click.option('--config', '-c', type=click.Path(exists=True, dir_okay=False),
              required=True,
              help="path to the configuration yaml file (config.yml).")
@click.option('--src', '-s', required=True,
              help="name of the source place as used in the "
              "configuration.")
@click.option('--dst', '-d', required=True,
              help="name of the destination as used in the "
              "configuration.")
@click.option('--when', '-w', default=None,
              help="time from when to start calculating the commute"
              ", defaults to the current time")
def cli(config, src, dst, when):
    """
    commute.py helper CLI to compute possible commute options.
    """
    if when is not None:
        when = int(time.mktime(Calendar().parseDT(when)[0].timetuple()))
    for rank, path in commute.get_all_paths(config, src, dst, when):
        click.echo(commute.format_path(rank, path))
        click.echo("-" * 5)


if __name__ == "__main__":
    cli()
