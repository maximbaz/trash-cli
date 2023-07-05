import unittest

from trashcli import trash
from .. import run_command
from ..support.my_path import MyPath


class TestEmptyEndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = MyPath.make_temp_dir()

    def test_help(self):
        result = run_command.run_command(self.tmp_dir, "trash-empty",
                                         ['--help'])
        self.assertEqual(["usage: trash-empty [-h] [--print-completion {bash,zsh,tcsh}] [--version]", '', 0],
                         [result.stdout[0:72],
                          result.stderr,
                          result.exit_code])

    def test_h(self):
        result = run_command.run_command(self.tmp_dir, "trash-empty",
                                         ['-h'])
        self.assertEqual(["usage:", '', 0],
                         [result.stdout[0:6],
                          result.stderr,
                          result.exit_code])

    def test_version(self):
        result = run_command.run_command(self.tmp_dir, "trash-empty",
                                         ['--version'])
        self.assertEqual(['trash-empty %s\n' % trash.version, '', 0],
                         [result.stdout,
                          result.stderr,
                          result.exit_code])

    def test_on_invalid_option(self):
        result = run_command.run_command(self.tmp_dir, "trash-empty",
                                         ['--wrong-option'])

        self.assertEqual(['',
                          'trash-empty: error: unrecognized arguments: --wrong-option',
                          2],
                         [result.stdout,
                          result.stderr.splitlines()[-1],
                          result.exit_code])

    def test_on_print_time(self):
        result = run_command.run_command(
            self.tmp_dir, "trash-empty",
            ['--print-time'],
            env={'TRASH_DATE': '1970-12-31T23:59:59'})

        self.assertEqual(['1970-12-31T23:59:59\n',
                          '',
                          0],
                         result.all)

    def test_on_trash_date_not_parsable(self):
        result = run_command.run_command(
            self.tmp_dir, "trash-empty",
            ['--print-time'],
            env={'TRASH_DATE': 'not a valid date'})

        self.assertEqual(['trash-empty: invalid TRASH_DATE: not a valid date\n',
                          0],
                         [result.stderr, result.exit_code])

    def tearDown(self):
        self.tmp_dir.clean_up()
