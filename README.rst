doxygen-python-interface
========================

|BuildStatus| |PyPILastVersion| |License| |Docs|

This library provide a way to update `Doxygen`_ configuration and launch
a build of documentation

Example
-------

.. code:: python


    from doxygen import ConfigParser
    from doxygen import Generator


    my_doxyfile_path = "path/to/my/Doxyfile"

    # 1. Load the configuration from your Doxyfile
    config_parser = ConfigParser()
    configuration = config_parser.load_configuration(my_doxyfile_path)

    # 2. Update the configuration
    configuration['PROJECT_NUMBER'] = '1.2.3.4'
    configuration['BRIEF_MEMBER_DESC'] = 'NO'
    configuration['FILE_PATTERNS'].append('*.abc')

    # 3. Store the configure
    config_parser.store_configuration(configuration, my_doxyfile_path)

    # 4. Build the doc and generate a zip
    doxy_builder = Generator(my_doxyfile_path)
    output_zip_archive = doxy_builder.build(clean=True, generate_zip=True)

.. _Doxygen: http://www.stack.nl/~dimitri/doxygen/

.. |BuildStatus| image:: https://travis-ci.org/TraceSoftwareInternational/doxygen-python-interface.svg?branch=master
    :target: https://travis-ci.org/TraceSoftwareInternational/doxygen-python-interface

.. |PyPILastVersion| image:: https://badge.fury.io/py/doxygen-interface.svg
    :target: https://badge.fury.io/py/doxygen-interface

.. |License| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/gpl-3.0

.. |Docs| image:: https://img.shields.io/badge/Docs-HostMyDocs-green.svg
    :target: https://docs.trace-software.com
