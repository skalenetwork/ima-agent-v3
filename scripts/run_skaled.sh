# params:
# SKALED_RELEASE - dockerhub schain container version

# returns
# ENDPOINT_URL - URL for running skaled instance
# CHAIN_ID - chainID
# SCHAIN_OWNER - account with money and/or special permissions

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo -- Get schain image --
docker pull --platform linux/amd64 skalenetwork/schain:$SKALED_RELEASE

echo -- Run container --
CONTAINER_ID=$(docker run --platform linux/amd64 --name skaled1 --ulimit nofile=65535:65535 -d -v $SCRIPT_DIR/data_dir:/data_dir -v $SCRIPT_DIR/node_data:/skale_node_data -p 1233-1234:1233-1234/tcp -e DATA_DIR=/data_dir --cap-add SYS_ADMIN --privileged --network skale-net --stop-timeout 40 skalenetwork/schain:$SKALED_RELEASE --http-port 1234 --ws-port 1233 --config /skale_node_data/skaled1/config.json -d /data_dir --ipcpath /data_dir -v 4 --web3-trace --enable-debug-behavior-apis --aa no --sgx-url https://sgx-simulator:1026)

if [ -z "$CONTAINER_ID" ]; then
    echo "Error: Failed to start the skaled container."
    exit 1
fi

export ENDPOINT_URL="http://127.0.0.1:1234"
# export CHAIN_ID=$( python3 $SCRIPT_DIR/config.py extract $SCRIPT_DIR/data_dir/config.json params.chainID )
export INSECURE_ETH_PRIVATE_KEY="0x0e394ff21db60660a27a6383aedf8c75070648965acbef7c369c1bae2141a485"

sleep 10