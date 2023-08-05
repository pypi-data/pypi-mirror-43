from web3 import Web3

from squid_py.keeper.utils import build_condition_key
from tests.resources.tiers import e2e_test


@e2e_test
def test_generate_condition_id():
    # :TODO:
    contract_address = Web3.toChecksumAddress('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
    template_id = '0x044852b2a670ade5407e78fb2863c51de9fcb96542a07186fe3aeda6bb8a116d'

    fingerprint_lock_payment = '0x668453f0'
    condition_key = '0x1699b99d88626025f8b13de3b666cccec63eaf744d664d901a95b62c36d2b531'
    assert build_condition_key(contract_address=contract_address,
                               fingerprint=Web3.toBytes(hexstr=fingerprint_lock_payment),
                               template_id=template_id) == condition_key
    fingerprint_grant_access = '0x25bfdd8a'
    condition_key = '0x600b855012216922339cafd208590e02fdd8c8b8bbfd761d951976801a2b2b05'
    assert build_condition_key(contract_address=contract_address,
                               fingerprint=Web3.toBytes(hexstr=fingerprint_grant_access),
                               template_id=template_id) == condition_key
