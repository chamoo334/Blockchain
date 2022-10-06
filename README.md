# Blockchain

## Getting Started
### Verify Application
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
python3 -m backend.app
```
4. To run a peer instance, start the port_selector server in a 2nd terminal. Run the peer port updater script and the start the application as a peer in a 3rd terminal.
```sh
# 2nd terminal
python3 -m backend.port_selector

# 3rd terminal
python3 -m backend.scripts.update_peer_port
export PEER=TRUE && python3 -m backend.app
```

### Run as Containers
1. build main server images
```
docker build --no-cache -t backend -f ./dockerfiles/Dockerfile.server.main .
docker build --no-cache -t port_selector -f ./dockerfiles/Dockerfile.server.helper .
```
2. run main server containers <br>
<mark>Note</mark>: default ports for backend.app and backen.port_selector are 5000 and 5001. These ports can be adjusted by altering backend.config
```
docker run -p 8998:5000 --name backend backend
docker run -p 8999:5001 --name port_selector port_selector
```
3. obtain port number for peer instance and update appropriate documents <br>
<mark>Note</mark>: you will need to observe and annotate the port selected to run the container. This port can be found in backend.config as `PEER_PORT` once successfully run
```
python3 -m backend.scripts.update_peer_port
```
4. build peer image
```
docker build --no-cache -t peer_<PEER_PORT> -f ./dockerfiles/Dockerfile.server.peer .
```
5. run peer instance
```
docker run -p 9000:<PEER_PORT> --name peer_<PEER_PORT> peer_<PEER_PORT>
```
