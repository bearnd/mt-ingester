# coding=utf-8

import datetime
import os

from fform.orm_mt import Supplemental
from fform.orm_mt import SupplementalClassType

from mt_ingester.parsers import ParserXmlMeshSupplementals
from mt_ingester.ingesters import IngesterDocumentSupplemental

from tests.dal_mixins import DalMtTestBase
from tests.assets.samples_mesh import get_sample_file
from tests.assets.samples_mesh import EnumMeshFileSample


class IngesterMeshSupplementalTest(DalMtTestBase):
    """ Tests the `IngesterDocumentSupplemental` class."""

    def setUp(self):
        """ Retrieves and parses sample supplementals file and initializes the
            DAL.
        """

        super(IngesterMeshSupplementalTest, self).setUp()

        self.dal = self.setup_dal()

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.SUPP)

        self.parser = ParserXmlMeshSupplementals()

        supplementals = self.parser.parse(filename_xml=self.file.name)
        self.document = next(supplementals)

    def tearDown(self):
        """ Deletes the temporary supplementals file."""

        self.file.close()
        os.remove(self.file.name)

    def test_ingest_supplemental_fields(self):
        """ Tests the `ingest` method of the parser class and asserts the
            top-level fields of the `Supplemental` record.
        """

        ingester = IngesterDocumentSupplemental(
            dal=self.dal,
            do_ingest_links=False,
        )

        obj_id = ingester.ingest(doc=self.document)

        obj = self.dal.get(
            orm_class=Supplemental,
            pk=obj_id,
        )  # type: Supplemental

        self.assertEqual(obj.supplemental_class, SupplementalClassType.ONE)
        self.assertEqual(obj.ui, "C000002")
        self.assertEqual(obj.name, "bevonium")
        self.assertEqual(obj.created, datetime.date(1971, 1, 1))
        self.assertEqual(obj.revised, datetime.date(2018, 9, 24))
        self.assertEqual(obj.note, "structure given in first source")
        self.assertEqual(obj.frequency, "1")

    def test_ingest_supplemental_relationships(self):
        """ Tests the `ingest` method of the parser class and asserts the
            relationships of the `Supplemental` record.
        """

        ingester = IngesterDocumentSupplemental(
            dal=self.dal,
            do_ingest_links=False,
        )

        obj_id = ingester.ingest(doc=self.document)

        obj = self.dal.get_joined(
            orm_class=Supplemental,
            pk=obj_id,
            joined_relationships=["sources", "concepts"]
        )  # type: Supplemental

        self.assertIsNotNone(obj.sources)
        self.assertEqual(len(obj.sources), 2)
        self.assertIsNotNone(obj.concepts)
        self.assertEqual(len(obj.concepts), 2)
