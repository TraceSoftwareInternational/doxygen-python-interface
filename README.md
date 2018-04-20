# doxygen-python-interface

This library provide a way to update [Doxygen](http://www.stack.nl/~dimitri/doxygen/) configuration and launch a build of documentation

## Example

```python

from doxygen.configParser import ConfigParser
from doxygen.generator import Generator


my_doxyfile_path = "path/to/my/Doxyfile"

# 1. Load the configuration from your Doxyfile
config_parser = ConfigParser()
configuration = config_parser.load_configuration(my_doxyfile_path)

# 2. Update the configuration 
configuration['PROJECT_NUMBER'] = '1.2.3.4'
configuration['BRIEF_MEMBER_DESC'] = 'NO'

# 3. Store the configure
config_parser.store_configuration(configuration, my_doxyfile_path)

# 4. Build the doc and generate a zip
doxy_builder =Generator(my_doxyfile_path)
output_zip_archive = doxy_builder.build(clean=True, generate_zip=True)

```