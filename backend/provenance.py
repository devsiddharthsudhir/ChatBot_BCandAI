from pathlib import Path
import json
import os
from hashlib import sha256

from web3 import Web3
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")

ARTIFACT_PATH = BASE_DIR / "blockchain" / "artifacts" / "contracts" / "ProvenanceRegistry.sol" / "ProvenanceRegistry.json"

with open(ARTIFACT_PATH, "r", encoding="utf-8") as f:
    artifact = json.load(f)
contract_abi = artifact["abi"]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(
    address = Web3.toChecksumAddress(CONTRACT_ADDRESS),
    abi=contract_abi,
)

def _build_and_send_tx(func):
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
    tx = func.build_transaction(
        {
            "from": ACCOUNT_ADDRESS,
            "nonce": nonce,
            "gas": 500000,
            "gasPrice": w3.eth.gas_price,
        }
    )
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt.transactionHash.hex()

def hash_file(path: Path) -> bytes:
    h = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.digest()

def register_dataset(dataset_id: str, data_path: Path, metadata: str = "") -> str:
    file_hash = hash_file(data_path)
    return _build_and_send_tx(
        contract.functions.registerDataset(dataset_id, file_hash, metadata)
    )

def register_model(model_version: str, model_path: Path, dataset_id: str) -> str:
    file_hash = hash_file(model_path)
    return _build_and_send_tx(
        contract.functions.registerModel(model_version, file_hash, dataset_id)
    )

def commit_log(session_id: str, log_path: Path, model_version: str) -> str | None:
    if not log_path.exists():
        return None
    file_hash = hash_file(log_path)
    return _build_and_send_tx(
        contract.functions.commitLog(session_id, file_hash, model_version)
    )
