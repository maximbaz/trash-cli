import datetime
import unittest

import pytest

from tests import run_command
from tests.fake_trash_dir import FakeTrashDir
from tests.support.my_path import MyPath


@pytest.mark.slow
class TestEndToEndList(unittest.TestCase):
    def setUp(self):
        self.temp_dir = MyPath.make_temp_dir()
        self.trash_dir = self.temp_dir / 'trash-dir'
        self.fake_trash_dir = FakeTrashDir(self.trash_dir)

    def test_list(self):
        self.fake_trash_dir.add_trashinfo2("/file1",
                                           datetime.datetime(2000, 1, 1, 0, 0,
                                                             1))
        self.fake_trash_dir.add_trashinfo2("/file2",
                                           datetime.datetime(2000, 1, 1, 0, 0,
                                                             1))

        result = run_command.run_command(self.temp_dir, "trash-list",
                                         ['--trash-dir', self.trash_dir])

        assert [
                   '2000-01-01 00:00:01 /file1',
                   '2000-01-01 00:00:01 /file2',
               ] == sorted(result.stdout.splitlines())

    def test_list_trash_dirs(self):
        result = run_command.run_command(
            self.temp_dir, "trash-list",
            ['--trash-dirs', '--trash-dir=/home/user/.local/share/Trash'])
        assert (result.stderr,
                sorted(result.stdout.splitlines()), result.exit_code) == (
                   '', [
                       '/home/user/.local/share/Trash'
                   ], 0)

    def test_list_with_paths(self):
        self.fake_trash_dir.add_trashinfo3("base1", "/file1",
                                           datetime.datetime(2000, 1, 1, 0, 0,
                                                             1))
        self.fake_trash_dir.add_trashinfo3("base2", "/file2",
                                           datetime.datetime(2000, 1, 1, 0, 0,
                                                             1))

        result = run_command.run_command(self.temp_dir, "trash-list",
                                         ['--trash-dir', self.trash_dir,
                                          '--files'])

        assert ('', [
            '2000-01-01 00:00:01 /file1 -> %s/files/base1' % self.trash_dir,
            '2000-01-01 00:00:01 /file2 -> %s/files/base2' % self.trash_dir,
        ]) == (result.stderr, sorted(result.stdout.splitlines()))

    def test_help(self):
        result = run_command.run_command(self.temp_dir, "trash-list", ['--help'])
        self.assertEqual("usage: trash-list [-h] [--print-completion {bash,zsh,tcsh}] [--version]",
                         result.stderr + result.stdout[0:71])

    def tearDown(self):
        self.temp_dir.clean_up()
