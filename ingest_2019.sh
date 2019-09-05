[ -n "$PATH_DATA_MESH" ] || echo "PATH_DATA_MESH variable undefined." && exit 1
[ -n "$PATH_DATA_UMLS" ] || echo "PATH_DATA_UMLS variable undefined." && exit 1

# Ingest qualifiers without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode qualifiers --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" "$PATH_DATA_MESH"/qual2019.xml
# Ingest qualifiers with links.
python -m mt_ingester.mt_ingester --mode qualifiers --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" "$PATH_DATA_MESH"/qual2019.xml

# Ingest descriptors without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode descriptors --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" "$PATH_DATA_MESH"/desc2019.xml
# Ingest descriptors with links.
python -m mt_ingester.mt_ingester --mode descriptors --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" "$PATH_DATA_MESH"/desc2019.xml

# Ingest supplementals without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode supplementals --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" "$PATH_DATA_MESH"/supp2019.xml
# Ingest supplementals with links.
python -m mt_ingester.mt_ingester --mode supplementals --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" "$PATH_DATA_MESH"/supp2019.xml

# Ingest MeSH descriptor synonyms.
python -m mt_ingester.mt_ingester --mode synonyms --config-file="/etc/mt-ingester/mt-ingester.json" "$PATH_DATA_UMLS"/MRSAT.RRF "$PATH_DATA_UMLS"/MRCONSO.RRF
# Ingest MeSH descriptor definitions.
python -m mt_ingester.mt_ingester --mode definitions --config-file="/etc/mt-ingester/mt-ingester.json" "$PATH_DATA_UMLS"/MRDEF.RRF "$PATH_DATA_UMLS"/MRSAT.RRF
