# Blockchain

- [Blockchain](#blockchain)
  - [Quick Start with Docker Compose](#quick-start-with-docker-compose)
  - [Verify Applications](#verify-applications)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Run as Containers](#run-as-containers)
    - [Backend Only](#backend-only)
    - [Frontend Only](#frontend-only)
    - [All together](#all-together)

## Quick Start with Docker Compose
1. TODO: update
## Verify Applications
### Backend
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
export PEER=TRUE && python3 -m backend.app
```
### Frontend
1. cd frontend
2. `npm run start`
## Run as Containers
### Backend Only
1. build main server images <br>
<mark>Note</mark>: default ports for backend.app and backend.port_selector are 5000 and 5001. These ports can be adjusted by altering backend.config and updating Dockerfiles located in ./dockerfiles
```
docker build --no-cache -t backendhelper -f ./dockerfiles/Dockerfile.server.helper .
docker build --no-cache -t backendmain -f ./dockerfiles/Dockerfile.server.main .
docker build --no-cache -t backendpeer -f ./dockerfiles/Dockerfile.server.peer .
```
2. run main server containers <br>
<mark>Note</mark>: These run commands are set to use localhost for general use within various environments. Please adjust the declared network to use and update urls in backend.config for your needs.
```
docker run -p 5001:5001 --name backendhelper --net=host -d backendhelper
docker run -p 5000:5000 --name backendmain --net=host -d backendmain
docker run -p 5002-6002:5002-6002 --name backendpeer --net=host -d backendpeer
```
1. obtain ports
```
wget http://localhost:5001/get/ports
```
<mark>Note: </mark> At this point, 3 ports should be present: 5000 (backend.app non-peer instance), 5001 (backend.port_selector), and a third port for backend.app peer instance
4. Proceed with tests:
   1. via `python3 -m backend.scripts.test_app`. This test can be modified by altering the TEST_ADDRESS specified in backend.config.
   2. Alternatively, test the /blockchain and /blockchain/mine endpoints for each container by making calls to the respective ports on the specified network.

### Frontend Only

### All together