set -e

[ -n "$PATH_DATA_MESH" ] || echo "PATH_DATA_MESH variable undefined."
[ -n "$PATH_DATA_MESH" ] || exit 1
echo "PATH_DATA_MESH set to '$PATH_DATA_MESH'."
[ -n "$PATH_DATA_UMLS" ] || echo "PATH_DATA_UMLS variable undefined."
[ -n "$PATH_DATA_UMLS" ] || exit 1
echo "PATH_DATA_UMLS set to '$PATH_DATA_UMLS'."

echo "Ingest qualifiers without adding links (in case they haven't been added yet)."
python -m mt_ingester.mt_ingester --mode qualifiers --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester-prod.json" "$PATH_DATA_MESH"/qual2019.xml

echo "Ingest qualifiers with links."
python -m mt_ingester.mt_ingester --mode qualifiers --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester-prod.json" "$PATH_DATA_MESH"/qual2019.xml

echo "Ingest descriptors without adding links (in case they haven't been added yet)."
python -m mt_ingester.mt_ingester --mode descriptors --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester-prod.json" "$PATH_DATA_MESH"/desc2019.xml

echo "Ingest descriptors with links."
python -m mt_ingester.mt_ingester --mode descriptors --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester-prod.json" "$PATH_DATA_MESH"/desc2019.xml

echo "Ingest supplementals without adding links (in case they haven't been added yet)."
python -m mt_ingester.mt_ingester --mode supplementals --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester-prod.json" "$PATH_DATA_MESH"/supp2019.xml

echo "Ingest supplementals with links."
python -m mt_ingester.mt_ingester --mode supplementals --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester-prod.json" "$PATH_DATA_MESH"/supp2019.xml

echo "Ingest MeSH descriptor synonyms."
python -m mt_ingester.mt_ingester --mode synonyms --config-file="/etc/mt-ingester/mt-ingester-prod.json" "$PATH_DATA_UMLS"/MRSAT.RRF "$PATH_DATA_UMLS"/MRCONSO.RRF

echo "Ingest MeSH descriptor definitions."
python -m mt_ingester.mt_ingester --mode definitions --config-file="/etc/mt-ingester/mt-ingester-prod.json" "$PATH_DATA_UMLS"/MRDEF.RRF "$PATH_DATA_UMLS"/MRSAT.RRF
