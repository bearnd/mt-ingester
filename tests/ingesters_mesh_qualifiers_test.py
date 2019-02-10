# coding=utf-8

import datetime
import os

from fform.orm_mt import Qualifier


from mt_ingester.parsers import ParserXmlMeshQualifiers
from mt_ingester.ingesters import IngesterDocumentQualifier

from tests.dal_mixins import DalMtTestBase
from tests.assets.samples_mesh import get_sample_file
from tests.assets.samples_mesh import EnumMeshFileSample


class IngesterMeshQualifierTest(DalMtTestBase):
    """ Tests the `IngesterDocumentQualifier` class."""

    def setUp(self):
        """ Retrieves and parses sample qualifiers file and initializes the
            DAL.
        """

        super(IngesterMeshQualifierTest, self).setUp()

        self.dal = self.setup_dal()

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.QUAL)

        self.parser = ParserXmlMeshQualifiers()

        qualifiers = self.parser.parse(filename_xml=self.file.name)
        self.document = next(qualifiers)

    def tearDown(self):
        """ Deletes the temporary qualifiers file."""

        self.file.close()
        os.remove(self.file.name)

    def test_ingest_qualifier_fields(self):
        """ Tests the `ingest` method of the parser class and asserts the
            top-level fields of the `Qualifier` record.
        """

        ingester = IngesterDocumentQualifier(
            dal=self.dal,
            do_ingest_links=False,
        )

        obj_id = ingester.ingest(doc=self.document)

        obj = self.dal.get(
            orm_class=Qualifier,
            pk=obj_id,
        )  # type: Qualifier

        self.assertEqual(obj.ui, "Q000000981")
        self.assertEqual(obj.name, "diagnostic imaging")
        self.assertEqual(obj.created, datetime.date(2016, 6, 29))
        self.assertEqual(obj.revised, datetime.date(2016, 6, 8))
        self.assertEqual(obj.established, datetime.date(2017, 1, 1))
        self.assertEqual(
            obj.annotation,
            ("subheading only; coordinate with specific imaging technique "
             "if pertinent"),
        )
        self.assertEqual(obj.history_note, "2017(1967)")
        self.assertEqual(
            obj.online_note,
            ("search policy: Online Manual; use: main heading/AB or AB (SH) "
             "or SUBS APPLY AB"),
        )

    def test_ingest_descriptor_relationships(self):
        """ Tests the `ingest` method of the parser class and asserts the
            relationships of the `Descriptor` record.
        """

        ingester = IngesterDocumentQualifier(
            dal=self.dal,
            do_ingest_links=False,
        )

        obj_id = ingester.ingest(doc=self.document)

        obj = self.dal.get_joined(
            orm_class=Qualifier,
            pk=obj_id,
            joined_relationships=["tree_numbers", "concepts"]
        )  # type: Qualifier

        self.assertIsNotNone(obj.tree_numbers)
        self.assertEqual(len(obj.tree_numbers), 2)
        self.assertIsNotNone(obj.concepts)
        self.assertEqual(len(obj.concepts), 2)
