# coding=utf-8

import os
import datetime
import unittest

from fform.orm_mt import SupplementalClassType

from mt_ingester.parsers import ParserXmlMeshSupplementals

from tests.assets.samples_mesh import get_sample_file
from tests.assets.samples_mesh import EnumMeshFileSample


class ParserMeshSupplementalsTest(unittest.TestCase):
    """ Tests the `ParserXmlMeshSupplementals` class."""

    def setUp(self):
        """ Retrieves a sample qualifiers file and instantiates the parser."""

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.SUPP)

        self.parser = ParserXmlMeshSupplementals()

        self.file_xml = self.parser.open_xml_file(filename_xml=self.file.name)

        elements = self.parser.generate_xml_elements(
            file_xml=self.file_xml,
            element_tag="SupplementalRecord"
        )

        self.supplemental_element = next(elements)

    def tearDown(self):
        """ Deletes the temporary descriptors file."""

        self.file.close()
        self.file_xml.close()
        os.remove(self.file.name)

    def test_parse_supplemental_record(self):
        """ Tests the `parse_supplemental_record` method and asserts the values
            on the top-level fields.
        """

        record = self.parser.parse_supplemental_record(
            element=self.supplemental_element,
        )

        self.assertEqual(record["SupplementalClass"], SupplementalClassType.ONE)
        self.assertEqual(record["SupplementalRecordUI"], "C000002")
        self.assertEqual(record["SupplementalRecordName"], "bevonium")
        self.assertEqual(record["DateCreated"], datetime.date(1971, 1, 1))
        self.assertEqual(record["DateRevised"], datetime.date(2018, 9, 24))
        self.assertEqual(record["Note"], "structure given in first source")
        self.assertEqual(record["Frequency"], "1")
        # Skipping `PreviousIndexingList`. Covered in different unit-tests.
        # Skipping `HeadingMappedToList`. Covered in later test.
        # Skipping `IndexingInformationList`. Covered in later test.
        # Skipping `PharmacologicalActionList`. Covered in different unit-tests.
        # Skipping `SourceList`. Covered in later test.
        # Skipping `ConceptList`. Covered in different unit-tests.

    def test_parse_heading_mapped_to_list(self):
        """ Tests the `parse_heading_mapped_to_list` method."""

        records = self.parser.parse_heading_mapped_to_list(
            self.supplemental_element.find("HeadingMappedToList")
        )

        self.assertListEqual(
            records,
            [
                {
                    'DescriptorReferredTo': {
                        'DescriptorName': 'Benzilates',
                        'DescriptorUI': 'D001561'
                    },
                    'QualifierReferredTo': {}
                },
                {
                    'DescriptorReferredTo': {
                        'DescriptorName': 'Acetylglucosamine',
                        'DescriptorUI': 'D000117'
                    },
                    'QualifierReferredTo': {
                        'QualifierName': 'analogs & derivatives',
                        'QualifierUI': 'Q000031'
                    }
                }
            ]
        )

    def test_parse_indexing_information_list(self):
        """ Tests the `parse_indexing_information_list` method."""

        records = self.parser.parse_indexing_information_list(
            self.supplemental_element.find("IndexingInformationList")
        )

        self.assertListEqual(
            records,
            [
                {
                    'DescriptorReferredTo': {
                        'DescriptorName': 'Leprosy',
                        'DescriptorUI': 'D007918'
                    },
                    'QualifierReferredTo': {
                        'QualifierName': 'drug therapy',
                        'QualifierUI': 'Q000188'
                    }
                },
                {
                    'DescriptorReferredTo': {
                        'DescriptorName': 'Street Drugs',
                        'DescriptorUI': 'D013287'
                    },
                    'QualifierReferredTo': {}
                }
            ]
        )

    def test_parse_source_list(self):
        """ Tests the `parse_source_list` method."""

        records = self.parser.parse_source_list(
            self.supplemental_element.find("SourceList")
        )

        self.assertListEqual(
            records,
            [
                {'Source': 'S Afr Med J 50(1):4;1976'},
                {'Source': 'Q J Med 1979;48(191):493'}
            ]
        )

    def test_parse(self):
        """ Tests the `parse` method."""

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.SUPP)

        records = self.parser.parse(self.file.name)

        self.assertEqual(len(list(records)), 1)
