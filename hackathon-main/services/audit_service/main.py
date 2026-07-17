import hashlib
import json
from datetime import datetime
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Audit and Cryptographic Evidence Store", version="2.0.0")

class AuditLogEntry(BaseModel):
    correlation_id: str
    actor: str
    department: str
    action: str
    classification_level: str
    input_hash: str
    output_hash: str
    risk_score: int
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ChainBlock(BaseModel):
    index: int
    timestamp: str
    log_data: AuditLogEntry
    previous_hash: str
    hash: str

class LedgerSystem:
    def __init__(self):
        self.chain: List[ChainBlock] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        dummy_log = AuditLogEntry(
            correlation_id="00000000-0000-0000-0000-000000000000",
            actor="SYSTEM", department="SEC-OPS",
            action="GENESIS", classification_level="GENERAL",
            input_hash="0", output_hash="0", risk_score=0
        )
        genesis_block = ChainBlock(
            index=0,
            timestamp=datetime.utcnow().isoformat(),
            log_data=dummy_log,
            previous_hash="0",
            hash=self._hash_block(0, "0", dummy_log)
        )
        self.chain.append(genesis_block)

    def _hash_block(self, index: int, prev_hash: str, log_data: AuditLogEntry) -> str:
        payload = f"{index}{prev_hash}{json.dumps(log_data.dict(), sort_keys=True)}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def append_entry(self, entry: AuditLogEntry) -> ChainBlock:
        last_block = self.chain[-1]
        next_index = last_block.index + 1
        next_hash = self._hash_block(next_index, last_block.hash, entry)

        new_block = ChainBlock(
            index=next_index,
            timestamp=datetime.utcnow().isoformat(),
            log_data=entry,
            previous_hash=last_block.hash,
            hash=next_hash
        )
        self.chain.append(new_block)
        return new_block

ledger = LedgerSystem()

@app.post("/api/audit/log", response_model=ChainBlock, status_code=status.HTTP_201_CREATED)
async def add_audit_entry(entry: AuditLogEntry):
    try:
        block = ledger.append_entry(entry)
        return block
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record block: {str(e)}")

@app.get("/api/audit/chain", response_model=List[ChainBlock])
async def get_tamper_proof_chain():
    return ledger.chain
