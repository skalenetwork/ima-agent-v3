export SGX_WALLET_TAG=2f334437f5adf04a48d3ea40504790be59e9c56d
echo "SGX_WALLET_TAG=$SGX_WALLET_TAG" >> $GITHUB_ENV
bash ./scripts/run_sgx_container.sh $SGX_WALLET_TAG
echo "Waiting for SGX wallet to be ready..."
for i in {1..60}; do
  if curl -s -o /dev/null -w "%{http_code}" https://127.0.0.1:1026 2>/dev/null | grep -q "405\|200"; then
    echo "SGX wallet is ready after $((i*2)) seconds"
    break
  fi
  echo "Attempt $i: SGX wallet not ready yet..."
  sleep 2
done
docker logs sgx-simulator 2>&1 | tail -20 || true