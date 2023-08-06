"""
semvermanager
=================
`semvermamager` exports a single class Version which implements
a restricted subset of the  SEMVER_ standard.

.. _SEMVER: http://semver.org/

Version defines a Semantic version using the following field
structure:

.. code-block:: python

    # MAJOR.MINOR.PATCH-TAG

    int MAJOR  # 0 to N
    int MINOR  # 0 to N
    int PATCH  # 0 to N
    str TAG    # one of "alpha", "beta".
    int TAG_VERSION # appended to the tag if the tag is alpha or beta.

Versions may be bumped by a single increment using any of the
`bump` functions. Bumping a PATCH value simply increments it.
Bumping a MINOR value zeros the PATCH value and bumping a MAJOR
zeros the MINOR and the PATCH value.

`semvermanager` only supports Python 3.6 and greater.
"""

import os
import re
import sys
import argparse

from typing import List
from .command import Command,  Query, QueryError,  CommandError, OperationRunner, EchoCommand

VERSION = '1.0.9'


class VersionError(ValueError):
    """Exception for handling errors in Version Class"""
    pass


class Version:
    """
    Handle creation and storage of SEMVER version numbers. In this case
    SEMVERs must be of the form a.b.c-tag, Where a,b and c are integers
    in the range 0-n and tag is one of `Version.TAGS`.

    Version numbers may be bumped by using the various bump functions.
    Bumping minor zeros patch, bumping major zeros minor.

    """

    TAGS = {0: "alpha", 1: "beta", 2: ""}
    FIELDS = ["major", "minor", "patch", "tag", "tag_version"]
    FILENAME = "VERSION"

    def __init__(self, major=0, minor=0, patch=0, tag="alpha", tag_version=0, lhs="VERSION", separator="="):
        """
        :param major: 0-n
        :param minor: 0-n
        :param patch: 0-n
        :param tag: member of Version.TAGs.values()
        :param tag_version: The version of the tag value (e.g. alpha0, alpha1 etc.)
        :param lhs : str The candidate str for the lhs of a VERSION line
        :param separator: str the seperator string between the field name and the version
        """
        if isinstance(lhs, str):
            self._lhs = lhs
        else:
            raise VersionError(f"{lhs} is not a str type")

        if isinstance(major, int) and major >= 0:

            self._major = major
        else:
            raise VersionError(f"{major} is not an int type or is a negative int")

        if isinstance(minor, int) and minor >= 0:
            self._minor = minor
        else:
            raise VersionError(f"{minor} is not an int type or is a negative int")

        if isinstance(patch, int) and patch >= 0:
            self._patch = patch
        else:
            raise VersionError(f"{patch} is not an int type or is a negative int")

        self._separator = separator
        self._tag_index = None
        self._tag = None
        for k, v in Version.TAGS.items():
            if tag == v:
                self._tag = v
                self._tag_index = k

        if isinstance(tag_version, int) and tag_version >= 0 :
            self._tag_version = tag_version
        else:
            raise VersionError(f"{tag_version} is not an int or is negative")

        if self._tag_index is None:
            raise VersionError(f"'{tag}' is not a valid version tag")

    def bump(self, field):
        self.bump_map()[field]()

    def bump_major(self):
        self._patch = 0
        self._minor = 0
        self._major += 1

    def bump_minor(self):
        self._patch = 0
        self._minor += 1

    def bump_patch(self):
        self._patch += 1

    def bump_tag(self):
        if self._tag_index == len(Version.TAGS) - 1:
            self._tag_index = 0
        else:
            self._tag_index += 1
        self._tag = Version.TAGS[self._tag_index]
        if self._tag == "":  # prod
            self._tag_version = 0

    def bump_tag_version(self):
        if self._tag != "":
            self.tag_version = self.tag_version + 1
        else:
            raise VersionError("tag is not 'alpha' or 'beta' no bumping allowed for tag_version")
        return self._tag_version

    @property
    def lhs(self):
        return self._lhs

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, value):
        assert isinstance(value, int) and value >= 0
        self._major = value

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, value):
        assert isinstance(value, int) and value >= 0
        self._minor = value

    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, value):
        assert isinstance(value, int) and value >= 0
        self._patch = value

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        assert self._tag in self.TAGS.values()
        self._tag = value

    @property
    def tag_version(self):
        return self._tag_version

    @tag_version.setter
    def tag_version(self, value):
        assert isinstance(value, int) and value >= 0
        self._tag_version = value


    def bump_map(self):
        """
        a mapping of field names to corresponding bump methods
        :return: a dict of field names to bump methods
        """
        return {"major": self.bump_major,
                "minor": self.bump_minor,
                "patch": self.bump_patch,
                "tag": self.bump_tag,
                "tag_version": self.bump_tag_version}

    def field_map(self):
        """
        Mapping of field names to field values.
        :return: A dict of field names to their properties.
        """
        return {"major": self.major,
                "minor": self.minor,
                "patch": self.patch,
                "tag": self.tag,
                "tag_version": self._tag_version}

    def field(self, field):
        """
        Return the mapping from a field to its corresponding
        property.
        :param field: str in Version.FIELDS
        :return:
        """

        if field not in self.FIELDS:
            raise VersionError(f"No such field name'{field}'")
        return self.field_map()[field]

    @staticmethod
    def update(filename, version, lhs="VERSION", separator="="):
        """
        Find any line starting with "VERSION" and replace that line with
        the new `version`.


        :param filename: A path to a file containing at least one VERSION line
        :param version: The new version object
        :param lhs: The label string
        :param separator: label<seperator>value
        :return: A tuple (number of lines updated, list(line_numbers))
        """

        count = 0 # Number of replacements
        lines: List[int] = [] # line numbers of replacement lines
        with open(filename, "r") as input_file:
            with open(filename+".temp", "w") as output_file:
                for i, line in enumerate(input_file, 1):
                    candidate = line.strip()
                    if candidate.startswith(lhs):
                        try:
                            v = Version.parse_version(line, lhs, separator=separator)
                            if v:
                                output_file.write(f"{str(version)}\n")
                                lines.append(i)
                                count = count + 1
                        except VersionError:
                            output_file.write(line)

                    else:
                        output_file.write(line)

        os.rename(filename, filename+".old")
        os.rename(filename+".temp", filename)

        return filename, lines

    def write(self, filename):
        """
        Write a single line containing the version object to filename.
        This will overwrite the existing file if it exists.

        :param filename: The file to create with the new version object
        :return: A tuple of the filename and the version object
        """

        with open(filename, "w") as file:
            file.write(f"{str(self)}\n")

        return filename, self

    @staticmethod
    def find(filename, lhs="VERSION", separator="="):
        """Look for the first instance of a VERSION definition in a file
        and try and parse it as a `Version`"""

        version = None
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith(lhs):
                    version = Version.parse_version(line, lhs=lhs, separator=separator)
                    break

        return version

    def read(self, filename, lhs=None, separator=None):
        """
        Read a single line from filename and parse it as version string.

        :param filename: a file containing a single line VERSION string.
        :param lhs : override the class field string
        :param separator: the character seperating the VERSION label from the value
        :return: a Version object

        :raises VersionError if it fails to parse the file.
        """

        with open(filename, "r") as file:
            line = file.readline()
            line.rstrip()

        if not lhs:
            lhs = self._lhs

        if not separator:
            separator = self._separator

        return self.parse_version(line, lhs, separator)
        # try:
        #     _, rhs = line.split(self._separator)
        # except ValueError as e:
        #     raise VersionError(e)
        #
        # try:
        #     version, tag = rhs.split("-")
        #     tag = tag.strip()
        #     tag = tag.strip("\"\'")
        #     version = version.strip()  # whitespace
        #     version = version.strip("\"\'")  # quotes
        # except ValueError as e:
        #     raise VersionError(e)
        #
        # try:
        #     major, minor, patch = [int(x) for x in version.split('.')]
        # except ValueError as e:
        #     raise VersionError(e)
        #
        # return Version(major, minor, patch, tag, tag_version=t separator=separator)

    @staticmethod
    def parse_version(line: str, lhs: str = "VERSION", separator="=") -> object:
        tag_version = 0
        line = line.strip()

        if line.startswith(lhs):
            try:
                version_label, rhs = line.split(separator)
                version_label = version_label.strip()
                rhs = rhs.strip()
                if version_label != lhs:
                    raise VersionError(f"{line} has wrong left hand side {version_label}")
            except ValueError as e:
                raise VersionError(f"{e} : in '{line}'")
        else:
            rhs = line

        try:
            if "-" in rhs:
                version, tag = rhs.split("-")
                tag = tag.strip()
                tag = tag.strip("\"\'")
                match = re.match(r"([a-z]+)([0-9]+)", tag, re.I)
                if match:
                    tag, tag_version = match.groups()
                    tag_version = int(tag_version)
                version = version.strip()
                version = version.strip("\"\'")
            else:
                version = rhs.strip()
                version = version.strip("\"\'")

                tag = ""
                tag_version = 0

        except ValueError as e:
            raise VersionError(f"{e} : in '{rhs}'")

        try:
            major, minor, patch = [int(x) for x in version.split('.')]
        except ValueError as e:
            raise VersionError(f"{e} : in {lhs} '{version}'")

        return Version(major, minor, patch, tag, tag_version, lhs=lhs, separator=separator)

    def __eq__(self, other):
        return self.major == other.major and \
               self.minor == other.minor and \
               self.patch == other.patch and \
               self.tag == other.tag and \
               self.tag_version == other.tag_version

    def __str__(self):
        if self.tag == "":
            return f"{self._lhs} {self._separator} '{self._major}.{self._minor}.{self._patch}'"
        else:
            return f"{self._lhs} {self._separator} '{self._major}.{self._minor}.{self._patch}-{self._tag}{self._tag_version}'"

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.major}, {self.minor}, {self.patch}, '{self.tag}', {self.tag_version}, '{self._lhs}', '{self._separator}')"

    @property
    def bare_version(self):
        if self.tag == "":
            return f'{self._major}.{self._minor}.{self._patch}'
        else:
            return f'{self._major}.{self._minor}.{self._patch}-{self._tag}{self.tag_version}'


VERSION = '1.0.9'


class BumpCommand(Command):

    def __call__(self, filename, label, separator, bump_field):
        if not os.path.isfile(filename):
            print(f'No such file: \'{filename}\' cannot bump {bump_field} version')
            return filename, None
        v = Version.find(filename, label, separator)
        if v:
            print(f"Bumping '{bump_field}' value from {v.field(bump_field)} ", end="")
            v.bump(bump_field)
            print(f"to {v.field(bump_field)} in '{filename}'")
            Version.update(filename, v, label, separator)
            print(f"new version: {v}")
        else:
            print(f"Couldn't bump value in {filename}")
        return filename, v


class MakeCommand(Command):

    def __init__(self, overwrite):
        super().__init__()
        self._overwrite = overwrite

    def __call__(self, filename, version_label, separator):

        v = Version(lhs=version_label, separator=separator)
        if self._overwrite or not os.path.isfile(filename):
            f, v = v.write(filename)

        elif os.path.isfile(filename):
            answer = input(f"Overwrite file '{filename}' (Y/N [N]: ")
            if len(answer) > 0 and answer.strip().lower() == 'y':
                f, v = v.write(filename)
            else:
                f = filename
                v = None

        return f, v


def script_main():
    main(sys.argv)


def main(args=None):
    if not args:
        args = sys.argv

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--version",
        help="Specify a version in the form major.minor.patch-tag"
    )

    parser.add_argument(
        "--make",
        default=False,
        action="store_true",
        help="Make a new version file")

    parser.add_argument(
        "--bump",
        choices=Version.FIELDS,
        help="Bump a version field")

    parser.add_argument(
        "--getversion",
        default=False,
        action="store_true",
        help="Report the current version in the specified file")

    parser.add_argument(
        "--bareversion",
        default=False,
        action="store_true",
        help="Return the unquoted version strin with VERSION=")

    parser.add_argument(
        "--overwrite",
        default=False,
        action="store_true",
        help="overwrite files without checking [default: %(default)s]"
    )

    parser.add_argument(
        "--update",
        default=False,
        action="store_true",
        help="Update multiple version strings in file"
    )

    parser.add_argument(
        "--label",
        default="VERSION",
        help="field used to determine which line is the version line [default: %(default)s]"
    )

    parser.add_argument(
        "--separator",
        default="=",
        help="Character used to separate the version label from the version [default: %(default)s]"
    )

    parser.add_argument(
        "filenames",
        nargs='*',
        help="Files to use as version file"
    )

    parser.add_argument(
        "--program_version",
        action="store_true",
        default=False,
        help="Report the version number"
    )
    args = parser.parse_args(args)

    if args.program_version:
        print(f"{sys.argv[0]} {VERSION}")

    if args.version:
        version = Version.parse_version("VERSION=" + args.version, lhs=args.label)

    if args.make:
        cmd_runner = OperationRunner(MakeCommand(args.overwrite))
        if not args.filenames:
            args.filenames = ["VERSION"]  # make a default file
        for f, v in cmd_runner(args.filenames, args.label, args.separator):
            if v:
                print(f"Created version {v} in '{f}'")
            else:
                print(f"Failed to create version file '{f}'")

    if args.getversion:
        if os.path.isfile(args.filename):
            v = Version.find(args.filename)
            print(v)
        else:
            print(f"No such version file: '{args.filename}'")

    if args.bareversion:
        if os.path.isfile(args.filename):
            v = Version.find(args.filename, args.label)
            print(v.bare_version())
        else:
            print(f"No such version file: '{args.filename}'")

    if args.bump:
        if args.bump in Version.FIELDS:
            cmd_runner = OperationRunner(BumpCommand())

            for filename, v in cmd_runner(args.filenames, args.label, args.separator, args.bump):
                if v:
                    print(f"Processed version {v} in file : '{filename}'")
                else:
                    print(f"Couldn't process '{filename}'")

            # if not os.path.isfile(args.filename):
            #     print(f"No such file:'{args.filename}' can't bump {args.bump} version")
            #     sys.exit(1)
            # v = Version.find(args.filename, args.versionlabel)
            # print(f"Bumping '{args.bump}' value from {v.field(args.bump)} ", end="")
            # v.bump(args.bump)
            # print(f"to {v.field(args.bump)} in '{args.filename}'")
            # Version.update(args.filename, v, args.versionlabel)
            # print(f"new version: {v}")
        else:
            print(f"{args.bump} is not a valid version field, choose one of {Version.FIELDS}")
            sys.exit(1)

    if args.update:
        print(f"Updating '{args.filename}' with version '{version}'")
        Version.update(filename=args.filename, version=version, lhs=args.label)


if __name__ == "__main__":
    main(sys.argv[1:])  # clip off the program name
