# coding=utf-8

from mt_ingester.utils import EnumBase


class DescriptorClassType(EnumBase):
    """Enumeration of the descriptor-class types."""

    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"


class RelationNameType(EnumBase):
    """Enumeration of the relation-name types."""

    NRW = "NRW"
    BRD = "BRD"
    REL = "REL"


class LexicalTagType(EnumBase):
    """Enumeration of the lexical-tag types."""

    ABB = "ABB"
    ABX = "ABX"
    ACR = "ACR"
    ACX = "ACX"
    EPO = "EPO"
    LAB = "LAB"
    NAM = "NAM"
    NON = "NON"
    TRD = "TRD"
    Frelex = "Frelex"


class EntryCombinationType(EnumBase):
    """Enumeration of the entry-combination types."""

    ECIN = "ECIN"
    ECOUT = "ECOUT"


class SupplementalClassType(EnumBase):
    """Enumeration of the supplemental-class types."""

    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
