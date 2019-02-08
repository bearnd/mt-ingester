# coding=utf-8

import os
import datetime
from typing import List

from fform.orm_mt import DescriptorClassType
from fform.orm_mt import DescriptorSynonym
from fform.orm_mt import DescriptorDefinition
from fform.dals_mt import DalMesh

from mt_ingester.parsers import ParserUmlsConso
from mt_ingester.parsers import ParserUmlsDef
from mt_ingester.ingesters import IngesterUmlsConso
from mt_ingester.ingesters import IngesterUmlsDef

from tests.dal_mixins import DalMtTestBase
from tests.assets.samples_umls import get_sample_file
from tests.assets.samples_umls import EnumUmlsFileSample


def _create_fake_descriptor(
    dal: DalMesh,
    ui: str,
) -> int:
    """ Adds a fake `Descriptor` record with a given UI to the DB and
        returns its ID.

    Args:
        dal (DalMesh): The DalMesh class that faciliates interaction with the
            DB.
        ui (str): The UI of the fake descriptor to be added.

    Returns:
        int: The PK ID of the added descriptor.
    """

    return dal.iodu_descriptor(
        descriptor_class=DescriptorClassType.ONE,
        ui=ui,
        name=ui,
        created=datetime.date.today(),
        revised=datetime.date.today(),
        established=datetime.date.today(),
        annotation="annotation",
        history_note="history_note",
        nlm_classification_number="nlm_classification_number",
        online_note="online_note",
        public_mesh_note="public_mesh_note",
        consider_also="consider_also",
    )


class IngesterUmlsConsoTest(DalMtTestBase):
    """ Tests the `IngesterUmlsConso` class."""

    def setUp(self):
        """ Parses the MRCONSO.RRF data and instantiates the ingester."""

        super(IngesterUmlsConsoTest, self).setUp()

        self.dal = self.setup_dal()

        self.file_mrsat = get_sample_file(
            umls_file_type=EnumUmlsFileSample.MRSAT,
        )
        self.file_mrconso = get_sample_file(
            umls_file_type=EnumUmlsFileSample.MRCONSO,
        )

        self.parser = ParserUmlsConso()
        self.dui_synonyms = self.parser.parse(
            filename_mrsat_rrf=self.file_mrsat.name,
            filename_mrconso_rrf=self.file_mrconso.name,
        )

        self.ingester = IngesterUmlsConso(dal=self.dal)

    def tearDown(self):
        """ Deletes the temporary MRSAT.RRF and MRCONSO.RRF files."""

        super(IngesterUmlsConsoTest, self).tearDown()

        os.remove(self.file_mrsat.name)
        os.remove(self.file_mrconso.name)

    def test_parse(self):
        """ Tests the `parse` method of the parser class."""

        dui_ids = []
        for dui in self.dui_synonyms.keys():
            dui_ids.append(_create_fake_descriptor(dal=self.dal, ui=dui))

        self.ingester.ingest(document=self.dui_synonyms)

        for dui_id, synonyms_refr in zip(dui_ids, self.dui_synonyms.values()):
            synonym_objs = self.dal.bget_by_attr(
                orm_class=DescriptorSynonym,
                attr_name="descriptor_id",
                attr_values=[dui_id],
            )  # type: List[DescriptorSynonym]
            synonyms_eval = [
                synonym_obj.synonym for synonym_obj in synonym_objs
            ]

            self.assertListEqual(synonyms_eval, synonyms_refr)


class IngesterUmlsDefTest(DalMtTestBase):
    """ Tests the `IngesterUmlsDef` class."""

    def setUp(self):
        """ Parses the MRDEF.RRF data and instantiates the ingester."""

        super(IngesterUmlsDefTest, self).setUp()

        self.dal = self.setup_dal()

        self.file_mrsat = get_sample_file(
            umls_file_type=EnumUmlsFileSample.MRSAT,
        )
        self.file_mrdef = get_sample_file(
            umls_file_type=EnumUmlsFileSample.MRDEF,
        )

        self.parser = ParserUmlsDef()
        self.dui_definitions = self.parser.parse(
            filename_mrsat_rrf=self.file_mrsat.name,
            filename_mrdef_rrf=self.file_mrdef.name,
        )

        self.ingester = IngesterUmlsDef(dal=self.dal)

    def tearDown(self):
        """ Deletes the temporary MRSAT.RRF and MRDEF.RRF files."""

        super(IngesterUmlsDefTest, self).tearDown()

        os.remove(self.file_mrsat.name)
        os.remove(self.file_mrdef.name)

    def test_parse(self):
        """ Tests the `parse` method of the parser class."""

        dui_ids = []
        for dui in self.dui_definitions.keys():
            dui_ids.append(_create_fake_descriptor(dal=self.dal, ui=dui))

        self.ingester.ingest(document=self.dui_definitions)

        for dui_id, data in zip(dui_ids, self.dui_definitions.values()):
            definition_objs = self.dal.bget_by_attr(
                orm_class=DescriptorDefinition,
                attr_name="descriptor_id",
                attr_values=[dui_id],
            )  # type: List[DescriptorDefinition]

            definitions_eval = [
                definition_obj.definition for definition_obj in definition_objs
            ]

            definitions_refr = []
            for k, v in data.items():
                definitions_refr.extend(v)

            self.assertListEqual(definitions_eval, definitions_refr)
