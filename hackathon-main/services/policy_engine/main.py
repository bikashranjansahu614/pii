from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Policy Decision Point (PDP)", version="2.0.0")

class AuthorizationQuery(BaseModel):
    user_role: str
    department: str
    data_classification: str
    risk_score: int
    requested_model: str

class PolicyVerdict(BaseModel):
    authorized: bool
    action: str # "ALLOW", "BLOCK", "TOKENIZE", "REQUIRE_APPROVAL"
    reason: str
    required_remediation: List[str]

@app.post("/api/policy/evaluate", response_model=PolicyVerdict)
async def evaluate_access_policy(query: AuthorizationQuery):
    """
    Evaluates context against enterprise access schemas.
    """
    verdict = PolicyVerdict(
        authorized=True,
        action="ALLOW",
        reason="Implicit authorization granted.",
        required_remediation=[]
    )

    # Rule 1: Highly Confidential Block
    if query.data_classification == "HIGHLY_CONFIDENTIAL":
        verdict.authorized = False
        verdict.action = "BLOCK"
        verdict.reason = "Highly Confidential corporate IP cannot be sent to LLMs."
        verdict.required_remediation.append("REDACTION_MANDATORY")
        return verdict

    # Rule 2: Risk-based routing rules
    if query.risk_score >= 75:
        verdict.authorized = False
        verdict.action = "BLOCK"
        verdict.reason = f"Composite risk evaluation of {query.risk_score} exceeds acceptable thresholds."
        return verdict

    # Rule 3: Restrict external engines for confidential workloads
    if query.data_classification in ["RESTRICTED", "CONFIDENTIAL"]:
        if query.requested_model in ["openai_external", "claude_external"]:
            verdict.authorized = True
            verdict.action = "TOKENIZE"
            verdict.reason = "External processing of sensitive metadata requires formatting preservation tokenization."
            verdict.required_remediation.append("ENFORCE_TOKENIZATION")
        else:
            verdict.authorized = True
            verdict.action = "ALLOW"
            verdict.reason = "Processing allowed on isolated internal model architectures."

    return verdict
