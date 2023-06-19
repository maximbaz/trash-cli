from __future__ import print_function
from __future__ import unicode_literals

from typing import List

from trashcli.lib.my_input import Input
from trashcli.restore.file_system import ReadCwd
from trashcli.restore.output import Output
from trashcli.restore.output_recorder import OutputRecorder
from trashcli.restore.restore_asking_the_user import RestoreAskingTheUser
from trashcli.restore.restorer import Restorer
from trashcli.restore.run_restore_action import Handler
from trashcli.restore.trashed_file import TrashedFile


class HandlerImpl(Handler):
    def __init__(self,
                 input,  # type: Input
                 cwd,  # type: ReadCwd
                 restorer,  # type: Restorer
                 output,  # type: Output
                 ):
        self.input = input
        self.cwd = cwd
        self.restorer = restorer
        self.output = output

    def handle_trashed_files(self,
                             trashed_files,  # type: List[TrashedFile]
                             overwrite,  # type: bool
                             ):
        if not trashed_files:
            self.output.println(Outputs.NoFileFound(self.cwd.getcwd_as_realpath()).as_string())
        else:
            for i, trashed_file in enumerate(trashed_files):
                self.output.println(Outputs.PrintFile(i, trashed_file).as_string())
            self.restore_asking_the_user(trashed_files, overwrite)

    def restore_asking_the_user(self, trashed_files, overwrite):
        my_output = OutputRecorder()
        restore_asking_the_user = RestoreAskingTheUser(self.input,
                                                       self.restorer,
                                                       my_output)
        restore_asking_the_user.restore_asking_the_user(trashed_files,
                                                        overwrite)
        my_output.apply_to(self.output)


class Outputs:
    class NoFileFound:
        def __init__(self, directory):
            self.directory = directory

        def as_string(self):
            return "No files trashed from current dir ('%s')" % self.directory

    class PrintFile:
        def __init__(self, index,  # type: int
                     trashed_file,  # type: TrashedFile
                     ):
            self.index = index
            self.trashed_file = trashed_file

        def as_string(self):
            return "%4d %s %s" % (self.index,
                                  self.trashed_file.deletion_date,
                                  self.trashed_file.original_location)
