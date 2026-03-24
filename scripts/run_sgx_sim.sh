#!/bin/bash
set -e

DEFAULT_SGX_WALLET_TAG="2f334437f5adf04a48d3ea40504790be59e9c56d"
SGX_WALLET_TAG="${1:-${SGX_WALLET_TAG:-$DEFAULT_SGX_WALLET_TAG}}"
SGX_WALLET_CONTAINER_NAME="sgx-simulator"
SGX_WALLET_IMAGE_NAME="skalenetwork/sgxwallet_sim:$SGX_WALLET_TAG"

docker rm -f "$SGX_WALLET_CONTAINER_NAME" || true
docker pull "$SGX_WALLET_IMAGE_NAME"
docker run -d --network skale-net -p 1026-1031:1026-1031 --name "$SGX_WALLET_CONTAINER_NAME" \
  --entrypoint /bin/bash "$SGX_WALLET_IMAGE_NAME" \
  -c "source /opt/intel/sgxsdk/environment && cd /usr/src/sdk && ./sgxwallet -s -y -d -V"

echo "Waiting for SGX wallet to be ready..."
for i in $(seq 1 60); do
  if curl -sk -o /dev/null -w "%{http_code}" https://127.0.0.1:1026 2>/dev/null | grep -q "405\|200"; then
    echo "SGX wallet is ready after $((i*2)) seconds"
    break
  fi
  echo "Attempt $i: SGX wallet not ready yet..."
  sleep 2
done

docker logs "$SGX_WALLET_CONTAINER_NAME" 2>&1 | tail -20 || true