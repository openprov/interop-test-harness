# Interoperability test harness design and implementation

Mike Jackson, The Software Sustainability Institute / EPCC, The University of Edinburgh based on requirements from Trung Dong Huynh, Electronics and Computer Science, University of Southampton.

## Motivation

The motivation behind the interoperability test harness is to provide a test infrastructure which systematically checks convertibility and round-trip conversions across combinations of Provenance Tool Suite packages and services operating collectively. This includes testing of:

* Round-trip interoperability between ProvPy and ProvToolbox.
* Round-trip interoperability between ProvPy and ProvToolbox and deployed ProvStore and ProvTranslator services whether these be deployed locally (on a developer's own machine) or remotely.
* Command-line utilities that are provided within ProvToolbox (e.g. `provconvert`) and ProvPy (e.g. `prov-convert`).

The round-trip interoperability tests are intended to make sure that Provenance Tool Suite tools and services support all PROV representations and maintain their semantics across all supported PROV representations.

---

## Format

In what follows, all modules are relative to `prov_interop`.

---

## Key concepts

### Test cases

A single *test case* consists of a set of files, where each file holds a document in one of the PROV representations:

| Representation  | Extension     |
| --------------- | ------------- |
| PROV-N          | .provn        |
| PROV-O (Turtle) | .ttl          |
| PROV-O (TriG)   | .trig         |
| PROV-XML        | .provx        |
| PROV-JSON       | .json         |

For example, a test case whose name is `testcase1` consists a set of files with extensions `.provn`, `.xml`, `.json`, `.ttl`, and `.trig`. Each document within a single test case is semantically equivalent to the others within the same test case.

Some test cases only have files for a subset of representations, as there are cases that cannot be validly encoded in a particular representation (e.g. PROV-XML). If a file for a specific representation is absent, then it can be assumed that conversions to and from that representation do not need to be tested for that test case. For example, the absence of `testcase1.xml` means that conversions to from `testcase1.ttl` to PROV-XML do not need to be tested.

The test cases are curated manually and published in a Github repository, [testcases](https://github.com/prov-suite/testcases). They are maintained as a community resource.

The test harness assumes that:

* Test directories are named `testcaseNNNN` (e.g. `testcase1`, `testcase2`, `testcase2015` etc).
* Test case files are named `NAME.[provx | provn | json | ttl | trig]` (e.g. `testcase.json`, `primer.ttl`, `example.provn` etc).

### Converters

*Converters* convert, or transform, PROV documents from one format into another. Converters are the components that are tested by the test harness.

Example converters include:

* ProvPy's `prov-convert` script.
* ProvToolbox's `provconvert` script.
* ProvTranslator service.
* ProvStore service.

### Comparators

*Comparators* compare PROV documents to see if they are semantically equivalent. Comparators, in conjunction with test cases, are used to validate converters. Example comparators include:

* ProvPy's `prov-compare` script.

Comparators do not need to understand PROV concepts. A PROV-agnostic comparator that compares XML, Turtle, Trig or JSON documents can be used.

Comparators are deemed to be both authoritative and correct. They may need test cases of their own in future, but this is out of scope at this time.

### Test procedure

The procedure for testing a converter using a test case and a comparator is as follows:
 
* A converter translates `testcaseNNNN/file.<ext_in>` to `converted.<ext_out>`.
* A comparator compares `testcaseNNNN/file.<ext_out>` to `converted.<ext_out>` for equivalence, which results in either success or failure.

---

## `standards` - W3C PROV formats

This module defines canonical names for each of the PROV formats:

```
PROVN = "provn"
TTL = "ttl"
TRIG = "trig"
PROVX = "provx"
JSON = "json"
```

and a list of these:

```
FORMATS = [PROVN, TTL, TRIG, PROVX, JSON]
```

These correspond to the supported extensions of test case files. 

Classes that manage the invocation of specific components are responsible for mapping file extensions to those supported by those components where applicable (e.g. command-line flags, HTTP content-types etc).

---

## `component` - configurable components

Converters and comparators are invoked via Python classes. These have a common base class representing a configurable component:

```
class ConfigurableComponent(object)
```

A component is configured using a Python dictionary which is assumed to hold component-specific configuration:

```
def configure(self, config)
```

Any configuration not specific to a component is ignored. If any problems arise (e.g. there are missing or invalid configuration values) then an error is raised:

```
class ConfigError(Exception)
```

The test harness assumes that both converters and comparators are either executable from the command-line (for scripts or executable programs) or via REST operations (for services).

### Command-line components

Command-line components are represented by:

```
class CommandLineComponent(ConfigurableComponent)
```

The configuration must hold:

* `executable`: the name of the executable. This may be a single executable file name or an executable name and a script name. Executables may be prefixed with their absolute path depending on whether or not they are on the system path.
* `arguments`: arguments for the executable.

Valid configurations include:

```
{
  "executable": "/home/user/ProvToolbox/bin/provconvert",
  "arguments": "-infile INPUT -outfile OUTPUT"
}
{
  "executable": "prov-convert",
  "arguments": "-f FORMAT INPUT OUTPUT"
}
{
  "executable": "python /home/user/ProvPy/scripts/prov-convert",
  "arguments": "-f FORMAT INPUT OUTPUT"
}
```

Both values may include tokens that can be replaced at run time with actual values. This is the responsibility of sub-classes. For example, `INPUT` and `OUTPUT` would be replaced with input and output file names.

### RESTful components

RESTful components are represented by the class:

```
class RestComponent(ConfigurableComponent)
```

The configuration must hold:

* `url`: REST endpoint for POST requests.

A valid configuration is:

```        
{
  "url": "https://provenance.ecs.soton.ac.uk/validator/provapi/documents/"
}
```

---

## `converter` - invoking converters

Converters are represented by sub-classes of:

```
class Converter(ConfigurableComponent)
```

The configuration must hold:

* `input-formats`: input formats supported by the converter, each of which must be one of those in `standards.FORMATS`.
* `output-formats`: output formats supported by the converter, each of which must be one of those in `standards.FORMATS`.

A valid configuration is:

```
{
  "input-formats": ["json"], 
  "output-formats": ["provn", "provx", "json"]
}
```

Conversions are invoked via:

```
def convert(self, in_file, out_file)
```

`in_file` holds the document to be converted. If the conversion is successful then `out_file` holds the converted document. The file extensions of `in_file` and `out_file` must each be one of those in `standards.FORMATS`.

If any problems arise, for example `in_file` cannot be found, then an exception is raised:

```
class ConversionError(Exception)
```

Command-line converters, invoked by sub-classes, need to exit with a non-zero exit code in case of problems and/or not write an output file, so that conversion failures can be detected.

### `provpy.converter` - invoking ProvPy `prov-convert`

Invocation of ProvPy's `prov-convert` script is managed by:

```
class ProvPyConverter(Converter, CommandLineComponent)
```

The configuration must hold:

* `Converter` configuration
* `CommandLineComponent` configuration

`arguments` must have tokens `FORMAT`, `INPUT`, `OUTPUT`, which are place-holders for the output format, input file and output file.

A valid configuration is:

```
{
  "executable": "prov-convert"
  "arguments": "-f FORMAT INPUT OUTPUT"
  "input-formats": ["json"]
  "output-formats": ["provn", "provx", "json"]
}
```

`convert` behaves as follows:

* Input and output formats are derived from `in_file` and `out_file` file extensions.
* A check is done to see that `in_file` exists and that the input and output format are in `input-formats` and `output-formats` respectively.
* `executable` and `arguments` are used to create a command-line invocation, with `FORMAT`, `INPUT` and `OUTPUT` being replaced with the output format, `in_file`, and `out_file`
  - If the output format is `provx` then `xml` is used as `FORMAT` (as `prov-convert` does not recognise `provx`).
  - An example command-line invocation is:

```
prov-convert -f xml testcase1.json testcase1.provx
```

* A check is done to see that `out_file` exists.
* A `ConversionError` is raised if any problems arise or the exit code is non-zero.

`prov-convert` returns an exit code of 2 if there is no input file, the input file is not a valid PROV document or the output format is not supported. For these last two situations, it will create an empty output file. As a result, its exit code can be used to check for conversion failures.

### `provtoolbox.converter` - invoking ProvToolbox `provconvert`

Invocation of ProvToolbox's `provconvert` script is managed by:

```
class ProvToolboxConverter(Converter, CommandLineComponent)
```

The configuration must hold:

* `Converter` configuration
* `CommandLineComponent` configuration

`arguments` must have tokens `INPUT` and `OUTPUT`, which are place-holders for the input file and output file.

A valid configuration is:

```
{
  "executable": "/home/user/ProvToolbox/bin/provconvert"
  "arguments": "-infile INPUT -outfile OUTPUT"
  "input-formats": ["provn", "ttl", "trig", "provx", "json"]
  "output-formats": ["provn", "ttl", "trig", "provx", "json"]
}
```

`convert` behaves as follows:

* Input and output formats are derived from `in_file` and `out_file` file extensions.
* A check is done to see that `in_file` exists and that the input and output format are in `input-formats` and `output-formats` respectively.
* `executable` and `arguments` are used to create a command-line invocation, with `INPUT` and `OUTPUT` being replaced with `in_file`, and `out_file`
  - An example command-line invocation is:

```
/home/user/ProvToolbox/bin/provconvert -infile testcase1.json -outfile testcase1.provx
```

* A check is done to see that `out_file` exists.
* A `ConversionError` is raised if any problems arise or the exit code is non-zero.

`provconvert` returns an exit code of 1 if there is no input file, the input file is not a valid PROV document or the input file format is not supported. It returns an exit code of 0 if successful or, problematically, if the output file format is not supported. However, as it does not create any output files if any file or file format is invalid, the non-existence of an output file can be used to check for conversion failures.

### `provstore.converter` - invoking ProvStore

Invocation of the ProvStore service is managed by:

```
class ProvStoreConverter(Converter, RestComponent)
```

The configuration must hold:

* `Converter` configuration
* `RestComponent` configuration
* `authorization`: value for `Authorization` HTTP header. For ProvStore, this is of form `ApiKey USER:APIKEY` where `USER` is a ProvStore user name, and `APIKEY` is the user's ProvStore API key.

A valid configuration is:

```
{
  "url": "https://provenance.ecs.soton.ac.uk/store/api/v0/documents/"
  "authorization": "ApiKey user:12345qwerty"
  "input-formats": ["provn", "ttl", "trig", "provx", "json"]
  "output-formats": ["provn", "ttl", "trig", "provx", "json"]
}
```

`convert` behaves as follows:

* Input and output formats are derived from `in_file` and `out_file` file extensions.
* A check is done to see that `in_file` exists and that the input and output format are in `input-formats` and `output-formats` respectively.
* The input and output formats and `authorization` are used to set HTTP `Content-type`, `Accept` and `Authorization` header values, respectively. 
* For `Content-type` and `Accept`, the class stores mappings from `standards.FORMATS` values to these e.g. `standards.PROVX` maps to `application/xml`.
* The contents of `in_file` are loaded and used to create a ProvStore compliant HTTP POST request which is submitted to `url`, to store the document.
* The HTTP status is checked to be 201 CREATED.
* The HTTP response is parsed to get the URL of the newly-stored document.
* The output format is used to set the HTTP `Accept` header value.
* An HTTP GET request is submitted to the URL of the new document to get it in the desired output format.
* The HTTP status is checked to to be 200 OK.
* The HTTP response is parsed to get the converted document, and this is saved to `out_file`.
* An HTTP DELETE request is submitted to the URL of the newly-stored document to remove it.
* The HTTP status is checked to to be 204 NO CONTENT.
* A `ConversionError` is raised if any problems arise.

### `provtranslator.converter` - invoking ProvTranslator

Invocation of the ProvTranslator service is managed by:

```
class ProvTranslatorConverter(Converter, RestComponent)
```

The configuration must hold:

* `Converter` configuration
* `RestComponent` configuration

A valid configuration is:

```
{
  "url": "https://provenance.ecs.soton.ac.uk/validator/provapi/documents/"
  "input-formats": ["provn", "ttl", "trig", "provx", "json"]
  "output-formats": ["provn", "ttl", "trig", "provx", "json"]
}
```

`convert` behaves as follows:

* Input and output formats are derived from `in_file` and `out_file` file extensions.
* A check is done to see that `in_file` exists and that the input and output format are in `input-formats` and `output-formats` respectively.
* The input and output formats are used to set HTTP `Content-type` and `Accept` header values, respectively. 
* For `Content-type` and `Accept`, the class stores mappings from `standards.FORMATS` values to these e.g. `standards.PROVX` maps to `application/provenance+xml`.
* The contents of `in_file` are loaded and used to create a ProvTranslator-compliant HTTP POST request which is submitted to `url`, to convert the document.
* The HTTP status is checked to to be 200 OK.
* The HTTP response is parsed to get the converted document, and this is saved to `out_file`.
* A `ConversionError` is raised if any problems arise.

---

## `comparators` - invoking comparators

Comparators are represented by sub-classes of:

```
class Comparator(ConfigurableComponent)
```

The configuration must hold:

* formats`: formats supported by the comparator, each of which must be one of those in `standards.FORMATS`.

A valid configuration is:

```
{
  "formats": ["provx", "json"]
}
```

Comparisons are invoked via:

```
def compare(self, file1, file2)
```

`file1` and `file` hold the documents to be compared.  The file extensions of `file1` and `file2` must each be one of those in `standards.FORMATS`. If the documents are semantically equivalent then `True` is returned, else `False` is returned. 

If any problems arise, for example `file1` or `file2` cannot be found, then an exception is raised:

```
class ComparisonError(Exception)
```

Command-line comparators, invoked by sub-cclasses, need to exit with a non-zero exit code in case of a non-equivalent pair of files being given, or another error arising (e.g. no such file). The error code for a non-equivalent pair should differ from that for other errors (e.g. a missing input file).

### `provpy.comparator` - invoking ProvPy `prov-compare`

Invocation of ProvPy's `prov-compare` script is managed by:

```
class ProvPyComparator(Comparator, CommandLineComponent)
```

The configuration must hold:

* `Comparator` configuration
* `CommandLineComponent` configuration

`arguments` must have tokens `FORMAT1`, `FORMAT2`, `FILE1`, `FILE2`, which are place-holders for the the files and their formats.

A valid configuration is:

```
{
  "executable": "prov-compare"
  "arguments": "-f FORMAT1 -F FORMAT2 FILE1 FILE2"
  "formats": ["provx", "json"]
}
```

`compare` behaves as follows:

* File formats are derived from `file1` and `file1` file extensions.
* A check is done to see that `file1` and `file2` exist and that their formats are in `formats`.
* `executable` and `arguments` are used to create a command-line invocation, with `FORMAT1`, `FORMAT2`, `FILE1` and `FILE2` being replaced with the file formats, `in_file`, and `out_file`
  - If either format is `provx` then `xml` is used (as `prov-compare` does not recognise `provx`).
  - An example command-line invocation is:

```
prov-compare -f xml -F xml testcase1.provx converted.provx
```

* A `ComparisonError` is raised if any problems arise or the exit code is non-zero.

---

## `harness` - managing test harness configuration

A component is used to manage test harness configuration including the test cases:

```
class HarnessResources(ConfigurableComponent)
```

The configuration must hold:

* `test-cases`: location of test cases directory.
* `comparators`: a list of comparator configurations keyed by name. Each configuration consists of:
  - `class`: name of class that manages invocations of that comparator.
  - Configuration values required by the value of `class`.

A valid configuration is:

```
{
  "test-cases": "/home/user/test-cases",
  "comparators": 
  {
    "ProvPyComparator": 
    {
      "class": "prov_interop.provpy.comparator.ProvPyComparator",
      "executable": "prov-compare",
      "arguments": "-f FORMAT1 -F FORMAT2 FILE1 FILE2",
      "formats": ["provx", "json"],
    }
  }
}
```

When configured, this class invokes methods to populate data structures needed to run interoperability tests using the test cases.

```
def register_comparators(self, comparators)
```

This method populates `comparators`, a dictionary of comparator objects, keyed by comparator name. These are created using the `comparators` part of the configuration. The `class` determines the comparator object to create and the associated configuration is used to configure it - this uses dynamic object creation (see the `factory` module below). Using the above configuration there would be a mapping from `ProvPyComparator` to an instance of `prov_interop.provpy.comparator.ProvPyComparator`.

It also populates `format_comparators`, a dictionary of comparator instances, keyed by formats in `standards.FORMATS`. Using the above configuration there would be mappings from both `provx` and `json` to an instance of `prov_interop.provpy.comparator.ProvPyComparator`.

If no comparators are defined, or there are any problems creating their instances or configuring the comparators then a `ConfigError` is raised.

```
def register_test_cases(self, test_cases_dir, format_filter)
```

This method populates `test_cases`, a list of test cases, each of which is a tuple of form:

```
(test case index, format1, file1, format2, file2)
```

where `file1` and `file2` have extension `format1` and `format2` respectively and both `format1` and `format2` are in `standards.FORMATS`.

For example

```
(1, "json", "/home/user/test-cases/testcase1.json", 
    "provx", "/home/user/test-cases/testcase1.provx")
(1, "trig", "/home/user/test-cases/testcase1.trig", 
    "provx", "/home/user/test-cases/testcase1.provx")
```

The method traverses the directory named in `test-cases`, looking for sub-directories whose name matches the pattern `testcase[0-9][0-9]*`. For each directory, it filters its files to get only those which have an extension in both `standards.FORMATS` and `format_filter`, a subset of `standards.FORMATS` (a list of the formats for which a comparator has been registered). From the files left it calculates all possible combinations of pairs of files and creates tuples as above. So, if `/home/user/test-cases` contained:

```
testcase1/
  README.md
  testcase1.json
  testcase1.provn
  testcase1.provx
  testcase1.trig
  testcase1.ttl
testcase3/
  README.md
  primer.json
  primer.provn
  primer.trig
  primer.ttl
example/
  example.json
```

this, together with the configuration, would give the test case tuples:

```
[
  (1, json, /home/user/test-cases/testcase1.json
      json, /home/user/test-cases/testcase1.json),
  (1, json, /home/user/test-cases/testcase1.json
      provx, /home/user/test-cases/testcase1.provx),
  (1, provx, /home/user/test-cases/testcase1.provx
      json, /home/user/test-cases/testcase1.json),
  (1, provx, /home/user/test-cases/testcase1.provx
      provx, /home/user/test-cases/testcase1.provx),
  (3, json, /home/user/test-cases/primer.json
      json, /home/user/test-cases/primer.json)
]
```

There are tuples only for `json` and `provx`, as those are the only formats for which a comparator has been specified.

If the directory defined in `test-cases` cannot be found then a `ConfigError` is raised.

---

## `interop_tests.harness` - bootstrapping the test harness

This module bootstraps the test harness. As soon as this module is loaded, it invokes its own function:

```
def initialise_harness_from_file(file_name = None)
```

This function creates an instance of `harness.HarnessResources` and then configures it using configuration loaded from a [YAML](http://yaml.org/) file (using `factory.load_yaml`). The file loaded is:

* `file_name` if this argument is provided (when called from within this module itself, no value is provided).
* Else, the file named in an environment variable with name `PROV_HARNESS_CONFIGURATION`, if such an environment variable has been defined.
* Else, `localconfig/harness.yaml`.

The function will not reinitialise the `harness.HarnessResources` instance once it has been created and initialised.

The test harness needs to be bootstrapped as soon as the module is loaded to allow the use of dynamic test method generation from the test cases, as described below.

A valid YAML configuration file, which, when loaded, yields a Python dictionary holding the configuration required by `harness.HarnessResources` is:

```
---
test-cases: /home/user/test-cases
comparators:
  ProvPyComparator: 
    class: prov_interop.provpy.comparator.ProvPyComparator
    executable: prov-compare
    arguments: -f FORMAT1 -F FORMAT2 FILE1 FILE2
    formats: [provx, json]
```

---

## `interop_tests.test_converter` - interoperability test procedure

This module provides a generic test class to represent the test procedure. This class is sub-classed by test classes for each converter.

```
class ConverterTestCase(unittest.TestCase)
```

There are 5 PROV representations giving a possible 120 (ext_in, ext_out) pairs per test cases. If there are N test cases, that implies there are 120*N possible tests that could be run for each of the 4 converters. Providing a test method for each of these tests is unscalable.

However, using a single test method that iterates across all the test cases is also problematic. Running this under an xUnit test framework would result in a report that only 1 test has been run for a converter, corresponding to this single test method (regardless of the number of conversions done and validated). For example, for Python the output, using [nose](https://nose.readthedocs.org/en/latest/):

```
$ nosetests
.
----------------------------------------------------------------------
Ran 1 test in 1.000s

OK
```

It is important to know all the cases that fail, and for which pair(s) of representations. This knowledge may provide clues as to what the issue is. In addition, it should not desirable that a failure of one test case prevents the rest from running, since the test cases can be viewed as independent.

To address these requirements, generic test method is provided and [nose_parameterized](https://pypi.python.org/pypi/nose-parameterized/), in conjunction with the test case tuples cached in `harness.HarnessResources`, is used to dynamically create test methods for each test case tuple. 

The generic test method is defined as:

```
@parameterized.expand(harness.harness_resources.test_cases,
                      testcase_func_name=test_case_name)
def test_case(self, index, ext_in, file_ext_in, ext_out, file_ext_out):
```

When run, `nose_parameterized` will iterate through each of the test cases and create corresponding test methods:

```
test_case_1_json_json
test_case_1_provx_json
test_case_1_json_provx
test_case_1_provx_provx
...
```

The arguments passed into each test method, `(index, ext_in, file_ext_in, ext_out, file_ext_out)` are those from the tuple that was used to create that method. 

This module imports `interop_tests.harness` thereby bootstrapping the test harness. This bootstrapping is necessary so that the list of tuples is available to `nose_parameterized` when it dynamically creates the test methods.

The argument `testcase_func_name=test_case_name` is a `nose_parameterized` callback to another method in this module:

```
def test_case_name(testcase_func, param_num, param)
```

This overrides the default method names created by `nose_parameterized`, defining method names of form `test_case_<index>_<ext_in>_<ext_out>`).

The generic test method implements the test procedure with a couple of additiona actions:

* If the test case index is in the `skip-tests` for the converter then the test is skipped, by raising `nose.plugins.skip.SkipTest`.
* If `ext_in` or `ext_out` are not in the `input-formats` or `output-formats` for the converter then the test is skipped, again by raising `nose.plugins.skip.SkipTest`.
* The converter translates `testcaseNNNN/file.<ext_in>` to `out.<ext_out>`.
* The comparator for `<ext_out>` registered with `harness.HarnessResources` is retrieved.
* The comparator compares `testcaseNNNN/file.<ext_out>` to `out.<ext_out>` for equivalence, which results in either success or failure.

A helper method is also provided to get the configuration for the converter to be tested within a sub-class:

```
def configure(self, config_key, env_var, default_file_name)
```

The method assumes the converter has been created and stored in an instance variable. It loads the contents of a YAML file (using `factory.load_yaml`) into a Python dictionary. The file loaded is:

* The value of an entry in `harness.HarnessResource` configuration with name `config_key`, if any.
* Else, the file named in the environment variable named in `env_var`, if such an environment variable has been defined.
* Else, `default_file_name`.

Once loaded, a dictionary entry with whose key is the value of `config_key` is extracted and used to configure the converter via its `configure` method.

In addition to converter-specific configuration, this configuration can also hold:

* `skip-tests`: a list of the indices of zero or more tests that are to be skipped for this converter.

If so, then this list is cached in an instance variable.

An example configuration, in the form of a Python dictionary, and for ProvPy `prov-convert`, is:

```
{
"ProvPy: {
  "executable": "prov-convert"
  "arguments": "-f FORMAT INPUT OUTPUT"
  "input-formats": ["json"]
  "output-formats": ["provn", "provx", "json"]
  skip-tests: [2, 3, 5]
  }
}
```

The corresponding YAML configuration file is:

```
---
ProvPy: 
  executable: prov-convert
  arguments: -f FORMAT INPUT OUTPUT
  input-formats: [json]
  output-formats: [provn, provx, json]
  skip-tests: [2, 3, 5]
}
```

### `interop_tests.test_provpy` - ProvPy `provconvert` interoperability tests

This module provides the interoperability test class for ProvPy's `prov-convert`:

```
class ProvPyTestCase(ConverterTestCase)
```

Its configuration, loaded via `ConverterTestCase.configure` is expected to be in a YAML file:

* Either provided as the value of a `ProvPy` key in the `harness.HarnessResource` configuration.
* Or, named in an environment variable, `PROVPY_TEST_CONFIGURATION`.
* Or in `localconfig/provpy.yaml`.

The configuration is expected to have the key `ProvPy`.

A valid YAML configuration file is:

```
---
ProvPy: 
  executable: prov-convert
  arguments: -f FORMAT INPUT OUTPUT
  input-formats: [json]
  output-formats: [provn, provx, json]
  skip-tests: []
```

### `interop_tests.test_provtoolbox` - ProvToolbox `prov-convert` interoperability tests

This module provides the interoperability test class for ProvToolbox's `provconvert`:

```
class ProvToolboxTestCase(ConverterTestCase)
```

Its configuration, loaded via `ConverterTestCase.configure` is expected to be in a YAML file:

* Either provided as the value of a `ProvToolbox` key in the `harness.HarnessResource` configuration.
* Or, named in an environment variable, `PROVTOOLBOX_TEST_CONFIGURATION`.
* Or in `localconfig/provtoolbox.yaml`.

The configuration is expected to have the key `ProvToolbox`.

A valid YAML configuration file is:

```
---
ProvToolbox: 
  executable: provconvert
  arguments: -infile INPUT -outfile OUTPUT
  input-formats: [provn, ttl, trig, provx, json]
  output-formats: [provn, ttl, trig, provx, json]
  skip-tests: []
```

### `interop_tests.test_provstore` - ProvStore interoperability tests

This module provides the interoperability test class for ProvStore:

```
class ProvStoreTestCase(ConverterTestCase)
```

Its configuration, loaded via `ConverterTestCase.configure` is expected to be in a YAML file:

* Either provided as the value of a `ProvStore` key in the `harness.HarnessResource` configuration.
* Or, named in an environment variable, `PROVSTORE_TEST_CONFIGURATION`.
* Or in `localconfig/provstore.yaml`.

The configuration is expected to have the key `ProvStore`.

A valid YAML configuration file is:

```
---
ProvStore:
  url: https://provenance.ecs.soton.ac.uk/store/api/v0/documents/
  authorization: ApiKey user:12345qwerty
  input-formats: [provn, ttl, trig, provx, json]
  output-formats: [provn, ttl, trig, provx, json]
  skip-tests: []
```

### `interop_tests.test_provtranslator` - ProvTranslator interoperability tests

This module provides the interoperability test class for ProvTranslator:

```
class ProvTranslatorTestCase(ConverterTestCase)
```

Its configuration, loaded via `ConverterTestCase.configure` is expected to be in a YAML file:

* Either provided as the value of a `ProvTranslator` key in the `harness.HarnessResource` configuration.
* Or, named in an environment variable, `PROVTRANSLATOR_TEST_CONFIGURATION`.
* Or in `localconfig/provtranslator.yaml`.

The configuration is expected to have the key `ProvTranslator`.

A valid YAML configuration file is:

```
---
ProvTranslator:
  url: https://provenance.ecs.soton.ac.uk/validator/provapi/documents/
  input-formats: [provn, ttl, trig, provx, json]
  output-formats: [provn, ttl, trig, provx, json]
  skip-tests: []
```

---

## Utility modules

### `factory` - dynamic class loading and object creation

This module provides functions to load classes, and create instances of these, from strings.

```
def get_class(name)
```

This function loads a class given a module-prefixed class name and returns the class (a value of type `classobj`). A valid module-prefixed class name is, for example, ``prov_interop.component.Component``. An invalid class name is ``Component``.

```
def get_instance(name)
```

This function invokes `get_class` then creates an instance of the class. It assumes the class has a zero-arity constructor.

### `files` - loading YAML files

This module provides functions to load YAML files. 

```
def load_yaml(env_var, default_file_name, file_name = None)
```

This function loads the contents of a YAML file:

* If `file_name` is provided then the contents of the file are loaded and returned.
* Else, if an environment variable with name `env_var` is defined,  then the contents of the file named in that variable are loaded.
* Else, the contents of the default file, `default_file_name`, are loaded and returned

If there are any problems then an error is raised:

```
class YamlError(Exception)
```

### `http` - HTTP request constants

This module holds constants relating to HTTP requests:

```
CONTENT_TYPE = "Content-type"
ACCEPT = "Accept"
AUTHORIZATION = "Authorization"
```

---

## Unit tests

`prov_interop/tests` contains unit tests for all the test harness classes.

### `provpy` and `provtoolbox` packages

For unit testing `provpy.converter` and `provpy.comparator`, simple scripts which mimic the behaviour of `prov-convert` and `prov-compare` are available:

```
provpy/prov_compare_dummy.py
provpy/prov_convert_dummy.py
```

These accept the same command-line arguments and exit with the same exit codes, but don't do any conversion (the input file is just copied to the output file) or comparison (the files are considered equal if their contents are the same).

Likewise, for unit testing `provtoolbox.converter`, a simple script which mimics the behaviour of `provconvert`:

```
provtoolbox/provconvert_dummy.py
```

### `provstore` and `provtranslator` packages

`provstore.converter` and `provtranslator.converter` use REST services via the Python [requests](http://docs.python-requests.org/en/latest/) library. To unit test these packages, the [requests-mock](https://requests-mock.readthedocs.org/en/latest/) library is used.

---

## YAML and configuration files

[YAML](http://yaml.org/) (YAML Ain't Markup Language) is used for configuration files. It is a simple human-readable file format, which can express dictionaries and lists. JSON can be considered a subset of YAML (see [YAML version 1.2](http://yaml.org/spec/1.2/spec.html)).

[PyYAML](http://pyyaml.org/wiki/PyYAML) is a Python package for parsing YAML strings or files into Python dictionaries.

---

## xUnit test framework integration

The interoperability test packages, modules and classes are named so they can be run via the [nose](https://nose.readthedocs.org/en/latest/) xUnit test framework:

```
$ nosetests prov_interop.interop_tests
```

Or, running tests for each converter in turn:

```
$ nosetests prov_interop.interop_tests.test_provpy
$ nosetests prov_interop.interop_tests.test_provtoolbox
$ nosetests prov_interop.interop_tests.test_provstore
$ nosetests prov_interop.interop_tests.test_provtranslator
```

Adopting this approach means that xUnit framework support for test logging and report generation can be exploited. For example, run tests in verbose mode:

```
$ nosetests -v prov_interop.interop_tests
```

For example, run tests and create an XML test report:

```
$ nosetests --with-xunit prov_interop.interop_tests
$ cat nosetests.xml
```

---

## Creating localised configuration

`config/` contains example configuration files for configuring the test harness and each of the four converter-specific interoperability test classes:

```
harness.yaml
provpy.yaml
provstore.yaml
provtoolbox.yaml
provtranslator.yaml
```

These need to be edited to reflect the local execution environment before they can be used. For example:

* `harness.yaml` needs `test-cases` to be set to the location of the test cases directory.
* `provstore.yaml` needs `authorization` to be set with a valid ProvStore user name and API key (e.g. `user:12345qwerty`):
* `provpy.yaml` needs `executable` to be set to either `prov-convert` or `python /home/user/ProvPy/scripts/prov-convert` (with the path to the location of ProvPy) depending upon whether the ProvPy library or Git repository are being used.
* `provtoolbox.yaml` needs `executable` to be set to the location `provtoolbox` which will depend on whether the ProvToolbox binary or source release, or Git repository is being used.

`prov_interop/set_yaml_value.py` provides a simple command-line tool that can be used to set configuration values in YAML files. Given the fully-qualified path of keys to the value to be replaced, and a file name, it performs the replacement. For example, given `localconfig/provstore.yaml`

```
---
ProvStore:
  authorization: ApiKey APIKEY
  input-formats: [provn, ttl, trig, provx, json]
  output-formats: [provn, ttl, trig, provx, json]
  skip-tests: []
  url: https://provenance.ecs.soton.ac.uk/store/api/v0/documents/
```

Running:

```
$ python prov_interop/set_yaml_value.py localconfig/provstore.yaml \
  ProvStore.authorization="ApiKey user:12345qwerty"
```

updates the file to:

```
---
ProvStore:
  authorization: ApiKey user:12345qwerty
  input-formats: [provn, ttl, trig, provx, json]
  output-formats: [provn, ttl, trig, provx, json]
  skip-tests: []
  url: https://provenance.ecs.soton.ac.uk/store/api/v0/documents/
```

Given `localconfig/harness.yaml`:

```
test-cases: /home/user/test-cases
comparators:
  ProvPyComparator: 
    class: prov_interop.provpy.comparator.ProvPyComparator
    executable: prov-compare
    arguments: -f FORMAT1 -F FORMAT2 FILE1 FILE2
    formats: [provx, json]
```

Running:

```
$ python prov_interop/set_yaml_value.py localconfig/harness.yaml \
  comparators.ProvPyComparator.executable="python /home/mjj/ProvPy/scripts/prov-compare"
```

updates the file to:

```
comparators:
  ProvPyComparator:
    arguments: -f FORMAT1 -F FORMAT2 FILE1 FILE2
    class: prov_interop.provpy.comparator.ProvPyComparator
    executable: python /home/mjj/ProvPy/scripts/prov-compare
    formats: [provx, json]
```

---

## Python

### Python 2 and 3

ProvPy supports Python 2.6, 2.7, 3.3, 3.4 and pypy. There are different behaviours in Python 2.x and 3.x with respect to handling strings. It is unclear whether ProvPy's `prov-convert` tool outputs the same results in both environments. As a result, the test harness runs under both Python 2 and 3 (both its code and unit tests) to allow interoperability testing of `prov-convert` under both Python 2 and 3.

All Python files include:

```
from __future__ import (absolute_import, division, print_function,  unicode_literals)
```

All changes proposed by the Python [2to3](https://docs.python.org/2/library/2to3.html) tool have been applied.

### Libraries

| Library | Use |
| ------- | --- |
| [nose](https://nose.readthedocs.org/en/latest/) | Unit test library |
| [nose_parameterized](https://pypi.python.org/pypi/nose-parameterized/) | Parameterized unit tests |
| [PyYaml](http://pyyaml.org/wiki/PyYAML) | YAML parser |
| [requests](http://docs.python-requests.org/en/latest/) | HTTP library which can be used to invoke REST endpoints |
| [requests-mock](https://requests-mock.readthedocs.org/en/latest/) | Mock testing of code that uses requests |
| [subprocess](https://docs.python.org/2/library/subprocess.html) | invoke command-line tools and capture return codes, output and error streams |
