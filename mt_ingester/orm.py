# coding=utf-8

import hashlib

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types

from mt_ingester.orm_base import Base, OrmBase
from mt_ingester.orm_enums import DescriptorClassType
from mt_ingester.orm_enums import RelationNameType
from mt_ingester.orm_enums import LexicalTagType
from mt_ingester.orm_enums import EntryCombinationType
from mt_ingester.orm_enums import SupplementalClassType


class TreeNumber(Base, OrmBase):
    """Table of `<TreeNumber>` element records."""

    # Set table name.
    __tablename__ = "tree_numbers"

    # Autoincrementing primary key ID.
    tree_number_id = sqlalchemy.Column(
        name="tree_number_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<TreeNumber>` element.
    tree_number = sqlalchemy.Column(
        name="tree_number",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # MD5 hash of the tree-number.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    # Relationship to a list of `Descriptor` records.
    descriptors = sqlalchemy.orm.relationship(
        argument="Descriptors",
        secondary="mesh.descriptor_tree_numbers",
        back_populates="tree_numbers",
    )

    # Relationship to a list of `Qualifier` records.
    qualifiers = sqlalchemy.orm.relationship(
        argument="Qualifier",
        secondary="mesh.qualifier_tree_numbers",
        back_populates="tree_numbers",
    )

    # Set table arguments.
    __table_args__ = {
        # Set table schema.
        "schema": "mesh"
    }

    @sqlalchemy.orm.validates("tree_number")
    def update_md5(self, key, value):
        # Dumb hack to make the linter shut up that the `key` isn't used.
        assert key

        # Encode the tree-number to UTF8 (in case it contains unicode
        # characters).
        tree_number_encoded = str(value).encode("utf-8")

        # Calculate the MD5 hash of the encoded tree-number and store under the
        # `md5` attribute.
        md5 = hashlib.md5(tree_number_encoded).digest()
        self.md5 = md5

        return value


class ThesaurusId(Base, OrmBase):
    """Table of `<ThesaurusID>` element records."""

    # Set table name.
    __tablename__ = "thesaurus_ids"

    # Autoincrementing primary key ID.
    thesaurus_id_id = sqlalchemy.Column(
        name="thesaurus_id_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<ThesaurusID>` element.
    thesaurus_id = sqlalchemy.Column(
        name="thesaurus_id",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # MD5 hash of the tree-number.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    # Relationship to a list of `Term` records.
    terms = sqlalchemy.orm.relationship(
        argument="Term",
        secondary="mesh.term_thesaurus_ids",
        back_populates="thesaurus_ids",
    )

    # Set table arguments.
    __table_args__ = {
        # Set table schema.
        "schema": "mesh"
    }

    @sqlalchemy.orm.validates("thesaurus_id")
    def update_md5(self, key, value):
        # Dumb hack to make the linter shut up that the `key` isn't used.
        assert key

        # Encode the thesaurus-id to UTF8 (in case it contains unicode
        # characters).
        thesaurus_id_encoded = str(value).encode("utf-8")

        # Calculate the MD5 hash of the encoded thesaurus-id and store under the
        # `md5` attribute.
        md5 = hashlib.md5(thesaurus_id_encoded).digest()
        self.md5 = md5

        return value


class Term(Base, OrmBase):
    """Table of `<Term>` element records."""

    # Set table name.
    __tablename__ = "terms"

    # Autoincrementing primary key ID.
    term_id = sqlalchemy.Column(
        name="term_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<ConceptUI>` element.
    ui = sqlalchemy.Column(
        name="ui",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
        unique=True,
    )

    # Referring to the `<ConceptName>` element.
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the value of the `<DateCreated>` element.
    created = sqlalchemy.Column(
        name="created",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the `<Abbreviation>` element.
    abbreviation = sqlalchemy.Column(
        name="abbreviation",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<SortVersion>` element.
    sort_version = sqlalchemy.Column(
        name="sort_version",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<EntryVersion>` element.
    entry_version = sqlalchemy.Column(
        name="entry_version",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `ThesaurusId` records.
    thesaurus_ids = sqlalchemy.orm.relationship(
        argument="ThesaurusId",
        secondary="mesh.term_thesaurus_ids",
        back_populates="terms",
    )

    # Referring to the `<TermNote>` element.
    note = sqlalchemy.Column(
        name="note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Relationship to a list of `Concept` records.
    concepts = sqlalchemy.orm.relationship(
        argument="Concept",
        secondary="mesh.concept_terms",
        back_populates="terms",
    )


class TermThesaurusId(Base, OrmBase):
    """Associative table between `Term` and `ThesaurusId` records."""

    # Set table name.
    __tablename__ = "term_thesaurus_ids"

    # Autoincrementing primary key ID.
    term_thesaurus_id_id = sqlalchemy.Column(
        name="term_thesaurus_id_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the term ID.
    term_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.terms.term_id"),
        name="term_id",
        nullable=False,
    )

    # Foreign key to the tree-number ID.
    thesaurus_id_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.thesaurus_ids.thesaurus_id_id",
        ),
        name="thesaurus_id_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('term_id', 'thesaurus_id_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class Concept(Base, OrmBase):
    """Table of `<Concept>` element records."""

    # Set table name.
    __tablename__ = "concepts"

    # Autoincrementing primary key ID.
    concept_id = sqlalchemy.Column(
        name="concept_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<ConceptUI>` element.
    ui = sqlalchemy.Column(
        name="ui",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
        unique=True,
    )

    # Referring to the `<ConceptName>` element.
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the `<CASN1Name>` element.
    casn1_name = sqlalchemy.Column(
        name="casn1_name",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<RegistryNumber>` element.
    registry_number = sqlalchemy.Column(
        name="registry_number",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
        index=True,
    )

    # Referring to the `<ScopeNote>` element.
    scope_note = sqlalchemy.Column(
        name="scope_note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the `<TranslatorsEnglishScopeNote>` element.
    translators_english_scope_note = sqlalchemy.Column(
        name="translators_english_scope_note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the `<TranslatorsScopeNote>` element.
    translators_scope_note = sqlalchemy.Column(
        name="translators_scope_note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # TODO: RelatedRegistryNumberList (nullable)

    # Relationship to a list of `Concept` records referenced in concept-relation
    # elements.
    related_concepts = sqlalchemy.orm.relationship(
        argument="Concept",
        secondary="mesh.concept_related_concepts",
    )

    # Relationship to a list of `Term` records.
    terms = sqlalchemy.orm.relationship(
        argument="Term",
        secondary="mesh.concept_terms",
        back_populates="concepts",
    )

    # Relationship to a list of `Qualifier` records.
    qualifiers = sqlalchemy.orm.relationship(
        argument="Qualifier",
        secondary="mesh.qualifier_concepts",
        back_populates="concepts",
    )

    # Relationship to a list of `Descriptor` records.
    descriptors = sqlalchemy.orm.relationship(
        argument="Descriptor",
        secondary="mesh.qualifier_descriptors",
        back_populates="concepts",
    )

    # Relationship to a list of `Supplemental` records.
    supplementals = sqlalchemy.orm.relationship(
        argument="Supplemental",
        secondary="mesh.supplemental_concepts",
        back_populates="concepts",
    )


class ConceptRelatedConcept(Base, OrmBase):
    """Associative table between `Concept` and other `Concept` records
    referenced in concept-relation elements."""

    # Set table name.
    __tablename__ = "concept_related_concepts"

    # Autoincrementing primary key ID.
    concept_related_concept_id = sqlalchemy.Column(
        name="concept_related_concept_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    concept_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.concepts.concept_id"),
        name="concept_id",
        nullable=False,
    )

    # Foreign key to the related descriptor ID.
    related_concept_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.concepts.concept_id"),
        name="related_concept_id",
        nullable=False,
    )

    # Referring to the value of the `RelationName` attribute of the
    # `<ConceptRelation>` element casted to a boolean.
    relation_name = sqlalchemy.Column(
        name="relation_name",
        type_=sqlalchemy.types.Enum(RelationNameType),
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('concept_id', 'related_concept_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class ConceptTerm(Base, OrmBase):
    """Associative table between `Concept` and `Term` records."""

    # Set table name.
    __tablename__ = "concept_terms"

    # Autoincrementing primary key ID.
    concept_term_id = sqlalchemy.Column(
        name="concept_term_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the concept ID.
    concept_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.concepts.concept_id"),
        name="concept_id",
        nullable=False,
    )

    # Foreign key to the term ID.
    term_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.terms.term_id"),
        name="term_id",
        nullable=False,
    )

    # Referring to the value of the `ConceptPreferredTermYN` attribute of the
    # `<Term>` element casted to a boolean.
    is_concept_preferred_term = sqlalchemy.Column(
        name="is_concept_preferred_term",
        type_=sqlalchemy.types.Boolean(),
        nullable=False,
    )

    # Referring to the value of the `IsPermutedTermYN` attribute of the `<Term>`
    # element casted to a boolean.
    is_permuted_term = sqlalchemy.Column(
        name="is_permuted_term",
        type_=sqlalchemy.types.Boolean(),
        nullable=False,
    )

    # Referring to the value of the `LexicalTag` attribute of the `<Term>`
    # element casted to a boolean.
    lexical_tag = sqlalchemy.Column(
        name="lexical_tag",
        type_=sqlalchemy.types.Enum(LexicalTagType),
        nullable=False,
    )

    # Referring to the value of the `RecordPreferredTermYN` attribute of the
    # `<Term>` element casted to a boolean.
    is_record_preferred_term = sqlalchemy.Column(
        name="is_record_preferred_term",
        type_=sqlalchemy.types.Boolean(),
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('descriptor_id', 'qualifier_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class Qualifier(Base, OrmBase):
    """Table of `<Qualifier>` element records."""

    # Set table name.
    __tablename__ = "qualifiers"

    # Autoincrementing primary key ID.
    qualifier_id = sqlalchemy.Column(
        name="qualifier_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<QualifierUI>` element.
    ui = sqlalchemy.Column(
        name="ui",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
        unique=True,
    )

    # Referring to the `<QualifierName>` element.
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the value of the `<DateCreated>` element.
    created = sqlalchemy.Column(
        name="created",
        type_=sqlalchemy.types.Date(),
        nullable=False,
    )

    # Referring to the value of the `<DateRevised>` element.
    revised = sqlalchemy.Column(
        name="revised",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<DateEstablished>` element.
    established = sqlalchemy.Column(
        name="established",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the `<Annotation>` element.
    annotation = sqlalchemy.Column(
        name="annotation",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the `<HistoryNote>` element.
    history_note = sqlalchemy.Column(
        name="history_note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the `<OnlineNote>` element.
    online_note = sqlalchemy.Column(
        name="online_note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Relationship to a list of `TreeNumber` records.
    tree_numbers = sqlalchemy.orm.relationship(
        argument="TreeNumber",
        secondary="mesh.qualifier_tree_numbers",
        back_populates="qualifiers",
    )

    # Relationship to a list of `Concept` records.
    concepts = sqlalchemy.orm.relationship(
        argument="Concept",
        secondary="mesh.qualifier_concepts",
        back_populates="qualifiers",
    )

    # Relationship to a list of `Descriptor` records.
    descriptors = sqlalchemy.orm.relationship(
        argument="Descriptor",
        secondary="mesh.descriptor_allowable_qualifiers",
        back_populates="qualifiers",
    )


class QualifierConcept(Base, OrmBase):
    """Associative table between `Qualifier` and `Concept` records."""

    # Set table name.
    __tablename__ = "qualifier_concepts"

    # Autoincrementing primary key ID.
    qualifier_concept_id = sqlalchemy.Column(
        name="qualifier_concept_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the qualifier ID.
    qualifier_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.qualifiers.qualifier_id"),
        name="qualifier_id",
        nullable=False,
    )

    # Foreign key to the concept ID.
    concept_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.concepts.concept_id"),
        name="concept_id",
        nullable=False,
    )

    # Referring to the value of the `PreferredConceptYN` attribute of the
    # `<Concept>` element casted to a boolean.
    is_preferred = sqlalchemy.Column(
        name="is_preferred",
        type_=sqlalchemy.types.Boolean(),
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('qualifier_id', 'concept_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class QualifierTreeNumber(Base, OrmBase):
    """Associative table between `Qualifier` and `TreeNumber` records."""

    # Set table name.
    __tablename__ = "qualifier_tree_numbers"

    # Autoincrementing primary key ID.
    qualifier_tree_number_id = sqlalchemy.Column(
        name="qualifier_tree_number_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the qualifier ID.
    qualifier_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.qualifiers.qualifier_id"),
        name="qualifier_id",
        nullable=False,
    )

    # Foreign key to the tree-number ID.
    tree_number_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.tree_numbers.tree_number_id",
        ),
        name="tree_number_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('qualifier_id', 'tree_number_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class PreviousIndexing(Base, OrmBase):
    """Table of `<PreviousIndexing>` element records."""

    # Set table name.
    __tablename__ = "previous_indexings"

    # Autoincrementing primary key ID.
    previous_indexing_id = sqlalchemy.Column(
        name="previous_indexing_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<PreviousIndexing>` element.
    previous_indexing = sqlalchemy.Column(
        name="previous_indexing",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Relationship to a list of `Descriptors` records.
    descriptors = sqlalchemy.orm.relationship(
        argument="Descriptors",
        secondary="mesh.descriptor_previous_indexings",
        back_populates="previous_indexings",
    )

    # Relationship to a list of `Supplemental` records.
    supplementals = sqlalchemy.orm.relationship(
        argument="Supplemental",
        secondary="mesh.supplemental_previous_indexings",
        back_populates="previous_indexings",
    )

    # MD5 hash of the tree-number.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = {
        # Set table schema.
        "schema": "mesh"
    }

    @sqlalchemy.orm.validates("previous_indexing")
    def update_md5(self, key, value):
        # Dumb hack to make the linter shut up that the `key` isn't used.
        assert key

        # Encode the previous-indexing to UTF8 (in case it contains unicode
        # characters).
        previous_indexing_encoded = str(value).encode("utf-8")

        # Calculate the MD5 hash of the encoded previous-indexing and store
        # under the `md5` attribute.
        md5 = hashlib.md5(previous_indexing_encoded).digest()
        self.md5 = md5

        return value


class EntryCombination(Base, OrmBase):
    """Associative table between `Descriptor` and `Qualifier` records denoting
    descriptor-qualifier combinations defined in `<EntryCombination>`,
    `<IndexingInformation>`, and `<HeadingMappedTo>` elements."""

    # Set table name.
    __tablename__ = "entry_combinations"

    # Autoincrementing primary key ID.
    entry_combination_id = sqlalchemy.Column(
        name="entry_combination_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="descriptor_id",
        nullable=False,
    )

    # Foreign key to the qualifier ID.
    qualifier_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.qualifiers.qualifier_id"),
        name="qualifier_id",
        nullable=True,
    )

    # Whether this combination was defined under an `<ECIN>` or `<ECOUT>`
    # element. This only applies to `<EntryCombination>` elements.
    combination_type = sqlalchemy.Column(
        name="type",
        type_=sqlalchemy.types.Enum(EntryCombinationType),
        nullable=True,
    )

    # Relationship to a list of `Descriptor` records.
    descriptors = sqlalchemy.orm.relationship(
        argument="Descriptor",
        back_populates="entry_combinations",
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('descriptor_id', 'qualifier_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class Descriptor(Base, OrmBase):
    """Table of `<DescriptorRecord>` element records."""

    # Set table name.
    __tablename__ = "descriptors"

    # Autoincrementing primary key ID.
    descriptor_id = sqlalchemy.Column(
        name="descriptor_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `DescriptorClass` attribute of the
    # `<DescriptorRecord>` element.
    descriptor_class = sqlalchemy.Column(
        name="class",
        type_=sqlalchemy.types.Enum(DescriptorClassType),
        nullable=False,
    )

    # Referring to the `<DescriptorUI>` element.
    ui = sqlalchemy.Column(
        name="ui",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
        unique=True,
        index=False
    )

    # Referring to the `<DescriptorName>` element.
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the value of the `<DateCreated>` element.
    created = sqlalchemy.Column(
        name="created",
        type_=sqlalchemy.types.Date(),
        nullable=False,
    )

    # Referring to the value of the `<DateRevised>` element.
    revised = sqlalchemy.Column(
        name="revised",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the value of the `<DateEstablished>` element.
    established = sqlalchemy.Column(
        name="established",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Relationship to a list of `Qualifier` records.
    allowable_qualifiers = sqlalchemy.orm.relationship(
        argument="Qualifier",
        secondary="mesh.descriptor_allowable_qualifiers",
        back_populates="descriptors",
    )

    # Referring to the `<Annotation>` element.
    annotation = sqlalchemy.Column(
        name="annotation",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the `<HistoryNote>` element.
    history_note = sqlalchemy.Column(
        name="history_note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the `<NLMClassificationNumber>` element.
    nlm_classification_number = sqlalchemy.Column(
        name="nlm_classification_number",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Referring to the `<OnlineNote>` element.
    online_note = sqlalchemy.Column(
        name="online_note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the `<PublicMeSHNote>` element.
    public_mesh_note = sqlalchemy.Column(
        name="public_mesh_note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Relationship to a list of `PreviousIndexing` records.
    previous_indexings = sqlalchemy.orm.relationship(
        argument="PreviousIndexing",
        secondary="mesh.descriptor_previous_indexings",
        back_populates="descriptors",
    )

    # Relationship to a list of `EntryCombination` records.
    entry_combinations = sqlalchemy.orm.relationship(
        argument="EntryCombination",
        secondary="mesh.descriptor_entry_combinations",
        back_populates="descriptors",
    )

    # Relationship to a list of `Descriptor` records referenced in
    # see-related elements.
    related_descriptors = sqlalchemy.orm.relationship(
        argument="Descriptor",
        secondary="mesh.descriptor_related_descriptors",
    )

    # Referring to the `<ConsiderAlso>` element.
    consider_also = sqlalchemy.Column(
        name="consider_also",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `Descriptor` records referenced in
    # pharmacological-actions.
    pharmacological_action_descriptors = sqlalchemy.orm.relationship(
        argument="Descriptor",
        secondary="mesh.descriptor_pharmacological_action_descriptors",
    )

    # Relationship to a list of `TreeNumber` records.
    tree_numbers = sqlalchemy.orm.relationship(
        argument="TreeNumber",
        secondary="mesh.descriptor_tree_numbers",
        back_populates="descriptors",
    )

    # Relationship to a list of `Concept` records.
    concepts = sqlalchemy.orm.relationship(
        argument="Concept",
        secondary="mesh.descriptor_concepts",
        back_populates="descriptors",
    )


class DescriptorEntryCombination(Base, OrmBase):
    """Associative table between `Descriptor` and `EntryCombination` records."""

    # Set table name.
    __tablename__ = "descriptor_entry_combinations"

    # Autoincrementing primary key ID.
    descriptor_entry_combination_id = sqlalchemy.Column(
        name="descriptor_entry_combination_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="descriptor_id",
        nullable=False,
    )

    # Foreign key to the entry-combination ID.
    entry_combination_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.entry_combinations.entry_combination_id",
        ),
        name="entry_combination_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('descriptor_id', 'entry_combination_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class DescriptorConcept(Base, OrmBase):
    """Associative table between `Descriptor` and `Concept` records."""

    # Set table name.
    __tablename__ = "descriptor_concepts"

    # Autoincrementing primary key ID.
    descriptor_concept_id = sqlalchemy.Column(
        name="descriptor_concept_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="descriptor_id",
        nullable=False,
    )

    # Foreign key to the concept ID.
    concept_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.concepts.concept_id"),
        name="concept_id",
        nullable=False,
    )

    # Referring to the value of the `PreferredConceptYN` attribute of the
    # `<Concept>` element casted to a boolean.
    is_preferred = sqlalchemy.Column(
        name="is_preferred",
        type_=sqlalchemy.types.Boolean(),
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('descriptor_id', 'concept_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class DescriptorPreviousIndexing(Base, OrmBase):
    """Associative table between `Descriptor` and `PreviousIndexing` records."""

    # Set table name.
    __tablename__ = "descriptor_previous_indexings"

    # Autoincrementing primary key ID.
    descriptor_previous_indexing_id = sqlalchemy.Column(
        name="descriptor_previous_indexing_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="descriptor_id",
        nullable=False,
    )

    # Foreign key to the previous-indexing ID.
    previous_indexing_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.previous_indexings.previous_indexing_id",
        ),
        name="previous_indexing_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('descriptor_id', 'previous_indexing_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class DescriptorAllowableQualifier(Base, OrmBase):
    """Associative table between `Descriptor` and `Qualifier` records denoting
    which qualifiers are allowed for a given descriptor."""

    # Set table name.
    __tablename__ = "descriptor_allowable_qualifiers"

    # Autoincrementing primary key ID.
    descriptor_allowable_qualifier_id = sqlalchemy.Column(
        name="descriptor_allowable_qualifier_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="descriptor_id",
        nullable=False,
    )

    # Foreign key to the qualifier ID.
    qualifier_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.qualifiers.qualifier_id"),
        name="qualifier_id",
        nullable=False,
    )

    # Referring to the `<Abbreviation>` element.
    abbreviation = sqlalchemy.Column(
        name="abbreviation",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('descriptor_id', 'qualifier_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class DescriptorTreeNumber(Base, OrmBase):
    """Associative table between `Descriptor` and `TreeNumber` records."""

    # Set table name.
    __tablename__ = "descriptor_tree_numbers"

    # Autoincrementing primary key ID.
    descriptor_tree_number_id = sqlalchemy.Column(
        name="descriptor_tree_number_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="descriptor_id",
        nullable=False,
    )

    # Foreign key to the tree-number ID.
    tree_number_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.tree_numbers.tree_number_id",
        ),
        name="tree_number_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('descriptor_id', 'tree_number_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class DescriptorPharmacologicalActionDescriptor(Base, OrmBase):
    """Associative table between `Descriptor` and other `Descriptor` records
    referenced in pharmacological-actions."""

    # Set table name.
    __tablename__ = "descriptor_pharmacological_action_descriptors"

    # Autoincrementing primary key ID.
    descriptor_pharmacological_action_descriptor_id = sqlalchemy.Column(
        name="descriptor_pharmacological_action_descriptor_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="descriptor_id",
        nullable=False,
    )

    # Foreign key to the pharmacological-action-referenced descriptor ID.
    pharmacological_action_descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="pharmacological_action_descriptor_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint(
            'descriptor_id',
            'pharmacological_action_descriptor_id',
        ),
        # Set table schema.
        {"schema": "mesh"}
    )


class DescriptorRelatedDescriptor(Base, OrmBase):
    """Associative table between `Descriptor` and other `Descriptor` records
    referenced in see-related elements."""

    # Set table name.
    __tablename__ = "descriptor_related_descriptors"

    # Autoincrementing primary key ID.
    descriptor_related_descriptor_id = sqlalchemy.Column(
        name="descriptor_related_descriptor_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the descriptor ID.
    descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="descriptor_id",
        nullable=False,
    )

    # Foreign key to the related descriptor ID.
    related_descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="related_descriptor_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('descriptor_id', 'related_descriptor_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class Source(Base, OrmBase):
    """Table of `<Source>` element records."""

    # Set table name.
    __tablename__ = "sources"

    # Autoincrementing primary key ID.
    source_id = sqlalchemy.Column(
        name="source_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the `<Source>` element.
    source = sqlalchemy.Column(
        name="source",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # MD5 hash of the tree-number.
    md5 = sqlalchemy.Column(
        name="md5",
        type_=sqlalchemy.types.Binary(),
        unique=True,
        index=True,
        nullable=False,
    )

    # Relationship to a list of `Supplemental` records.
    supplementals = sqlalchemy.orm.relationship(
        argument="Supplemental",
        secondary="mesh.supplemental_sources",
        back_populates="sources",
    )

    # Set table arguments.
    __table_args__ = {
        # Set table schema.
        "schema": "mesh"
    }

    @sqlalchemy.orm.validates("source")
    def update_md5(self, key, value):
        # Dumb hack to make the linter shut up that the `key` isn't used.
        assert key

        # Encode the source to UTF8 (in case it contains unicode characters).
        source_encoded = str(value).encode("utf-8")

        # Calculate the MD5 hash of the encoded source and store under the `md5`
        # attribute.
        md5 = hashlib.md5(source_encoded).digest()
        self.md5 = md5

        return value


class Supplemental(Base, OrmBase):
    """Table of `<SupplementalRecord>` element records."""

    # Set table name.
    __tablename__ = "supplementals"

    # Autoincrementing primary key ID.
    supplemental_id = sqlalchemy.Column(
        name="supplemental_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Referring to the value of the `SCRClass` attribute of the
    # `<SupplementalRecord>` element.
    supplemental_class = sqlalchemy.Column(
        name="class",
        type_=sqlalchemy.types.Enum(SupplementalClassType),
        nullable=False,
    )

    # Referring to the `<SupplementalRecordUI>` element.
    ui = sqlalchemy.Column(
        name="ui",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
        unique=True,
        index=False
    )

    # Referring to the `<SupplementalRecordName>` element.
    name = sqlalchemy.Column(
        name="name",
        type_=sqlalchemy.types.Unicode(),
        nullable=False,
    )

    # Referring to the value of the `<DateCreated>` element.
    created = sqlalchemy.Column(
        name="created",
        type_=sqlalchemy.types.Date(),
        nullable=False,
    )

    # Referring to the value of the `<DateRevised>` element.
    revised = sqlalchemy.Column(
        name="revised",
        type_=sqlalchemy.types.Date(),
        nullable=True,
    )

    # Referring to the `<Note>` element.
    note = sqlalchemy.Column(
        name="note",
        type_=sqlalchemy.types.UnicodeText(),
        nullable=True,
    )

    # Referring to the `<Frequency>` element.
    frequency = sqlalchemy.Column(
        name="frequency",
        type_=sqlalchemy.types.Unicode(),
        nullable=True,
    )

    # Relationship to a list of `PreviousIndexing` records.
    previous_indexings = sqlalchemy.orm.relationship(
        argument="PreviousIndexing",
        secondary="mesh.supplemental_previous_indexings",
        back_populates="supplementals",
    )

    # Relationship to a list of `EntryCombination` records defined via
    # `<HeadingMappedTo>` elements.
    heading_mapped_tos = sqlalchemy.orm.relationship(
        argument="EntryCombination",
        secondary="mesh.supplemental_heading_mapped_tos",
    )

    # Relationship to a list of `EntryCombination` records defined via
    # `<IndexingInformation>` elements.
    indexing_informations = sqlalchemy.orm.relationship(
        argument="EntryCombination",
        secondary="mesh.supplemental_indexing_informations",
    )

    # Relationship to a list of `Descriptor` records referenced in
    # pharmacological-actions.
    pharmacological_action_descriptors = sqlalchemy.orm.relationship(
        argument="Descriptor",
        secondary="mesh.supplemental_pharmacological_action_descriptors",
    )

    # Relationship to a list of `Source` records.
    sources = sqlalchemy.orm.relationship(
        argument="Source",
        secondary="mesh.supplemental_sources",
        back_populates="supplementals",
    )

    # Relationship to a list of `Concept` records.
    concepts = sqlalchemy.orm.relationship(
        argument="Concept",
        secondary="mesh.supplemental_concepts",
        back_populates="supplementals",
    )


class SupplementalHeadingMappedTo(Base, OrmBase):
    """Associative table between `Descriptor` and `EntryCombination` records
    via `<HeadingMappedTo>` elements."""

    # Set table name.
    __tablename__ = "supplemental_heading_mapped_tos"

    # Autoincrementing primary key ID.
    supplemental_heading_mapped_to_id = sqlalchemy.Column(
        name="supplemental_heading_mapped_to_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the supplemental ID.
    supplemental_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.supplementals.supplemental_id"),
        name="supplemental_id",
        nullable=False,
    )

    # Foreign key to the entry-combination ID.
    entry_combination_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.entry_combinations.entry_combination_id",
        ),
        name="entry_combination_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('supplemental_id', 'entry_combination_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class SupplementalIndexingInformation(Base, OrmBase):
    """Associative table between `Descriptor` and `EntryCombination` records
    via `<IndexingInformation>` elements."""

    # Set table name.
    __tablename__ = "supplemental_indexing_informations"

    # Autoincrementing primary key ID.
    supplemental_indexing_information_id = sqlalchemy.Column(
        name="supplemental_indexing_information_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the supplemental ID.
    supplemental_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.supplementals.supplemental_id"),
        name="supplemental_id",
        nullable=False,
    )

    # Foreign key to the entry-combination ID.
    entry_combination_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.entry_combinations.entry_combination_id",
        ),
        name="entry_combination_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('supplemental_id', 'entry_combination_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class SupplementalConcept(Base, OrmBase):
    """Associative table between `Supplemental` and `Concept` records."""

    # Set table name.
    __tablename__ = "supplemental_concepts"

    # Autoincrementing primary key ID.
    supplemental_concept_id = sqlalchemy.Column(
        name="supplemental_concept_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the supplemental ID.
    supplemental_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.supplementals.supplemental_id"),
        name="supplemental_id",
        nullable=False,
    )

    # Foreign key to the concept ID.
    concept_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.concepts.concept_id"),
        name="concept_id",
        nullable=False,
    )

    # Referring to the value of the `PreferredConceptYN` attribute of the
    # `<Concept>` element casted to a boolean.
    is_preferred = sqlalchemy.Column(
        name="is_preferred",
        type_=sqlalchemy.types.Boolean(),
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('supplemental_id', 'concept_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class SupplementalPreviousIndexing(Base, OrmBase):
    """Associative table between `Supplemental` and `PreviousIndexing`
    records."""

    # Set table name.
    __tablename__ = "supplemental_previous_indexings"

    # Autoincrementing primary key ID.
    supplemental_previous_indexing_id = sqlalchemy.Column(
        name="supplemental_previous_indexing_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the supplemental ID.
    supplemental_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.supplementals.supplemental_id"),
        name="supplemental_id",
        nullable=False,
    )

    # Foreign key to the previous-indexing ID.
    previous_indexing_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.previous_indexings.previous_indexing_id",
        ),
        name="previous_indexing_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('supplemental_id', 'previous_indexing_id'),
        # Set table schema.
        {"schema": "mesh"}
    )


class SupplementalPharmacologicalActionDescriptor(Base, OrmBase):
    """Associative table between `Supplemental` and `Descriptor` records
    referenced in pharmacological-actions."""

    # Set table name.
    __tablename__ = "supplemental_pharmacological_action_descriptors"

    # Autoincrementing primary key ID.
    supplemental_pharmacological_action_descriptor_id = sqlalchemy.Column(
        name="supplemental_pharmacological_action_descriptor_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the supplemental ID.
    supplemental_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.supplementals.supplemental_id"),
        name="supplemental_id",
        nullable=False,
    )

    # Foreign key to the pharmacological-action-referenced descriptor ID.
    pharmacological_action_descriptor_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.descriptors.descriptor_id"),
        name="pharmacological_action_descriptor_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint(
            'descriptor_id',
            'pharmacological_action_descriptor_id',
        ),
        # Set table schema.
        {"schema": "mesh"}
    )


class SupplementalSource(Base, OrmBase):
    """Associative table between `Supplemental` and `Source` records."""

    # Set table name.
    __tablename__ = "supplemental_sources"

    # Autoincrementing primary key ID.
    supplemental_source_id = sqlalchemy.Column(
        name="supplemental_source_id",
        type_=sqlalchemy.types.BigInteger(),
        primary_key=True,
        autoincrement="auto",
    )

    # Foreign key to the supplemental ID.
    supplemental_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("mesh.supplementals.supplemental_id"),
        name="supplemental_id",
        nullable=False,
    )

    # Foreign key to the source ID.
    source_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            "mesh.sources.source_id",
        ),
        name="source_id",
        nullable=False,
    )

    # Set table arguments.
    __table_args__ = (
        # Set unique constraint.
        sqlalchemy.UniqueConstraint('supplemental_id', 'source_id'),
        # Set table schema.
        {"schema": "mesh"}
    )
