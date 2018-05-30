#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main module."""

import os
import argparse

from fform.dals_mt import DalMesh

from mt_ingester.parsers import ParserXmlMeshDescriptors
from mt_ingester.parsers import ParserXmlMeshQualifiers
from mt_ingester.parsers import ParserXmlMeshSupplementals
from mt_ingester.ingesters import IngesterDocumentDescriptor
from mt_ingester.ingesters import IngesterDocumentQualifier
from mt_ingester.ingesters import IngesterDocumentSupplemental
from mt_ingester.config import import_config


def load_config(args):
    if args.config_file:
        cfg = import_config(fname_config_file=args.config_file)
    elif "CT_INGESTER_CONFIG" in os.environ:
        fname_config_file = os.environ["CT_INGESTER_CONFIG"]
        cfg = import_config(fname_config_file=fname_config_file)
    else:
        msg_fmt = "Configuration file path not defined."
        raise ValueError(msg_fmt)

    return cfg


def main(args):
    cfg = load_config(args=args)

    dal = DalMesh(
        sql_username=cfg.sql_username,
        sql_password=cfg.sql_password,
        sql_host=cfg.sql_host,
        sql_port=cfg.sql_port,
        sql_db=cfg.sql_db,
    )

    parser = None
    ingester = None
    if arguments.mode == "descriptors":
        parser = ParserXmlMeshDescriptors()
        ingester = IngesterDocumentDescriptor(
            dal=dal,
            do_ingest_links=arguments.do_ingest_links,
        )
    elif arguments.mode == "qualifiers":
        parser = ParserXmlMeshQualifiers()
        ingester = IngesterDocumentQualifier(
            dal=dal,
            do_ingest_links=arguments.do_ingest_links,
        )
    elif arguments.mode == "supplementals":
        parser = ParserXmlMeshSupplementals()
        ingester = IngesterDocumentSupplemental(
            dal=dal,
            do_ingest_links=arguments.do_ingest_links,
        )

    for filename in args.filenames:
        docs = parser.parse(filename_xml=filename)
        for doc in docs:
            ingester.ingest(doc=doc)


# main sentinel
if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(
        description="mt-ingester: MeSH XML dump parser and SQL ingester."
    )
    argument_parser.add_argument(
        "filenames",
        nargs="+",
        help="MeSH XML files to ingest.",
    )
    argument_parser.add_argument(
        "--mode",
        dest="mode",
        help="Ingestion mode",
        choices=["descriptors", "qualifiers", "supplementals"],
        required=True,
    )
    argument_parser.add_argument(
        "--do-ingest-links",
        dest="do_ingest_links",
        action="store_true",
    )
    argument_parser.add_argument(
        "--no-do-ingest-links",
        dest="do_ingest_links",
        action="store_false",
    )
    argument_parser.add_argument(
        "--config-file",
        dest="config_file",
        help="configuration file",
        required=False,
    )
    arguments = argument_parser.parse_args()

    main(args=arguments)
