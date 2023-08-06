"""
<Module Name>
  common.py

<Author>
  Santiago Torres-Arias <santiago@nyu.edu>

<Started>
  Nov 15, 2017

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Provides algorithm-agnostic gpg public key and signature parsing functions.
  The functions select the appropriate functions for each algorithm and
  call them.

"""
import binascii
import logging
import struct

import securesystemslib.gpg.util
from securesystemslib.gpg.constants import (FULL_KEYID_SUBPACKET, PACKET_TYPES,
                                            PARTIAL_KEYID_SUBPACKET,
                                            SIGNATURE_HANDLERS,
                                            SIGNATURE_TYPE_BINARY,
                                            SUPPORTED_HASH_ALGORITHMS,
                                            SUPPORTED_PUBKEY_PACKET_VERSIONS,
                                            SUPPORTED_SIGNATURE_ALGORITHMS,
                                            SUPPORTED_SIGNATURE_PACKET_VERSIONS)
from securesystemslib.gpg.exceptions import (KeyNotFoundError,
                                             PacketVersionNotSupportedError,
                                             SignatureAlgorithmNotSupportedError)
from securesystemslib.gpg.formats import GPG_HASH_ALGORITHM_STRING

log = logging.getLogger('securesystemslib_gpg_common')


def parse_pubkey_payload(data):
  """
  <Purpose>
    Parse the passed public-key packet (payload only) and construct a
    public key dictionary.

  <Arguments>
    data:
          An RFC4880 public key packet payload as described in section 5.5.2.
          (version 4) of the RFC.

          NOTE: The payload can be parsed from a full key packet (header +
          payload) by using securesystemslib.gpg.util.parse_packet_header.

          WARNING: this doesn't support armored pubkey packets, so use with
          care. pubkey packets are a little bit more complicated than the
          signature ones

  <Exceptions>
    ValueError
          If the passed public key data is empty.

    securesystemslib.gpg.exceptions.PacketVersionNotSupportedError
          If the packet version does not match
          securesystemslib.gpg.constants.SUPPORTED_PUBKEY_PACKET_VERSIONS

    securesystemslib.gpg.exceptions.SignatureAlgorithmNotSupportedError
          If the signature algorithm does not match one of
          securesystemslib.gpg.constants.SUPPORTED_SIGNATURE_ALGORITHMS

  <Side Effects>
    None.

  <Returns>
    A public key in the format securesystemslib.gpg.formats.PUBKEY_SCHEMA

  """
  if not data:
    raise ValueError("Could not parse empty pubkey payload.")

  ptr = 0
  keyinfo = {}
  version_number = data[ptr]
  ptr += 1
  if version_number not in SUPPORTED_PUBKEY_PACKET_VERSIONS: # pragma: no cover
    raise PacketVersionNotSupportedError(
        "This pubkey packet version is not supported!")

  # NOTE: Uncomment this line to decode the time of creation
  # time_of_creation = struct.unpack(">I", data[ptr:ptr + 4])
  ptr += 4

  algorithm = data[ptr]

  ptr += 1

  # TODO: Should we only export keys with signing capabilities?
  # Section 5.5.2 of RFC4880 describes a public-key algorithm octet with one
  # of the values described in section 9.1 that could be used to determine the
  # capabilities. However, in case of RSA subkeys this field doesn't seem to
  # correctly encode the capabilities. It always has the value 1, i.e.
  # RSA (Encrypt or Sign).
  # For RSA public keys we would have to parse the subkey's signature created
  # with the master key, for the signature's key flags subpacket, identified
  # by the value 27 (see section 5.2.3.1.) containing a list of binary flags
  # as described in section 5.2.3.21.
  if algorithm not in SUPPORTED_SIGNATURE_ALGORITHMS:
    raise SignatureAlgorithmNotSupportedError(
        "This signature algorithm is not supported. Please"
        " verify that this gpg key is used for creating either DSA or RSA"
        " signatures.")
  else:
    keyinfo['type'] = SUPPORTED_SIGNATURE_ALGORITHMS[algorithm]['type']
    keyinfo['method'] = SUPPORTED_SIGNATURE_ALGORITHMS[algorithm]['method']
    handler = SIGNATURE_HANDLERS[keyinfo['type']]

  keyinfo['keyid'] = securesystemslib.gpg.util.compute_keyid(data)
  key_params = handler.get_pubkey_params(data[ptr:])

  return {
    "method": keyinfo['method'],
    "type": keyinfo['type'],
    "hashes": [GPG_HASH_ALGORITHM_STRING],
    "keyid": keyinfo['keyid'],
    "keyval" : {
      "private": "",
      "public": key_params
      }
    }


def parse_pubkey_bundle(data, keyid):
  """
  <Purpose>
    Parse the public key data received by GPG_EXPORT_PUBKEY_COMMAND and
    construct a public key dictionary, containing a master key and optional
    subkeys, where either the master key or the subkeys are identified by
    the passed keyid.

    NOTE: If the keyid matches one of the subkeys, a warning is issued to
    notify the user about potential privilege escalation.

  <Arguments>
    data:
          Public key data as written to stdout by GPG_EXPORT_PUBKEY_COMMAND.

  <Exceptions>
    ValueError:
          If no data is passed

    securesystemslib.gpg.exceptions.KeyNotFoundError
          If neither the master key or one of the subkeys match the passed
          keyid.

  <Side Effects>
    None.

  <Returns>
    A public key in the format securesystemslib.gpg.formats.PUBKEY_SCHEMA
    containing available subkeys, where either the master key or one of the
    subkeys match the passed keyid.

  """
  master_public_key = None
  sub_public_keys = {}

  # Iterate over the passed public key data and parse out master and sub keys.
  # The individual keys' headers identify the key as master or sub key.
  packet_start = 0
  while packet_start < len(data):
    payload, length, _type = securesystemslib.gpg.util.parse_packet_header(
        data[packet_start:])

    try:
      if _type == PACKET_TYPES["master_pubkey_packet"]:
        master_public_key = \
            securesystemslib.gpg.common.parse_pubkey_payload(payload)

      elif _type == PACKET_TYPES["pub_subkey_packet"]:
        sub_public_key = \
            securesystemslib.gpg.common.parse_pubkey_payload(payload)
        sub_public_keys[sub_public_key["keyid"]] = sub_public_key

    # The data might contain non-supported subkeys, which we just ignore
    except (ValueError, PacketVersionNotSupportedError,
        SignatureAlgorithmNotSupportedError):
      pass

    packet_start += length

  # Since GPG returns all pubkeys associated with a keyid (master key and
  # subkeys) we check which key matches the passed keyid.
  # If the matching key is a subkey, we warn the user because we return
  # the whole bundle (master plus all subkeys) and not only the subkey.
  # If no matching key is found we raise a KeyNotFoundError.
  for idx, public_key in enumerate(
      [master_public_key] + list(sub_public_keys.values())):
    if public_key and public_key["keyid"].endswith(keyid.lower()):
      if idx > 1: # pragma: no cover
        log.warning("Exporting master key '{}' including subkeys '{}'. For"
            " passed keyid '{}'.".format(master_public_key["keyid"],
            ", ".join(list(sub_public_keys.keys())), keyid))
      break

  else:
    raise KeyNotFoundError("No key found for gpg keyid '{}'".format(keyid))

  # Add subkeys dictionary to master pubkey "subkeys" field if subkeys exist
  if sub_public_keys:
    master_public_key["subkeys"] = sub_public_keys

  return master_public_key


def parse_signature_packet(data):
  """
  <Purpose>
    Parse the signature information on an RFC4880-encoded binary signature data
    buffer.

    NOTE: Older gpg versions (< FULLY_SUPPORTED_MIN_VERSION) might only
    reveal the partial key id. It is the callers responsibility to determine
    the full keyid based on the partial keyid, e.g. by exporting the related
    public and replacing the paritla keyid with the full keyid.

  <Arguments>
    data:
           the RFC4880-encoded binary signature data buffer as described in
           section 5.2 (and 5.2.3.1).

  <Exceptions>
    ValueError: if the signature packet is not supported or the data is
      malformed

  <Side Effects>
    None.

  <Returns>
    A signature dictionary matching
    securesystemslib.gpg.formats.SIGNATURE_SCHEMA

  """
  data, junk_length, junk_type = securesystemslib.gpg.util.parse_packet_header(
      data, PACKET_TYPES['signature_packet'])

  ptr = 0

  # we get the version number, which we also expect to be v4, or we bail
  # FIXME: support v3 type signatures (which I haven't seen in the wild)
  version_number = data[ptr]
  ptr += 1
  if version_number not in SUPPORTED_SIGNATURE_PACKET_VERSIONS: # pragma: no cover
    raise ValueError("Only version 4 gpg signatures are supported.")

  # here, we want to make sure the signature type is indeed PKCSV1.5 with RSA
  signature_type = data[ptr]
  ptr += 1

  # INFO: as per RFC4880 (section 5.2.1) there are multiple types of signatures
  # with different purposes (e.g., there is one for pubkey signatures, key
  # revocation, etc.). Binary document signatures are the ones done over
  # "arbitrary text," and it's the one it's defaulted to when doing a signature
  # (i.e., gpg --sign [...])
  if signature_type != SIGNATURE_TYPE_BINARY: # pragma: no cover
    raise ValueError("We can only use binary signature types (i.e., "
        "gpg --sign [...] or signatures created by securesystemslib).")

  signature_algorithm = data[ptr]
  ptr += 1

  if signature_algorithm not in SUPPORTED_SIGNATURE_ALGORITHMS: # pragma: no cover
    raise ValueError("This signature algorithm is not supported. please"
        " verify that your gpg configuration is creating either DSA or RSA"
        " signatures")

  key_type = SUPPORTED_SIGNATURE_ALGORITHMS[signature_algorithm]['type']
  handler = SIGNATURE_HANDLERS[key_type]

  hash_algorithm = data[ptr]
  ptr += 1

  if hash_algorithm not in SUPPORTED_HASH_ALGORITHMS: # pragma: no cover
    raise ValueError("This library only supports SHA256 as "
        "the hash algorithm!")

  # Obtain the hashed octets
  hashed_octet_count = struct.unpack(">H", data[ptr:ptr+2])[0]
  ptr += 2
  hashed_subpackets = data[ptr:ptr+hashed_octet_count]
  hashed_subpacket_info = \
      securesystemslib.gpg.util.parse_subpackets(hashed_subpackets)

  # Check whether we were actually able to read this much hashed octets
  if len(hashed_subpackets) != hashed_octet_count: # pragma: no cover
    raise ValueError("This signature packet seems to be corrupted."
        "It is missing hashed octets!")

  ptr += hashed_octet_count
  other_headers_ptr = ptr

  unhashed_octet_count = struct.unpack(">H", data[ptr: ptr + 2])[0]
  ptr += 2

  unhashed_subpackets = data[ptr:ptr+unhashed_octet_count]
  unhashed_subpacket_info = securesystemslib.gpg.util.parse_subpackets(
      unhashed_subpackets)

  ptr += unhashed_octet_count

  keyid = ""
  short_keyid = ""

  # Parse Issuer (short keyid) and Issuer Fingerprint (full keyid) from hashed
  # and unhashed signature subpackets. Full keyids are only available in newer
  # signatures. (see RFC4880 and rfc4880bis-06 5.2.3.1.)
  # NOTE: A subpacket may be found either in the hashed or unhashed subpacket
  # sections of a signature. If a subpacket is not hashed, then the information
  # in it cannot be considered definitive because it is not part of the
  # signature proper.
  # (see RFC4880 5.2.3.2.)
  # NOTE: Signatures may contain conflicting information in subpackets. In most
  # cases, an implementation SHOULD use the last subpacket, but MAY use any
  # conflict resolution scheme that makes more sense.
  # (see RFC4880 5.2.4.1.)
  # Below we only consider the last and favor hashed over unhashed subpackets
  for subpacket_type, subpacket_data in \
      unhashed_subpacket_info + hashed_subpacket_info:
    if subpacket_type == FULL_KEYID_SUBPACKET:
      # NOTE: The first byte of the subpacket payload is a version number
      # (see rfc4880bis-06 5.2.3.28.)
      keyid = binascii.hexlify(subpacket_data[1:]).decode("ascii")

    # We also return the short keyid, because the full might not be available
    if subpacket_type == PARTIAL_KEYID_SUBPACKET:
      short_keyid = binascii.hexlify(subpacket_data).decode("ascii")


  # Fail if there is no keyid at all (this should not happen)
  if not (keyid or short_keyid): # pragma: no cover
    raise ValueError("This signature packet seems to be corrupted. It does "
        "not have an 'Issuer' or 'Issuer Fingerprint' subpacket (see RFC4880 "
        "and rfc4880bis-06 5.2.3.1. Signature Subpacket Specification).")

  # Fail keyid and short keyid are specified but don't match
  if keyid and not keyid.endswith(short_keyid): # pragma: no cover
    raise ValueError("This signature packet seems to be corrupted. The key ID "
        "'{}' of the 'Issuer' subpacket must match the lower 64 bits of the "
        "fingerprint '{}' of the 'Issuer Fingerprint' subpacket (see RFC4880 "
        "and rfc4880bis-06 5.2.3.28. Issuer Fingerprint).".format(
        short_keyid, keyid))

  # Uncomment this variable to obtain the left-hash-bits information (used for
  # early rejection)
  #left_hash_bits = struct.unpack(">H", data[ptr:ptr+2])[0]
  ptr += 2

  signature = handler.get_signature_params(data[ptr:])

  return {
    'keyid': "{}".format(keyid),
    'short_keyid': "{}".format(short_keyid),
    'other_headers': binascii.hexlify(data[:other_headers_ptr]).decode('ascii'),
    'sig': binascii.hexlify(signature).decode('ascii')
  }
