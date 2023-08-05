import types

from plenum.common.constants import DOMAIN_LEDGER_ID, CONSISTENCY_PROOF, CURRENT_PROTOCOL_VERSION
from plenum.common.ledger import Ledger
from plenum.test.node_request.message_request.helper import \
    count_msg_reqs_of_type
from plenum.test.view_change.helper import ensure_view_change
from stp_core.common.log import getlogger
from plenum.common.messages.node_messages import LedgerStatus
from plenum.test.helper import sdk_send_random_requests
from plenum.test.node_catchup.helper import waitNodeDataEquality

# Do not remove the next imports
from plenum.test.node_catchup.conftest import whitelist
from plenum.test.batching_3pc.conftest import tconf

logger = getlogger()
# So that `three_phase_key_for_txn_seq_no` always works, it makes the test
# easy as the requesting node selects a random size for the ledger
Max3PCBatchSize = 1
TestRunningTimeLimitSec = 150


def testNodeRequestingConsProof(tconf, txnPoolNodeSet,
                                sdk_node_created_after_some_txns_not_started):
    """
    All of the 4 old nodes delay the processing of LEDGER_STATUS from the newly
    joined node while they are processing requests which results in them sending
    consistency proofs which are not same so that the newly joined node cannot
    conclude about the state of transactions in the system. So the new node
    requests consistency proof for a particular range from all nodes.
    """
    looper, new_node, sdk_pool_handle, new_steward_wallet_handle = sdk_node_created_after_some_txns_not_started

    # So nodes wont tell the clients about the newly joined node so they
    # dont send any request to the newly joined node
    for node in txnPoolNodeSet:
        node.sendPoolInfoToClients = types.MethodType(lambda x, y: None, node)

    # The new node sends different ledger statuses to every node so it
    # does not get enough similar consistency proofs
    next_size = 0
    origMethod = new_node.build_ledger_status

    def build_broken_ledger_status(self, ledger_id):
        nonlocal next_size
        if ledger_id != DOMAIN_LEDGER_ID:
            return origMethod(ledger_id)

        size = self.domainLedger.size
        next_size = next_size + 1 if next_size < size else 1
        print("new size {}".format(next_size))

        newRootHash = Ledger.hashToStr(
            self.domainLedger.tree.merkle_tree_hash(0, next_size))
        three_pc_key = self.three_phase_key_for_txn_seq_no(ledger_id,
                                                           next_size)
        v, p = three_pc_key if three_pc_key else None, None
        ledgerStatus = LedgerStatus(1, next_size, v, p, newRootHash,
                                    CURRENT_PROTOCOL_VERSION)
        print("dl status {}".format(ledgerStatus))
        return ledgerStatus

    new_node.build_ledger_status = types.MethodType(
        build_broken_ledger_status, new_node)

    logger.debug(
        'Domain Ledger status sender of {} patched'.format(new_node))

    looper.add(new_node)
    txnPoolNodeSet.append(new_node)
    sdk_send_random_requests(looper, sdk_pool_handle,
                             new_steward_wallet_handle, 10)
    #  wait more than `ConsistencyProofsTimeout`
    # TODO: apply configurable timeout here
    # `ConsistencyProofsTimeout` is set to 60 sec, so need to wait more than
    # 60 sec, hence large timeout. Dont reduce it.
    waitNodeDataEquality(looper, new_node, *txnPoolNodeSet[:-1],
                         customTimeout=75)
    # Other nodes should have received a request for `CONSISTENCY_PROOF` and
    # processed it.
    for node in txnPoolNodeSet[:-1]:
        assert count_msg_reqs_of_type(node, CONSISTENCY_PROOF) > 0, node
