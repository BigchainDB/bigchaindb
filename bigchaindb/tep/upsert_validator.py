import json
import base58

from bigchaindb.tep.transactional_election import TransactionalElection
from bigchaindb.tendermint.lib import BigchainDB
from bigchaindb.models import Transaction
from bigchaindb.tendermint.utils import (GO_AMINO_ED25519,
                                         key_from_base64,)
from bigchaindb.common.crypto import (key_pair_from_ed25519_key,
                                      public_key_from_ed25519_key)


class UpsertValidator(TransactionalElection):

    version = '1.0'
    name = 'upsert-validator'

    def __init__(self, bigchain=None):
        if not bigchain:
            bigchain = BigchainDB()

        self.bigchain = bigchain

    def _new_election_object(self, args):
        new_election_object = {
            'type': 'election',
            'name': self.name,
            'version': self.version,
            'args': args
        }
        return new_election_object

    def _recipients(self):
        """Convert validator dictionary to a recipient list for `Transaction`"""

        recipients = []
        for public_key, voting_power in self._validators().items():
            recipients.append(([public_key], voting_power))

        return recipients

    def _validators(self):
        """Return a dictionary of validators with key as `public_key` and
           value as the `voting_power`
        """

        validators = {}
        for validator in self.bigchain.get_validators():
            if validator['pub_key']['type'] == GO_AMINO_ED25519:
                public_key = public_key_from_ed25519_key(key_from_base64(validator['pub_key']['value']))
                validators[public_key] = validator['voting_power']
            else:
                # TODO: use appropriate exception
                raise NotImplementedError

        return validators

    def _get_vote(self, tx_election, public_key):
        """For a given `public_key` return the `input` and `amount` as
           voting power
        """
        for i, tx_input in enumerate(tx_election.to_inputs()):
            if tx_input.owners_before == [public_key] and \
               tx_election.outputs[i].public_keys == [public_key]:
                return ([tx_input], tx_election.outputs[i].amount)

        return ([], 0)

    def _is_same_topology(self, current_topology, election_topology):

        voters = {}
        for voter in election_topology:
            [public_key] = voter.public_keys
            voting_power = voter.amount
            voters[public_key] = voting_power

        # Check whether the voters and their votes is same to that of the
        # validators and their voting power in the network
        return (current_topology.items() == voters.items())

    @classmethod
    def election_id(cls, tx_election_id):
        return base58.b58encode(bytes.fromhex(tx_election_id))

    def _execute_action(self, tx):
        (code, msg) = self.bigchain.write_transaction(tx, 'broadcast_tx_commit')
        return (True if code == 202 else False)

    def propose(self, validator_data, node_key_path):
        validator_public_key = validator_data['public_key']
        validator_power = validator_data['power']
        validator_node_id = validator_data['node_id']

        node_key = load_node_key(node_key_path)

        args = {
            'public_key': validator_public_key,
            'power': validator_power,
            'node_id': validator_node_id
        }

        tx = Transaction.create([node_key.public_key],
                                self._recipients(),
                                asset=self._new_election_object(args))\
                        .sign([node_key.private_key])
        return self._execute_action(tx)

    def is_valid_proposal(self, tx_election):
        """Check if `tx_election` is a valid election

        NOTE:
        * A valid election is the one which was initiated by an existing validator.

        * A valid election is one in which voters are validators and votes are
          alloacted cannonical to the voting power of each validator node.
        """

        current_validators = self._validators()

        # NOTE: Proposer should be a single node
        if len(tx_election.inputs) != 1:
            return False

        # NOTE: Check if the proposer is a validator
        [election_initiator_node_pub_key] = tx_election.inputs[0].owners_before
        if election_initiator_node_pub_key not in current_validators.keys():
            return False

        # NOTE: Check if all validators have been assigned votes equal to their voting power
        return self._is_same_topology(current_validators, tx_election.outputs)

    def vote(self, tx_election_id, node_key_path):
        """Vote on the given `election_id`"""

        tx_election = self.bigchain.get_transaction(tx_election_id)
        node_key = load_node_key(node_key_path)
        (tx_vote_input,
         voting_power) = self._get_vote(tx_election, node_key.public_key)

        election_id = self.election_id(tx_election_id)

        # NOTE: Node will spend all its allocated votes
        tx_vote = Transaction.transfer(tx_vote_input,
                                       [([election_id], voting_power)],
                                       metadata={'type': 'vote'},
                                       asset_id=tx_election.id)\
                             .sign([node_key.private_key])
        return self._execute_action(tx_vote)

    def is_valid_vote(self, tx_vote):
        """Validate casted vote.

        NOTE:
        * We don't need to check the amount of votes since the same has been
          validated when the election was initiated and a voter can't spend
          more votes than allocated to them in the election proposal.

        * A voter can choose to spend their votes whichever way they like i.e.
          they can tranfer their votes to `election_id` or someone else. The only
          thing that counts is whether the number of votes casted to the `election_id`
          reach a majority of >2/3. It is the responsibility of the voter to
          spend their votes wisely.

        * The byzantine behavour cannot be amplified by sending votes to non-validators
          i.e. if 1/3 of the network is byzantine then their no way to amplify this behavour
          by merely transfering votes to other byzantine nodes.
        """

        return True

    def is_concluded(self, tx_election_id, current_votes=[]):
        """Check if the Election with `election_id` has gained majority vote

        NOTE:
        * An election is concluded only if the >2/3 of network has casted their vote.

        * If the network topology has changed from the time the election was
          proposed to the time when the majority was achieved then the validator
          updates are not applied. The election can only be concluded if the
          network topology reverts back to the time when the election was proposed.

        * If an election cannot be concluded because of topology changes then a new
          election can be initiated.
        """

        tx_election = self.bigchain.get_transaction(tx_election_id)
        current_validators = self._validators()

        # NOTE: Check if network topology is exactly same to when the election was initiated
        if not self._is_same_topology(current_validators, tx_election.outputs):
            return (False, 'inconsistant_topology')

        total_votes = sum(current_validators.values())
        votes = 0
        #  Aggregate vote count for `election_id`

        for output_id, output in enumerate(tx_election.outputs):
            vote = self.bigchain.get_spent(tx_election_id, output_id, current_votes)

            if vote:
                votes = votes + vote.outputs[0].amount

        # NOTE: Check if >2/3 of total votes have been casted
        if votes > (2/3)*total_votes:
            return (True, tx_election.asset['data'])

        return (False, 'insufficient_votes')


# Load Tendermint's public and private key from the file path
def load_node_key(path):
    with open(path) as json_data:
        priv_validator = json.load(json_data)
        priv_key = priv_validator['priv_key']['value']
        hex_private_key = key_from_base64(priv_key)
        return key_pair_from_ed25519_key(hex_private_key)
