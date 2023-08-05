#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
from datetime import datetime, timedelta
from os import path, listdir, makedirs, remove
from subprocess import Popen
from zipfile import ZipFile
from shutil import rmtree


def _get_all_file_paths(directory):
    """ Get a list that preserves the files that will form the backup.

        :param directory: Path where all backup files are located.
        :type directory: str
        :return: List of files path
        :rtype: list
    """
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


class PyMongoBackup(object):

    def __init__(self, username=None, password=None, host='localhost', days_backup=None, path_backup='BackupMongo',
                 log=False, path_log=os.path.join('BackupMongo', 'log'), datetime_format='%Y-%m-%d_%H-%M',
                 prefix='back_'):

        """Main class to create the object with the configurations to create the MongoDB backups.

        :param username: Username for login MongoDB. Default None.
        :type username:
        :param password: Password for login MongoDB. Default None.
        :type password: str
        :param host: IP address of the MongoDB server. Default localhost.
        :type host: str
        :param days_backup: Maximum days that are saved backup. Default None (always save).
        :type days_backup: int
        :param path_backup: Path where the backup is saved. Default ./BackupMongo.
        :type path_backup: str
        :param log: Indicates if the output is written to a log file. Default False.
        :type log: bool
        :param path_log: Path where the log is saved. Default ./BackupMongo/log.
        :type path_log str
        :param prefix: Indicates the prefix with which the backup will be saved. Default back_.
        :type prefix: str
        :param datetime_format: Indicates the date format to name the backup. Default %Y-%m-%d_%H-%M.
        :type datetime_format: str

        Note: Example file back_2019-03-09_12-21.zip

        """
        self.username = username
        self.password = password
        self.host = host
        self.days_backup = days_backup
        self.path_backup = path_backup
        self.log = log
        self.path_log = path_log
        self.datetime_format = datetime_format
        self.prefix = prefix
        self.date_start = self._get_time()
        self.backup_name = "{0}{1}".format(self.prefix, self.date_start)
        self.absolute_path = os.path.join(self.path_backup, self.backup_name)

        self.logger = logging.getLogger("PyMongoBackup")
        self.logger.setLevel('DEBUG')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Log in file
        if self.log:
            if not path.exists(self.path_log):
                try:
                    makedirs(self.path_log)
                    print("Created: {0}".format(self.path_log))

                except PermissionError as pe:
                    print("Error: {0}".format(pe))

            log_name = "PyMongoBackup_{0}.log".format(self.date_start)
            fh = logging.FileHandler(os.path.join(self.path_log, log_name))
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        # Log in terminal
        ch = logging.StreamHandler()
        ch.setLevel('DEBUG')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def _get_time(self):
        """Get date start.

            :return: Returns current date
            :rtype: datetime
        """
        date_now = datetime.now().strftime(self.datetime_format)

        return date_now

    def _create_dir(self, pth):
        """ Check if a directory exists and if it does not exist, create it.

            :param pth: Path of directory.
            :type pth: str
        """
        if not path.exists(pth):
            try:
                makedirs(pth)
                self.logger.info("Created: {0}".format(pth))

            except PermissionError as pe:
                self.logger.error("Error: {0}".format(pe))
                sys.exit(1)

    def _get_file_date(self, pth):
        """ Returns the date of creation of a file

            :param pth: Full path of the file
            :type pth: str
            :return: Timestamp creation file. Error 0
            :rtype: int
        """
        try:
            return os.stat(pth).st_ctime

        except Exception as e:
            self.logger.error('Error get date: {0} {1}'.format(pth, e))
            return 0

    def _clean_path(self, pth, prf):
        """ Delete old backups (Zip and logs).

            :param pth: Path for clean
            :type pth: str
            :param prf: Prefix of file to delete.
            :type prf: str
        """
        self.logger.info("Clean path: {0}".format(pth))
        for file_name in listdir(pth):

            if re.search(prf, file_name):
                full_path = os.path.join(pth, file_name)
                date_file = self._get_file_date(full_path)

                date_threshold = (datetime.now() - timedelta(days=self.days_backup)).timestamp()

                if date_threshold > date_file:
                    self.logger.info('Delete: {0}'.format(file_name))
                    try:
                        remove(full_path)

                    except Exception as eremove:
                        self.logger.error("Error deleted: {0} {1}".format(file_name, eremove))

    def _clean_old_files(self):
        """ check if backup cleanup is enabled and execute it. """
        if self.days_backup is None:
            self.logger.info('Clean backup files: disabled')
        else:
            self.logger.info('Clean backup files > {0} days'.format(self.days_backup))

            self._clean_path(self.path_backup, self.prefix)
            self._clean_path(self.path_log, 'PyMongoBackup_')

    def _create_zip(self, directory):
        """ Create zip with all the files that make up the backup.

            :param directory: Path where the zip file is saved.
            :type directory: str
        """
        self.logger.info('Create zip: {0}'.format(directory))
        try:
            file_paths = _get_all_file_paths(directory)

            with ZipFile(directory + '.zip', 'w') as zip_file:
                for file in file_paths:
                    zip_file.write(file)

        except Exception as ezip:
            self.logger.info('Error create zip: {0} {1}'.format(directory, ezip))

    def _delete_dir(self, pth):
        """ Delete directory.

            :param pth: Path of directory to delete.
            :type pth: str
        """
        self.logger.info('Delete dir: {0}'.format(pth))
        try:
            rmtree(pth)
        except Exception as edd:
            self.logger.error('Error delete dir: {0} {1}'.format(pth, edd))

    def _exec_command(self, cmd):
        """ Execute the command that starts the mongodb backup.

            :param cmd: List with the values ​​of the command.
            :type cmd: list
        """
        self.logger.info(cmd)
        try:
            proc = Popen(cmd)
            (out, err) = proc.communicate()

            if proc.returncode != 0:
                self.logger.error("Error on backup: {0}".format(err))

            elif proc.returncode == 0:
                self.logger.info("Create backup: OK")

        except Exception as ecmd:
            self.logger.error("Error executed command: {0}".format(ecmd))
            self.logger.error("Please check that you have installed 'mongodb' or 'mongodb-org-tools'.")

    def create_full_backup(self):
        """ Create backup of all databases. """
        self._create_dir(self.absolute_path)
        command = ['mongodump', '--host', self.host]

        if self.username is not None:
            command.append('--username')
            command.append(self.username)

        if self.password is not None:
            command.append('--password')
            command.append(self.password)

        command.append('--out')
        command.append(self.absolute_path)

        self._exec_command(command)
        self._create_zip(self.absolute_path)
        self._delete_dir(self.absolute_path)
        self._clean_old_files()

    def create_backup(self, db):
        """ Create backup of a database in particular.

            :param db: Name of database.
            :type db: str
        """
        self._create_dir(self.absolute_path)
        self.logger.info("Create backup: {0}".format(db))
        command = ['mongodump', '--host', self.host]

        if self.username is not None:
            command.append('--username')
            command.append(self.username)

        if self.password is not None:
            command.append('--password')
            command.append(self.password)

        command.append('--out')
        command.append(self.absolute_path)

        command.append('--db')
        command.append(db)

        self._exec_command(command)
        self._create_zip(self.absolute_path)
        self._delete_dir(self.absolute_path)
        self._clean_old_files()

    def create_multidb_backup(self, dbs):
        """ Create backup of several databases.

            :param dbs: List of databases.
            :type dbs: list
        """
        self._create_dir(self.absolute_path)

        for db in dbs:
            self.logger.info("Create backup: {0}".format(db))
            command = ['mongodump', '--host', self.host]

            if self.username is not None:
                command.append('--username')
                command.append(self.username)

            if self.password is not None:
                command.append('--password')
                command.append(self.password)

            command.append('--out')
            command.append(self.absolute_path)

            command.append('--db')
            command.append(db)

            self._exec_command(command)

        self._create_zip(self.absolute_path)
        self._delete_dir(self.absolute_path)
        self._clean_old_files()
