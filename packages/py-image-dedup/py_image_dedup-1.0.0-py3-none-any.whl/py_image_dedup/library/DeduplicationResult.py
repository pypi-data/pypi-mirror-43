from tabulate import tabulate

from py_image_dedup.persistence import MetadataKey
from py_image_dedup.util import echo

BYTE_IN_A_MB = 1048576


class DeduplicationResult:

    def __init__(self):
        self._removed_files = set()
        self._removed_folders = set()
        self._reference_files = {}
        self._file_duplicates = {}

    def get_duplicate_count(self) -> int:
        """
        :return: amount of files that have at least one duplicate
        """
        count = 0
        for key, value in self._file_duplicates.items():
            if len(value) > 0:
                count += 1

        return count

    def get_removed_files(self) -> []:
        """
        :return: a list of all the files that have been removed
        """
        return self._removed_files

    def add_removed_file(self, file: str):
        """
        Adds a file to the list of removed files
        :param file: the file to add
        """
        self._removed_files.add(file)

    def get_removed_empty_folders(self) -> []:
        """
        :return: a list of empty folders that have been removed
        """
        return self._removed_folders

    def add_removed_empty_folder(self, folder: str):
        """
        Adds a folder to the list of removed empty folders
        :param folder: the folder to add
        """
        self._removed_folders.add(folder)

    def set_file_duplicates(self, reference_file: dict, duplicate_files: []):
        """
        Set a list of files that are duplicates of the reference file
        :param reference_file: the file that is used as a baseline
        :param duplicate_files: duplicates of the reference_file
        """
        reference_file_path = reference_file[MetadataKey.PATH.value]
        self._reference_files[reference_file_path] = reference_file
        self._file_duplicates[reference_file_path] = duplicate_files

    def get_file_duplicates(self) -> {}:
        """
        Get a list of files that are duplicates of other files
        """
        return self._file_duplicates

    def print_to_console(self):
        title = "" * 7 + "Summary"
        echo(title, color='cyan')
        echo('=' * 21, color='cyan')
        echo("Files with duplicates: %s" % self.get_duplicate_count())

        headers = ("Action", "File path", "Dist", "Filesize", "Pixels")

        for reference_file_path, folder in self.get_file_duplicates().items():
            duplicate_count = len(folder)
            if duplicate_count > 0:
                columns = []
                echo()

                for item in [self._reference_files[reference_file_path]] + folder:
                    row = []
                    file_path = item[MetadataKey.PATH.value]
                    distance = item[MetadataKey.DISTANCE.value]
                    distance_rounded = round(distance, 3)
                    file_size = item[MetadataKey.METADATA.value][MetadataKey.FILE_SIZE.value]
                    file_size_mb = round(file_size / BYTE_IN_A_MB, 3)
                    pixel_count = item[MetadataKey.METADATA.value][MetadataKey.PIXELCOUNT.value]

                    if file_path in self.get_removed_files():
                        row.append("remove")
                    else:
                        row.append("-")

                    row.append(file_path)
                    row.append(distance_rounded)
                    row.append(file_size_mb)
                    row.append(pixel_count)

                    columns.append(row)

                self._echo_table(tabulate(columns, headers=headers, stralign='center'))

        echo()
        echo("Removed (empty) folders (%s):" % len(self.get_removed_empty_folders()))
        for folder in self.get_removed_empty_folders():
            echo("%s" % folder, color='red')

    @staticmethod
    def _echo_table(table: str):
        lines = table.splitlines()

        for line in lines[:2]:
            echo(line, color='cyan')

        for line in lines[2:]:
            if line.lstrip().startswith("remove"):
                echo(line, color='red')
            else:
                echo(line, color='green')
