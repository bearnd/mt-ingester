# coding=utf-8

import os
import datetime
import unittest

from mt_ingester.parsers import ParserXmlMeshQualifiers

from tests.assets.samples_mesh import get_sample_file
from tests.assets.samples_mesh import EnumMeshFileSample


class ParserMeshQualifiersTest(unittest.TestCase):
    """ Tests the `ParserXmlMeshQualifiers` class."""

    def setUp(self):
        """ Retrieves a sample qualifiers file and instantiates the parser."""

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.QUAL)

        self.parser = ParserXmlMeshQualifiers()

        self.file_xml = self.parser.open_xml_file(filename_xml=self.file.name)

        elements = self.parser.generate_xml_elements(
            file_xml=self.file_xml,
            element_tag="QualifierRecord"
        )

        self.qualifier_element = next(elements)

    def tearDown(self):
        """ Deletes the temporary descriptors file."""

        self.file.close()
        self.file_xml.close()
        os.remove(self.file.name)

    def test_parse_qualifier_record(self):
        """ Tests the `parse_qualifier_record` method and asserts the values
            on the top-level fields.
        """

        record = self.parser.parse_qualifier_record(
            element=self.qualifier_element,
        )

        self.assertEqual(record["QualifierUI"], "Q000000981")
        self.assertEqual(record["QualifierName"], "diagnostic imaging")
        self.assertEqual(record["DateCreated"], datetime.date(2016, 6, 29))
        self.assertEqual(record["DateRevised"], datetime.date(2016, 6, 8))
        self.assertEqual(record["DateEstablished"], datetime.date(2017, 1, 1))
        self.assertEqual(
            record["Annotation"],
            ("subheading only; coordinate with specific imaging technique "
             "if pertinent"),
        )
        self.assertEqual(record["HistoryNote"], "2017(1967)")
        self.assertEqual(
            record["OnlineNote"],
            "search policy: Online Manual; use: main heading/AB or AB (SH) "
            "or SUBS APPLY AB",
        )
        # Skipping `TreeNumberList`. Covered in different unit-tests.
        self.assertTrue(record["TreeNumberList"])
        # Skipping `ConceptList`. Covered in different unit-tests.
        self.assertTrue(record["ConceptList"])

    def test_parse(self):
        """ Tests the `parse` method."""

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.QUAL)

        records = self.parser.parse(self.file.name)

        self.assertEqual(len(list(records)), 1)

