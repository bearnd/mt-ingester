# coding: utf-8

import datetime

import sqlalchemy.orm
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.engine.result import ResultProxy


from mt_ingester.loggers import create_logger
from mt_ingester.dal_base import DalBase
from mt_ingester.dal_base import with_session_scope
from mt_ingester.orm import TreeNumber
from mt_ingester.orm import ThesaurusId
from mt_ingester.orm import Term
from mt_ingester.orm import TermThesaurusId
from mt_ingester.orm import Concept
from mt_ingester.orm import ConceptRelatedConcept
from mt_ingester.orm import ConceptTerm
from mt_ingester.orm import Qualifier
from mt_ingester.orm import QualifierConcept
from mt_ingester.orm import QualifierTreeNumber
from mt_ingester.orm import PreviousIndexing
from mt_ingester.orm import EntryCombination
from mt_ingester.orm import Descriptor
from mt_ingester.orm import DescriptorEntryCombination
from mt_ingester.orm import DescriptorConcept
from mt_ingester.orm import DescriptorPreviousIndexing
from mt_ingester.orm import DescriptorAllowableQualifier
from mt_ingester.orm import DescriptorTreeNumber
from mt_ingester.orm import DescriptorPharmacologicalActionDescriptor
from mt_ingester.orm import DescriptorRelatedDescriptor
from mt_ingester.orm import Source
from mt_ingester.orm import Supplemental
from mt_ingester.orm import SupplementalHeadingMappedTo
from mt_ingester.orm import SupplementalIndexingInformation
from mt_ingester.orm import SupplementalConcept
from mt_ingester.orm import SupplementalPreviousIndexing
from mt_ingester.orm import SupplementalPharmacologicalActionDescriptor
from mt_ingester.orm import SupplementalSource
from mt_ingester.orm_enums import RelationNameType
from mt_ingester.orm_enums import LexicalTagType
from mt_ingester.orm_enums import EntryCombinationType
from mt_ingester.orm_enums import DescriptorClassType
from mt_ingester.orm_enums import SupplementalClassType
from fform.utils import return_first_item


class DalMesh(DalBase):
    def __init__(
        self,
        sql_username,
        sql_password,
        sql_host,
        sql_port,
        sql_db,
        *args,
        **kwargs
    ):

        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

        super(DalMesh, self).__init__(
            sql_username=sql_username,
            sql_password=sql_password,
            sql_host=sql_host,
            sql_port=sql_port,
            sql_db=sql_db,
            *args,
            **kwargs
        )

    @with_session_scope()
    def get_by_md5(
        self,
        orm_class,
        md5: bytes,
        session: sqlalchemy.orm.Session = None,
    ):
        """Retrieves an object of a class derived off `OrmBase` through its MD5.

        Args:
            md5 (bytes): The MD5 has of the `OrmBase` record to be retrieved.
            orm_class: An object of a class derived off `OrmBase` implementing
                an `md5` attribute.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            The matching `OrmBase` record object or `None` if no such record
                exists.
        """

        query = session.query(orm_class)
        query = query.filter(orm_class.md5 == md5)

        obj = query.one_or_none()

        return obj

    @with_session_scope()
    def get_by_attrs(
        self,
        orm_class,
        attrs_names_values: dict,
        session: sqlalchemy.orm.Session = None,
    ):
        """Retrieves the record object of `orm_class` type through attribute
        name-value pairs.

        Note:
            This method should only be used through unique attributes/fields as
            it uses the `one_or_none` retrieval method and will raise an
            exception should multiple records with a given attribute value be
            found.

        Args:
            orm_class: An object of a class derived off `OrmBase` implementing
                an `md5` attribute.
            attrs_names_values (dict): A dictionary of attribute name-value
                pairs to be used in filtering out a single record.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            orm_class: The record object of type `orm_class` matching the
                attribute name-value pairs and `None` if no record exists.

        Raises:
            sqlalchemy.orm.exc.MultipleResultsFound: Raised when multiple
                records were found with the given attribute(s).
        """

        query = session.query(orm_class)
        for attr_name, attr_value in attrs_names_values.items():
            query = query.filter(
                getattr(orm_class, attr_name) == attr_value
            )

        obj = query.one_or_none()

        return obj

    @return_first_item
    @with_session_scope()
    def iodi_tree_number(
        self,
        tree_number: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `TreeNumber` record in an IODI manner.

        Args:
            tree_number (str): The tree-number.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `TreeNumber` record.
        """

        # Create and populate a `TreeNumber` object so that we can retrieve the
        # MD5 hash.
        obj = TreeNumber()
        obj.tree_number = tree_number

        statement = insert(
            TreeNumber,
            values={
                "tree_number": tree_number,
                "md5": obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_md5(
                orm_class=TreeNumber,
                md5=obj.md5,
                session=session,
            )  # type: TreeNumber
            return obj.tree_number_id

    @return_first_item
    @with_session_scope()
    def iodi_thesaurus_id(
        self,
        thesaurus_id: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `ThesaurusId` record in an IODI manner.

        Args:
            thesaurus_id (str): The thesaurus-id.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ThesaurusId` record.
        """

        # Create and populate a `ThesaurusId` object so that we can retrieve the
        # MD5 hash.
        obj = TreeNumber()
        obj.thesaurus_id = thesaurus_id

        statement = insert(
            ThesaurusId,
            values={
                "thesaurus_id": thesaurus_id,
                "md5": obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_md5(
                orm_class=ThesaurusId,
                md5=obj.md5,
                session=session,
            )  # type: ThesaurusId
            return obj.thesaurus_id_id

    @return_first_item
    @with_session_scope()
    def iodu_term(
        self,
        ui: str,
        name: str,
        created: datetime.date,
        abbreviation: str,
        sort_version: str,
        entry_version: str,
        note: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Term` record in an IODU manner.

        Args:
            ui (str): The term UI.
            name (str): The term name.
            created (datetime.date): The date the term was created.
            abbreviation (str): The term abbreviation.
            sort_version (str): The term sort version.
            entry_version (str): The term entry version.
            note (str): The term note.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Term` record.
        """

        # Upsert the `Term` record.
        statement = insert(
            Term,
            values={
                "ui": ui,
                "name": name,
                "created": created,
                "abbreviation": abbreviation,
                "sort_version": sort_version,
                "entry_version": entry_version,
                "note": note,
            }
        ).on_conflict_do_update(
            set_={
                "name": name,
                "created": created,
                "abbreviation": abbreviation,
                "sort_version": sort_version,
                "entry_version": entry_version,
                "note": note,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=Term,
                attrs_names_values={
                    "ui": ui,
                },
                session=session,
            )  # type: Term
            return obj.term_id

    @return_first_item
    @with_session_scope()
    def iodi_term_thesaurus_id(
        self,
        term_id: int,
        thesaurus_id_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `TermThesaurusId` record in an IODI manner.

        Args:
            term_id (int): The linked `Term` record primary-key ID.
            thesaurus_id_id (int): The linked `ThesaurusId` record primary-key
                ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `TermThesaurusId` record.
        """

        statement = insert(
            TermThesaurusId,
            values={
                "term_id": term_id,
                "thesaurus_id_id": thesaurus_id_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=TermThesaurusId,
                attrs_names_values={
                    "term_id": term_id,
                    "thesaurus_id_id": thesaurus_id_id,
                },
                session=session,
            )  # type: TermThesaurusId
            return obj.term_thesaurus_id_id

    @return_first_item
    @with_session_scope()
    def iodu_concept(
        self,
        ui: str,
        name: str,
        casn1_name: str,
        registry_number: str,
        scope_note: str,
        translators_english_scope_note: str,
        translators_scope_note: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Concept` record in an IODU manner.

        Args:
            ui (str): The concept UI.
            name (str): The concept name.
            casn1_name (str): The concept CASN1 name.
            registry_number (str): The concept registry-number.
            scope_note (str): The concept scope-note.
            translators_english_scope_note (str): The concept translator's
                English scope-note.
            translators_scope_note (str): The concept translator's scope-note.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Concept` record.
        """

        # Upsert the `Concept` record.
        statement = insert(
            Concept,
            values={
                "ui": ui,
                "name": name,
                "casn1_name": casn1_name,
                "registry_number": registry_number,
                "scope_note": scope_note,
                "translators_english_scope_note": (
                    translators_english_scope_note
                ),
                "translators_scope_note": translators_scope_note,
            }
        ).on_conflict_do_update(
            set_={
                "name": name,
                "casn1_name": casn1_name,
                "registry_number": registry_number,
                "scope_note": scope_note,
                "translators_english_scope_note": (
                    translators_english_scope_note
                ),
                "translators_scope_note": translators_scope_note,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=Concept,
                attrs_names_values={
                    "ui": ui,
                },
                session=session,
            )  # type: Concept
            return obj.concept_id

    @return_first_item
    @with_session_scope()
    def iodu_concept_related_concept(
        self,
        concept_id: int,
        related_concept_id: int,
        relation_name: RelationNameType,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `ConceptRelatedConcept` record in an IODU manner.

        Args:
            concept_id (int): The linked `Concept` record primary-key ID.
            related_concept_id (int): The related linked `Concept` record
                primary-key ID.
            relation_name (RelationNameType): The relation name type.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ConceptRelatedConcept` record.
        """

        statement = insert(
            ConceptRelatedConcept,
            values={
                "concept_id": concept_id,
                "related_concept_id": related_concept_id,
                "relation_name": relation_name,
            }
        ).on_conflict_do_update(
            set_={
                "relation_name": relation_name,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=ConceptRelatedConcept,
                attrs_names_values={
                    "concept_id": concept_id,
                    "related_concept_id": related_concept_id,
                },
                session=session,
            )  # type: ConceptRelatedConcept
            return obj.concept_related_concept_id

    @return_first_item
    @with_session_scope()
    def iodu_concept_term(
        self,
        concept_id: int,
        term_id: int,
        is_concept_preferred_term: bool,
        is_permuted_term: bool,
        lexical_tag: LexicalTagType,
        is_record_preferred_term: bool,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `ConceptTerm` record in an IODU manner.

        Args:
            concept_id (int): The linked `Concept` record primary-key ID.
            term_id (int): The linked `Term` record primary-key ID.
            is_concept_preferred_term (bool): Whether the term is the preferred
                one for the concept.
            is_permuted_term (bool): Whether the term is permuted.
            lexical_tag (LexicalTagType): The term's lexical tag type.
            is_record_preferred_term (bool): Whether the term is the preferred
                one for the record.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `ConceptTerm` record.
        """

        statement = insert(
            ConceptTerm,
            values={
                "concept_id": concept_id,
                "term_id": term_id,
                "is_concept_preferred_term": is_concept_preferred_term,
                "is_permuted_term": is_permuted_term,
                "lexical_tag": lexical_tag,
                "is_record_preferred_term": is_record_preferred_term,
            }
        ).on_conflict_do_update(
            set_={
                "is_concept_preferred_term": is_concept_preferred_term,
                "is_permuted_term": is_permuted_term,
                "lexical_tag": lexical_tag,
                "is_record_preferred_term": is_record_preferred_term,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=ConceptTerm,
                attrs_names_values={
                    "concept_id": concept_id,
                    "term_id": term_id,
                },
                session=session,
            )  # type: ConceptTerm
            return obj.concept_term_id

    @return_first_item
    @with_session_scope()
    def iodu_qualifier(
        self,
        ui: str,
        name: str,
        created: datetime.date,
        revised: datetime.date,
        established: datetime.date,
        annotation: str,
        history_note: str,
        online_note: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Qualifier` record in an IODU manner.

        Args:
            ui (str): The qualifier UI.
            name (str): The qualifier name.
            created (datetime.date): The date the qualifier was created.
            revised (datetime.date): The date the qualifier was revised.
            established (datetime.date): The date the qualifier was established.
            annotation (str): The qualifier annotation.
            history_note (str): The qualifier history-note.
            online_note (str): The qualifier online-note.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Qualifier` record.
        """

        # Upsert the `Qualifier` record.
        statement = insert(
            Qualifier,
            values={
                "ui": ui,
                "name": name,
                "created": created,
                "revised": revised,
                "established": established,
                "annotation": annotation,
                "history_note": history_note,
                "online_note": online_note,
            }
        ).on_conflict_do_update(
            set_={
                "name": name,
                "created": created,
                "revised": revised,
                "established": established,
                "annotation": annotation,
                "history_note": history_note,
                "online_note": online_note,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=Qualifier,
                attrs_names_values={
                    "ui": ui,
                },
                session=session,
            )  # type: Qualifier
            return obj.qualifier_id

    @return_first_item
    @with_session_scope()
    def iodu_qualifier_concept(
        self,
        qualifier_id: int,
        concept_id: int,
        is_preferred: bool,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `QualifierConcept` record in an IODU manner.

        Args:
            qualifier_id (int): The linked `Qualifier` record primary-key ID.
            concept_id (int): The linked `Concept` record primary-key ID.
            is_preferred (bool): Whether the concept is the preferred one for
                the qualifier.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `QualifierConcept` record.
        """

        statement = insert(
            QualifierConcept,
            values={
                "qualifier_id": qualifier_id,
                "concept_id": concept_id,
                "is_preferred": is_preferred,
            }
        ).on_conflict_do_update(
            set_={
                "is_preferred": is_preferred,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=QualifierConcept,
                attrs_names_values={
                    "qualifier_id": qualifier_id,
                    "concept_id": concept_id,
                },
                session=session,
            )  # type: QualifierConcept
            return obj.qualifier_concept_id

    @return_first_item
    @with_session_scope()
    def iodi_qualifier_tree_number(
        self,
        qualifier_id: int,
        tree_number_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `QualifierTreeNumber` record in an IODI manner.

        Args:
            qualifier_id (int): The linked `Qualifier` record primary-key ID.
            tree_number_id (int): The linked `TreeNumber` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `QualifierTreeNumber` record.
        """

        statement = insert(
            QualifierTreeNumber,
            values={
                "qualifier_id": qualifier_id,
                "tree_number_id": tree_number_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=QualifierTreeNumber,
                attrs_names_values={
                    "qualifier_id": qualifier_id,
                    "tree_number_id": tree_number_id,
                },
                session=session,
            )  # type: QualifierTreeNumber
            return obj.qualifier_tree_number_id

    @return_first_item
    @with_session_scope()
    def iodi_previous_indexing(
        self,
        previous_indexing: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `PreviousIndexing` record in an IODU manner.

        Args:
            previous_indexing (str): The previous-indexing.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `PreviousIndexing` record.
        """

        # Create and populate a `PreviousIndexing` object so that we can
        # retrieve the MD5 hash.
        obj = PreviousIndexing()
        obj.previous_indexing = previous_indexing

        # Upsert the `PreviousIndexing` record.
        statement = insert(
            PreviousIndexing,
            values={
                "previous_indexing": previous_indexing,
                "md5": obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_md5(
                orm_class=PreviousIndexing,
                md5=obj.md5,
                session=session,
            )  # type: PreviousIndexing
            return obj.previous_indexing_id

    @return_first_item
    @with_session_scope()
    def iodu_entry_combination(
        self,
        descriptor_id: int,
        qualifier_id: int,
        combination_type: EntryCombinationType,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `EntryCombination` record in an IODU manner.

        Args:
            descriptor_id (int): The linked `Descriptor` record primary-key ID.
            qualifier_id (int): The linked `Qualifier` record primary-key ID.
            combination_type (EntryCombinationType): The type of
                entry-combination. This only applies to combinations in
                `<EntryCombination>` elements.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `EntryCombination` record.
        """

        statement = insert(
            EntryCombination,
            values={
                "descriptor_id": descriptor_id,
                "qualifier_id": qualifier_id,
                "type": combination_type,
            }
        ).on_conflict_do_update(
            set_={
                "type": combination_type,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=EntryCombination,
                attrs_names_values={
                    "descriptor_id": descriptor_id,
                    "qualifier_id": qualifier_id,
                },
                session=session,
            )  # type: EntryCombination
            return obj.entry_combination_id

    @return_first_item
    @with_session_scope()
    def iodu_descriptor(
        self,
        descriptor_class: DescriptorClassType,
        ui: str,
        name: str,
        created: datetime.date,
        revised: datetime.date,
        established: datetime.date,
        annotation: str,
        history_note: str,
        nlm_classification_number: str,
        online_note: str,
        public_mesh_note: str,
        consider_also: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Descriptor` record in an IODU manner.

        Args:
            descriptor_class (DescriptorClassType): The descriptor class type.
            ui (str): The descriptor UI.
            name (str): The descriptor name.
            created (datetime.date): The date the descriptor was created.
            revised (datetime.date): The date the descriptor was revised.
            established (datetime.date): The date the descriptor was
                established.
            annotation (str): The descriptor annotation.
            history_note (str): The descriptor history-note.
            nlm_classification_number (str): The descriptor NLM classification
                number.
            online_note (str): The descriptor online-note.
            public_mesh_note (str): The descriptor public-mesh-note.
            consider_also (str): The descriptor consider-also note.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Descriptor` record.
        """

        # Upsert the `Descriptor` record.
        statement = insert(
            Descriptor,
            values={
                "class": descriptor_class,
                "ui": ui,
                "name": name,
                "created": created,
                "revised": revised,
                "established": established,
                "annotation": annotation,
                "history_note": history_note,
                "nlm_classification_number": nlm_classification_number,
                "online_note": online_note,
                "public_mesh_note": public_mesh_note,
                "consider_also": consider_also,
            }
        ).on_conflict_do_update(
            set_={
                "class": descriptor_class,
                "name": name,
                "created": created,
                "revised": revised,
                "established": established,
                "annotation": annotation,
                "history_note": history_note,
                "nlm_classification_number": nlm_classification_number,
                "online_note": online_note,
                "public_mesh_note": public_mesh_note,
                "consider_also": consider_also
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=Descriptor,
                attrs_names_values={
                    "ui": ui,
                },
                session=session,
            )  # type: Descriptor
            return obj.descriptor_id

    @return_first_item
    @with_session_scope()
    def iodi_descriptor_entry_combination(
        self,
        descriptor_id: int,
        entry_combination_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `DescriptorEntryCombination` record in an IODI manner.

        Args:
            descriptor_id (int): The linked `Descriptor` record primary-key ID.
            entry_combination_id (int): The linked `EntryCombination` record
                primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `DescriptorEntryCombination` record.
        """

        statement = insert(
            DescriptorEntryCombination,
            values={
                "descriptor_id": descriptor_id,
                "entry_combination_id": entry_combination_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=DescriptorEntryCombination,
                attrs_names_values={
                    "descriptor_id": descriptor_id,
                    "entry_combination_id": entry_combination_id,
                },
                session=session,
            )  # type: DescriptorEntryCombination
            return obj.descriptor_entry_combination_id

    @return_first_item
    @with_session_scope()
    def iodu_descriptor_concept(
        self,
        descriptor_id: int,
        concept_id: int,
        is_preferred: bool,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `DescriptorConcept` record in an IODU manner.

        Args:
            descriptor_id (int): The linked `Descriptor` record primary-key ID.
            concept_id (int): The linked `Concept` record primary-key ID.
            is_preferred (bool): Whether the concept is the preferred one for
                the descriptor.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `DescriptorConcept` record.
        """

        statement = insert(
            DescriptorConcept,
            values={
                "descriptor_id": descriptor_id,
                "concept_id": concept_id,
                "is_preferred": is_preferred,
            }
        ).on_conflict_do_update(
            set_={
                "is_preferred": is_preferred,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=DescriptorConcept,
                attrs_names_values={
                    "descriptor_id": descriptor_id,
                    "concept_id": concept_id,
                },
                session=session,
            )  # type: DescriptorConcept
            return obj.entry_combination_id

    @return_first_item
    @with_session_scope()
    def iodi_descriptor_previous_indexing(
        self,
        descriptor_id: int,
        previous_indexing_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `DescriptorPreviousIndexing` record in an IODI manner.

        Args:
            descriptor_id (int): The linked `Descriptor` record primary-key ID.
            previous_indexing_id (int): The linked `PreviousIndexing` record
                primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `DescriptorPreviousIndexing` record.
        """

        statement = insert(
            DescriptorPreviousIndexing,
            values={
                "descriptor_id": descriptor_id,
                "previous_indexing_id": previous_indexing_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=DescriptorPreviousIndexing,
                attrs_names_values={
                    "descriptor_id": descriptor_id,
                    "previous_indexing_id": previous_indexing_id,
                },
                session=session,
            )  # type: DescriptorPreviousIndexing
            return obj.descriptor_previous_indexing_id

    @return_first_item
    @with_session_scope()
    def iodu_descriptor_allowable_qualifier(
        self,
        descriptor_id: int,
        qualifier_id: int,
        abbreviation: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `DescriptorAllowableQualifier` record in an IODU
        manner.

        Args:
            descriptor_id (int): The linked `Descriptor` record primary-key ID.
            qualifier_id (int): The linked `Qualifier` record primary-key ID.
            abbreviation (bool): The abbreviation of the allowable qualifier.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `DescriptorAllowableQualifier`
                record.
        """

        statement = insert(
            DescriptorAllowableQualifier,
            values={
                "descriptor_id": descriptor_id,
                "qualifier_id": qualifier_id,
                "abbreviation": abbreviation,
            }
        ).on_conflict_do_update(
            set_={
                "abbreviation": abbreviation,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=DescriptorAllowableQualifier,
                attrs_names_values={
                    "descriptor_id": descriptor_id,
                    "qualifier_id": qualifier_id,
                },
                session=session,
            )  # type: DescriptorAllowableQualifier
            return obj.descriptor_allowable_qualifier_id

    @return_first_item
    @with_session_scope()
    def iodi_descriptor_tree_number(
        self,
        descriptor_id: int,
        tree_number_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `DescriptorTreeNumber` record in an IODI manner.

        Args:
            descriptor_id (int): The linked `Descriptor` record primary-key ID.
            tree_number_id (int): The linked `TreeNumber` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `DescriptorTreeNumber` record.
        """

        statement = insert(
            DescriptorTreeNumber,
            values={
                "descriptor_id": descriptor_id,
                "tree_number_id": tree_number_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=DescriptorTreeNumber,
                attrs_names_values={
                    "descriptor_id": descriptor_id,
                    "tree_number_id": tree_number_id,
                },
                session=session,
            )  # type: DescriptorTreeNumber
            return obj.descriptor_tree_number_id

    @return_first_item
    @with_session_scope()
    def iodi_descriptor_pharmacological_action_descriptor(
        self,
        descriptor_id: int,
        pharmacological_action_descriptor_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `DescriptorPharmacologicalActionDescriptor` record in
        an IODI manner.

        Args:
            descriptor_id (int): The linked `Descriptor` record primary-key ID.
            pharmacological_action_descriptor_id (int): The other linked
                `Descriptor` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the
                `DescriptorPharmacologicalActionDescriptor` record.
        """

        statement = insert(
            DescriptorPharmacologicalActionDescriptor,
            values={
                "descriptor_id": descriptor_id,
                "pharmacological_action_descriptor_id": (
                    pharmacological_action_descriptor_id
                ),
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=DescriptorPharmacologicalActionDescriptor,
                attrs_names_values={
                    "descriptor_id": descriptor_id,
                    "pharmacological_action_descriptor_id": (
                        pharmacological_action_descriptor_id
                    ),
                },
                session=session,
            )  # type: DescriptorPharmacologicalActionDescriptor
            return obj.descriptor_pharmacological_action_descriptor_id

    @return_first_item
    @with_session_scope()
    def iodi_descriptor_related_descriptor(
        self,
        descriptor_id: int,
        related_descriptor_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `DescriptorRelatedDescriptor` record in an IODI manner.

        Args:
            descriptor_id (int): The linked `Descriptor` record primary-key ID.
            related_descriptor_id (int): The related linked `Descriptor` record
                primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `DescriptorRelatedDescriptor` record.
        """

        statement = insert(
            DescriptorRelatedDescriptor,
            values={
                "descriptor_id": descriptor_id,
                "related_descriptor_id": related_descriptor_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=DescriptorRelatedDescriptor,
                attrs_names_values={
                    "descriptor_id": descriptor_id,
                    "related_descriptor_id": related_descriptor_id,
                },
                session=session,
            )  # type: DescriptorRelatedDescriptor
            return obj.descriptor_related_descriptor_id

    @return_first_item
    @with_session_scope()
    def iodi_source(
        self,
        source: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Source` record in an IODI manner.

        Args:
            source (str): The source.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Source` record.
        """

        # Create and populate a `Source` object so that we can retrieve the
        # MD5 hash.
        obj = Source()
        obj.source = source

        statement = insert(
            Source,
            values={
                "source": source,
                "md5": obj.md5,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_md5(
                orm_class=Source,
                md5=obj.md5,
                session=session,
            )  # type: Source
            return obj.source_id

    @return_first_item
    @with_session_scope()
    def iodu_supplemental(
        self,
        supplemental_class: SupplementalClassType,
        ui: str,
        name: str,
        created: datetime.date,
        revised: datetime.date,
        note: str,
        frequency: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `Supplemental` record in an IODU manner.

        Args:
            supplemental_class (SupplementalClassType): The supplemental class
                type.
            ui (str): The supplemental UI.
            name (str): The supplemental name.
            created (datetime.date): The date the supplemental was created.
            revised (datetime.date): The date the supplemental was revised.
            note (str): The supplemental note.
            frequency (str): The supplemental frequency.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `Supplemental` record.
        """

        # Upsert the `Supplemental` record.
        statement = insert(
            Supplemental,
            values={
                "class": supplemental_class,
                "ui": ui,
                "name": name,
                "created": created,
                "revised": revised,
                "note": note,
                "frequency": frequency,
            }
        ).on_conflict_do_update(
            set_={
                "class": supplemental_class,
                "name": name,
                "created": created,
                "revised": revised,
                "note": note,
                "frequency": frequency,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=Supplemental,
                attrs_names_values={
                    "ui": ui,
                },
                session=session,
            )  # type: Supplemental
            return obj.supplemental_id

    @return_first_item
    @with_session_scope()
    def iodi_supplemental_heading_mapped_to(
        self,
        supplemental_id: int,
        entry_combination_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `SupplementalHeadingMappedTo` record in an IODI manner.

        Args:
            supplemental_id (int): The linked `Supplemental` record primary-key
                ID.
            entry_combination_id (int): The linked `EntryCombination` record
                primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `SupplementalHeadingMappedTo` record.
        """

        statement = insert(
            SupplementalHeadingMappedTo,
            values={
                "supplemental_id": supplemental_id,
                "entry_combination_id": entry_combination_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=SupplementalHeadingMappedTo,
                attrs_names_values={
                    "supplemental_id": supplemental_id,
                    "entry_combination_id": entry_combination_id,
                },
                session=session,
            )  # type: SupplementalHeadingMappedTo
            return obj.supplemental_heading_mapped_to_id

    @return_first_item
    @with_session_scope()
    def iodi_supplemental_indexing_information(
        self,
        supplemental_id: int,
        entry_combination_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `SupplementalIndexingInformation` record in an IODI
        manner.

        Args:
            supplemental_id (int): The linked `Supplemental` record primary-key
                ID.
            entry_combination_id (int): The linked `EntryCombination` record
                primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `SupplementalIndexingInformation`
                record.
        """

        statement = insert(
            SupplementalIndexingInformation,
            values={
                "supplemental_id": supplemental_id,
                "entry_combination_id": entry_combination_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=SupplementalIndexingInformation,
                attrs_names_values={
                    "supplemental_id": supplemental_id,
                    "entry_combination_id": entry_combination_id,
                },
                session=session,
            )  # type: SupplementalIndexingInformation
            return obj.supplemental_indexing_information_id

    @return_first_item
    @with_session_scope()
    def iodu_supplemental_concept(
        self,
        supplemental_id: int,
        concept_id: int,
        is_preferred: str,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `SupplementalConcept` record in an IODU manner.

        Args:
            supplemental_id (int): The linked `Supplemental` record primary-key
                ID.
            concept_id (int): The linked `Concept` record primary-key ID.
            is_preferred (bool): Whether the concept is the preferred one for
                the supplemental.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `SupplementalConcept` record.
        """

        statement = insert(
            SupplementalConcept,
            values={
                "supplemental_id": supplemental_id,
                "concept_id": concept_id,
                "is_preferred": is_preferred,
            }
        ).on_conflict_do_update(
            set_={
                "is_preferred": is_preferred,
            }
        )  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=SupplementalConcept,
                attrs_names_values={
                    "supplemental_id": supplemental_id,
                    "concept_id": concept_id,
                },
                session=session,
            )  # type: SupplementalConcept
            return obj.supplemental_concept_id

    @return_first_item
    @with_session_scope()
    def iodi_supplemental_previous_indexing(
        self,
        supplemental_id: int,
        previous_indexing_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `SupplementalPreviousIndexing` record in an IODI
        manner.

        Args:
            supplemental_id (int): The linked `Supplemental` record primary-key
                ID.
            previous_indexing_id (int): The linked `PreviousIndexing` record
                primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `SupplementalPreviousIndexing`
                record.
        """

        statement = insert(
            SupplementalPreviousIndexing,
            values={
                "supplemental_id": supplemental_id,
                "previous_indexing_id": previous_indexing_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=SupplementalPreviousIndexing,
                attrs_names_values={
                    "supplemental_id": supplemental_id,
                    "previous_indexing_id": previous_indexing_id,
                },
                session=session,
            )  # type: SupplementalPreviousIndexing
            return obj.supplemental_previous_indexing_id

    @return_first_item
    @with_session_scope()
    def iodi_supplemental_pharmacological_action_descriptor(
        self,
        supplemental_id: int,
        pharmacological_action_descriptor_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `SupplementalPharmacologicalActionDescriptor` record in
        an IODI manner.

        Args:
            supplemental_id (int): The linked `Descriptor` record primary-key
                ID.
            pharmacological_action_descriptor_id (int): The other linked
                `Descriptor` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the
                `SupplementalPharmacologicalActionDescriptor` record.
        """

        statement = insert(
            SupplementalPharmacologicalActionDescriptor,
            values={
                "supplemental_id": supplemental_id,
                "pharmacological_action_descriptor_id": (
                    pharmacological_action_descriptor_id
                ),
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=SupplementalPharmacologicalActionDescriptor,
                attrs_names_values={
                    "supplemental_id": supplemental_id,
                    "pharmacological_action_descriptor_id": (
                        pharmacological_action_descriptor_id
                    ),
                },
                session=session,
            )  # type: SupplementalPharmacologicalActionDescriptor
            return obj.supplemental_pharmacological_action_descriptor_id

    @return_first_item
    @with_session_scope()
    def iodi_supplemental_source(
        self,
        supplemental_id: int,
        source_id: int,
        session: sqlalchemy.orm.Session = None,
    ) -> int:
        """Creates a new `SupplementalSource` record in an IODI manner.

        Args:
            supplemental_id (int): The linked `Supplemental` record primary-key
                ID.
            source_id (int): The linked `Source` record primary-key ID.
            session (sqlalchemy.orm.Session, optional): An SQLAlchemy session
                through which the record will be added. Defaults to `None` in
                which case a new session is automatically created and terminated
                upon completion.

        Returns:
            int: The primary key ID of the `SupplementalSource` record.
        """

        statement = insert(
            SupplementalSource,
            values={
                "supplemental_id": supplemental_id,
                "source_id": source_id,
            }
        ).on_conflict_do_nothing()  # type: Insert

        result = session.execute(statement)  # type: ResultProxy

        if result.inserted_primary_key:
            return result.inserted_primary_key
        else:
            obj = self.get_by_attrs(
                orm_class=SupplementalSource,
                attrs_names_values={
                    "supplemental_id": supplemental_id,
                    "source_id": source_id,
                },
                session=session,
            )  # type: SupplementalSource
            return obj.supplemental_source_id
