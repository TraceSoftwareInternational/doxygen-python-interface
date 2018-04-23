doxygen-python-interface
========================

|Build Status|

This library provide a way to update `Doxygen`_ configuration and launch
a build of documentation

Example
-------

.. code:: python


    from doxygen.configParser import ConfigParser
    from doxygen.generator import Generator


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

.. |Build Status| image:: https://travis-ci.org/TraceSoftwareInternational/doxygen-python-interface.svg?branch=master
   :target: https://travis-ci.org/TraceSoftwareInternational/doxygen-python-interface
