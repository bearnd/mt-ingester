
# Ingest qualifiers without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode qualifiers --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" /mnt/Downloads/_DUMP/download_station/MeSH/2019/Files/qual2019.xml
# Ingest qualifiers with links.
python -m mt_ingester.mt_ingester --mode qualifiers --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" /mnt/Downloads/_DUMP/download_station/MeSH/2019/Files/qual2019.xml

# Ingest descriptors without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode descriptors --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" /mnt/Downloads/_DUMP/download_station/MeSH/2019/Files/desc2019.gz
# Ingest descriptors with links.
python -m mt_ingester.mt_ingester --mode descriptors --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" /mnt/Downloads/_DUMP/download_station/MeSH/2019/Files/desc2019.gz

# Ingest supplementals without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode supplementals --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" /mnt/Downloads/_DUMP/download_station/MeSH/2019/Files/supp2019.gz
# Ingest supplementals with links.
python -m mt_ingester.mt_ingester --mode supplementals --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" /mnt/Downloads/_DUMP/download_station/MeSH/2019/Files/supp2019.gz

# Ingest MeSH descriptor synonyms.
python -m mt_ingester.mt_ingester --mode synonyms --config-file="/etc/mt-ingester/mt-ingester.json" /mnt/Downloads/_DUMP/download_station/UMLS/2018AB/MRSAT_SUBSET.RRF /mnt/Downloads/_DUMP/download_station/UMLS/2018AB/MRCONSO_SUBSET.RRF
# Ingest MeSH descriptor definitions.
python -m mt_ingester.mt_ingester --mode definitions --config-file="/etc/mt-ingester/mt-ingester.json" /mnt/Downloads/_DUMP/download_station/UMLS/2018AB/MRDEF.RRF /mnt/Downloads/_DUMP/download_station/UMLS/2018AB/MRSAT_SUBSET.RRF
