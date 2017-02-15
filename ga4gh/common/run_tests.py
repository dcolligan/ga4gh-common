"""
Emulates a Travis CI run
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ga4gh.common
import ga4gh.common.cli as cli
import ga4gh.common.utils as utils


class TravisSimulator(object):

    logStrPrefix = '***'
    yamlFileLocation = '.travis.yml'

    def __init__(self, args):
        self.args = args

    def parseTestCommands(self):
        yamlData = utils.getYamlDocument(self.yamlFileLocation)
        return yamlData['script']

    def runTests(self):
        testCommands = self.parseTestCommands()
        for command in testCommands:
            if self.args.python is not None and command[0:6] == 'python':
                command = self.args.python + command[6:]
            self.log('Running: "{}"'.format(command))
            utils.runCommand(command)
        self.log('SUCCESS')

    def log(self, logStr):
        utils.log("{0} {1}".format(self.logStrPrefix, logStr))


def run_tests_main():
    parser = cli.createArgumentParser("runs tests for a ga4gh package")
    versionString = "GA4GH Runtests Version {}".format(
        ga4gh.common.__version__)
    parser.add_argument(
        "--version", version=versionString, action="version")
    parser.add_argument(
        "-p", "--python",
        help="path of the python executable to use", default=None)
    args = parser.parse_args()

    travisSimulator = TravisSimulator(args)
    travisSimulator.runTests()
