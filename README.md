# State Delta Audit

### Overview
`state-delta-audit` compares contract storage values between two Ethereum blocks and computes a verifiable Keccak commitment to all slots that changed.

---

### Installation
1. Ensure Python 3.9+ and pip are installed.
2. Install dependencies:
   pip install web3

---

### Usage
Run with a target contract address and two block numbers:
  python state_audit.py 0xABC...DEF 18000000 19000000 --slots=0,1,2,3

If `--slots` is omitted, the first 16 slots are checked.

---

### Output
A JSON structure:
  - `root`: a Keccak hash committing to all changed slots.
  - `changed`: list of slot indexes that differ.
  - `slots`: dictionary of old/new values per slot.

---

### Example
  python state_audit.py 0xA0b8...eB48 18500000 18600000 --slots=0x0,0x1,0x2

---

### Notes
- Use a real RPC endpoint (`RPC_URL` environment variable or Infura key).
- Works on any EVM chain (Mainnet, Sepolia, Polygon, etc.).
- For deep history (old blocks), an archive node may be required.
