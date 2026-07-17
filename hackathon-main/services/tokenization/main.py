import hashlib
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Tokenization Service", version="2.0.0")

class TokenizeItem(BaseModel):
    entity_type: str
    value: str
    start: int
    end: int

class TokenizationRequest(BaseModel):
    text: str
    entities: List[TokenizeItem]
    masking_mode: str = "format_preserving" # "format_preserving", "redact", "mask"

class TokenizationResponse(BaseModel):
    tokenized_text: str
    token_mapping: Dict[str, str]
    hash_audit_map: Dict[str, str]

class TokenizationEngine:
    def __init__(self):
        self.prefixes = {
            "PERSON": "TOK_USR",
            "CREDIT_CARD": "TOK_CCN",
            "EMAIL_ADDRESS": "TOK_EML",
            "API_KEY": "TOK_KEY",
            "EMPLOYEE_ID": "TOK_EMP"
        }

    def process(self, request: TokenizationRequest) -> TokenizationResponse:
        tokenized_text = request.text
        token_mapping = {}
        hash_audit_map = {}

        # Sort in reverse order of starting position to safely replace inline strings
        sorted_entities = sorted(request.entities, key=lambda x: x.start, reverse=True)

        for idx, ent in enumerate(sorted_entities):
            raw_val = ent.value
            sha_val = hashlib.sha256(raw_val.encode()).hexdigest()

            if request.masking_mode == "redact":
                token = f"[{ent.entity_type}_REDACTED]"
            elif request.masking_mode == "mask":
                if ent.entity_type == "EMAIL_ADDRESS" and "@" in raw_val:
                    parts = raw_val.split("@")
                    token = f"xxxx@{parts[1]}"
                elif ent.entity_type == "CREDIT_CARD" and len(raw_val) >= 4:
                    token = f"xxxx-xxxx-xxxx-{raw_val[-4:]}"
                else:
                    token = "********"
            else: # Format Preserving Representation
                prefix = self.prefixes.get(ent.entity_type, "TOK_GEN")
                token = f"{prefix}_{self.hash_val_short(raw_val)}"

            token_mapping[token] = raw_val
            hash_audit_map[sha_val] = token

            tokenized_text = (
                tokenized_text[:ent.start] +
                token +
                tokenized_text[ent.end:]
            )

        return TokenizationResponse(
            tokenized_text=tokenized_text,
            token_mapping=token_mapping,
            hash_audit_map=hash_audit_map
        )

    def hash_val_short(self, value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()[:6].upper()

@app.post("/api/token/tokenize", response_model=TokenizationResponse)
async def apply_tokenization(request: TokenizationRequest):
    try:
        engine = TokenizationEngine()
        return engine.process(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
