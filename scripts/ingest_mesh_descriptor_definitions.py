# coding=utf-8

import os
import argparse

from fform.dals_mt import DalMesh

from mt_ingester.parsers import ParserUmlsDef
from mt_ingester.ingesters import IngesterUmlsDef
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

    parser = ParserUmlsDef()
    ingester = IngesterUmlsDef(dal=dal)

    doc = parser.parse(
        filename_mrsat_rrf=args.filename_mrsat_rrf,
        filename_mrdef_rrf=args.filename_mrdef_rrf,
    )

    ingester.ingest(document=doc)


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description="mt-ingester: UMLS MRDEF ingester."
    )

    argument_parser.add_argument(
        "--mr-sat-filename",
        dest="filename_mrsat_rrf",
        help="MRSAT.rrf filename",
        required=True,
    )

    argument_parser.add_argument(
        "--mr-def-filename",
        dest="filename_mrdef_rrf",
        help="MRDEF.rrf filename",
        required=True,
    )

    arguments = argument_parser.parse_args()

    main(args=arguments)
