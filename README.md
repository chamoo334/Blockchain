# Blockchain

## Getting Started
**(Suggested)** Activating Virtual Environment
```
python3 -m venv blockchain
source blockchain/bin/activate
```
1. Install required packages
```
pip3 install -r requirements.txt
```
2. Run tests
```
python3 -m pytest backend/tests
```
3. Run the application and API
```
python3 -m backend.peer_helper
python3 -m backend.app
```
4. Run a peer instance in a separate terminal
```
export PEER=TRUE && python3 -m backend.app
```
5. build images
```
docker build --no-cache -t backend -f ./containers/Dockerfile.server.main .
docker build --no-cache -t backend_peer -f ./containers/Dockerfile.server.peer .
```
6. 
