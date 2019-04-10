# coding=utf-8

import abc
import gzip
import datetime
import csv
import sys
from typing import Union, Optional, List, Dict

from lxml import etree

from fform.orm_mt import DescriptorClassType
from fform.orm_mt import RelationNameType
from fform.orm_mt import LexicalTagType
from fform.orm_mt import SupplementalClassType

from mt_ingester.loggers import create_logger
from mt_ingester.parser_utils import convert_yn_boolean


# Set the maximum CSV field size to the system maximum as UMLS files may have
# large fields.
csv.field_size_limit(sys.maxsize)


class ParserBase(object):
    def __init__(self, **kwargs):

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )


class ParserXmlBase(ParserBase):
    def __init__(self, **kwargs):

        super(ParserXmlBase, self).__init__(kwargs=kwargs)

    @staticmethod
    def _et(
        element: etree.Element,
    ) -> Union[str, None]:
        """Extracts the element text (ET)."""

        text = None
        if element is not None:
            text = element.text

        if not text:
            text = None
        else:
            text = text.strip()

        return text

    @staticmethod
    def _eav(element, attribute):
        """Extracts the element attribute value (EAV)"""

        value = None
        if element is not None:
            value = element.get(attribute)

        if not value:
            value = None

        return value

    @staticmethod
    def generate_xml_elements(file_xml, element_tag=None):

        document = etree.iterparse(
            file_xml,
            events=("start", "end"),
            tag=element_tag
        )

        start_tag = None
        for event, element in document:
            if event == 'start' and start_tag is None:
                start_tag = element.tag
            if event == 'end' and element.tag == start_tag:
                yield element
                start_tag = None
                element.clear()

    def open_xml_file(self, filename_xml):

        msg_fmt = "Opening XML file '{0}'".format(filename_xml)
        self.logger.info(msg=msg_fmt)

        if filename_xml.endswith(".gz"):
            file_xml = gzip.GzipFile(filename=filename_xml, mode="rb")
        else:
            file_xml = open(filename_xml, "rb")

        return file_xml

    @abc.abstractmethod
    def parse(self, filename_xml):
        raise NotImplementedError


class ParserXmlMeshBase(ParserXmlBase):
    def __init__(self, **kwargs):

        super(ParserXmlMeshBase, self).__init__(kwargs=kwargs)

    def _ets(
        self,
        element: etree.Element,
    ) -> Union[str, None]:
        """Extracts the text out of an element containing an element of
        `<String>` type.

        Args:
            element (etree.Element): Element containing an element of `<String>`
                type.

        Returns:
            str: The contained text or `None` if undefined.
        """

        if element is None:
            return None

        element_string = element.find("String")

        if element_string is None:
            return None

        str_value = self._et(element_string)

        if not str_value:
            return None

        return str_value

    def _ed(
        self,
        element: etree.Element,
    ) -> Union[datetime.date, None]:
        """Parses a date-element containing elements of type `<Year>`,
        `<Month>`, and `<Day>` and and returns a `datetime.date` object
        representing that date.

        Args:
            element (etree.Element): The date-element.

        Returns:
            datetime.date: The parsed date or `None` if undefined..
        """

        if element is None:
            return None

        element_year = element.find("Year")
        element_month = element.find("Month")
        element_day = element.find("Day")

        if (
            element_year is None or
            element_month is None or
            element_day is None
        ):
            return None

        year = self._et(element_year)
        month = self._et(element_month)
        day = self._et(element_day)

        if not (
            (year and year.isdigit()) and
            (month and month.isdigit()) and
            (day and day.isdigit())
        ):
            return None

        dt = datetime.date(int(year), int(month), int(day))

        return dt

    def parse_tree_number(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<TreeNumber>` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `<TreeNumber>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        tree_number = {
            "TreeNumber": self._et(element),
        }

        return tree_number

    def parse_tree_number_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<TreeNumber>` from
        a `<TreeNumberList>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type
                `<TreeNumberList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        tree_numbers = []

        if element is None:
            return []

        for _element in element.findall("TreeNumber"):
            tree_numbers.append(
                self.parse_tree_number(_element)
            )

        return tree_numbers

    def parse_related_registry_number(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<RelatedRegistryNumber>` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `<RelatedRegistryNumber>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        related_registry_number = {
            "RelatedRegistryNumber": self._et(element),
        }

        return related_registry_number

    def parse_related_registry_number_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<RelatedRegistryNumber>` from a
        `<RelatedRegistryNumberList>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type
                `<RelatedRegistryNumberList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        related_registry_numbers = []

        if element is None:
            return []

        for _element in element.findall("RelatedRegistryNumber"):
            related_registry_numbers.append(
                self.parse_related_registry_number(_element)
            )

        return related_registry_numbers

    def parse_concept_relation(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<ConceptRelation>` and returns the values
        of the contained elements.

        Args:
            element (etree.Element): The element of type `<ConceptRelation>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        concept_relation = {
            "RelationName": RelationNameType.get_member(
                self._eav(element, "RelationName"),
            ),
            "Concept1UI": self._et(element.find("Concept1UI")),
            "Concept2UI": self._et(element.find("Concept2UI")),
        }

        return concept_relation

    def parse_concept_relation_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<ConceptRelation>` from a
        `<ConceptRelationList>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type
                `<ConceptRelationList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        concept_relations = []

        if element is None:
            return []

        for _element in element.findall("ConceptRelation"):
            concept_relations.append(
                self.parse_concept_relation(_element)
            )

        return concept_relations

    def parse_thesaurus_id(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<ThesaurusID>` and returns the values of
        the contained elements.

        Args:
            element (etree.Element): The element of type `<ThesaurusID>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        thesaurus_id = {
            "ThesaurusID": self._et(element),
        }

        return thesaurus_id

    def parse_thesaurus_id_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<ThesaurusID>` from a
        `<ThesaurusIDlist>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type `<ThesaurusIDlist>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        thesaurus_ids = []

        if element is None:
            return []

        for _element in element.findall("ThesaurusID"):
            thesaurus_ids.append(
                self.parse_thesaurus_id(_element)
            )

        return thesaurus_ids

    def parse_term(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<Term>` and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type `<Term>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        term = {
            "ConceptPreferredTermYN": self._eav(
                element,
                "ConceptPreferredTermYN",
            ),
            "IsPermutedTermYN": self._eav(
                element,
                "IsPermutedTermYN",
            ),
            "LexicalTag": LexicalTagType.get_member(
                self._eav(element, "LexicalTag"),
            ),
            "RecordPreferredTermYN": self._eav(
                element,
                "RecordPreferredTermYN",
            ),
            "TermUI": self._et(element.find("TermUI")),
            "String": self._et(element.find("String")),
            "DateCreated": self._ed(element.find("DateCreated")),
            "Abbreviation": self._et(element.find("Abbreviation")),
            "SortVersion": self._et(element.find("SortVersion")),
            "EntryVersion": self._et(element.find("EntryVersion")),
            "ThesaurusIDlist": self.parse_thesaurus_id_list(
                element.find("ThesaurusIDlist"),
            ),
            "TermNote": self._et(element.find("TermNote")),
        }

        term["ConceptPreferredTermYN"] = convert_yn_boolean(
            term["ConceptPreferredTermYN"],
        )

        term["IsPermutedTermYN"] = convert_yn_boolean(term["IsPermutedTermYN"])

        term["RecordPreferredTermYN"] = convert_yn_boolean(
            term["RecordPreferredTermYN"],
        )

        return term

    def parse_term_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<Term>` from a `<TermList>`
        element and returns the values of the contained elements.

        Args:
            element (etree.Element): The element of type `<TermList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        terms = []

        if element is None:
            return []

        for _element in element.findall("Term"):
            terms.append(self.parse_term(_element))

        return terms

    def parse_concept(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<Concept>` and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type `<Concept>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        concept = {
            "PreferredConceptYN": self._eav(element, "PreferredConceptYN"),
            "ConceptUI": self._et(element.find("ConceptUI")),
            "ConceptName": self._ets(element.find("ConceptName")),
            "CASN1Name": self._et(element.find("CASN1Name")),
            "RegistryNumber": self._et(element.find("RegistryNumber")),
            "ScopeNote": self._et(element.find("ScopeNote")),
            "TranslatorsEnglishScopeNote": self._et(
                element.find("TranslatorsEnglishScopeNote"),
            ),
            "TranslatorsScopeNote": self._et(
                element.find("TranslatorsScopeNote"),
            ),
            "RelatedRegistryNumberList":
                self.parse_related_registry_number_list(
                element.find("RelatedRegistryNumberList"),
            ),
            "ConceptRelationList": self.parse_concept_relation_list(
                element.find("ConceptRelationList"),
            ),
            "TermList": self.parse_term_list(element.find("TermList")),
        }

        concept["PreferredConceptYN"] = convert_yn_boolean(
            concept["PreferredConceptYN"],
        )

        return concept

    def parse_concept_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<Concept>` from a
        `<ConceptList>` element and returns the values of the contained
        elements.

        Args:
            element (etree.Element): The element of type `<ConceptList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        concepts = []

        if element is None:
            return []

        for _element in element.findall("Concept"):
            concepts.append(
                self.parse_concept(_element)
            )

        return concepts

    def parse_previous_indexing(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<PreviousIndexing>` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `<PreviousIndexing>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        previous_indexing = {
            "PreviousIndexing": self._et(element),
        }

        return previous_indexing

    def parse_previous_indexing_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<PreviousIndexing>` from
        a `<PreviousIndexingList>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type
                `<PreviousIndexingList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        previous_indexing = []

        if element is None:
            return []

        for _element in element.findall("PreviousIndexing"):
            previous_indexing.append(
                self.parse_previous_indexing(_element)
            )

        return previous_indexing

    def parse_descriptor_reference(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of base-type `<DescriptorReference>` and returns
        the values of the contained elements.

        Note:
            Element with a base-type of `<DescriptorReference>` can be of type
            `<DescriptorReferredTo>`.

        Args:
            element (etree.Element): The element of base-type
                `<DescriptorReference>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        descriptor_reference = {
            "DescriptorUI": self._et(element.find("DescriptorUI")),
            "DescriptorName": self._ets(element.find("DescriptorName")),
        }

        # Remove the `*` that appears in some descriptor reference UIs.
        descriptor_reference["DescriptorUI"] = descriptor_reference[
            "DescriptorUI"
        ].replace("*", "")

        return descriptor_reference

    def parse_qualifier_reference(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of base-type `<QualifierReference>` and returns
        the values of the contained elements.

        Note:
            Element with a base-type of `<QualifierReference>` can be of type
            `<QualifierReferredTo>`.

        Args:
            element (etree.Element): The element of base-type
                `<QualifierReference>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        qualifier_reference = {
            "QualifierUI": self._et(element.find("QualifierUI")),
            "QualifierName": self._ets(element.find("QualifierName")),
        }

        # Remove the `*` that appears in some qualifier reference UIs.
        qualifier_reference["QualifierUI"] = qualifier_reference[
            "QualifierUI"
        ].replace("*", "")

        return qualifier_reference

    def parse_pharmacological_action(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<PharmacologicalAction>` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `<PharmacologicalAction>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        pharmacological_action = {
            "DescriptorReferredTo": self.parse_descriptor_reference(
                element.find("DescriptorReferredTo")
            ),
        }

        return pharmacological_action

    def parse_pharmacological_action_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<PharmacologicalAction>` from
        a `<PharmacologicalActionList>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type
                `<PharmacologicalActionList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        pharmacological_actions = []

        if element is None:
            return []

        for _element in element.findall("PharmacologicalAction"):
            pharmacological_actions.append(
                self.parse_pharmacological_action(_element)
            )

        return pharmacological_actions

    @abc.abstractmethod
    def parse(self, filename_xml):
        raise NotImplementedError


class ParserXmlMeshDescriptors(ParserXmlMeshBase):
    def __init__(self, **kwargs):

        super(ParserXmlMeshDescriptors, self).__init__(kwargs=kwargs)

    def parse_allowable_qualifier(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<AllowableQualifier>` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `<AllowableQualifier>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        allowable_qualifier = {
            "QualifierReferredTo": self.parse_qualifier_reference(
                element.find("QualifierReferredTo")
            ),
            "Abbreviation": self._et(element.find("Abbreviation")),
        }

        return allowable_qualifier

    def parse_allowable_qualifiers_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<AllowableQualifier>` from
        a `<AllowableQualifiersList>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type
                `<AllowableQualifiersList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        allowable_qualifiers = []

        if element is None:
            return []

        for _element in element.findall("AllowableQualifier"):
            allowable_qualifiers.append(
                self.parse_allowable_qualifier(_element)
            )

        return allowable_qualifiers

    def parse_entry_combination(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<EntryCombination>` and returns the values
        of the contained elements.

        Args:
            element (etree.Element): The element of type `<EntryCombination>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        element_ecin = element.find("ECIN")
        element_ecout = element.find("ECOUT")

        entry_combination = {
            "ECIN": {
                "DescriptorReferredTo": self.parse_descriptor_reference(
                    element_ecin.find("DescriptorReferredTo"),
                ),
                "QualifierReferredTo": self.parse_qualifier_reference(
                    element_ecin.find("QualifierReferredTo"),
                ),
            },
            "ECOUT": {
                "DescriptorReferredTo": self.parse_descriptor_reference(
                    element_ecout.find("DescriptorReferredTo"),
                ),
                "QualifierReferredTo": self.parse_qualifier_reference(
                    element_ecout.find("QualifierReferredTo"),
                ),
            },
        }

        return entry_combination

    def parse_entry_combination_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<EntryCombination>` from a
        `<EntryCombinationList>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type
                `<EntryCombinationList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        entry_combinations = []

        if element is None:
            return []

        for _element in element.findall("EntryCombination"):
            entry_combinations.append(
                self.parse_entry_combination(_element)
            )

        return entry_combinations

    def parse_see_related_descriptor(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<SeeRelatedDescriptor>` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `<SeeRelatedDescriptor>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        see_related_descriptor = {
            "DescriptorReferredTo": self.parse_descriptor_reference(
                element.find("DescriptorReferredTo"),
            )
        }

        return see_related_descriptor

    def parse_see_related_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<SeeRelatedDescriptor>` from a
        `<SeeRelatedList>` element and returns the values of the contained
        elements.

        Args:
            element (etree.Element): The element of type `<SeeRelatedList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        see_relateds = []

        if element is None:
            return []

        for _element in element.findall("SeeRelatedDescriptor"):
            see_relateds.append(
                self.parse_see_related_descriptor(_element)
            )

        return see_relateds

    def parse_descriptor_record(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<DescriptorRecord>` and returns the values
        of the contained elements.

        Args:
            element (etree.Element): The element of type `<DescriptorRecord>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        descriptor_record = {
            "DescriptorClass": DescriptorClassType.get_member(
                self._eav(element, "DescriptorClass"),
            ),
            "DescriptorUI": self._et(element.find("DescriptorUI")),
            "DescriptorName": self._ets(element.find("DescriptorName")),
            "DateCreated": self._ed(element.find("DateCreated")),
            "DateRevised": self._ed(element.find("DateRevised")),
            "DateEstablished": self._ed(element.find("DateEstablished")),
            "AllowableQualifiersList": self.parse_allowable_qualifiers_list(
                element.find("AllowableQualifiersList", )
            ),
            "Annotation": self._et(element.find("Annotation")),
            "HistoryNote": self._et(element.find("HistoryNote")),
            "NLMClassificationNumber": self._et(
                element.find("NLMClassificationNumber"),
            ),
            "OnlineNote": self._et(element.find("OnlineNote")),
            "PublicMeSHNote": self._et(element.find("PublicMeSHNote")),
            "PreviousIndexingList": self.parse_previous_indexing_list(
                element.find("PreviousIndexingList"),
            ),
            "EntryCombinationList": self.parse_entry_combination_list(
                element.find("EntryCombinationList"),
            ),
            "SeeRelatedList": self.parse_see_related_list(
                element.find("SeeRelatedList"),
            ),
            "ConsiderAlso": self._et(element.find("ConsiderAlso")),
            "PharmacologicalActionList": self.parse_pharmacological_action_list(
                element.find("PharmacologicalActionList"),
            ),
            "TreeNumberList": self.parse_tree_number_list(
                element.find("TreeNumberList")
            ),
            "ConceptList": self.parse_concept_list(element.find("ConceptList")),
        }

        return descriptor_record

    def parse(self, filename_xml):

        msg = "Parsing MeshTerm Descriptor XML file '{0}'"
        msg_fmt = msg.format(filename_xml)
        self.logger.info(msg=msg_fmt)

        file_xml = self.open_xml_file(filename_xml=filename_xml)

        elements = self.generate_xml_elements(
            file_xml=file_xml,
            element_tag="DescriptorRecord"
        )

        for element in elements:
            descriptor_record = self.parse_descriptor_record(element)

            # Guard against empty documents.
            if not descriptor_record:
                continue

            yield descriptor_record

        file_xml.close()


class ParserXmlMeshQualifiers(ParserXmlMeshBase):
    def __init__(self, **kwargs):

        super(ParserXmlMeshQualifiers, self).__init__(kwargs=kwargs)

    def parse_qualifier_record(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<QualifierRecord>` and returns the values
        of the contained elements.

        Args:
            element (etree.Element): The element of type `<QualifierRecord>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        qualifier_record = {
            "QualifierUI": self._et(element.find("QualifierUI")),
            "QualifierName": self._ets(element.find("QualifierName")),
            "DateCreated": self._ed(element.find("DateCreated")),
            "DateRevised": self._ed(element.find("DateRevised")),
            "DateEstablished": self._ed(element.find("DateEstablished")),
            "Annotation": self._et(element.find("Annotation")),
            "HistoryNote": self._et(element.find("HistoryNote")),
            "OnlineNote": self._et(element.find("OnlineNote")),
            "TreeNumberList": self.parse_tree_number_list(
                element.find("TreeNumberList")
            ),
            "ConceptList": self.parse_concept_list(element.find("ConceptList")),
        }

        return qualifier_record

    def parse(self, filename_xml):

        msg = "Parsing MeshTerm Qualifier XML file '{0}'"
        msg_fmt = msg.format(filename_xml)
        self.logger.info(msg=msg_fmt)

        file_xml = self.open_xml_file(filename_xml=filename_xml)

        elements = self.generate_xml_elements(
            file_xml=file_xml,
            element_tag="QualifierRecord"
        )

        for element in elements:
            qualifier_record = self.parse_qualifier_record(element)

            # Guard against empty documents.
            if not qualifier_record:
                continue

            yield qualifier_record

        file_xml.close()


class ParserXmlMeshSupplementals(ParserXmlMeshBase):
    def __init__(self, **kwargs):

        super(ParserXmlMeshSupplementals, self).__init__(kwargs=kwargs)

    def parse_heading_mapped_to(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<HeadingMappedTo>` and returns the values
        of the contained elements.

        Args:
            element (etree.Element): The element of type `<HeadingMappedTo>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        heading_mapped_to = {
            "DescriptorReferredTo": self.parse_descriptor_reference(
                element.find("DescriptorReferredTo"),
            ),
            "QualifierReferredTo": self.parse_qualifier_reference(
                element.find("QualifierReferredTo"),
            ),
        }

        return heading_mapped_to

    def parse_heading_mapped_to_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<HeadingMappedTo>` from a
        `<HeadingMappedToList>` element and returns the values of the contained
        elements.

        Args:
            element (etree.Element): The element of type
                `<HeadingMappedToList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        heading_mapped_tos = []

        if element is None:
            return []

        for _element in element.findall("HeadingMappedTo"):
            heading_mapped_tos.append(
                self.parse_heading_mapped_to(_element)
            )

        return heading_mapped_tos

    def parse_indexing_information(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<IndexingInformation>` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type
                `<IndexingInformation>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        indexing_information = {
            "DescriptorReferredTo": self.parse_descriptor_reference(
                element.find("DescriptorReferredTo"),
            ),
            "QualifierReferredTo": self.parse_qualifier_reference(
                element.find("QualifierReferredTo"),
            ),
        }

        return indexing_information

    def parse_indexing_information_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<IndexingInformation>` from a
        `<IndexingInformationList>` element and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type
                `<IndexingInformationList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        indexing_informations = []

        if element is None:
            return []

        for _element in element.findall("IndexingInformation"):
            indexing_informations.append(
                self.parse_indexing_information(_element)
            )

        return indexing_informations

    def parse_source(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<Source>` and returns the values of the
        contained elements.

        Args:
            element (etree.Element): The element of type `<Source>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        source = {
            "Source": self._et(element),
        }

        return source

    def parse_source_list(
        self,
        element: etree.Element,
    ) -> list:
        """Extracts and parses elements of type `<Source>` from a `<SourceList>`
        element and returns the values of the contained elements.

        Args:
            element (etree.Element): The element of type `<SourceList>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        sources = []

        if element is None:
            return []

        for _element in element.findall("Source"):
            sources.append(self.parse_source(_element))

        return sources

    def parse_supplemental_record(
        self,
        element: etree.Element,
    ) -> dict:
        """Parses an element of type `<SupplementalRecord>` and returns the
        values of the contained elements.

        Args:
            element (etree.Element): The element of type `<SupplementalRecord>`.

        Returns:
            dict: The parsed values of the contained elements.
        """

        if element is None:
            return {}

        supplemental_record = {
            "SupplementalClass": SupplementalClassType.get_member(
                self._eav(element, "SCRClass"),
            ),
            "SupplementalRecordUI": self._et(
                element.find("SupplementalRecordUI"),
            ),
            "SupplementalRecordName": self._ets(
                element.find("SupplementalRecordName"),
            ),
            "DateCreated": self._ed(element.find("DateCreated")),
            "DateRevised": self._ed(element.find("DateRevised")),
            "Note": self._et(element.find("Note")),
            "Frequency": self._et(element.find("Frequency")),
            "PreviousIndexingList": self.parse_previous_indexing_list(
                element.find("PreviousIndexingList"),
            ),
            "HeadingMappedToList": self.parse_heading_mapped_to_list(
                element.find("HeadingMappedToList"),
            ),
            "IndexingInformationList": self.parse_indexing_information_list(
                element.find("IndexingInformationList"),
            ),
            "PharmacologicalActionList": self.parse_pharmacological_action_list(
                element.find("PharmacologicalActionList"),
            ),
            "SourceList": self.parse_source_list(element.find("SourceList")),
            "ConceptList": self.parse_concept_list(element.find("ConceptList")),
        }

        return supplemental_record

    def parse(self, filename_xml):

        msg = "Parsing MeshTerm Supplemental XML file '{0}'"
        msg_fmt = msg.format(filename_xml)
        self.logger.info(msg=msg_fmt)

        file_xml = self.open_xml_file(filename_xml=filename_xml)

        elements = self.generate_xml_elements(
            file_xml=file_xml,
            element_tag="SupplementalRecord"
        )

        for element in elements:
            supplemental_record = self.parse_supplemental_record(element)

            # Guard against empty documents.
            if not supplemental_record:
                continue

            yield supplemental_record

        file_xml.close()


class ParserUmlsSat(ParserBase):
    """ Class used to parse the UMLS MRSAT.rrf file and create a map between
        UMLS CUIs and MeSH descriptor IDs.
    """

    # Define the header field names of the MRSAT.rrf file as defined in
    # https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T
    # .simple_concept_and_atom_attribute/?report=objectonly
    fieldnames_mrsat = [
        "CUI",
        "LUI",
        "SUI",
        "METAUI",
        "STYPE",
        "CODE",
        "ATUI",
        "SATUI",
        "ATN",
        "SAB",
        "ATV",
        "SUPPRESS",
        "CVF",
    ]

    def __init__(
        self,
        **kwargs: dict
    ):
        """ Constructor and initialization."""
        super(ParserUmlsSat, self).__init__(kwargs=kwargs)

    def parse(
        self,
        filename_mrsat_rrf: str,
    ) -> Dict[str, str]:
        """ Parses the MRSAT.rrf file and creates a dictionary keyed on UMLS
            CUIs with values of MeSH descriptor IDs.

        Args:
            filename_mrsat_rrf (str): Path to the MRSAT.rrf file.

        Returns:
            Dict[str, str]: Result dictionary keyed on UMLS CUIs with values of
                MeSH descriptor IDs.
        """

        msg = "Parsing UMLS MRSAT RRF file '{0}'"
        msg_fmt = msg.format(filename_mrsat_rrf)
        self.logger.info(msg=msg_fmt)

        # Iterate over the MRSAT.rrf lines and create a dictionary mapping UMLS
        # concept IDs (CUIs) to MeSH descriptor IDs (DUIs).
        map_cui_dui = {}
        with open(filename_mrsat_rrf, "r") as finp:
            reader = csv.DictReader(
                finp,
                fieldnames=self.fieldnames_mrsat,
                delimiter="|",
            )

            for entry in reader:
                # Skip entries that don't establish the relationship between
                # a UMLS concept and a MeSH descriptor.
                if not entry.get("ATN") == "MESH_DUI":
                    continue

                # Skip entries that don't define a value for CUI or ATV.
                if not entry.get("CUI") or not entry.get("ATV"):
                    continue

                map_cui_dui[entry["CUI"]] = entry["ATV"]

        return map_cui_dui


class ParserUmlsConso(ParserBase):
    """ Class used to parse the UMLS MRCONSO.rrf file and collect a unique list
        of synonyms for the different MeSH descriptors defined in the file.

    Notes:
        This parser also requires the MRSAT.rrf file in order to establlish a
        relationship between the UMLS concept IDs and the MeSH descriptor IDs.
    """

    # Define the header field names of the MRCONSO.rrf file as defined in
    # https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T
    # .concept_names_and_sources_file_mr/?report=objectonly
    fieldnames_mrconso = [
        "CUI",
        "LAT",
        "TS",
        "LUI",
        "STT",
        "SUI",
        "ISPREF",
        "AUI",
        "SAUI",
        "SCUI",
        "SDUI",
        "SAB",
        "TTY",
        "CODE",
        "STR",
        "SRL",
        "SUPPRESS",
        "CVF",
    ]

    def __init__(
        self,
        **kwargs: dict
    ):
        """ Constructor and initialization."""

        super(ParserUmlsConso, self).__init__(kwargs=kwargs)

    def parse(
        self,
        filename_mrsat_rrf: str,
        filename_mrconso_rrf: str,
    ) -> Dict[str, List[str]]:
        """ Parses the MRSAT.rrf and MRCONSO.rrf files and creates a dictionary
            keyed on MeSH descriptor IDs with values of lists of synonyms.

        Args:
            filename_mrconso_rrf (str): Path to the MRCONSO.rrf file.
            filename_mrsat_rrf (str): Path to the MRSAT.rrf file.

        Returns:
            Dict[str, List[str]]: Result dictionary keyed on MeSH
            descriptor IDs with values of lists of synonyms.
        """

        # Create a `ParserUmlsSat` parser and use it to parse the MRSAT.RRF file
        # to create a map between CUIs and MeSH descriptor IDs.
        parser_mrsat = ParserUmlsSat()
        map_cui_dui = parser_mrsat.parse(filename_mrsat_rrf=filename_mrsat_rrf)

        msg = "Parsing UMLS MRCONSO RRF file '{0}'"
        msg_fmt = msg.format(filename_mrconso_rrf)
        self.logger.info(msg=msg_fmt)

        dui_synonyms = {}
        with open(filename_mrconso_rrf, "r") as finp:
            reader = csv.DictReader(
                finp,
                fieldnames=self.fieldnames_mrconso,
                delimiter="|",
            )

            for entry in reader:
                # Skip that do not refer to a MeSH entity.
                if not entry.get("SDUI"):
                    continue

                # Skip non-Engish entries.
                if entry.get("LAT") != "ENG":
                    continue

                if entry["CUI"] not in map_cui_dui.keys():
                    continue

                dui = map_cui_dui[entry["CUI"]]

                dui_synonyms.setdefault(dui, []).append(entry["STR"])

        # Lowercase all synonyms
        for dui, synonyms in dui_synonyms.items():
            dui_synonyms[dui] = [synonym.lower() for synonym in synonyms]

        # Deduplicate the synonyms.
        for dui, synonyms in dui_synonyms.items():
            dui_synonyms[dui] = list(set(synonyms))

        return dui_synonyms


class ParserUmlsDef(ParserBase):
    """ Class used to parse the UML MRDEF.rrf file and collect a dictionary of
        definitions for the different MeSH entities.

    Notes:
        This parser also requires the MRSAT.rrf file in order to establlish a
        relationship between the UMLS concept IDs and the MeSH UIDs.
    """

    # Define the header field names of the MRDEF.rrf file as defined in
    # https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T
    # .definitions_file_mrdef_rrf/?report=objectonly
    fieldnames_mrdef = [
        "CUI",
        "AUI",
        "ATUI",
        "SATUI",
        "SAB",
        "DEF",
        "SUPPRESS",
        "CVF",
    ]

    def __init__(
        self,
        **kwargs: dict
    ):
        """ Constructor and initialization."""

        super(ParserUmlsDef, self).__init__(kwargs=kwargs)

    def parse(
        self,
        filename_mrdef_rrf: str,
        filename_mrsat_rrf: str,
        sources_include: Optional[List[str]] = None,
        sources_exclude: Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, List[str]]]:
        """ Parses the MRSAT.rrf and MRDEF.rrf files and creates a dictionary
            keyed on MeSH descriptor IDs with values of dictionaries of
            definitions which are themselves keyed on the definition source name
            and valued with a list of the definitions themselves.

        Notes:
            A MeSH descriptor may have multiple definitions defined under the
            same source.

        Args:
            filename_mrdef_rrf (str): Path to the MRDEF.rrf file.
            filename_mrsat_rrf (str): Path to the MRSAT.rrf file.
            sources_include (Optional[List[str]] = None): A list of source names
                to which the results will be limited to. Should *not* be used in
                conjunction with the `sources_exclude` argument.
            sources_exclude (Optional[List[str]] = None): A list of source names
                to be excluded from the results. Should *not* be used in
                conjunction with the `sources_include` argument.

        Returns:
            Dict[str, Dict[str, List[str]]]: Result dictionary keyed on MeSH
            descriptor IDs with values of dictionaries of definitions which are
            themselves keyed on the definition source name and valued with a
            list of the definitions themselves.
        """

        # Create a `ParserUmlsSat` parser and use it to parse the MRSAT.RRF file
        # to create a map between CUIs and MeSH IDs.
        parser_mrsat = ParserUmlsSat()
        map_cui_dui = parser_mrsat.parse(filename_mrsat_rrf=filename_mrsat_rrf)

        msg = "Parsing UMLS MRDEF RRF file '{0}'"
        msg_fmt = msg.format(filename_mrdef_rrf)
        self.logger.info(msg=msg_fmt)

        dui_definitions = {}
        with open(filename_mrdef_rrf, "r") as finp:
            reader = csv.DictReader(
                finp,
                fieldnames=self.fieldnames_mrdef,
                delimiter="|",
            )

            for entry in reader:
                # Skip entries whose CUIs don't refer to MeSH descriptors as
                # defined in the `map_cui_dui` dictionary.
                if entry.get("CUI") not in map_cui_dui.keys():
                    continue

                # Skip entries that don't define a definition source.
                if not entry.get("SAB"):
                    continue

                # Skip entries that don't define a definition.
                if not entry.get("DEF"):
                    continue

                # If `sources_include` is defined then skip entries with a
                # source not present in `sources_include`.
                if sources_include is not None:
                    if entry["SAB"] not in sources_include:
                        continue

                # If `sources_exclude` is defined then skip entries with a
                # source present in `sources_exclude`.
                if sources_exclude is not None:
                    if entry["SAB"] in sources_exclude:
                        continue

                # Retrieve the list of definitions for this MeSH descriptor and
                # definition source.
                definitions = dui_definitions.setdefault(
                    map_cui_dui[entry["CUI"]],
                    {},
                ).setdefault(entry["SAB"], [])

                # Add the new definition if it doesn't already exist in the
                # list.
                if entry["DEF"] not in definitions:
                    definitions.append(entry["DEF"])

        return dui_definitions
