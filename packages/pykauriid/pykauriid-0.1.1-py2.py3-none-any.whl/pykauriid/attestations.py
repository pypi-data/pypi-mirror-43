# -*- coding: utf-8 -*-
"""Attestations of claim sets."""

# Created: 2018-09-11 Guy K. Kloss <guy@mysinglesource.io>
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

import datetime
import time
from typing import List, Dict, Union, Tuple
import uuid

import prov.model
from sspyjose.jwe import Jwe
from sspyjose.jwk import Jwk
from sspyjose.jws import Jws

from pykauriid.claims import (ClaimSet,
                              ClaimSetKeys,
                              validate_commitment)
from pykauriid.config import config


PROV_NAMESPACES = {
    # KauriID system (present by default)
    'kauriid': 'http://kauriid.nz/ns/prov#',
    # Dublin Core Terms (present by default)
    'dcterms': 'http://purl.org/dc/terms/'
}


class _SimpleUTC(datetime.tzinfo):
    """
    Class to augment a Python datetime object object for a UTC time offset.
    """

    def tzname(self, **kwargs) -> str:  # @UnusedVariable
        return 'UTC'

    def utcoffset(self, dt: datetime.datetime  # @UnusedVariable
                  ) -> datetime.timedelta:
        return datetime.timedelta(0)


def make_utc_datetime(ts: int = None) -> datetime.datetime:
    """
    Make a datetime object of the current time with UTC time offset.

    :param iat: UN*X epoch time stamp to obtain a datetime object for. If
        `None`, use the current time (default: None).
    :return: UTC datetime object.
    """
    ts = int(time.time()) if ts is None else ts
    result = datetime.datetime.utcfromtimestamp(ts)
    return result.replace(tzinfo=_SimpleUTC())


def _delegation_exists(prov_document: prov.model.ProvDocument,
                       delegate: Union[prov.model.ProvAgent, str],
                       responsible: Union[prov.model.ProvAgent, str]) -> bool:
    """
    Check whether a given delegation exists in the given document or not.

    :param prov_document: Provenance document to check within.
    :param delegate: Delegate to check for (object or identifier).
    :param responsible: Responsible to check for (object or identifier).
    :return: Outcome of check.
    """
    if isinstance(delegate, prov.model.ProvAgent):
        delegate = str(delegate.identifier)
    if isinstance(responsible, prov.model.ProvAgent):
        responsible = str(responsible.identifier)
    delegations = [item.attributes
                   for item in prov_document.records
                   if type(item) is prov.model.ProvDelegation]
    for delegation in delegations:
        party1, party2 = delegation
        if party1[0].localpart == 'delegate':
            recorded_delegate = str(party1[1])
            recorded_responsible = str(party2[1])
        else:
            # Just in case they're in reverse order.
            recorded_delegate = str(party2[1])
            recorded_responsible = str(party1[1])
        if (recorded_delegate == delegate
                and recorded_responsible == responsible):
            return True
    return False


class AttestationStatement:
    """Attestation statement container object with meta-data."""

    metadata = None  # type: dict
    """Meta-data for the attestation statement."""
    exp = None  # type: int
    """Time to live (last time valid as UNIX epoch time stamp in seconds)."""
    ttl = config.default_ttl  # type: int
    """Time span for the time to live (in seconds)."""

    def __init__(self, *,
                 ttl: int = config.default_ttl,
                 metadata: dict = None):
        """
        Constructor.

        :param ttl: Time to live from time of attestation
            (default: `config.default_ttl`).
        :param metadata: Meta-data for this specific attestation statement.
        """
        self.ttl = ttl
        if metadata:
            self.metadata = metadata

    def finalise(self, iat: int) -> dict:
        """
        Finalise the statement. Computes the TTL from the given time stamp.

        :param iat: Time stamp of attestation (as UNIX epoch time stamp in
            seconds).
        :return: Dictionary with attestation statement data.
        """
        self.exp = iat + self.ttl
        return {
            'exp': self.exp,
            'metadata': self.metadata
        }


class Attestation:
    """Attestation management container object."""

    iss = None  # type: str
    """Issuer attesting/signing the attestation."""
    delegation_chain = None  # type: List[str]
    """
    Chain of delegation to the iss. Highest level down to direct
    delegator of iss.
    """
    iat = None  # type: int
    """Time stamp of creation (as UNIX epoch time stamp in seconds)."""
    provenance = None  # type: str
    """Provenance trace for this attestation (in PROV-N format)."""
    provenance_namespaces = None  # type: dict[str, str]
    """
    Namespace short names and URIs that are used/referenced in the provenance
    trail.
    """
    statements = None  # type: List[Union[AttestationStatement, dict]]
    """Statements with meta-data for this attestation."""
    commitments = None  # type: [str]
    """Cryptographic commitments to the claim set."""
    commitment_payloads = None  # type: Dict[str, dict]
    """Unpacked commitments to the claim set."""
    content = None  # type: str
    """Signed attestation content by issuer."""
    content_payload = None  # type: dict
    """Unpacked attestation content."""
    claim_set_keys = None  # type: ClaimSetKeys
    """Object containing all keys for the claim set."""
    _ancestors = None  # type: Dict[str, Tuple[str, Jwk, Jwk]]
    """
    Mapping of the different ancestor references (PROV/IPFS resolvable
    identifiers) to the 'IPFS wrapped' ancestor and symmetric object keys for
    the ancestors of the attestation.
    """
    _prov_document = None  # type: prov.model.ProvDocument
    """The PROV document (as created with the Python PROV module)."""

    def __init__(self, *,
                 claim_set_keys: Union[ClaimSetKeys, str, bytes, dict] = None,
                 from_binary: Union[str, bytes] = None):
        """
        Constructor.

        :param claim_set_keys: Claim set keys object, either as JSON or
            dictionary.
        :param from_binary: An attestation to load/access.
        """
        if claim_set_keys:
            if isinstance(claim_set_keys, ClaimSetKeys):
                self.claim_set_keys = claim_set_keys
            else:
                self.claim_set_keys = ClaimSetKeys(data=claim_set_keys)
        claim_set = (self.claim_set_keys.encrypted_claim_set
                     if self.claim_set_keys else None)
        if claim_set:
            # This is (should be) a claim set in verbatim. Let's parse it!
            self.claim_set_keys.claim_set = ClaimSet(
                from_binary=claim_set,
                object_key=self.claim_set_keys.object_key)
        self.statements = []
        self.commitments = {}
        self.commitment_payloads = {}
        self._ancestors = {}
        self.delegation_chain = []
        self.provenance_namespaces = {}
        self._prov_document = prov.model.ProvDocument()
        # Add Kauri ID and Dublin Core Terms namespaces.
        self._prov_document.add_namespace('kauriid',
                                          PROV_NAMESPACES['kauriid'])
        self._prov_document.add_namespace('dcterms',
                                          PROV_NAMESPACES['dcterms'])
        if from_binary:
            if not claim_set_keys:
                raise ValueError(
                    'Claim set key parameter missing for deserialisation.')
            self.load(from_binary)

    def add_ancestor(self, ancestor_ref: str,
                     object_key: Jwk,
                     trace_key: Jwk,
                     *, wrapped_ref: str = None):
        """
        Add an ancestor reference with their object and trace keys.

        :param ancestor_ref: Fully qualified URI of the ancestor or reference
            using a known name space.
        :param object_key: Object key as JWK JSON for the ancestor.
        :param trace_key: Trace key as JWK JSON for the ancestor.
        :param wrapped_ref: In case the ancestor is a 'wrapper' (IPFS storage
            object), this is the reference of the internal ancestor object.
        """
        self._ancestors[ancestor_ref] = (wrapped_ref, object_key, trace_key)

    @property
    def ancestors(self) -> List[Dict[str, Dict[str, Jwk]]]:
        """
        List all ancestors with their object and trace keys.
        """
        return {ref: {'object_key': ok, 'trace_key': tk}
                for ref, (_, ok, tk) in self._ancestors.items()}

    def add_attestation_prov(self,
                             evidence_elements: Dict[str, str],
                             verification_procedure: str,
                             *,
                             content=()):
        """
        Add the attestation provenance to the attestation meta-data.

        :param evidence_elements: URIs (or shortened via name space keys)
            of all evidence elements used in this attestation mapping to a
            description of the evicende (e.g. 'original document').
        :param verification_procedure: URI (or shortened via name space key)
            of the evidence verification procedure used in the veification
            sub-action of the attestation process.
        :return: Target entity object.
        """
        # Make the time stamp on when this all happens.
        self.iat = int(time.time())
        # Add the required name spaces.
        for ns, uri in self.provenance_namespaces.items():
            self._prov_document.add_namespace(ns, uri)
        # Make target entity.
        target_id = uuid.uuid4()
        target_name = 'kauriid:attestations/{}'.format(target_id)
        other_attributes = {'prov:content': content} if content else {}
        target = self._prov_document.entity(
            target_name, other_attributes=other_attributes)
        # Make activities.
        evidence_verification = self._prov_document.activity(
            'kauriid:evidenceVerification/{}'.format(target_id))
        attestation = self._prov_document.activity(
            'kauriid:identityAttestation/{}'.format(target_id),
            other_attributes={
                'dcterms:hasPart': evidence_verification})
        attestation.wasInformedBy(evidence_verification)
        # Add delegations.
        if len(self.delegation_chain) > 0:
            previous_delegator = self.delegation_chain[0]
            for actor_id in self.delegation_chain[1:] + [self.iss]:
                if not _delegation_exists(self._prov_document,
                                          actor_id, previous_delegator):
                    self._prov_document.actedOnBehalfOf(actor_id,
                                                        previous_delegator)
                previous_delegator = actor_id
        # Add associations.
        attestation.wasAssociatedWith(
            self.iss, attributes={'prov:hadRole': 'kauriid:attester'})
        evidence_verification.wasAssociatedWith(
            self.iss, verification_procedure,
            attributes={'prov:hadRole': 'kauriid:verifier'})
        # Add generation.
        target.wasGeneratedBy(
            attestation, attributes={'prov:generatedAtTime':
                                     make_utc_datetime(self.iat)})
        # Add derivations and usages.
        for ancestor in self._ancestors.keys():
            wrapped_ref = self._ancestors[ancestor][0]
            if wrapped_ref:
                target_ipfs = self._prov_document.entity(
                    ancestor,
                    other_attributes={'prov:type': 'prov:Collection'})
                target_ipfs.hadMember(wrapped_ref)
            attestation.used(ancestor)
            target.wasDerivedFrom(ancestor)
        for evidence_uri, description in evidence_elements.items():
            entity_id = 'kauriid:evidence/{}'.format(uuid.uuid4())
            evidence_entity = self._prov_document.entity(
                entity_id, other_attributes={
                    'dcterms:source': evidence_uri,
                    'dcterms:description': description
                }
            )
            attestation.used(evidence_entity)
            evidence_verification.used(evidence_entity)
            target.wasDerivedFrom(evidence_entity)
        self.provenance = self._prov_document.get_provn()
        return target.identifier

    def _make_salty_hashes(self):
        """
        Make the commitment salts and hashes on the claim set.

        This is required if (some) commitment salts or hashes are missing,
        and no commitment exists, yet.
        """
        self.claim_set_keys.claim_set.commitment_salts = []
        self.claim_set_keys.claim_set.commitment_hashes = []
        for i in range(len(self.claim_set_keys.claim_set.claims)):
            claim_key = self.claim_set_keys.claim_keys[i]
            claim_bytes = self.claim_set_keys.claim_set.access_claim(
                i, claim_key, raw_bytes=True)
            commitment_salt, commitment_hash = (
                self.claim_set_keys.claim_set.make_salty_hash(claim_bytes))
            self.claim_set_keys.claim_set.commitment_salts.append(
                commitment_salt)
            self.claim_set_keys.claim_set.commitment_hashes.append(
                commitment_hash)

    def finalise(self, signing_key: Jwk) -> str:
        """
        Finalise the attestation to return a completed attestation object.

        :param signing_key: Signing key of the iss.
        :return: JWE encrypted attestation object.
        """
        # Make the missing commitment salts and hashes.
        claim_set = self.claim_set_keys.claim_set
        if (len(claim_set.commitment_hashes) < len(claim_set.claims)):
            self._make_salty_hashes()
        # Get attester commitment.
        self.commitments['attester'] = claim_set.get_commitment(
            committer_key=signing_key)
        # Migrate subject commitment (if present).
        if claim_set.commitment:
            self.commitments['subject'] = claim_set.commitment
            self.commitment_payloads['subject'] = (
                validate_commitment(claim_set.commitment).payload)
            claim_set.commitment = None
            self.claim_set_keys.finalise_claim_set(retain_order=True,
                                                   include_commitment=False)
        # Encrypt ancestor keys.
        trace_key = Jwk.get_instance(generate=True)
        self.claim_set_keys.trace_key = trace_key
        ancestor_keys = {}
        for uri, (_, object_jwk, trace_jwk) in self._ancestors.items():
            ancestor_keys[uri] = {}
            encrypter = Jwe.get_instance(jwk=trace_key)
            encrypter.message = (object_jwk if isinstance(object_jwk, dict)
                                 else object_jwk.to_dict())
            encrypter.encrypt()
            ancestor_keys[uri]['object_key'] = encrypter.serialise()
            encrypter.message = (trace_jwk if isinstance(trace_jwk, dict)
                                 else trace_jwk.to_dict())
            encrypter.encrypt()
            ancestor_keys[uri]['trace_key'] = encrypter.serialise()
        # Serialise statements.
        statements = []
        for item in self.statements:
            if isinstance(item, AttestationStatement):
                statements.append(item.finalise(self.iat))
            else:
                statements.append(item)
        # Sign attestation payload.
        self.content_payload = {
            'iss': self.iss,
            'iat': self.iat,
            'provenance': self.provenance,
            'statements': statements,
            'ancestor_keys': ancestor_keys
        }
        signer = Jws.get_instance(jwk=signing_key)
        signer.payload = self.content_payload
        signer.sign()
        self.content = signer.serialise(try_compact=True)

        return self.serialise()

    def load(self, attestation_data: Union[str, bytes]):
        """
        Load attestation data into the object.

        Decrypt and validates the objects's consistency.

        :param attestation_data: Attestation data JWE encrypted to the
            recipient.
        """
        # Decrypt attestation object.
        decrypter = Jwe.get_instance(from_compact=attestation_data,
                                     jwk=self.claim_set_keys.object_key)
        decrypted_attestation_object = decrypter.decrypt()
        # Unpack the content.
        self.commitments = decrypted_attestation_object['commitments']
        self.content = decrypted_attestation_object['content']
        claim_set = ClaimSet(
            from_binary=decrypted_attestation_object['claim_set'],
            object_key=self.claim_set_keys.object_key)
        self.claim_set_keys.claim_set = claim_set
        # Verify commitments.
        _lasts = None
        attester_signing_key = None
        for role, commitment in self.commitments.items():
            commitment_verifier = validate_commitment(commitment)
            payload = commitment_verifier.payload
            claim_set.unpack_commitment_elements(payload)
            if role == 'attester':
                attester_signing_key = commitment_verifier.jwk
            # Do some sanity checks.
            if payload['role'] != role:
                raise RuntimeError('Mismatch of role in commitment!')
            salts = tuple(claim_set.commitment_salts)
            if _lasts:
                if salts != _lasts['salts']:
                    raise RuntimeError(
                        "Mismatch of salts in attestation's commitments!")
                if payload['sub'] != _lasts['sub']:
                    raise RuntimeError(
                        'Mismatching subjects in attestation and commitment.')
                if payload['commitment'] != _lasts['commitment']:
                    raise RuntimeError(
                        'Mismatch of commitment data in commitments.')
            _lasts = {'salts': salts,
                      'sub': payload['sub'],
                      'commitment': payload['commitment']}
            # Now store the commitment.
            self.commitment_payloads[role] = payload

        content_verifier = Jws.get_instance(jwk=attester_signing_key,
                                            from_compact=self.content)
        content_verifier.verify()
        self.content_payload = content_verifier.payload
        self.iss = self.content_payload['iss']
        self.iat = self.content_payload['iat']
        self.provenance = self.content_payload['provenance']
        self.statements = self.content_payload['statements']
        ancestor_keys = self.content_payload['ancestor_keys']
        # Unpick the ancestor keys.
        self._ancestors = {}
        trace_key = self.claim_set_keys.trace_key
        for uri, keys in ancestor_keys.items():
            decrypter = Jwe.get_instance(jwk=trace_key)
            decrypter.load_compact(keys['object_key'])
            object_key = decrypter.decrypt()
            decrypter.load_compact(keys['trace_key'])
            trace_key = decrypter.decrypt()
            self._ancestors[uri] = (None, object_key, trace_key)

    def serialise(self):
        """
        Serialise the attestation object.

        :return: JWE encrypted attestation object.
        """
        # Create encrypted attestation data structure.
        attestation_data = {
            'claim_set': self.claim_set_keys.encrypted_claim_set,
            'commitments': self.commitments,
            'content': self.content
        }
        object_encrypter = Jwe.get_instance(jwk=self.claim_set_keys.object_key)
        object_encrypter.message = attestation_data
        object_encrypter.encrypt()

        return object_encrypter.serialise()

    def cosign(self, signing_key: Jwk):
        """
        Counter sign a commitment by the subject.

        Creates a subject commitment in the meta-data of the claim set object.

        :param subject_signing_key: The subject's (private) signing key.
        """
        self.claim_set_keys.claim_set.signing_key = signing_key
        commitment = self.claim_set_keys.claim_set.get_commitment()
        self.commitments['subject'] = commitment
