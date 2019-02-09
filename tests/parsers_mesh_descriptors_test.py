# coding=utf-8

import os
import datetime
import unittest

from fform.orm_mt import DescriptorClassType
from fform.orm_mt import RelationNameType
from fform.orm_mt import LexicalTagType

from mt_ingester.parsers import ParserXmlMeshDescriptors

from tests.assets.samples_mesh import get_sample_file
from tests.assets.samples_mesh import EnumMeshFileSample


class ParserMeshDescriptorsTest(unittest.TestCase):
    """ Tests the `ParserXmlMeshDescriptors` class."""

    def setUp(self):
        """ Retrieves a sample descriptors file and instantiates the parser."""

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.DESC)

        self.parser = ParserXmlMeshDescriptors()

        self.file_xml = self.parser.open_xml_file(filename_xml=self.file.name)

        elements = self.parser.generate_xml_elements(
            file_xml=self.file_xml,
            element_tag="DescriptorRecord"
        )

        self.descriptor_element = next(elements)

    def tearDown(self):
        """ Deletes the temporary descriptors file."""

        self.file.close()
        self.file_xml.close()
        os.remove(self.file.name)

    def test_parse_descriptor_record(self):
        """ Tests the `parse_descriptor_record` method and asserts the values
            on the top-level fields.
        """

        record = self.parser.parse_descriptor_record(
            element=self.descriptor_element,
        )

        self.assertEqual(record["DescriptorClass"], DescriptorClassType.ONE)
        self.assertEqual(record["DescriptorUI"], "D000001")
        self.assertEqual(record["DescriptorName"], "Calcimycin")
        self.assertEqual(record["DateCreated"], datetime.date(1974, 11, 19))
        self.assertEqual(record["DateRevised"], datetime.date(2016, 5, 27))
        self.assertEqual(record["DateEstablished"], datetime.date(1984, 1, 1))
        # Skipping `AllowableQualifiersList`. Covered in later test.
        self.assertEqual(
            record["Annotation"],
            "for use to kill or control insects...",
        )
        self.assertEqual(
            record["HistoryNote"],
            "91(75); was A 23187 1975-90 (see under ANTIBIOTICS 1975-83)",
        )
        self.assertEqual(record["NLMClassificationNumber"], "QV 175")
        self.assertEqual(
            record["OnlineNote"],
            "use CALCIMYCIN to search A 23187 1975-90",
        )
        self.assertEqual(
            record["PublicMeSHNote"],
            "91; was A 23187 1975-90 (see under ANTIBIOTICS 1975-83)",
        )
        # Skipping `PreviousIndexingList`. Covered in later test.
        # Skipping `EntryCombinationList`. Covered in later test.
        # Skipping `SeeRelatedList`. Covered in later test.
        self.assertEqual(
            record["ConsiderAlso"],
            "consider also terms at PROCT-",
        )
        # Skipping `PharmacologicalActionList`. Covered in later test.
        # Skipping `TreeNumberList`. Covered in later test.
        # Skipping `ConceptList`. Covered in later test.

    def test_parse_allowable_qualifiers_list(self):
        """ Tests the `parse_allowable_qualifiers_list` method."""

        records = self.parser.parse_allowable_qualifiers_list(
            self.descriptor_element.find("AllowableQualifiersList")
        )

        self.assertEqual(len(records), 3)

        self.assertListEqual(
            records,
            [
                {
                    'Abbreviation': 'IP',
                    'QualifierReferredTo': {
                        'QualifierName': 'isolation & purification',
                        'QualifierUI': 'Q000302'
                    }
                },
                {
                    'Abbreviation': 'IM',
                    'QualifierReferredTo': {'QualifierName': 'immunology',
                                            'QualifierUI': 'Q000276'
                                            }
                },
                {
                    'Abbreviation': 'PK',
                    'QualifierReferredTo': {
                        'QualifierName': 'pharmacokinetics',
                        'QualifierUI': 'Q000493'
                    }
                }
            ]
        )

    def test_parse_previous_indexing_list(self):
        """ Tests the `parse_previous_indexing_list` method."""

        records = self.parser.parse_previous_indexing_list(
            self.descriptor_element.find("PreviousIndexingList")
        )

        self.assertListEqual(
            records,
            [
                {'PreviousIndexing': 'Antibiotics (1973-1974)'},
                {'PreviousIndexing': 'Carboxylic Acids (1973-1974)'}
            ]
        )

    def test_parse_entry_combination_list(self):
        """ Tests the `parse_entry_combination_list` method."""

        records = self.parser.parse_entry_combination_list(
            self.descriptor_element.find("EntryCombinationList")
        )

        self.assertListEqual(
            records,
            [
                {
                    'ECIN': {
                        'DescriptorReferredTo': {
                            'DescriptorName': 'Abortion, Spontaneous',
                            'DescriptorUI': 'D000022'
                        },
                        'QualifierReferredTo': {
                            'QualifierName': 'veterinary',
                            'QualifierUI': 'Q000662'
                        }
                    },
                    'ECOUT': {
                        'DescriptorReferredTo': {
                            'DescriptorName': 'Abortion, Veterinary',
                            'DescriptorUI': 'D000034'
                        },
                        'QualifierReferredTo': {}
                    }
                }
            ]
        )

    def test_parse_see_related_list(self):
        """ Tests the `parse_see_related_list` method."""

        records = self.parser.parse_see_related_list(
            self.descriptor_element.find("SeeRelatedList")
        )

        self.assertListEqual(
            records,
            [
                {
                    'DescriptorReferredTo': {
                        'DescriptorName': 'Empyema',
                        'DescriptorUI': 'D004653'
                    }
                },
                {
                    'DescriptorReferredTo': {
                        'DescriptorName': 'Intestinal Absorption',
                        'DescriptorUI': 'D007408'
                    }
                }
            ]
        )

    def test_parse_pharmacological_action_list(self):
        """ Tests the `parse_pharmacological_action_list` method."""

        records = self.parser.parse_pharmacological_action_list(
            self.descriptor_element.find("PharmacologicalActionList")
        )

        self.assertListEqual(
            records,
            [
                {
                    'DescriptorReferredTo': {
                        'DescriptorName': 'Anti-Bacterial Agents',
                        'DescriptorUI': 'D000900'
                    }
                },
                {
                    'DescriptorReferredTo': {
                        'DescriptorName': 'Calcium Ionophores',
                        'DescriptorUI': 'D061207'
                    }
                }
            ]
        )

    def test_parse_tree_number_list(self):
        """ Tests the `parse_tree_number_list` method."""

        records = self.parser.parse_tree_number_list(
            self.descriptor_element.find("TreeNumberList")
        )

        self.assertListEqual(
            records,
            [
                {'TreeNumber': 'D03.633.100.221.173'},
                {'TreeNumber': 'D03.633.100.221.174'}
            ]
        )

    def test_parse_concept_list(self):
        """ Tests the `parse_concept_list` method without actually asserting
            the contents of the returned records.
        """

        records = self.parser.parse_concept_list(
            self.descriptor_element.find("ConceptList")
        )

        self.assertEqual(len(records), 2)

    def test_parse_concept(self):
        """ Tests the `parse_descriptor_record` method and asserts the values
            on the top-level fields.
        """

        element_concept_list = self.descriptor_element.find("ConceptList")
        element = element_concept_list.find("Concept")

        record = self.parser.parse_concept(element)

        self.assertEqual(record["PreferredConceptYN"], True)
        self.assertEqual(record["ConceptUI"], "M0000001")
        self.assertEqual(record["ConceptName"], "Calcimycin")
        self.assertEqual(
            record["CASN1Name"],
            "4-Benzoxazolecarboxylic acid,5-(methylamino)-2-((3,9,11-"
            "trimethyl-8-(1-methyl-2-oxo-2-(1H-pyrrol-2-yl)ethyl)-1,7-"
            "dioxaspiro(5.5)undec-2-yl)methyl)-, (6S-(6alpha(2S*,3S*),"
            "8beta(R*),9beta,11alpha))-"
        )
        self.assertEqual(record["RegistryNumber"], "37H9VM9WZL")
        self.assertEqual(
            record["ScopeNote"],
            "An ionophorous, polyether antibiotic from Streptomyces "
            "chartreusensis. It binds and transports CALCIUM and other "
            "divalent cations across membranes and uncouples oxidative "
            "phosphorylation while inhibiting ATPase of rat liver "
            "mitochondria. The substance is used mostly as a biochemical "
            "tool to study the role of divalent cations in various biological "
            "systems."
        )
        self.assertEqual(record["TranslatorsEnglishScopeNote"], None)
        self.assertEqual(record["TranslatorsScopeNote"], None)
        # Skipping `RelatedRegistryNumberList`. Covered in later test.
        # Skipping `ConceptRelationList`. Covered in later test.
        # Skipping `TermList`. Covered in later test.

    def test_parse_related_registry_number_list(self):
        """ Tests the `parse_related_registry_number_list` method."""

        element_concept_list = self.descriptor_element.find("ConceptList")
        concept_element = element_concept_list.find("Concept")

        records = self.parser.parse_related_registry_number_list(
            concept_element.find("RelatedRegistryNumberList")
        )

        self.assertListEqual(
            records,
            [
                {'RelatedRegistryNumber': '52665-69-7 (Calcimycin)'},
                {'RelatedRegistryNumber': '3383-96-8 (Temefos)'}
            ]
        )

    def test_parse_concept_relation_list(self):
        """ Tests the `parse_concept_relation_list` method."""

        element_concept_list = self.descriptor_element.find("ConceptList")
        concept_element = element_concept_list.find("Concept")

        records = self.parser.parse_concept_relation_list(
            concept_element.find("ConceptRelationList")
        )

        self.assertListEqual(
            records,
            [
                {
                    'Concept1UI': 'M0000002',
                    'Concept2UI': 'M0352201',
                    'RelationName': RelationNameType.NRW,
                },
                {
                    'Concept1UI': 'M0000002',
                    'Concept2UI': 'M0352200',
                    'RelationName': RelationNameType.NRW,
                }
            ]
        )

    def test_parse_term_list(self):
        """ Tests the `parse_term_list` method without actually asserting the
            contents of the returned records.
        """

        element_concept_list = self.descriptor_element.find("ConceptList")
        concept_element = element_concept_list.find("Concept")

        records = self.parser.parse_term_list(concept_element.find("TermList"))

        self.assertEqual(len(records), 2)

    def test_parse_term(self):
        """ Tests the `parse_term` method."""

        element_concept_list = self.descriptor_element.find("ConceptList")
        concept_element = element_concept_list.find("Concept")
        element_term_list = concept_element.find("TermList")
        term_element = element_term_list.find("Term")

        record = self.parser.parse_term(term_element)

        self.assertEqual(record["ConceptPreferredTermYN"], True)
        self.assertEqual(record["IsPermutedTermYN"], False)
        self.assertEqual(record["LexicalTag"], LexicalTagType.NON)
        self.assertEqual(record["RecordPreferredTermYN"], True)
        self.assertEqual(record["TermUI"], "T000002")
        self.assertEqual(record["String"], "Calcimycin")
        self.assertEqual(record["DateCreated"], datetime.date(1999, 1, 1))
        self.assertEqual(record["SortVersion"], "AMPHETAMINE A D")
        self.assertEqual(record["EntryVersion"], "ABDOMINAL INJ")
        # Skipping `ThesaurusIDlist`. Covered in later test.
        self.assertEqual(record["TermNote"], None)

    def test_parse_thesaurus_id_list(self):
        """ Tests the `parse_thesaurus_id_list` method."""

        element_concept_list = self.descriptor_element.find("ConceptList")
        concept_element = element_concept_list.find("Concept")
        element_term_list = concept_element.find("TermList")
        term_element = element_term_list.find("Term")

        records = self.parser.parse_thesaurus_id_list(
            term_element.find("ThesaurusIDlist")
        )

        self.assertListEqual(
            records,
            [
                {'ThesaurusID': 'FDA SRS (2014)'},
                {'ThesaurusID': 'NLM (1975)'}
            ]
        )

    def test_parse(self):
        """ Tests the `parse` method."""

        self.file = get_sample_file(mesh_file_type=EnumMeshFileSample.DESC)

        records = self.parser.parse(self.file.name)

        self.assertEqual(len(list(records)), 1)
