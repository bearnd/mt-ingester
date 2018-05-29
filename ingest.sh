
# Ingest qualifiers without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode qualifiers --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" qual2018.xml
# Ingest qualifiers with links.
python -m mt_ingester.mt_ingester --mode qualifiers --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" qual2018.xml

# Ingest descriptors without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode descriptors --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" desc2018.gz
# Ingest descriptors with links.
python -m mt_ingester.mt_ingester --mode descriptors --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" desc2018.gz

# Ingest supplementals without adding links (in case they haven't been added yet).
python -m mt_ingester.mt_ingester --mode supplementals --no-do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" supp2018.gz
# Ingest supplementals with links.
python -m mt_ingester.mt_ingester --mode supplementals --do-ingest-links --config-file="/etc/mt-ingester/mt-ingester.json" supp2018.gz
