# coding=utf-8

import enum
import tempfile


sample_desc = """<?xml version="1.0"?>
<!DOCTYPE DescriptorRecordSet SYSTEM "https://www.nlm.nih.gov/databases/dtd/nlmdescriptorrecordset_20190101.dtd">
<DescriptorRecordSet LanguageCode="eng">
    <DescriptorRecord DescriptorClass="1">
        <DescriptorUI>D000001</DescriptorUI>
        <DescriptorName>
            <String>Calcimycin</String>
        </DescriptorName>
        <DateCreated>
            <Year>1974</Year>
            <Month>11</Month>
            <Day>19</Day>
        </DateCreated>
        <DateRevised>
            <Year>2016</Year>
            <Month>05</Month>
            <Day>27</Day>
        </DateRevised>
        <DateEstablished>
            <Year>1984</Year>
            <Month>01</Month>
            <Day>01</Day>
        </DateEstablished>
        <AllowableQualifiersList>
            <AllowableQualifier>
                <QualifierReferredTo>
                    <QualifierUI>Q000302</QualifierUI>
                    <QualifierName>
                        <String>isolation &amp; purification</String>
                    </QualifierName>
                </QualifierReferredTo>
                <Abbreviation>IP</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
                <QualifierReferredTo>
                    <QualifierUI>Q000276</QualifierUI>
                    <QualifierName>
                        <String>immunology</String>
                    </QualifierName>
                </QualifierReferredTo>
                <Abbreviation>IM</Abbreviation>
            </AllowableQualifier>
            <AllowableQualifier>
                <QualifierReferredTo>
                    <QualifierUI>Q000493</QualifierUI>
                    <QualifierName>
                        <String>pharmacokinetics</String>
                    </QualifierName>
                </QualifierReferredTo>
                <Abbreviation>PK</Abbreviation>
            </AllowableQualifier>
        </AllowableQualifiersList>
        <Annotation>for use to kill or control insects...
        </Annotation>
        <SeeRelatedList>
            <SeeRelatedDescriptor>
                <DescriptorReferredTo>
                    <DescriptorUI>D004653</DescriptorUI>
                    <DescriptorName>
                        <String>Empyema</String>
                    </DescriptorName>
                </DescriptorReferredTo>
            </SeeRelatedDescriptor>
           <SeeRelatedDescriptor>
                <DescriptorReferredTo>
                    <DescriptorUI>D007408</DescriptorUI>
                    <DescriptorName>
                        <String>Intestinal Absorption</String>
                    </DescriptorName>
                </DescriptorReferredTo>
            </SeeRelatedDescriptor>
        </SeeRelatedList>
        <ConsiderAlso>consider also terms at PROCT-
        </ConsiderAlso>
        <HistoryNote>91(75); was A 23187 1975-90 (see under ANTIBIOTICS 1975-83)
        </HistoryNote>
        <NLMClassificationNumber>QV 175</NLMClassificationNumber>
        <OnlineNote>use CALCIMYCIN to search A 23187 1975-90
        </OnlineNote>
        <PublicMeSHNote>91; was A 23187 1975-90 (see under ANTIBIOTICS 1975-83)
        </PublicMeSHNote>
        <EntryCombinationList>
            <EntryCombination>
                <ECIN>
                    <DescriptorReferredTo>
                        <DescriptorUI>D000022</DescriptorUI>
                        <DescriptorName>
                            <String>Abortion, Spontaneous</String>
                        </DescriptorName>
                    </DescriptorReferredTo>
                    <QualifierReferredTo>
                        <QualifierUI>Q000662</QualifierUI>
                        <QualifierName>
                            <String>veterinary</String>
                        </QualifierName>
                    </QualifierReferredTo>
                </ECIN>
                <ECOUT>
                    <DescriptorReferredTo>
                        <DescriptorUI>D000034</DescriptorUI>
                        <DescriptorName>
                            <String>Abortion, Veterinary</String>
                        </DescriptorName>
                    </DescriptorReferredTo>
                </ECOUT>
            </EntryCombination>
        </EntryCombinationList>
        <PreviousIndexingList>
            <PreviousIndexing>Antibiotics (1973-1974)</PreviousIndexing>
            <PreviousIndexing>Carboxylic Acids (1973-1974)</PreviousIndexing>
        </PreviousIndexingList>
        <PharmacologicalActionList>
            <PharmacologicalAction>
                <DescriptorReferredTo>
                    <DescriptorUI>D000900</DescriptorUI>
                    <DescriptorName>
                        <String>Anti-Bacterial Agents</String>
                    </DescriptorName>
                </DescriptorReferredTo>
            </PharmacologicalAction>
            <PharmacologicalAction>
                <DescriptorReferredTo>
                    <DescriptorUI>D061207</DescriptorUI>
                    <DescriptorName>
                        <String>Calcium Ionophores</String>
                    </DescriptorName>
                </DescriptorReferredTo>
            </PharmacologicalAction>
        </PharmacologicalActionList>
        <TreeNumberList>
            <TreeNumber>D03.633.100.221.173</TreeNumber>
            <TreeNumber>D03.633.100.221.174</TreeNumber>
        </TreeNumberList>
        <ConceptList>
            <Concept PreferredConceptYN="Y">
                <ConceptUI>M0000001</ConceptUI>
                <ConceptName>
                    <String>Calcimycin</String>
                </ConceptName>
                <CASN1Name>4-Benzoxazolecarboxylic acid,5-(methylamino)-2-((3,9,11-trimethyl-8-(1-methyl-2-oxo-2-(1H-pyrrol-2-yl)ethyl)-1,7-dioxaspiro(5.5)undec-2-yl)methyl)-, (6S-(6alpha(2S*,3S*),8beta(R*),9beta,11alpha))-
                </CASN1Name>
                <RegistryNumber>37H9VM9WZL</RegistryNumber>
                <ScopeNote>An ionophorous, polyether antibiotic from Streptomyces chartreusensis. It binds and transports CALCIUM and other divalent cations across membranes and uncouples oxidative phosphorylation while inhibiting ATPase of rat liver mitochondria. The substance is used mostly as a biochemical tool to study the role of divalent cations in various biological systems.
                </ScopeNote>
                <RelatedRegistryNumberList>
                    <RelatedRegistryNumber>52665-69-7 (Calcimycin)</RelatedRegistryNumber>
                    <RelatedRegistryNumber>3383-96-8 (Temefos)</RelatedRegistryNumber>
                </RelatedRegistryNumberList>
                <ConceptRelationList>
                     <ConceptRelation RelationName="NRW">
                        <Concept1UI>M0000002</Concept1UI>
                        <Concept2UI>M0352201</Concept2UI>
                     </ConceptRelation>
                     <ConceptRelation RelationName="NRW">
                         <Concept1UI>M0000002</Concept1UI>
                         <Concept2UI>M0352200</Concept2UI>
                     </ConceptRelation>
                 </ConceptRelationList>
                <TermList>
                    <Term ConceptPreferredTermYN="Y" IsPermutedTermYN="N"
                          LexicalTag="NON" RecordPreferredTermYN="Y">
                        <TermUI>T000002</TermUI>
                        <String>Calcimycin</String>
                        <DateCreated>
                            <Year>1999</Year>
                            <Month>01</Month>
                            <Day>01</Day>
                        </DateCreated>
                        <SortVersion>AMPHETAMINE A D</SortVersion>
                        <EntryVersion>ABDOMINAL INJ</EntryVersion>
                        <Abbreviation>BS</Abbreviation>
                        <ThesaurusIDlist>
                            <ThesaurusID>FDA SRS (2014)</ThesaurusID>
                            <ThesaurusID>NLM (1975)</ThesaurusID>
                        </ThesaurusIDlist>
                    </Term>
                    <Term ConceptPreferredTermYN="N" IsPermutedTermYN="Y"
                          LexicalTag="LAB" RecordPreferredTermYN="N">
                        <TermUI>T000001</TermUI>
                        <String>A 23187</String>
                    </Term>
                </TermList>
            </Concept>
            <Concept PreferredConceptYN="N">
                <ConceptUI>M0353609</ConceptUI>
                <ConceptName>
                    <String>A-23187</String>
                </ConceptName>
                <RegistryNumber>0</RegistryNumber>
                <ConceptRelationList>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M0000001</Concept1UI>
                        <Concept2UI>M0353609</Concept2UI>
                    </ConceptRelation>
                </ConceptRelationList>
                <TermList>
                    <Term ConceptPreferredTermYN="Y" IsPermutedTermYN="N"
                          LexicalTag="LAB" RecordPreferredTermYN="N">
                        <TermUI>T000001</TermUI>
                        <String>A-23187</String>
                        <DateCreated>
                            <Year>1990</Year>
                            <Month>03</Month>
                            <Day>08</Day>
                        </DateCreated>
                        <ThesaurusIDlist>
                            <ThesaurusID>NLM (1991)</ThesaurusID>
                        </ThesaurusIDlist>
                    </Term>
                </TermList>
            </Concept>
        </ConceptList>
    </DescriptorRecord>
</DescriptorRecordSet>
"""

sample_qual = """<?xml version="1.0"?>
<!DOCTYPE QualifierRecordSet SYSTEM "https://www.nlm.nih.gov/databases/dtd/nlmqualifierrecordset_20190101.dtd">
<QualifierRecordSet LanguageCode="eng">
    <QualifierRecord>
        <QualifierUI>Q000000981</QualifierUI>
        <QualifierName>
            <String>diagnostic imaging</String>
        </QualifierName>
        <DateCreated>
            <Year>2016</Year>
            <Month>06</Month>
            <Day>29</Day>
        </DateCreated>
        <DateRevised>
            <Year>2016</Year>
            <Month>06</Month>
            <Day>08</Day>
        </DateRevised>
        <DateEstablished>
            <Year>2017</Year>
            <Month>01</Month>
            <Day>01</Day>
        </DateEstablished>
        <Annotation>subheading only; coordinate with specific imaging technique if pertinent
        </Annotation>
        <HistoryNote>2017(1967)
        </HistoryNote>
        <OnlineNote>search policy: Online Manual; use: main heading/AB or AB (SH) or SUBS APPLY AB
        </OnlineNote>
        <TreeNumberList>
            <TreeNumber>Y04.010</TreeNumber>
            <TreeNumber>Y04.011</TreeNumber>
        </TreeNumberList>
        <ConceptList>
            <Concept PreferredConceptYN="Y">
                <ConceptUI>M000614856</ConceptUI>
                <ConceptName>
                    <String>diagnostic imaging</String>
                </ConceptName>
                <ScopeNote>Used for the visualization of an anatomical structure or for the diagnosis of disease. Commonly used imaging techniques include radiography, radionuclide imaging, thermography, tomography, and ultrasonography
                </ScopeNote>
                <ConceptRelationList>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M000614856</Concept1UI>
                        <Concept2UI>M0030904</Concept2UI>
                    </ConceptRelation>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M000614856</Concept1UI>
                        <Concept2UI>M0030903</Concept2UI>
                    </ConceptRelation>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M000614856</Concept1UI>
                        <Concept2UI>M0030734</Concept2UI>
                    </ConceptRelation>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M000614856</Concept1UI>
                        <Concept2UI>M0030733</Concept2UI>
                    </ConceptRelation>
                </ConceptRelationList>
                <TermList>
                    <Term ConceptPreferredTermYN="Y" IsPermutedTermYN="N"
                          LexicalTag="NON" RecordPreferredTermYN="Y">
                        <TermUI>T000895609</TermUI>
                        <String>diagnostic imaging</String>
                        <DateCreated>
                            <Year>2016</Year>
                            <Month>02</Month>
                            <Day>19</Day>
                        </DateCreated>
                        <Abbreviation>DG</Abbreviation>
                        <EntryVersion>DIAG IMAGE</EntryVersion>
                    </Term>
                </TermList>
            </Concept>
            <Concept PreferredConceptYN="N">
                <ConceptUI>M0030904</ConceptUI>
                <ConceptName>
                    <String>ultrasound</String>
                </ConceptName>
                <ConceptRelationList>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M000614856</Concept1UI>
                        <Concept2UI>M0030904</Concept2UI>
                    </ConceptRelation>
                </ConceptRelationList>
                <TermList>
                    <Term ConceptPreferredTermYN="Y" IsPermutedTermYN="N"
                          LexicalTag="NON" RecordPreferredTermYN="N">
                        <TermUI>T061379</TermUI>
                        <String>ultrasound</String>
                    </Term>
                </TermList>
            </Concept>
        </ConceptList>
    </QualifierRecord>
</QualifierRecordSet>"""

sample_supp = """<?xml version="1.0"?>
<!DOCTYPE SupplementalRecordSet SYSTEM "https://www.nlm.nih.gov/databases/dtd/nlmsupplementalrecordset_20190101.dtd">
<SupplementalRecordSet LanguageCode="eng">
    <SupplementalRecord SCRClass="1">
        <SupplementalRecordUI>C000002</SupplementalRecordUI>
        <SupplementalRecordName>
            <String>bevonium</String>
        </SupplementalRecordName>
        <DateCreated>
            <Year>1971</Year>
            <Month>01</Month>
            <Day>01</Day>
        </DateCreated>
        <DateRevised>
            <Year>2018</Year>
            <Month>09</Month>
            <Day>24</Day>
        </DateRevised>
        <Note>structure given in first source
        </Note>
        <Frequency>1</Frequency>
        <PreviousIndexingList>
            <PreviousIndexing>PIPERIDINES (71-81)</PreviousIndexing>
        </PreviousIndexingList>
        <HeadingMappedToList>
            <HeadingMappedTo>
                <DescriptorReferredTo>
                    <DescriptorUI>*D001561</DescriptorUI>
                    <DescriptorName>
                        <String>Benzilates</String>
                    </DescriptorName>
                </DescriptorReferredTo>
            </HeadingMappedTo>
           <HeadingMappedTo>
                <DescriptorReferredTo>
                    <DescriptorUI>D000117</DescriptorUI>
                    <DescriptorName>
                        <String>Acetylglucosamine</String>
                    </DescriptorName>
                </DescriptorReferredTo>
                <QualifierReferredTo>
                    <QualifierUI>*Q000031</QualifierUI>
                    <QualifierName>
                        <String>analogs &amp; derivatives</String>
                    </QualifierName>
                </QualifierReferredTo>
            </HeadingMappedTo>
        </HeadingMappedToList>
          <IndexingInformationList>
            <IndexingInformation>
                <DescriptorReferredTo>
                    <DescriptorUI>D007918</DescriptorUI>
                    <DescriptorName>
                        <String>Leprosy</String>
                    </DescriptorName>
                </DescriptorReferredTo>
                <QualifierReferredTo>
                    <QualifierUI>Q000188</QualifierUI>
                    <QualifierName>
                        <String>drug therapy</String>
                    </QualifierName>
                </QualifierReferredTo>
            </IndexingInformation>
            <IndexingInformation>
                <DescriptorReferredTo>
                    <DescriptorUI>D013287</DescriptorUI>
                    <DescriptorName>
                        <String>Street Drugs</String>
                    </DescriptorName>
                </DescriptorReferredTo>
            </IndexingInformation>
        </IndexingInformationList>
        <PharmacologicalActionList>
            <PharmacologicalAction>
                <DescriptorReferredTo>
                    <DescriptorUI>D000894</DescriptorUI>
                    <DescriptorName>
                        <String>Anti-Inflammatory Agents, Non-Steroidal</String>
                    </DescriptorName>
                </DescriptorReferredTo>
            </PharmacologicalAction>
        </PharmacologicalActionList>
        <SourceList>
            <Source>S Afr Med J 50(1):4;1976</Source>
            <Source>Q J Med 1979;48(191):493</Source>
        </SourceList>
        <ConceptList>
            <Concept PreferredConceptYN="Y">
                <ConceptUI>M0040005</ConceptUI>
                <ConceptName>
                    <String>bevonium</String>
                </ConceptName>
                <RegistryNumber>34B0471E08</RegistryNumber>
                <RelatedRegistryNumberList>
                    <RelatedRegistryNumber>33371-53-8 (bevonium)
                    </RelatedRegistryNumber>
                    <RelatedRegistryNumber>35517-05-6</RelatedRegistryNumber>
                    <RelatedRegistryNumber>5205-82-3 (bevoinum methylsulfate)
                    </RelatedRegistryNumber>
                    <RelatedRegistryNumber>UWC15E373Z</RelatedRegistryNumber>
                </RelatedRegistryNumberList>
                <ConceptRelationList>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M0040005</Concept1UI>
                        <Concept2UI>M0307342</Concept2UI>
                    </ConceptRelation>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M0040005</Concept1UI>
                        <Concept2UI>M0402330</Concept2UI>
                    </ConceptRelation>
                </ConceptRelationList>
                <TermList>
                    <Term ConceptPreferredTermYN="Y" IsPermutedTermYN="N"
                          LexicalTag="NON" RecordPreferredTermYN="Y">
                        <TermUI>T070005</TermUI>
                        <String>bevonium</String>
                        <ThesaurusIDlist>
                            <ThesaurusID>FDA SRS (2013)</ThesaurusID>
                            <ThesaurusID>NLM (1971)</ThesaurusID>
                        </ThesaurusIDlist>
                    </Term>
                    <Term ConceptPreferredTermYN="N" IsPermutedTermYN="N"
                          LexicalTag="NON" RecordPreferredTermYN="N">
                        <TermUI>T000946882</TermUI>
                        <String>2-(hydroxymethyl)-N,N-dimethylpiperidinium
                            benzilate
                        </String>
                        <DateCreated>
                            <Year>2018</Year>
                            <Month>09</Month>
                            <Day>18</Day>
                        </DateCreated>
                        <ThesaurusIDlist>
                            <ThesaurusID>NLM (2017)</ThesaurusID>
                        </ThesaurusIDlist>
                    </Term>
                </TermList>
            </Concept>
            <Concept PreferredConceptYN="N">
                <ConceptUI>M0307342</ConceptUI>
                <ConceptName>
                    <String>bevonium sulfate (1:1)</String>
                </ConceptName>
                <RegistryNumber>35517-05-6</RegistryNumber>
                <ConceptRelationList>
                    <ConceptRelation RelationName="NRW">
                        <Concept1UI>M0040005</Concept1UI>
                        <Concept2UI>M0307342</Concept2UI>
                    </ConceptRelation>
                </ConceptRelationList>
                <TermList>
                    <Term ConceptPreferredTermYN="Y" IsPermutedTermYN="N"
                          LexicalTag="NON" RecordPreferredTermYN="N">
                        <TermUI>T337342</TermUI>
                        <String>bevonium sulfate (1:1)</String>
                        <DateCreated>
                            <Year>1999</Year>
                            <Month>08</Month>
                            <Day>18</Day>
                        </DateCreated>
                        <ThesaurusIDlist>
                            <ThesaurusID>NLM (1971)</ThesaurusID>
                        </ThesaurusIDlist>
                    </Term>
                </TermList>
            </Concept>
        </ConceptList>
    </SupplementalRecord>
</SupplementalRecordSet>"""


class EnumMeshFileSample(enum.Enum):
    DESC = sample_desc
    QUAL = sample_qual
    SUPP = sample_supp


def get_sample_file(mesh_file_type: EnumMeshFileSample):

    fid = tempfile.NamedTemporaryFile(delete=False, mode="w")
    fid.write(mesh_file_type.value)
    fid.seek(0)
    fid.close()

    return fid
