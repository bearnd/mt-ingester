# coding=utf-8

import os
import unittest

from mt_ingester.parsers import ParserUmlsSat
from mt_ingester.parsers import ParserUmlsConso
from mt_ingester.parsers import ParserUmlsDef

from tests.assets.samples_umls import get_sample_file
from tests.assets.samples_umls import EnumUmlsFileSample


class ParserUmlsSatTest(unittest.TestCase):
    """ Tests the `ParserUmlsSat` class."""

    def setUp(self):
        """ Retrieves a sample MRSAT.RRF file and instantiates the parser."""

        self.file = get_sample_file(umls_file_type=EnumUmlsFileSample.MRSAT)

        self.parser = ParserUmlsSat()

    def tearDown(self):
        """ Deletes the temporary MRSAT.RRF file."""

        os.remove(self.file.name)

    def test_parse(self):
        """ Tests the `parse` method of the parser class."""

        map_cui_dui = self.parser.parse(filename_mrsat_rrf=self.file.name)

        self.assertDictEqual(
            map_cui_dui,
            {
                'C0001175': 'D000163',
                'C0006118': 'D001932',
                'C0024537': 'D016780',
                'C0153633': 'D001932',
                'C0750974': 'D001932',
                'C0750979': 'D001932',
                'C1527390': 'D001932',
            }
        )


class ParserUmlsConsoTest(unittest.TestCase):
    """ Tests the `ParserUmlsConso` class."""

    def setUp(self):
        """ Retrieves sample MRSAT.RRF and MRCONSO.RRF files and instantiates
            the parser.
        """

        self.file_mrsat = get_sample_file(
            umls_file_type=EnumUmlsFileSample.MRSAT,
        )
        self.file_mrconso = get_sample_file(
            umls_file_type=EnumUmlsFileSample.MRCONSO,
        )

        self.parser = ParserUmlsConso()

    def tearDown(self):
        """ Deletes the temporary MRSAT.RRF and MRCONSO.RRF files."""

        os.remove(self.file_mrsat.name)
        os.remove(self.file_mrconso.name)

    def test_parse(self):
        """ Tests the `parse` method of the parser class."""

        dui_synonyms = self.parser.parse(
            filename_mrsat_rrf=self.file_mrsat.name,
            filename_mrconso_rrf=self.file_mrconso.name,
        )

        dui_synonyms_refr = {
            'D000163': [
                'acquired immunodeficiency syndrome',
                'acquired immunodeficiency syndromes',
                'syndromes, acquired immunodeficiency',
            ],
            'D001932': [
                'neoplasm, brain',
                'brain tumors',
                'brain tumors, primary',
                'neoplasms, intracranial',
            ],
            'D016780': [
                'plasmodium vivax malaria',
                'vivax malaria',
            ]
        }

        self.assertListEqual(
            sorted(list(dui_synonyms.keys())),
            sorted(list(dui_synonyms_refr.keys())),
        )
        for k, v in dui_synonyms_refr.items():
            self.assertListEqual(
                sorted(list(dui_synonyms[k])),
                sorted(list(dui_synonyms_refr[k])),
            )


class ParserUmlsDefTest(unittest.TestCase):
    """ Tests the `ParserUmlsDef` class."""

    def setUp(self):
        """ Retrieves sample MRSAT.RRF and MRDEF.RRF files and instantiates
            the parser.
        """

        self.file_mrsat = get_sample_file(
            umls_file_type=EnumUmlsFileSample.MRSAT,
        )
        self.file_mrdef = get_sample_file(
            umls_file_type=EnumUmlsFileSample.MRDEF,
        )

        self.parser = ParserUmlsDef()

    def tearDown(self):
        """ Deletes the temporary MRSAT.RRF and MRDEF.RRF files."""

        os.remove(self.file_mrsat.name)
        os.remove(self.file_mrdef.name)

    def test_parse(self):
        """ Tests the `parse` method of the parser class."""

        dui_definitions = self.parser.parse(
            filename_mrsat_rrf=self.file_mrsat.name,
            filename_mrdef_rrf=self.file_mrdef.name,
        )

        dui_definitions_refr = {
            'D000163': {
                'CSP': [
                    ('one or more indicator diseases, depending on '
                     'laboratory evidence of HIV infection (CDC); late '
                     'phase of HIV infection characterized by marked '
                     'suppression of immune function resulting in '
                     'opportunistic infections, neoplasms, and other systemic '
                     'symptoms (NIAID).')
                ],
                'NCI_NICHD': [
                    ('A chronic, potentially life threatening condition that '
                     'is caused by human immunodeficiency virus (HIV) '
                     'infection, and is characterized by increased '
                     'susceptibility to opportunistic infections, certain '
                     'cancers and neurologic disorders.')
                ]
            },
            'D001932': {
                'NCI': [
                    ('A benign or malignant neoplasm that arises from or '
                     'metastasizes to the brain.')
                ],
                'NCI_NICHD': [
                    'An abnormal intracranial solid mass or growth.'
                ]
            },
            'D016780': {
                'MSH': [
                    ('Malaria caused by PLASMODIUM VIVAX. This form of '
                     'malaria is less severe than MALARIA, FALCIPARUM, but '
                     'there is a higher probability for relapses to occur. '
                     'Febrile paroxysms often occur every other day.')
                ],
                'NCI': [
                    'Malaria resulting from infection by Plasmodium vivax.'
                ]
            }
        }

        self.assertListEqual(
            sorted(list(dui_definitions.keys())),
            sorted(list(dui_definitions_refr.keys())),
        )
        for k, v in dui_definitions.items():
            self.assertListEqual(
                sorted(list(dui_definitions[k].keys())),
                sorted(list(dui_definitions_refr[k].keys())),
            )
            for kk, vv in dui_definitions[k].items():
                self.assertListEqual(
                    sorted(list(dui_definitions[k][kk])),
                    sorted(list(dui_definitions_refr[k][kk])),
                )
