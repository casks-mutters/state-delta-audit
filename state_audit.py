#!/usr/bin/env python3
import os, sys, time, json
from web3 import Web3

RPC_URL = os.getenv("RPC_URL", "https://mainnet.infura.io/v3/your_api_key")

def connect(rpc: str) -> Web3:
    w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 30}))
    if not w3.is_connected():
        print("❌ Failed to connect to RPC.")
        sys.exit(1)
    return w3

def get_storage(w3, addr, slot, block):
    try:
        return w3.eth.get_storage_at(addr, slot, block_identifier=block)
    except Exception as e:
        print(f"⚠️ Storage read failed @slot {slot}: {e}")
        return b"\x00" * 32

def keccak(data: bytes) -> str:
    return "0x" + Web3.keccak(data).hex()

def audit_diff(w3, address: str, slots: list[int], block_a: int, block_b: int):
    results, changed = {}, []
    for slot in slots:
        a = get_storage(w3, address, slot, block_a)
        b = get_storage(w3, address, slot, block_b)
        diff = (a != b)
        results[slot] = {"a": a.hex(), "b": b.hex(), "changed": diff}
        if diff:
            changed.append(slot)
    root = keccak(b"".join(int.to_bytes(s, 32, "big") for s in changed)) if changed else "0x0"
    return {"root": root, "changed": changed, "slots": results}

def main():
    if len(sys.argv) < 4:
        print("Usage: python state_audit.py <contract> <blockA> <blockB> [--slots=0,1,2]")
        sys.exit(1)

    addr = Web3.to_checksum_address(sys.argv[1])
    blockA, blockB = int(sys.argv[2]), int(sys.argv[3])
    if blockA == blockB: print("ℹ️ Both blocks are the same; diff will always be empty."); sys.exit(0)
    slots = [int(s, 0) for s in sys.argv[4].split("=")[1].split(",")] if len(sys.argv) > 4 else range(0, 16)
    w3 = connect(RPC_URL)
    print(f"🌐 Connected to chainId {w3.eth.chain_id}")
    t0 = time.time()
    res = audit_diff(w3, addr, slots, blockA, blockB)
    print(json.dumps(res, indent=2))
    print(f"⏱️ Done in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    main()
