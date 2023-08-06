# -*- coding: utf-8 -*-
"""
Module providing an entry point to make and read claim attestations via a CLI.
"""

# Created: 2018-11-07 Guy K. Kloss <guy@mysinglesource.io>
#
# (c) 2018-2019 by SingleSource Limited, Auckland, New Zealand
#     http://mysinglesource.io/
#     Apache 2.0 Licence.
#
# This work is licensed under the Apache 2.0 open source licence.
# Terms and conditions apply.
#
# You should have received a copy of the licence along with this
# program.

__author__ = 'Guy K. Kloss <guy@mysinglesource.io>'

import argparse
import io
import json
import logging
import time

from sspyjose.jwk import Jwk

from pykauriid import attestations


logger = logging.getLogger(__name__)


def attest_claim_set(claimsetkeys_file: str,
                     attester_data_fd: io.TextIOBase,
                     attestation_data_fd: io.TextIOBase,
                     attestation_file: str,
                     sig_key_fd: io.TextIOBase):
    """
    Attest a (self or foreign) claim set.

    :param claimsetkeys_file: File to write the claim set keys to.
    :param attester_data_fd: File containing information on the attester.
    :param attestation_data_fd: File containing data on the specific
        attestation to make.
    :param attestation_file: File to write the new attestation to.
    :param sig_key_fd: Key to use for signing (private).
    """
    attester_sig_key = Jwk.get_instance(crv='Ed25519',
                                        from_json=sig_key_fd.read())
    with open(claimsetkeys_file, 'rt') as fd:
        my_attestation = attestations.Attestation(claim_set_keys=fd.read())
    attester_data = json.load(attester_data_fd)
    attestation_data = json.load(attestation_data_fd)
    # Add attester data.
    for key, namespace in attester_data['provenance_namespaces'].items():
        my_attestation.provenance_namespaces[key] = namespace
    my_attestation.iss = attester_data['attester']
    my_attestation.delegation_chain = attester_data['delegation_chain']
    # Add attestation data.
    for key, namespace in attestation_data['provenance_namespaces'].items():
        my_attestation.provenance_namespaces[key] = namespace
    my_attestation.add_attestation_prov(
        attestation_data['evidence_elements'],
        attestation_data['evidence_verification'])
    for ancestor in attestation_data['ancestors']:
        my_attestation.add_ancestor(
            ancestor['uri'], ancestor['object_key'], ancestor['trace_key'])
    for statement in attestation_data['statements']:
        if 'ttl' in statement:
            statement['exp'] = int(time.time() + statement['ttl'])
            del statement['ttl']
        my_attestation.statements.append(statement)
    # Attest the claim set.
    with open(attestation_file, 'wt') as fd:
        fd.write(my_attestation.finalise(attester_sig_key))
    # Update claim set keys (now contains a trace key).
    with open(claimsetkeys_file, 'wt') as fd:
        fd.write(my_attestation.claim_set_keys.serialise(
            claim_type_hints=True))


def accept_attestation(claimsetkeys_file: str,
                       attestation_file: str,
                       sig_key_fd: io.TextIOBase):
    """
    Accept an attestation by co-signing it.

    :param claimsetkeys_file: File to read the claim set keys from.
    :param attestation_file: File of the attestation to read and update.
    :param sig_key_fd: Key to use for co-signing (private).
    """
    subject_sig_key = Jwk.get_instance(crv='Ed25519',
                                       from_json=sig_key_fd.read())
    with open(claimsetkeys_file, 'rt') as fd:
        my_attestation = attestations.Attestation(claim_set_keys=fd.read())
    with open(attestation_file, 'rt') as fd:
        my_attestation.load(fd.read())
    my_attestation.cosign(subject_sig_key)
    with open(attestation_file, 'wt') as fd:
        fd.write(my_attestation.serialise())


def access_attested_claims(claimsetkeys_file: str,
                           attestation_file: str,
                           index: int,
                           to_list: bool):
    """
    Access a claim set in a file using the given claim set keys.

    :param claimsetkeys_file: File to read the claim set keys from.
    :param attestation_file: File of the attestation to read and update.
    :param index: Index of the attribute to access (-1 for all).
    :param to_list: List the attribute types of the attestation.
    """
    with open(claimsetkeys_file, 'rt') as fd:
        my_attestation = attestations.Attestation(claim_set_keys=fd.read())
    with open(attestation_file, 'rt') as fd:
        my_attestation.load(fd.read())
    claims_keys = my_attestation.claim_set_keys
    claim_set = claims_keys.claim_set
    if to_list:
        print('Claim set contains claims with the following types:')
        for item in claims_keys.claim_type_hints:
            print('- {}'.format(item))
    elif index == -1:
        print('All claims:')
        for i in range(len(claim_set.claims)):
            claim_key = claims_keys.claim_keys[i]
            print('- {}'.format(json.dumps(
                claim_set.access_claim(i, claim_key), indent=2)))
    else:
        claim_key = claims_keys.claim_keys[index]
        print('Claim index {}:'.format(index))
        print(json.dumps(claim_set.access_claim(index, claim_key), indent=2))


def _indent_content(content: str, indent_by: int) -> str:
    """
    Indent the given content by the desired number of spaces.
    """
    lines = content.split('\n')
    indentation = ' ' * indent_by
    return '\n'.join('{}{}'.format(indentation, line)
                     for line in lines)


def dump_attestation_content(claimsetkeys_file: str,
                             attestation_file: str):
    """
    Access a claim set in a file using the given claim set keys.

    :param claimsetkeys_file: File to read the claim set keys from.
    :param attestation_file: File of the attestation to read and update.
    :param index: Index of the attribute to access (-1 for all).
    :param to_list: List the attribute types of the attestation.
    :param dump: Dump the content of an attestation in plain text
    """
    with open(claimsetkeys_file, 'rt') as fd:
        my_attestation = attestations.Attestation(claim_set_keys=fd.read())
    with open(attestation_file, 'rt') as fd:
        my_attestation.load(fd.read())
    claims_keys = my_attestation.claim_set_keys
    claim_set = claims_keys.claim_set
    print('Claim set:')
    print('  - sub: {}'.format(claim_set.sub))
    if claim_set.commitment is None:
        print('  - foreign claim set')
    else:
        print('  - self claim set')
    print('  - number of claims: {}'.format(len(claim_set.claims)))
    iat = claim_set.iat
    print('  - time stamp: {} ({})'
          .format(iat, attestations.make_utc_datetime(iat).isoformat()))
    exp = claim_set.exp
    print('  - expires at: {} ({})'
          .format(exp, attestations.make_utc_datetime(exp).isoformat()))
    print('Claims:')
    for i in range(len(claim_set.claims)):
        claim_key = claims_keys.claim_keys[i]
        claim_data = json.dumps(claim_set.access_claim(i, claim_key), indent=2)
        print('  - claim {}:\n{}'
              .format(i, _indent_content(claim_data, 6)))
    print('Attestation data:')
    print('  - attester: {}'.format(my_attestation.iss))
    iat = my_attestation.iat
    print('  - time stamp: {} ({})'
          .format(iat, attestations.make_utc_datetime(iat).isoformat()))
    print('  - PROV-N trail:\n{}'
          .format(_indent_content(my_attestation.provenance, 6)))
    print('  - attestation statements:')
    for item in my_attestation.statements:
        exp = item['exp']
        metadata = item['metadata']
        print('    - expires at: {} ({})'
              .format(exp, attestations.make_utc_datetime(exp).isoformat()))
        print('      metadata:\n{}'
              .format(_indent_content(json.dumps(metadata, indent=2), 8)))
    print('  - ancestors:')
    for ref, keys in my_attestation.ancestors.items():
        print('    - reference: {}'.format(ref))
        print('      - object key:\n{}'
              .format(_indent_content(
                  json.dumps(keys['object_key'], indent=2), 8)))
        print('      - trace key:\n{}'
              .format(_indent_content(json.dumps(
                  keys['trace_key'], indent=2), 8)))
    print('Commitments:')
    for _, commitment in my_attestation.commitment_payloads.items():
        print('  - subject: {}'.format(commitment['sub']))
        print('  - committer role: {}'.format(commitment['role']))
        print('  - committer ID: {}'.format(commitment['iss']))
        print('  - elements:')
        parts = commitment['commitment'].split('.')
        for i in range(int(len(parts) / 2)):
            print('    - salt {}: {}'.format(i, parts[2 * i]))
            print('    - salted hash {}: {}'.format(i, parts[2 * i + 1]))


def main(args: argparse.Namespace):
    """
    Delegate to the right functions from given (command line) arguments.

    :param args: Command line arguments provided:

        - args.operation - type: str
        - args.attestation - type: str
        - args.attester_data - type: io.TextIOBase
        - args.attestation_data - type: io.TextIOBase
        - args.sig_key - type: io.TextIOBase
        - args.claimsetkeys - type: str
        - args.index - type: int
        - args.list - type: bool
        - args.dump - type: bool
    """
    if args.operation == 'attest':
        attest_claim_set(args.claimsetkeys, args.attester_data,
                         args.attestation_data, args.attestation, args.sig_key)
    elif args.operation == 'accept':
        accept_attestation(args.claimsetkeys, args.attestation, args.sig_key)
    elif args.operation == 'access':
        if args.dump:
            dump_attestation_content(args.claimsetkeys, args.attestation)
        else:
            access_attested_claims(args.claimsetkeys, args.attestation,
                                   args.index, args.list)
    else:
        raise ValueError('Unsupported operation "{}" for attestations.'
                         .format(args.operation))

    logger.info('Operation "{}" finished.'.format(args.operation))
