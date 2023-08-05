import base64
import json
import logging
from enum import Enum

import base58
from google.protobuf.timestamp_pb2 import Timestamp

import event_chain.protos as protos
import forge.utils as forge_utils

logger = logging.getLogger('ec-helpers')


def gen_timestamp(datetime):
    res = Timestamp()
    res.FromDatetime(datetime)
    return res


def add_to_proto_list(info, repeated):
    res = {item for item in repeated}
    res.add(info)
    return res


def remove_from_proto_list(info, repeated):
    res = filter(lambda item: item != info, repeated)
    return res


class WalletResponse:
    def __init__(self, response):
        self.response = response
        self.user_info = response.get('userInfo')
        self.decoded_info = self.decode_user_info()
        self.requested_claim = self.decoded_info.get('requestedClaims')[0]

    def decode_user_info(self):
        if not self.user_info:
            logger.error(
                    "Fail to parse user_info from this Response {}.".format(
                            self.response,
                    ),
            )
        else:
            sig = self.user_info.split('.')[1]
            decoded = base64.b64decode(
                    (sig + '=' * (-len(sig) % 4)).encode(),
            ).decode()
            dict = json.loads(decoded)
            logger.debug("User info is decoded successfully. {}".format(dict))
            return dict

    def get_address(self):
        did = self.decoded_info.get('iss')
        logger.debug("Parsed wallet address successfully!: {}".format(did))
        return did.split(':')[-1]

    def get_signature(self):
        sig = self.requested_claim.get('sig')
        logger.debug("Parsed wallet signature successfully! {}".format(sig))
        str_sig = str(sig)
        str_sig = str_sig[1:]
        decoded_sig = base58.b58decode(str_sig)
        logger.debug("sig decoded: {}".format(decoded_sig))
        return decoded_sig

    def get_event_address(self):
        tx = self.requested_claim.get('tx')
        decoded_tx = base64.b64decode(
            (tx + '=' * (-len(tx) % 4)).encode('utf8'))

        parsed_tx = protos.Transaction()
        parsed_tx.ParseFromString(decoded_tx)
        logger.debug("Parsed tx successfully! {}".format(parsed_tx))
        exchange_itx = forge_utils.parse_to_proto(
                parsed_tx.itx.value,
                protos.ExchangeTx,
        )
        event_address = exchange_itx.data.value.decode('utf8')
        return event_address


def add_multi_sig_to_tx(tx, address, signature):
    multisig = protos.Multisig(
            signer=address,
            signature=signature,
    )
    parmas = {
        'from': getattr(tx, 'from'),
        'nonce': tx.nonce,
        'signature': tx.signature,
        'chain_id': tx.chain_id,
        'signatures': [multisig],
        'itx': tx.itx
    }
    new_tx = protos.Transaction(**parmas)
    return new_tx


class ForgeTxType(Enum):
    ACTIVATE_ASSET = 'fg:t:activate_asset'
    CREATE_ASSET = 'fg:t:create_asset'
    EXCHANGE = 'fg:t:exchange'
