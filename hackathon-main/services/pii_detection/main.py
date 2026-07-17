import re
import json
import os
from fastapi import FastAPI, status, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from presidio_analyzer import AnalyzerEngine

app = FastAPI(title="Configurable AI Privacy Detection Engine", version="2.1.0")

# --- Configuration Pydantic Schemas ---

class CustomRegexSchema(BaseModel):
    entity_type: str
    regex: str
    confidence: float
    capture_group: int = 0

class PIIConfiguration(BaseModel):
    department_multipliers: Dict[str, float]
    entity_weights: Dict[str, int]
    custom_regex_patterns: List[CustomRegexSchema]

# --- Runtime Request / Response Schemas ---

class PIIDetectionRequest(BaseModel):
    text: str
    department: str = Field(..., example="banking")
    enabled_detectors: List[str] = ["ner", "regex"]

class DetectedEntity(BaseModel):
    entity_type: str
    value: str
    start: int
    end: int
    confidence: float
    source: str

class PIIDetectionResponse(BaseModel):
    detected_entities: List[DetectedEntity]
    risk_score: int
    classification: str

# --- Configuration Store Manager ---

class ConfigStore:
    def __init__(self, config_path: str = "pii_config.json"):
        self.config_path = config_path
        self.config: PIIConfiguration = self._load_default_config()
        self.compiled_patterns: List[Dict[str, Any]] = []
        self.compile_regex_rules()

    def _load_default_config(self) -> PIIConfiguration:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return PIIConfiguration(**json.load(f))
        return PIIConfiguration(
            department_multipliers={"general": 1.0},
            entity_weights={"PERSON": 15},
            custom_regex_patterns=[]
        )

    def update_config(self, new_config: PIIConfiguration):
        self.config = new_config
        self.compile_regex_rules()
        with open(self.config_path, "w") as f:
            f.write(self.config.json(indent=2))

    def compile_regex_rules(self):
        self.compiled_patterns = []
        for rule in self.config.custom_regex_patterns:
            try:
                self.compiled_patterns.append({
                    "entity_type": rule.entity_type,
                    "compiled": re.compile(rule.regex),
                    "confidence": rule.confidence,
                    "capture_group": rule.capture_group
                })
            except re.error as e:
                print(f"Skipping invalid regex pattern for {rule.entity_type}: {e}")

# Global Config Store Singleton
store = ConfigStore()

# --- Configurable Processing Logic ---

class ConfigurablePIIEngine:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.config = store.config
        self.compiled_patterns = store.compiled_patterns

    def detect_custom_patterns(self, text: str) -> List[DetectedEntity]:
        matches = []
        for pattern_info in self.compiled_patterns:
            entity_type = pattern_info["entity_type"]
            compiled_re = pattern_info["compiled"]
            confidence = pattern_info["confidence"]
            group_idx = pattern_info["capture_group"]

            for match in compiled_re.finditer(text):
                try:
                    match_val = match.group(group_idx)
                    start = match.start(group_idx)
                    end = match.end(group_idx)
                except IndexError:
                    match_val = match.group(0)
                    start = match.start(0)
                    end = match.end(0)

                matches.append(DetectedEntity(
                    entity_type=entity_type,
                    value=match_val,
                    start=start,
                    end=end,
                    confidence=confidence,
                    source="configurable_regex"
                ))
        return matches

    def calculate_metrics(self, entities: List[DetectedEntity], department: str):
        multiplier = self.config.department_multipliers.get(department.lower(), 1.0)
        total_risk = 0.0

        for ent in entities:
            # Safely fall back to a weight of 10 for undefined custom types
            weight = self.config.entity_weights.get(ent.entity_type, 10)
            total_risk += weight * ent.confidence * multiplier

        risk_score = min(100, int(total_risk))

        if risk_score == 0:
            classification = "GENERAL"
        elif risk_score < 25:
            classification = "INTERNAL"
        elif risk_score < 55:
            classification = "CONFIDENTIAL"
        elif risk_score < 80:
            classification = "RESTRICTED"
        else:
            classification = "HIGHLY_CONFIDENTIAL"

        return risk_score, classification

# --- API Endpoints ---

@app.post("/api/pii/detect", response_model=PIIDetectionResponse)
async def detect_pii(request: PIIDetectionRequest):
    """Executes dynamic identification of PII and risk scoring using hot-reload config rules."""
    engine = ConfigurablePIIEngine()
    found_entities = []

    # 1. Base Presidio NER
    if "ner" in request.enabled_detectors:
        results = engine.analyzer.analyze(text=request.text, language="en")
        for res in results:
            found_entities.append(DetectedEntity(
                entity_type=res.entity_type,
                value=request.text[res.start:res.end],
                start=res.start,
                end=res.end,
                confidence=res.score,
                source="presidio_ner"
            ))

    # 2. Configurable Custom Regex
    if "regex" in request.enabled_detectors:
        found_entities.extend(engine.detect_custom_patterns(request.text))

    risk_score, classification = engine.calculate_metrics(found_entities, request.department)

    return PIIDetectionResponse(
        detected_entities=found_entities,
        risk_score=risk_score,
        classification=classification
    )

# --- Configuration Administration Endpoints ---

@app.get("/api/pii/config", response_model=PIIConfiguration, tags=["Configuration Management"])
async def get_pii_configuration():
    """Retrieve the currently active dynamic configuration mapping."""
    return store.config

@app.post("/api/pii/config", response_model=PIIConfiguration, tags=["Configuration Management"])
async def update_pii_configuration(new_config: PIIConfiguration):
    """Instantly update configuration parameters and compile patterns in-memory."""
    try:
        store.update_config(new_config)
        return store.config
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Configuration update failed: {str(e)}"
        )
