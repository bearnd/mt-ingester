## Changelog

### v0.4.4

- Fixed the fix that didn’t correctly skip unknown sources in the `ingest` method of the `IngesterUmlsDef` class.

### v0.4.3

- Added simple escape clause to skip source-less entries.
- Fixed bug in definition ingestion script.

### v0.4.2

- Fixed more issues in the `ingest` method of the `IngesterDocumentSupplemental` class where a missing descriptor would cause an exception to be raised.

### v0.4.1

- Fixed issue in the `ingest` method of the `IngesterDocumentSupplemental` class where a missing descriptor would cause an exception to be raised.
- Updated the entry script to support UMLS definition ingestion while also updating the way files are defined for UMLS synonym ingestion.
- Added a simple ingestion script for the 2019 datasets.

### v0.4.0

Issue No. 194:

- Created a new `ParserUmlsSat` parser class capable of parsing the `MRSAT.RRF` file and creating a dictionary keyed on UMLS CUIs and valued with MeSH descriptor IDs. Subsequently I removed this code from `ParserUmlsDef` which is now using the aforementioned class.
- Updated the `ParserUmlsConso` class so that it uses the new `ParserUmlsSat` class to establish a relationship between UMLS CUIs and MeSH descriptor IDs. This new dictionary is being used instead of performing multiple passes over the `MRCONSO.RRF` file and as such only synonyms for MeSH descriptors are extracted.
- Updated Makefile to run unit-tests with `unittest`.
- Added test packages and sample strings containing portions of the UMLS files processed by the different parser classes.
- Added unit-tests for the UMLS parsers.
- Updated the `IngesterUmlsConso` and `IngesterUmlsDef` to only ingest synonyms and definitions for descriptors and added docstrings.
- Updated Ansible role and added the extra schemata to allow for unit-testing.
- Added a new module with DAL mixin classes to be used in unit-tests.
- Added a new module with a utility function to load the service configuration.
- Added unit-tests for the UMLS ingester classes.
- Updated the `parse` methods of the MeSH parser classes to close the XML file once parsing is complete.
- Added a new module with MeSH file samples.
- Added unit-tests for the MeSH parsers.
- Updated the `ingest` methods of the MeSH ingester classes to return the ID of the newly created record.
- Added unit-tests for the different MeSH ingester classes.

### v0.3.1

- Bug fixes.

### v0.3.0

Issue No. 189: Develop a UMLS parser and ingester for MeSH definitions:

- Updated Ansible role to match the other services.
- Added a new `ParserUmlsDef` class to parse the UMLS MRSAT.rrf and MRDEF.rrf files and extract definitions for the different MeSH descriptors.
- Added a new `IngesterUmlsDef` class to ingest the definitions extracted from the `ParserUmlsDef` class.
- Added a `scripts` subpackage.
- Added a script to ingest the UMLS MRDEF.rrf definitions.

### v0.2.5

Issue No. 34: Cleanup the MeSH entity synonyms:

- `parsers.py`: Updated the `parse` method of the `ParserUmlsConso` class to lowercase all collected synonyms in order to reduce duplication among them for a given MeSH entity.
- `ingesters.py`: Updated the `ingest` method of the `IngesterUmlsConso` class and added more logging verbosity.

Issue No. 33: Remove the `concept_synonyms` table:

- `ingesters.py`: Updated the `ingest` method of the `IngesterUmlsConso` class and removed the ingestion of concept synonyms.

### v0.2.4

- `ingesters.py`: Fixed bug in the `ingest` method of the `IngesterUmlsConso` class and added fail-safes in case a MeSH entity defined in UMLS is not defined in the DB.

### v0.2.3

- `ingesters.py`: Fixed bug in the `ingest` method of the `IngesterUmlsConso` class.

### v0.2.2

- `ingesters.py`: Fixed bug in the `ingest` method of the `IngesterUmlsConso` where I confused supplementals for concepts.

### v0.2.1

- `ingesters.py`: Fixed bug in the `ingest` method of the `IngesterUmlsConso` where I was using the entity UI to add synonym records instead of the entity PKs.

### v0.2.0

Issue No. 28: Update `mt-ingester` to ingest UMLS synonyms:

- `.gitignore`: Updated to ignore `.rrf` files.
- Updated the Ansible role and fixed the issue with the ansible-vault encrypted variables.
- `parsers.py`: Added a new `ParserUmlsConso` class to parse UMLS MRCONSO.rrf files.
- `ingesters.py`: Added a new `IgesterUmlsConso` class that can ingest parsed UMLS MRCONSO.rrf data.
- `ingesters.py`: Fixed bug in the `ingest` method of the `IngesterUmlsConso` class.
- `mt_ingester.py`: Updated the entry script to handle the MRCONSO.RRF files.
- Updated the ingestion script to show how the MRCONSO.rrf file can be ingested.

### v0.1.0

- Initial release.
