# Copyright (c) 2012 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse
import getpass
import textwrap

try:
    # use argcomplete if available
    import argcomplete
except ImportError:
    argcomplete = None

class Subcommand(object):
    @staticmethod
    def options(parser):
        pass

class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    '''
    Custom subcommand help formatter that suppresses hidden subcommands from
    help.
    '''
    def _format_action(self, action):
        '''
        Override _format_action, which is called during parser.format_help() to
        format a single (sub)command. This implementation simply returns no
        information (empty string) for actions (i.e. (sub)commands) that have
        been suppressed.  The default behavior being overridden simply prints
        "== SUPPRESSED ==" for the action.
        '''
        parts = super(SubcommandHelpFormatter, self)._format_action(action)
        if action.help == argparse.SUPPRESS:
            return ''
        return parts

def parse_options(parser, argv):
    parser.formatter_class = SubcommandHelpFormatter
    subparsers = parser.add_subparsers(
        title="REST API",
        description="Interact with the RESTful API by the command line",
        help="API action", metavar="")

    for cls in sorted(Subcommand.__subclasses__(), key=lambda cls: cls.NAME):
        # Add a subparser for each subcommand
        subparser = subparsers.add_parser(
            cls.NAME, description=cls.DESCRIPTION, help=cls.DESCRIPTION)

        # Add options particular to the subcommand
        cls.options(subparser)

        # Set the subcommand class
        subparser.set_defaults(subcommand=cls)

    if argcomplete is not None:
        argcomplete.autocomplete(parser)
    return parser.parse_args(argv)

def read_password(user=None, prompt=None):
    if prompt is not None:
        return getpass.getpass(prompt)
    return getpass.getpass("Enter password for %s: " % user)

def ask(command, message):
    # Wrap long lines to make the CLI output more readable
    wrapped_message = '\n'.join(
        textwrap.fill(line) for line in message.splitlines())
    f = raw_input("%s (yes/no): " % wrapped_message)
    if f.lower() == 'no':
        print 'Cancelling the %s request' % command
        return False
    elif f.lower() != 'yes':
        raise ValueError("Please enter 'yes' or 'no'")

    return True
