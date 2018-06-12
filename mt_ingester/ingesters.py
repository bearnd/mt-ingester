# coding=utf-8

import abc
import hashlib
from typing import Union

from fform.orm_mt import Concept
from fform.orm_mt import Descriptor
from fform.orm_mt import Qualifier
from fform.orm_mt import Supplemental
from fform.orm_mt import EntryCombinationType
from fform.dals_mt import DalMesh

from mt_ingester.loggers import create_logger
from mt_ingester.utils import log_ingestion_of_document


class IngesterDocumentBase(object):
    def __init__(
        self,
        dal,
        do_ingest_links: bool,
        **kwargs
    ):

        # Internalize arguments.
        self.do_ingest_links = do_ingest_links
        self.dal = dal

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    @staticmethod
    def _get_dref_ui(
        doc: dict
    ) -> Union[str, None]:
        """Retrieves the UI from a descriptor reference.

        Args:
            doc (dict): The descriptor reference.

        Returns:
            str: The descriptor UI or `None` if undefined.
        """

        if not doc:
            return None

        ui = doc.get("DescriptorReferredTo", {}).get("DescriptorUI")

        return ui

    @staticmethod
    def _get_qref_ui(
        doc: dict
    ) -> Union[str, None]:
        """Retrieves the UI from a qualifier reference.

        Args:
            doc (dict): The qualifier reference.

        Returns:
            str: The qualifier UI or `None` if undefined.
        """

        if not doc:
            return None

        ui = doc.get("QualifierReferredTo", {}).get("QualifierUI")

        return ui

    @log_ingestion_of_document(document_name="TreeNumber")
    def ingest_tree_number(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<TreeNumber>` and creates a
        `TreeNumber` record.

        Args:
            doc (dict): The element of type `<TreeNumber>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `TreeNumber` record.
        """

        if not doc:
            return None

        tree_number = doc.get("TreeNumber")
        # Upsert the `TreeNumber` record.
        tree_number_id = self.dal.iodi_tree_number(
            tree_number=tree_number
        )

        return tree_number_id

    @log_ingestion_of_document(document_name="Term")
    def ingest_term(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<Term>` and creates a `Term`
        record.

        Args:
            doc (dict): The element of type `<Term>` parsed into a dictionary.

        Returns:
             int: The primary-key ID of the `Term` record.
        """

        if not doc:
            return None

        term_id = self.dal.iodu_term(
            ui=doc.get("TermUI"),
            name=doc.get("String"),
            created=doc.get("DateCreated"),
            abbreviation=doc.get("Abbreviation"),
            sort_version=doc.get("SortVersion"),
            entry_version=doc.get("EntryVersion"),
            note=doc.get("TermNote"),
        )

        # Upsert `ThesaurusID` and `TermThesaurusId` records.
        doc_thesaurus_ids = doc.get("ThesaurusIDlist")
        for doc_thesaurus_id in doc_thesaurus_ids:
            # Upsert `ThesaurusID` record.
            thesaurus_id_id = self.dal.iodi_thesaurus_id(
                thesaurus_id=doc_thesaurus_id.get("ThesaurusID")
            )
            # Upsert `TermThesaurusId` record.
            self.dal.iodi_term_thesaurus_id(
                term_id=term_id,
                thesaurus_id_id=thesaurus_id_id,
            )

        return term_id

    @log_ingestion_of_document(document_name="Concept")
    def ingest_concept(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<Concept>` and creates a
        `Concept` record.

        Args:
            doc (dict): The element of type `<Concept>` parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Concept` record.
        """

        if not doc:
            return None

        concept_id = self.dal.iodu_concept(
            ui=doc.get("ConceptUI"),
            name=doc.get("ConceptName"),
            casn1_name=doc.get("CASN1Name"),
            registry_number=doc.get("RegistryNumber"),
            scope_note=doc.get("ScopeNote"),
            translators_english_scope_note=doc.get(
                "TranslatorsEnglishScopeNote",
            ),
            translators_scope_note=doc.get("TranslatorsScopeNote"),
        )

        # Upsert `ConceptRelatedConcept` records.
        if self.do_ingest_links:
            for doc_concept_relations in doc.get("ConceptRelationList"):
                self.dal.iodu_concept_related_concept(
                    concept_id=self.dal.get_by_attrs(
                        Concept,
                        {"ui": doc_concept_relations.get("Concept1UI")}
                    ).concept_id,
                    related_concept_id=self.dal.get_by_attrs(
                        Concept,
                        {"ui": doc_concept_relations.get("Concept2UI")}
                    ).concept_id,
                    relation_name=doc_concept_relations.get("RelationName"),
                )

        # Upsert `Term` and `ConceptTerm` records.
        doc_terms = doc.get("TermList")
        for doc_term in doc_terms:
            # Upsert `Term` record.
            term_id = self.ingest_term(doc_term)
            # Upsert `ConceptTerm` record.
            self.dal.iodu_concept_term(
                concept_id=concept_id,
                term_id=term_id,
                is_concept_preferred_term=doc_term.get(
                    "ConceptPreferredTermYN",
                ),
                is_permuted_term=doc_term.get("IsPermutedTermYN"),
                lexical_tag=doc_term.get("LexicalTag"),
                is_record_preferred_term=doc_term.get("RecordPreferredTermYN"),
            )

        return concept_id

    @abc.abstractmethod
    def ingest(
        self,
        document: dict
    ):
        raise NotImplementedError


class IngesterDocumentQualifier(IngesterDocumentBase):
    """Class to ingest a parsed XML `<QualifierRecord>` document."""

    def __init__(
        self,
        dal: DalMesh,
        do_ingest_links: bool,
        **kwargs
    ):
        """Constructor and initialization.

        Args:
            dal (DalMesh): The `DalMesh` instance that will facilitate storing
                the qualifier dictionary to the DB.
        """

        super(IngesterDocumentQualifier, self).__init__(
            dal=dal,
            do_ingest_links=do_ingest_links,
            kwargs=kwargs,
        )

    @log_ingestion_of_document(document_name="QualifierRecord")
    def ingest(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<QualifierRecord>` and creates a
        `Qualifier` record.

        Args:
            doc (dict): The element of type `<QualifierRecord`> parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Qualifier` record.
        """

        if not doc:
            return None

        # Upsert the `Qualifier` record.
        qualifier_id = self.dal.iodu_qualifier(
            ui=doc.get("QualifierUI"),
            name=doc.get("QualifierName"),
            created=doc.get("DateCreated"),
            revised=doc.get("DateRevised"),
            established=doc.get("DateEstablished"),
            annotation=doc.get("Annotation"),
            history_note=doc.get("HistoryNote"),
            online_note=doc.get("OnlineNote"),
        )

        # Upsert the `TreeNumber` and `QualifierTreeNumber` records.
        doc_tree_numbers = doc.get("TreeNumberList", [])
        for doc_tree_number in doc_tree_numbers:
            # Upsert the `TreeNumber` record.
            tree_number_id = self.ingest_tree_number(doc_tree_number)
            # Upsert the `QualifierTreeNumber` record.
            self.dal.iodi_qualifier_tree_number(
                qualifier_id=qualifier_id,
                tree_number_id=tree_number_id
            )

        # Upsert the `Concept` and `QualifierConcept` records.
        for doc_concept in doc.get("ConceptList", []):
            # Upsert the `Concept` record.
            concept_id = self.ingest_concept(doc_concept)
            # Upsert the `QualifierConcept` record.
            self.dal.iodu_qualifier_concept(
                qualifier_id=qualifier_id,
                concept_id=concept_id,
                is_preferred=doc_concept.get("PreferredConceptYN"),
            )


class IngesterDocumentSupplemental(IngesterDocumentBase):
    """Class to ingest a parsed XML `<SupplementalRecord>` document."""

    def __init__(
        self,
        dal: DalMesh,
        do_ingest_links: bool,
        **kwargs
    ):
        """Constructor and initialization.

        Args:
            dal (DalMesh): The `DalMesh` instance that will facilitate storing
                the qualifier dictionary to the DB.
        """

        super(IngesterDocumentSupplemental, self).__init__(
            dal=dal,
            do_ingest_links=do_ingest_links,
            kwargs=kwargs,
        )

    @log_ingestion_of_document(document_name="SupplementalRecord")
    def ingest(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<SupplementalRecord>` and creates a
        `Supplemental` record.

        Args:
            doc (dict): The element of type `<SupplementalRecord`> parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Supplemental` record.
        """

        if not doc:
            return None

        # Upsert the `Supplemental` record.
        supplemental_id = self.dal.iodu_supplemental(
            supplemental_class=doc.get("SupplementalClass"),
            ui=doc.get("SupplementalRecordUI"),
            name=doc.get("SupplementalRecordName"),
            created=doc.get("DateCreated"),
            revised=doc.get("DateRevised"),
            note=doc.get("Note"),
            frequency=doc.get("Frequency"),
        )

        # Upsert the `PreviousIndexing` and `SupplementalPreviousIndexing`
        # records.
        for doc_previous_indexings in doc.get("PreviousIndexingList"):
            # Upsert the `PreviousIndexing` record.
            previous_indexing_id = self.dal.iodi_previous_indexing(
                previous_indexing=doc_previous_indexings.get(
                    "PreviousIndexing",
                ),
            )
            # Upsert the `SupplementalPreviousIndexing` record.
            self.dal.iodi_supplemental_previous_indexing(
                supplemental_id=supplemental_id,
                previous_indexing_id=previous_indexing_id,
            )

        # Upsert the `EntryCombination` records representing the
        # `<HeadingMappedTo>` elements and the `SupplementalHeadingMappedTo`
        # records.
        if self.do_ingest_links:
            for doc_heading_mapped_to in doc.get("HeadingMappedToList"):
                # Upsert the `EntryCombination` record.
                qualifier = self.dal.get_by_attrs(
                    Qualifier,
                    {"ui": self._get_qref_ui(doc_heading_mapped_to)}
                )
                entry_combination_id = self.dal.iodu_entry_combination(
                    descriptor_id=self.dal.get_by_attrs(
                        Descriptor,
                        {"ui": self._get_dref_ui(doc_heading_mapped_to)}
                    ).descriptor_id,
                    qualifier_id=qualifier.qualifier_id if qualifier else None,
                    combination_type=None,
                )
                # Upsert the `SupplementalHeadingMappedTo` record.
                self.dal.iodi_supplemental_heading_mapped_to(
                    supplemental_id=supplemental_id,
                    entry_combination_id=entry_combination_id
                )

        # Upsert the `EntryCombination` records representing the
        # `<IndexingInformation>` elements and the
        # `SupplementalHeadingMappedTo` records.
        if self.do_ingest_links:
            for doc_indexing_informations in doc.get("IndexingInformationList"):
                # Upsert the `EntryCombination` record.
                qualifier = self.dal.get_by_attrs(
                    Qualifier,
                    {"ui": self._get_qref_ui(doc_indexing_informations)}
                )
                entry_combination_id = self.dal.iodu_entry_combination(
                    descriptor_id=self.dal.get_by_attrs(
                        Descriptor,
                        {"ui": self._get_dref_ui(doc_indexing_informations)}
                    ).descriptor_id,
                    qualifier_id=qualifier.qualifier_id if qualifier else None,
                    combination_type=None,
                )
                # Upsert the `SupplementalIndexingInformation` record.
                self.dal.iodi_supplemental_indexing_information(
                    supplemental_id=supplemental_id,
                    entry_combination_id=entry_combination_id,
                )

        # Upsert the `SupplementalPharmacologicalActionDescriptor` records.
        if self.do_ingest_links:
            for doc_pharmacological_action in doc.get(
                "PharmacologicalActionList"):
                self.dal.iodi_supplemental_pharmacological_action_descriptor(
                    supplemental_id=supplemental_id,
                    pharmacological_action_descriptor_id=self.dal.get_by_attrs(
                        Descriptor,
                        {"ui": self._get_dref_ui(doc_pharmacological_action)},
                    ).descriptor_id,
                )

        # Upsert the `Source` and `SupplementalSource` records.
        for doc_source in doc.get("SourceList"):
            # Upsert the `Source` record.
            source_id = self.dal.iodi_source(source=doc_source.get("Source"))
            # Upsert the `SupplementalSource` record.
            self.dal.iodi_supplemental_source(
                supplemental_id=supplemental_id,
                source_id=source_id,
            )

        # Upsert the `Concept` and `SupplementalConcept` records.
        for doc_concept in doc.get("ConceptList", []):
            # Upsert the `Concept` record.
            concept_id = self.ingest_concept(doc_concept)
            # Upsert the `SupplementalConcept` record.
            self.dal.iodu_supplemental_concept(
                supplemental_id=supplemental_id,
                concept_id=concept_id,
                is_preferred=doc_concept.get("PreferredConceptYN"),
            )


class IngesterDocumentDescriptor(IngesterDocumentBase):
    """Class to ingest a parsed XML `<DescriptorRecord>` document."""

    def __init__(
        self,
        dal: DalMesh,
        do_ingest_links: bool,
        **kwargs
    ):
        """Constructor and initialization.

        Args:
            dal (DalMesh): The `DalMesh` instance that will facilitate storing
                the qualifier dictionary to the DB.
        """

        super(IngesterDocumentDescriptor, self).__init__(
            dal=dal,
            do_ingest_links=do_ingest_links,
            kwargs=kwargs,
        )

    @log_ingestion_of_document(document_name="DescriptorRecord")
    def ingest(
        self,
        doc: dict,
    ) -> Union[int, None]:
        """Ingests a parsed element of type `<DescriptorRecord>` and creates a
        `Descriptor` record.

        Args:
            doc (dict): The element of type `<DescriptorRecord`> parsed into a
                dictionary.

        Returns:
             int: The primary-key ID of the `Descriptor` record.
        """

        if not doc:
            return None

        # Upsert the `Descriptor` record.
        descriptor_id = self.dal.iodu_descriptor(
            descriptor_class=doc.get("DescriptorClass"),
            ui=doc.get("DescriptorUI"),
            name=doc.get("DescriptorName"),
            created=doc.get("DateCreated"),
            revised=doc.get("DateRevised"),
            established=doc.get("DateEstablished"),
            annotation=doc.get("Annotation"),
            history_note=doc.get("HistoryNote"),
            nlm_classification_number=doc.get("NLMClassificationNumber"),
            online_note=doc.get("OnlineNote"),
            public_mesh_note=doc.get("PublicMeSHNote"),
            consider_also=doc.get("ConsiderAlso"),
        )

        # Upsert the `DescriptorAllowableQualifier` records.
        if self.do_ingest_links:
            for doc_allowable_qualifier in doc.get("AllowableQualifiersList"):
                self.dal.iodu_descriptor_allowable_qualifier(
                    descriptor_id=descriptor_id,
                    qualifier_id=self.dal.get_by_attrs(
                        Qualifier,
                        {"ui": self._get_qref_ui(doc_allowable_qualifier)},
                    ).qualifier_id,
                    abbreviation=doc_allowable_qualifier.get("Abbreviation"),
                )

        # Upsert the `PreviousIndexing` and `DescriptorPreviousIndexing`
        # records.
        for doc_previous_indexings in doc.get("PreviousIndexingList"):
            # Upsert the `PreviousIndexing` record.
            previous_indexing_id = self.dal.iodi_previous_indexing(
                previous_indexing=doc_previous_indexings.get(
                    "PreviousIndexing",
                ),
            )
            # Upsert the `DescriptorPreviousIndexing` record.
            self.dal.iodi_descriptor_previous_indexing(
                descriptor_id=descriptor_id,
                previous_indexing_id=previous_indexing_id,
            )

        # Upsert the `EntryCombination` records.
        if self.do_ingest_links:
            for doc_entry_combination in doc.get("EntryCombinationList"):
                # Retrieve referenced `Qualifier` record.
                qualifier = self.dal.get_by_attrs(
                    Qualifier,
                    {
                        "ui": self._get_qref_ui(
                            doc_entry_combination.get("ECIN")
                        ),
                    }
                )
                # Upsert the ECIN `EntryCombination` record.
                self.dal.iodu_entry_combination(
                    descriptor_id=self.dal.get_by_attrs(
                        Descriptor,
                        {
                            "ui": self._get_dref_ui(
                                doc_entry_combination.get("ECIN")
                            ),
                        },
                    ).descriptor_id,
                    qualifier_id=qualifier.qualifier_id if qualifier else None,
                    combination_type=EntryCombinationType.ECIN,
                )
                # Retrieve referenced `Qualifier` record.
                qualifier = self.dal.get_by_attrs(
                    Qualifier,
                    {
                        "ui": self._get_qref_ui(
                            doc_entry_combination.get("ECOUT")
                        ),
                    }
                )
                # Upsert the ECOUT `EntryCombination` record.
                self.dal.iodu_entry_combination(
                    descriptor_id=self.dal.get_by_attrs(
                        Descriptor,
                        {
                            "ui": self._get_dref_ui(
                                doc_entry_combination.get("ECOUT")
                            ),
                        }
                    ).descriptor_id,
                    qualifier_id=qualifier.qualifier_id if qualifier else None,
                    combination_type=EntryCombinationType.ECOUT,
                )

        # Upsert `DescriptorRelatedDescriptor` records.
        if self.do_ingest_links:
            for related_descriptor in doc.get("SeeRelatedList"):
                self.dal.iodi_descriptor_related_descriptor(
                    descriptor_id=descriptor_id,
                    related_descriptor_id=self.dal.get_by_attrs(
                        Descriptor,
                        {"ui": self._get_dref_ui(related_descriptor)},
                    ).descriptor_id,
                )

        # Upsert the `DescriptorPharmacologicalActionDescriptor` records.
        if self.do_ingest_links:
            for doc_pharmacological_action in doc.get(
                "PharmacologicalActionList"):
                self.dal.iodi_descriptor_pharmacological_action_descriptor(
                    descriptor_id=descriptor_id,
                    pharmacological_action_descriptor_id=self.dal.get_by_attrs(
                        Descriptor,
                        {"ui": self._get_dref_ui(doc_pharmacological_action)},
                    ).descriptor_id,
                )

        # Upsert the `TreeNumber` and `DescriptorTreeNumber` records.
        doc_tree_numbers = doc.get("TreeNumberList", [])
        for doc_tree_number in doc_tree_numbers:
            # Upsert the `TreeNumber` record.
            tree_number_id = self.ingest_tree_number(doc_tree_number)
            # Upsert the `QualifierTreeNumber` record.
            self.dal.iodi_descriptor_tree_number(
                descriptor_id=descriptor_id,
                tree_number_id=tree_number_id
            )

        # Upsert the `Concept` and `DescriptorConcept` records.
        for doc_concept in doc.get("ConceptList", []):
            # Upsert the `Concept` record.
            concept_id = self.ingest_concept(doc_concept)
            # Upsert the `DescriptorConcept` record.
            self.dal.iodu_descriptor_concept(
                descriptor_id=descriptor_id,
                concept_id=concept_id,
                is_preferred=doc_concept.get("PreferredConceptYN"),
            )


class IngesterUmlsConso(object):

    def __init__(
        self,
        dal: DalMesh,
        **kwargs
    ):

        # Internalize arguments.
        self.dal = dal

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    def ingest(
        self,
        document: dict
    ):

        msg = "Ingesting synonyms for {} MeSH entities."
        msg_fmt = msg.format(len(document.keys()))
        self.logger.info(msg_fmt)

        # Iterate over the synonyms and ingest them according to the type of
        # MeSH entity they're referring to.
        for entity_ui, synonyms in document.items():

            # Calculate the MD5s of the synonyms.
            md5s = [
                hashlib.md5(synonym.encode("utf-8")).digest()
                for synonym in synonyms
            ]

            if entity_ui.startswith("D"):
                descriptor = self.dal.get_by_attr(
                    orm_class=Descriptor,
                    attr_name="ui",
                    attr_value=entity_ui,
                )  # type: Descriptor
                self.dal.biodi_descriptor_synonyms(
                    descriptor_id=descriptor.descriptor_id,
                    synonyms=synonyms,
                    md5s=md5s,
                )
            elif entity_ui.startswith("C"):
                supplemental = self.dal.get_by_attr(
                    orm_class=Supplemental,
                    attr_name="ui",
                    attr_value=entity_ui,
                )  # type: Supplemental
                self.dal.biodi_supplemental_synonyms(
                    supplemental_id=supplemental.supplemental_id,
                    synonyms=synonyms,
                    md5s=md5s,
                )
            elif entity_ui.startswith("M"):
                concept = self.dal.get_by_attr(
                    orm_class=Concept,
                    attr_name="ui",
                    attr_value=entity_ui,
                )  # type: Concept
                self.dal.biodi_concept_synonyms(
                    concept_id=concept.concept_id,
                    synonyms=synonyms,
                    md5s=md5s,
                )
            elif entity_ui.startswith("Q"):
                qualifier = self.dal.get_by_attr(
                    orm_class=Qualifier,
                    attr_name="ui",
                    attr_value=entity_ui,
                )  # type: Qualifier
                self.dal.biodi_qualifier_synonyms(
                    qualifier_id=qualifier.qualifier_id,
                    synonyms=synonyms,
                    md5s=md5s,
                )
            else:
                raise NotImplementedError
