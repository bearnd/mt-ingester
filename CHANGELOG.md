## Changelog

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
