# coding=utf-8

import enum
import tempfile


sample_mrconso = """
C0024537|ENG|P|L0024537|VW|S0099348|N|A0133263||M0025572|D016780|MSH|PM|D016780|Vivax Malaria|0|N|256|
C0024537|ENG|S|L0087000|PF|S0074287|Y|A26623559||M0025572|D016780|MSH|ET|D016780|Plasmodium vivax Malaria|0|N|256|
C0006118|ENG|P|L0006118|VO|S0065609|Y|A0090803||M0002885|D001932|MSH|PM|D001932|Neoplasm, Brain|0|N||
C0006118|ENG|S|L0377498|PF|S1676061|Y|A26673428||M0002885|D001932|MSH|ET|D001932|Brain Tumors|0|N|256|
C0001175|ENG|P|L0001175|VO|S0010340|Y|A0019182||M0000245|D000163|MSH|PM|D000163|Acquired Immunodeficiency Syndromes|0|N||
C0001175|ENG|P|L0001175|VO|S0090417|Y|A0122139||M0000245|D000163|MSH|PM|D000163|Syndromes, Acquired Immunodeficiency|0|N|256|
"""

sample_mrsat = """
C0024537|L7660634|S8886552|A17966473|SCUI|N0000003483|AT123617640||MESH_DUI|NDFRT|D016780|N||
C0006118|L7675761|S8867618|A18041757|SCUI|N0000000609|AT123610639||MESH_DUI|NDFRT|D001932|N||
C0001175|L7657036|S8855713|A17943093|SCUI|N0000000291|AT123608971||MESH_DUI|NDFRT|D000163|N||
"""

sample_mrdef = """
C0024537|A0082535|AT38140302||MSH|Malaria caused by PLASMODIUM VIVAX. This form of malaria is less severe than MALARIA, FALCIPARUM, but there is a higher probability for relapses to occur. Febrile paroxysms often occur every other day.|N||
C0024537|A7574502|AT219998083||NCI|Malaria resulting from infection by Plasmodium vivax.|N||
C0006118|A7576341|AT198017024||NCI|A benign or malignant neoplasm that arises from or metastasizes to the brain.|N||
C0006118|A7576341|AT210375650||NCI_NICHD|An abnormal intracranial solid mass or growth.|N||
C0001175|A0021048|AT51221477||CSP|one or more indicator diseases, depending on laboratory evidence of HIV infection (CDC); late phase of HIV infection characterized by marked suppression of immune function resulting in opportunistic infections, neoplasms, and other systemic symptoms (NIAID).|N||
C0001175|A7568512|AT219999003||NCI_NICHD|A chronic, potentially life threatening condition that is caused by human immunodeficiency virus (HIV) infection, and is characterized by increased susceptibility to opportunistic infections, certain cancers and neurologic disorders.|N||
"""


class EnumUmlsFileSample(enum.Enum):
    MRCONSO = sample_mrconso
    MRSAT = sample_mrsat
    MRDEF = sample_mrdef


def get_sample_file(umls_file_type: EnumUmlsFileSample):

    fid = tempfile.NamedTemporaryFile(delete=False, mode="w")
    fid.write(umls_file_type.value)
    fid.seek(0)
    fid.close()

    return fid
