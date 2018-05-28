# coding=utf-8

import abc
from typing import Union

from mt_ingester.orm import Concept
from mt_ingester.orm import Descriptor
from mt_ingester.orm import Qualifier
from mt_ingester.orm_enums import EntryCombinationType
from mt_ingester.loggers import create_logger
from mt_ingester.dals import DalMesh
from mt_ingester.utils import log_ingestion_of_document


class IngesterDocumentBase(object):
    def __init__(
        self,
        dal,
        num_pass: int,
        **kwargs
    ):

        # Internalize arguments.
        self.num_pass = num_pass
        self.dal = dal

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

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
        if self.num_pass > 1:
            for doc_concept_relations in doc.get("ConceptRelationList"):
                self.dal.iodu_concept_related_concept(
                    concept_id=self.dal.get_by_attrs(
                        Concept,
                        {"ui": doc_concept_relations.get("Concept1UI")}
                    ),
                    related_concept_id=self.dal.get_by_attrs(
                        Concept,
                        {"ui": doc_concept_relations.get("Concept2UI")}
                    ),
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
        num_pass: int,
        **kwargs
    ):
        """Constructor and initialization.

        Args:
            dal (DalMesh): The `DalMesh` instance that will facilitate storing
                the qualifier dictionary to the DB.
        """

        super(IngesterDocumentQualifier, self).__init__(
            dal=dal,
            num_pass=num_pass,
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
        num_pass: int,
        **kwargs
    ):
        """Constructor and initialization.

        Args:
            dal (DalMesh): The `DalMesh` instance that will facilitate storing
                the qualifier dictionary to the DB.
        """

        super(IngesterDocumentSupplemental, self).__init__(
            dal=dal,
            num_pass=num_pass,
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
        for doc_heading_mapped_to in doc.get("HeadingMappedToList"):
            # Upsert the `EntryCombination` record.
            entry_combination_id = self.dal.iodu_entry_combination(
                descriptor_id=self.dal.get_by_attrs(
                    Descriptor,
                    {
                        "ui": doc_heading_mapped_to.get(
                            "DescriptorReferredTo",
                        ).get("DescriptorUI"),
                    }
                ),
                qualifier_id=self.dal.get_by_attrs(
                    Qualifier,
                    {
                        "ui": doc_heading_mapped_to.get(
                            "QualifierReferredTo",
                        ).get("QualifierUI"),
                    }
                ),
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
        for doc_indexing_informations in doc.get("IndexingInformationList"):
            # Upsert the `EntryCombination` record.
            entry_combination_id = self.dal.iodu_entry_combination(
                descriptor_id=self.dal.get_by_attrs(
                    Descriptor,
                    {
                        "ui": doc_indexing_informations.get(
                            "DescriptorReferredTo",
                        ).get("DescriptorUI"),
                    }
                ),
                qualifier_id=self.dal.get_by_attrs(
                    Qualifier,
                    {
                        "ui": doc_indexing_informations.get(
                            "QualifierReferredTo",
                        ).get("QualifierUI"),
                    }
                ),
                combination_type=None,
            )
            # Upsert the `SupplementalIndexingInformation` record.
            self.dal.iodi_supplemental_indexing_information(
                supplemental_id=supplemental_id,
                entry_combination_id=entry_combination_id,
            )

        # Upsert the `SupplementalPharmacologicalActionDescriptor` records.
        for doc_pharmacological_action in doc.get("PharmacologicalActionList"):
            self.dal.iodi_supplemental_pharmacological_action_descriptor(
                supplemental_id=supplemental_id,
                pharmacological_action_descriptor_id=self.dal.get_by_attrs(
                    Descriptor,
                    {
                        "ui": doc_pharmacological_action.get(
                            "DescriptorReferredTo",
                        ).get("DescriptorUI"),
                    }
                ),
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
        num_pass: int,
        **kwargs
    ):
        """Constructor and initialization.

        Args:
            dal (DalMesh): The `DalMesh` instance that will facilitate storing
                the qualifier dictionary to the DB.
        """

        super(IngesterDocumentDescriptor, self).__init__(
            dal=dal,
            num_pass=num_pass,
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
        for doc_allowable_qualifier in doc.get("AllowableQualifiersList"):
            self.dal.iodu_descriptor_allowable_qualifier(
                descriptor_id=descriptor_id,
                qualifier_id=self.dal.get_by_attrs(
                    Qualifier,
                    {
                        "ui": doc_allowable_qualifier.get(
                            "QualifierReferredTo",
                        ).get("QualifierUI"),
                    }
                ),
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
        for doc_entry_combination in doc.get("EntryCombinationList"):
            # Upsert the ECIN `EntryCombination` record.
            self.dal.iodu_entry_combination(
                descriptor_id=self.dal.get_by_attrs(
                    Descriptor,
                    {
                        "ui": doc_entry_combination.get("ECIN").get(
                            "DescriptorReferredTo",
                        ).get("DescriptorUI"),
                    }
                ),
                qualifier_id=self.dal.get_by_attrs(
                    Qualifier,
                    {
                        "ui": doc_entry_combination.get("ECIN").get(
                            "QualifierReferredTo",
                        ).get("QualifierUI"),
                    }
                ),
                combination_type=EntryCombinationType.ECIN,
            )
            # Upsert the ECOUT `EntryCombination` record.
            self.dal.iodu_entry_combination(
                descriptor_id=self.dal.get_by_attrs(
                    Descriptor,
                    {
                        "ui": doc_entry_combination.get("ECOUT").get(
                            "DescriptorReferredTo",
                        ).get("DescriptorUI"),
                    }
                ),
                qualifier_id=self.dal.get_by_attrs(
                    Qualifier,
                    {
                        "ui": doc_entry_combination.get("ECOUT").get(
                            "QualifierReferredTo",
                        ).get("QualifierUI"),
                    }
                ),
                combination_type=EntryCombinationType.ECOUT,
            )

        # Upsert `DescriptorRelatedDescriptor` records.
        for related_descriptors in doc.get("SeeRelatedList"):
            self.dal.iodi_descriptor_related_descriptor(
                descriptor_id=descriptor_id,
                related_descriptor_id=self.dal.get_by_attrs(
                    Descriptor,
                    {
                        "ui": related_descriptors.get(
                            "DescriptorReferredTo",
                        ).get("DescriptorUI"),
                    },
                )
            )

        # Upsert the `DescriptorPharmacologicalActionDescriptor` records.
        for doc_pharmacological_action in doc.get("PharmacologicalActionList"):
            self.dal.iodi_descriptor_pharmacological_action_descriptor(
                descriptor_id=descriptor_id,
                pharmacological_action_descriptor_id=self.dal.get_by_attrs(
                    Descriptor,
                    {
                        "ui": doc_pharmacological_action.get(
                            "DescriptorReferredTo",
                        ).get("DescriptorUI"),
                    }
                ),
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
