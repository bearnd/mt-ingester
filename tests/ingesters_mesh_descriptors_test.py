# coding=utf-8

import datetime
import os

from fform.orm_mt import Descriptor
from fform.orm_mt import DescriptorClassType

from mt_ingester.parsers import ParserXmlMeshDescriptors
from mt_ingester.ingesters import IngesterDocumentDescriptor

from tests.dal_mixins import DalMtTestBase
from tests.assets.samples_mesh import get_sample_file
from tests.assets.samples_mesh import EnumMeshFileSample


class IngesterMeshDescriptorTest(DalMtTestBase):
    """ Tests the `IngesterDocumentDescriptor` class."""

    def setUp(self):
        """ Retrieves and parses sample descriptors file and initializes the
            DAL.
        """

        super(IngesterMeshDescriptorTest, self).setUp()

        self.dal = self.setup_dal()

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.DESC)

        self.parser = ParserXmlMeshDescriptors()

        descriptors = self.parser.parse(filename_xml=self.file.name)
        self.document = next(descriptors)

    def tearDown(self):
        """ Deletes the temporary descriptors file."""

        self.file.close()
        os.remove(self.file.name)

    def test_ingest_descriptor_fields(self):
        """ Tests the `ingest` method of the parser class and asserts the
            top-level fields of the `Descriptor` record.
        """

        ingester = IngesterDocumentDescriptor(
            dal=self.dal,
            do_ingest_links=False,
        )

        obj_id = ingester.ingest(doc=self.document)

        obj = self.dal.get(
            orm_class=Descriptor,
            pk=obj_id,
        )  # type: Descriptor

        self.assertEqual(obj.descriptor_class, DescriptorClassType.ONE)
        self.assertEqual(obj.ui, "D000001")
        self.assertEqual(obj.name, "Calcimycin")
        self.assertEqual(obj.created, datetime.date(1974, 11, 19))
        self.assertEqual(obj.revised, datetime.date(2016, 5, 27))
        self.assertEqual(obj.established, datetime.date(1984, 1, 1))
        self.assertEqual(
            obj.annotation,
            "for use to kill or control insects...",
        )
        self.assertEqual(
            obj.history_note,
            "91(75); was A 23187 1975-90 (see under ANTIBIOTICS 1975-83)",
        )
        self.assertEqual(obj.nlm_classification_number, "QV 175")
        self.assertEqual(
            obj.online_note,
            "use CALCIMYCIN to search A 23187 1975-90",
        )
        self.assertEqual(
            obj.public_mesh_note,
            "91; was A 23187 1975-90 (see under ANTIBIOTICS 1975-83)",
        )
        self.assertEqual(
            obj.consider_also,
            "consider also terms at PROCT-",
        )

    def test_ingest_descriptor_relationships(self):
        """ Tests the `ingest` method of the parser class and asserts the
            relationships of the `Descriptor` record.
        """

        ingester = IngesterDocumentDescriptor(
            dal=self.dal,
            do_ingest_links=False,
        )

        obj_id = ingester.ingest(doc=self.document)

        obj = self.dal.get_joined(
            orm_class=Descriptor,
            pk=obj_id,
            joined_relationships=["tree_numbers", "concepts"]
        )  # type: Descriptor

        self.assertIsNotNone(obj.tree_numbers)
        self.assertEqual(len(obj.tree_numbers), 2)
        self.assertIsNotNone(obj.concepts)
        self.assertEqual(len(obj.concepts), 2)
