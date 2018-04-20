#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import subprocess
import os.path
import shutil
import logging

from distutils.spawn import find_executable
from doxygen.configParser import ConfigParser


class Generator:
    """
    This class is used to generate the doxygen documentation
    """

    def __init__(self, doxyfile, doxygen_path=None):
        """
        :param doxyfile: Path to the doxygen configuration file.
        :param doxygen_path: Path to the doxygen executable if doxygen is not in your path
        :raise FileNotFoundError: If the doxygen executable of the configuration file cannot be reached
        """

        if doxygen_path:
            if not os.path.exists(doxygen_path):
                logging.error("Impossible to access to {}".format(doxygen_path))
                raise FileNotFoundError(doxygen_path)
        else:
            doxygen_path = find_executable("doxygen")
            if doxygen_path is None:
                logging.error("doxygen executable was not found in your path.")
                raise FileNotFoundError("doxygen executable was not found in your path.")

        self.doxygen_path = doxygen_path

        if not os.path.exists(doxyfile):
            logging.error("Impossible to access to {}".format(doxyfile))
            raise FileNotFoundError(doxyfile)
        self.doxyfile = doxyfile

    def build(self, generate_zip=False, clean=True):
        """
        Build the documentation according to the configuration
        :param generate_zip: If set, will zip the generated documentation
        :param clean: If true, will delete the output folder of the documentation before build and after zip generation if executed. Be careful if you set output path to non empty folder
        :return: The path to the output documentation. Path to the zip archive if you generate the archive. None in case of failure
        """

        logging.debug("build the documentation from {}".format(self.doxyfile))

        configuration = ConfigParser().load_configuration(self.doxyfile)
        output_doc_folder = configuration['OUTPUT_DIRECTORY'] if 'OUTPUT_DIRECTORY' in configuration else os.path.dirname(self.doxyfile)
        if not os.path.isabs(output_doc_folder):
            output_doc_folder = os.path.join(os.path.dirname(self.doxyfile), output_doc_folder)
        logging.debug("Output documentation folder {}".format(output_doc_folder))

        if clean and os.path.exists(output_doc_folder):
            logging.debug('Clean {}'.format(output_doc_folder))
            shutil.rmtree(output_doc_folder)

        if not self.__build_doc():
            logging.error('An error was occurred during documentation generation. Please check the log')
            return None

        if not os.listdir(output_doc_folder):
            logging.error('Nothing generated in output folder: {}'.format(output_doc_folder))
            return None

        logging.debug("Build with success")

        if not generate_zip:
            logging.warning("Exclude zip generation")
            return output_doc_folder

        archive_name = configuration['PROJECT_NAME'] if len(configuration['PROJECT_NAME']) != 0 else "doc"
        output_zip_path = os.path.join(os.path.dirname(self.doxyfile), archive_name + ".zip")

        if not self.__compress_doc(output_doc_folder, output_zip_path):
            logging.error("Error during archive creation:Input folder: {}\nOutput zip path: {}".format(output_doc_folder, output_zip_path))
            return None

        if clean and os.path.exists(output_doc_folder):
            logging.debug("Clean {}".format(output_doc_folder))
            shutil.rmtree(output_doc_folder)

        logging.info("Archived with success")
        return output_zip_path

    def __build_doc(self):
        """
        Build the documentation
        :return: True if success else False
        """

        logging.debug('Run {} {}'.format(self.doxygen_path, self.doxyfile))

        log_file = os.path.join(os.path.dirname(self.doxyfile), "doxygen_build.log")
        logging.debug("Log file {}".format(log_file))

        doxygen_build = open(log_file, "w")
        result = subprocess.run([self.doxygen_path, self.doxyfile], stdout=doxygen_build, stderr=subprocess.STDOUT, cwd=os.path.dirname(self.doxyfile))
        doxygen_build.close()
        logging.debug('Return code : {}'.format(result.returncode))

        if result.returncode == 0:
            logging.debug("Clean log file {}".format(log_file))
            os.remove(log_file)

        return result.returncode == 0

    def __compress_doc(self, doc_folder: str, output_zip_path: str):
        """
        Compress the previously generated doc
        :param doc_folder: Folder which will be compressed
        :param output_zip_path: Path where archive will be created
        :return: True if success else False
        """

        logging.debug("Compress the documentation {}".format(doc_folder))

        if os.path.exists(output_zip_path):
            logging.debug('Delete {}'.format(output_zip_path))
            os.remove(output_zip_path)

        shutil.make_archive(os.path.splitext(output_zip_path)[0], 'zip', doc_folder)
        return os.path.exists(output_zip_path) and os.path.getsize(output_zip_path) > 0

