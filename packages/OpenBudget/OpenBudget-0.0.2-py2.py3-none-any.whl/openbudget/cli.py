#!/usr/bin/env python
# coding: utf-8
#     Simple budget management planner
#     Copyright (C) 2019  Adrien Oliva
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    Main `OpenBudget` CLI.
"""
import os
import sys
import click

from openbudget import __version__


def version_msg():
    """Return the OpenBudget version,
    location and Python powering it.
    """
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = u'OpenBudget %(version)s from {} (Python {})'
    return message.format(location, python_version)


@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.version_option(__version__, u'-V', u'--version', message=version_msg())
def main():
    """OpenBudget main function
    """
    sys.exit(0)
