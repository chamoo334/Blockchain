APP_PORT = 5000
PEER_HELPER_PORT = 5001
PEER_PORT = None

APP_ADDRESS = 'http://localhost'
PEER_HELPER_ADDRESS = 'http://localhost'
PEER_ADDRESS = 'http://localhost'
TEST_ADDRESS = f'{APP_ADDRESS}:{APP_PORT}'
TRUSTED_CLIENT_PORT = 3000
TRUSTED_CLIENT_ADDRESS = f'http://localhost:{TRUSTED_CLIENT_PORT}'

SUBSCRIBE_KEY = None
PUBLISH_KEY = None

NANOSECONDS = 1
MICROSECONDS = 1000 * NANOSECONDS
MILLISECONDS = 1000 * MICROSECONDS
SECONDS = 1000 * MILLISECONDS

MINE_RATE = 4 * SECONDS

STARTING_BALANCE = 1000

MINING_REWARD = 50
MINING_REWARD_INPUT = { 'address': '*--official-mining-reward--*' }