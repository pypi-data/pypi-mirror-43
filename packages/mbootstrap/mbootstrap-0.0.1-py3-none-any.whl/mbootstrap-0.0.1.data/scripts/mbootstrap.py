#!python
# -*- coding: utf-8 -*-

"""Mini bootstrap script."""

from __future__ import print_function

__version__ = "0.0.1"
__author__ = "Markus Hutzler"
__license__ = 'BSD-3'

import sys
import argparse
import os
import hashlib
import shutil
import tarfile
import logging
from pkg_resources import parse_version

import yaml
import git

# Fix some Python 2 / Python 3 compatibility issues.

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

srcipt_name = 'mbootstrap'
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(srcipt_name)


class ResourceException(Exception):
    """Resource exception raised when one of the resource tasks fails."""


class Resource(object):
    """Describe a common resource."""
    def __init__(self, name, info, base_dir):
        self.info = info
        self.name = name
        self.repo = None
        self.src = info.get("src")
        self.method = info.get("method")
        self.branch = info.get("branch")
        self.ref = info.get("ref")
        self.path = info.get("path")
        self.patches = info.get("patches", [])
        self.sha256sum = info.get("sha256sum", None)

        self.base_dir = base_dir

        staging_dir = os.path.join(base_dir, ".{}-staging".format(srcipt_name),
                                   self.path)
        self.staging_dir = os.path.realpath(staging_dir)

        install_dir = os.path.join(base_dir, self.path)
        self.install_dir = os.path.realpath(install_dir)

    def fetch(self):
        """Fetch the resource."""

    def patch(self):
        """Patch the source files."""

    def install(self, force=False):
        """Install or move sources to target location."""
        logger.info("[%s] Installing files.", self.name)
        sub = self.info.get("subdirectory-filter", "")
        src_dir = os.path.join(self.staging_dir, sub)

        if os.path.isdir(self.install_dir) and force:
            shutil.rmtree(self.install_dir, True)
        shutil.move(src_dir, self.install_dir)

    def post_validate(self):
        """Post validation. This function is called from within validation().
        """

    def validate(self, force=False):
        """Validate resource configuration."""
        if os.path.isdir(self.install_dir) and not force:
            raise ResourceException(
                "[%s] Target folder already exists." % self.name)
        if not self.install_dir.startswith(self.base_dir + os.sep):
            raise ResourceException(
                "[%s] Target folder outside of structure." % self.name)
        self.post_validate()


class GitRepo(Resource):
    """A Git resource."""
    def fetch(self):
        """Clone a git repository and checkout given reference."""
        logger.info("[%s] Cloning '%s'...", self.name, self.src)

        if self.branch:
            self.repo = git.Repo.clone_from(self.src, self.staging_dir,
                                            branch=self.branch,
                                            single_branch=True)
        else:
            self.repo = git.Repo.clone_from(self.src, self.staging_dir)

        if self.ref:
            self.repo.git.checkout(self.ref)
        logger.info("[%s] Using ref: %s", self.name, self.repo.head.commit)

    def patch(self):
        """Apply patches using Git."""
        for patch in self.patches:
            logger.info("[%s] Applying patch %s", self.name, patch)
            ppath = os.path.join(os.getcwd(),
                                 ".{}-patches".format(srcipt_name), patch)
            self.repo.git.apply(["-3", ppath])


class TarPackage(Resource):
    """A Tar package resource."""
    def fetch(self):
        """Download a tar file and check its hash."""
        logger.info("[%s] Downloading '%s'...", self.name, self.src)
        tmp = urlretrieve(self.src, filename=None)[0]

        if self.sha256sum:
            sha256 = hashlib.sha256()

            with open(tmp, 'rb') as tmp_fh:
                while True:
                    data = tmp_fh.read(1024 * 64)
                    if not data:
                        break
                    sha256.update(data)
            if sha256.hexdigest() == self.sha256sum:
                logger.debug("[%s] Hash check OK...", self.name)
            else:
                raise ResourceException(
                    "[%s] Hash check failed." % (self.name))

        tar = tarfile.open(tmp)
        members = tar.getmembers()
        for member in members:
            if member.name.startswith('/'):
                raise ResourceException(
                    "[%s] Absolute path in archive found." % (self.name))
            if "../" in member.name:
                raise ResourceException(
                    "[%s] Relative path in archive found." % (self.name))
        tar.extractall(self.staging_dir)

    def post_validate(self):
        """Validate content of tar package."""
        if self.branch:
            raise ResourceException(
                "[%s] Branches not supported for tar resources." % (self.name))

        if self.ref:
            raise ResourceException(
                "[%s] References not supported for tar resources." %
                (self.name))

        if self.patches:
            raise ResourceException(
                "[%s] Patching not supported for tar resources." % (self.name))

        if not self.sha256sum:
            logger.warning("[%s] no hash given for verification...", self.name)


class BootstrapException(Exception):
    """Bootstrap exception, used for stopping the bootstrap script."""


class Bootstrap(object):
    """The main bootstrap class used for processing all resources."""
    methods = {
        'git': GitRepo,
        'tar': TarPackage,
    }

    def __init__(self, args, base_dir=None):
        if not base_dir:
            base_dir = os.getcwd()
        self.base_dir = os.path.realpath(base_dir)

        staging_dir = os.path.join(self.base_dir,
                                   ".{}-staging".format(srcipt_name))
        self.staging_dir = os.path.realpath(staging_dir)
        self.resources = []
        self.config = None
        self.args = args

    def read_config(self):
        """Read and validate configuration file."""
        config_files = [
            ".{}.yaml".format(srcipt_name),
            "{}.yaml".format(srcipt_name),
            "mbs.yaml",
            ".mbs.yaml"
        ]
        config_file = None
        for c_file in config_files:
            if os.path.isfile(c_file):
                config_file = c_file
                break
        if not config_file:
            raise FileNotFoundError

        self.config = yaml.load(open(config_file), Loader=Loader)

        requered_version = self.config.get("required_version")
        if requered_version and \
           parse_version(__version__) < parse_version(requered_version):
            logger.error("Required version %s < mbootstrap %s.",
                         requered_version, __version__)
            raise BootstrapException('validate')

    def validate(self):
        """Validate resources and target folders."""
        error = False
        for info in self.config.get("resources"):
            name = info.get("name")
            if not name:
                logger.error("Found resource without name.")
                error = True
                continue

            if self.args.resources and name not in self.args.resources:
                continue

            method = info.get('method', '')
            if method not in self.methods.keys():
                logger.error("[%s] Unknown method '%s'.", name, method)
                error = True
            res = self.methods.get(method, Resource)(name, info, self.base_dir)
            self.resources.append(res)

        for res in self.resources:
            try:
                res.validate(self.args.force)
            except ResourceException as err:
                logger.error(str(err))
                error = True

        if not self.resources:
            logger.warning("No matching resources found.")

        if error:
            raise BootstrapException('validate')

    def fetch(self):
        """Fetch all resources."""
        error = False
        for res in self.resources:
            try:
                res.fetch()
            except ResourceException as error:
                logger.error(str(error))
                error = True

        if error:
            raise BootstrapException('fetch')

    def patch(self):
        """Apply patches to all resources."""
        error = False
        for res in self.resources:
            try:
                res.patch()
            except ResourceException as error:
                logger.error(str(error))
                error = True

        if error:
            raise BootstrapException('patch')

    def install(self):
        """Install all resources."""
        error = False
        for res in self.resources:
            try:
                res.install(force=self.args.force)
            except ResourceException as error:
                logger.error(str(error))
                error = True

        if error:
            raise BootstrapException('install')


def parse_cli():
    """Parse command line for options."""
    parser = argparse.ArgumentParser(description='mini bootstrap script')
    parser.add_argument('resources', metavar='RES', type=str, nargs='*',
                        help='subset of resources')
    parser.add_argument('--force', dest='force', action='store_true',
                        help='overwrite target locations')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                       help='verbose logging, increase output to debug level')
    group.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                       help='quiet logging, reduce output to error level')
    parser.add_argument('--version', action='store_true', dest='version',
                        help='print version and exit')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.quiet:
        logger.setLevel(logging.ERROR)

    if args.version:
        print("{} version {}".format(srcipt_name, __version__))
        if args.verbose:
            print("Python {0}.{1}.{2}".format(sys.version_info.major,
                                              sys.version_info.minor,
                                              sys.version_info.micro))
        exit(0)
    return args


def main():
    args = parse_cli()
    base_dir = os.getcwd()
    staging_dir = os.path.join(base_dir, ".{}-staging".format(srcipt_name))

    # Prepare staging area
    shutil.rmtree(staging_dir, True)
    os.makedirs(staging_dir)

    strap = Bootstrap(args=args)

    logger.debug("Validating configuration...")
    try:
        strap.read_config()
        strap.validate()
    except FileNotFoundError:
        logger.error("Can not find configuration file.")
        exit(1)
    except BootstrapException:
        logger.error("Validation failed.")
        exit(1)
    except yaml.scanner.ScannerError as error:
        if error.problem.startswith("found character '\\t'"):
            mark = "{}:{}".format(error.problem_mark.line + 1,
                                  error.problem_mark.column + 1)
            logger.error(
                "Validation failed, no TABs in config file allowed. (%s)",
                mark)
        exit(1)

    logger.debug("Fetching sources...")
    try:
        strap.fetch()
    except BootstrapException:
        logger.error("Fetch failed.")
        exit(1)

    logger.debug("Patching sources...")
    try:
        strap.patch()
    except BootstrapException:
        logger.error("Patching failed.")
        exit(1)

    logger.debug("Installing resources...")
    try:
        strap.install()
    except BootstrapException:
        logger.error("Installation failed.")
        exit(1)

    # Clean staging area
    shutil.rmtree(staging_dir, True)


if __name__ == "__main__":
    main()
