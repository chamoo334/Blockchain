import os, requests, atexit, signal
from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub
from backend.config import APP_ADDRESS, APP_PORT, PEER_HELPER_PORT, PEER_HELPER_ADDRESS


PORT = APP_PORT

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet()
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route('/')
def route_default():
    return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)

    if transaction:
        transaction.update(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )
    else:
        transaction = Transaction(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )

    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.to_json())


@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({ 'address': wallet.address, 'balance': wallet.balance })

# instantiate peer network connection and update blockchain
if os.environ.get('PEER') == 'TRUE':

    PORT = requests.get(f'{PEER_HELPER_ADDRESS}:{PEER_HELPER_PORT}/peer/port').json()['peer_port']
    print(PORT)

    result = requests.get(f'{APP_ADDRESS}:{APP_PORT}/blockchain')
    result_blockchain = Blockchain.from_json(result.json())

    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'\n -- Error synchronizing: {e}')
else: # notify port_selector of server port in use
    notify = requests.post(f'{PEER_HELPER_ADDRESS}:{PEER_HELPER_PORT}/update/server/port', json={'server_port': PORT})

@atexit.register
def free_port():
    if os.environ.get('PEER') == 'TRUE':
        update = requests.post(f'{PEER_HELPER_ADDRESS}:{PEER_HELPER_PORT}/remove/port', json={'available_port': PORT})
    else:
        update = requests.post(f'{PEER_HELPER_ADDRESS}:{PEER_HELPER_PORT}/update/server/port', json={'server_port': PORT})
    return f'Port {PORT} is now available'

#TODO: switch to sys.exit for cleaner
def signal_handler(sig, frame):
    free_port()
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')