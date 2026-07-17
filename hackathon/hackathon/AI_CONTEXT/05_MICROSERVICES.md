# Enterprise AI Trust Gateway

# Microservices Architecture

Version: 1.0

Status: FINAL

Classification: PERMANENT

---

# Purpose

This document defines every microservice in the Enterprise AI Trust Gateway.

It specifies:

- Service responsibility
- Ownership
- Inputs
- Outputs
- Dependencies
- Database ownership
- Communication model
- Scalability
- Security boundary

No service may assume responsibilities belonging to another service.

Each service owns exactly one domain.

---

# Service Design Principles

Every service must:

- Have a single business responsibility
- Be independently deployable
- Own its own database schema
- Expose REST APIs (OpenAPI)
- Publish/consume events where appropriate
- Be stateless
- Support horizontal scaling
- Emit logs, metrics and traces
- Expose `/health`, `/ready`, `/live`
- Include Docker, Helm and Kubernetes deployment artifacts

---

# Service Dependency Rules

Services communicate only through:

- REST APIs (synchronous)
- Azure Service Bus
- Azure Event Grid

Forbidden:

- Direct database access
- Shared business logic
- Shared state
- Circular dependencies

---

# 1. email-agent

## Purpose

Ingest enterprise emails.

## Responsibilities

- Connect to Microsoft Graph
- Read mailboxes
- Download attachments
- Extract email metadata
- Publish processing requests

## Inputs

- Microsoft Graph
- EML
- MSG

## Outputs

- Email content
- Attachments
- Metadata
- Processing event

## Depends On

- Microsoft Graph API
- Azure Service Bus

---

# 2. document-agent

## Purpose

Receive enterprise documents.

## Responsibilities

- Accept uploads
- Validate file type
- Extract basic metadata
- Store raw document
- Publish processing event

## Inputs

- REST API
- Azure Storage

## Outputs

- Document reference
- Metadata
- Processing event

---

# 3. ocr-service

## Purpose

Convert documents into machine-readable text.

## Responsibilities

- OCR
- Image preprocessing
- Text extraction
- Layout extraction

## Inputs

- Images
- PDFs

## Outputs

- Plain text
- OCR metadata

## Uses

Azure AI Document Intelligence

---

# 4. pii-engine

## Purpose

Detect sensitive information.

## Responsibilities

- Regex detection
- Presidio analysis
- spaCy NER
- Custom dictionaries
- Confidence scoring

## Outputs

Detected entities

PII report

Confidence scores

---

# 5. classification-engine

## Purpose

Classify enterprise data.

## Responsibilities

- Data sensitivity
- Business category
- Compliance classification
- Risk level

Outputs

Classification report

---

# 6. policy-engine

## Purpose

Apply enterprise policies.

## Responsibilities

- OPA evaluation
- Business rules
- Compliance validation
- Decision making

Outputs

Allow

Block

Review

Mask

---

# 7. tokenization-service

## Purpose

Replace sensitive information.

## Responsibilities

- Format preserving tokenization
- AES encryption
- Token generation

Outputs

Sanitized document

Token list

---

# 8. token-vault

## Purpose

Secure storage of token mappings.

## Responsibilities

- Store token mappings
- Retrieve original values
- Secure encryption
- Audit access

Forbidden

No business logic.

No policy decisions.

---

# 9. prompt-firewall

## Purpose

Protect LLM requests.

## Responsibilities

- Prompt Injection detection
- Jailbreak detection
- Prompt Shielding
- Safety validation

Outputs

Approved prompt

Rejected prompt

---

# 10. llm-gateway

## Purpose

Single gateway to AI providers.

## Responsibilities

- Model routing
- Provider abstraction
- Retry
- Rate limiting
- Cost tracking

Current Provider

Azure OpenAI

Future Providers

Claude

Gemini

OpenAI

Local LLM

---

# 11. response-validator

## Purpose

Validate AI responses.

## Responsibilities

- Hallucination detection
- Policy validation
- Toxicity detection
- Output verification

Outputs

Validated response

Risk report

---

# 12. rehydration-service

## Purpose

Restore enterprise information.

## Responsibilities

- Replace tokens
- Verify mappings
- Preserve formatting

Outputs

Final enterprise response

---

# 13. audit-service

## Purpose

Enterprise audit trail.

## Responsibilities

- Immutable logs
- AI Trust Score
- Compliance records
- Audit reports

Storage

Append-only

---

# 14. dashboard-api

## Purpose

Serve operational dashboards.

## Responsibilities

- Analytics APIs
- Risk dashboards
- Usage metrics
- Trust metrics
- Compliance metrics

Clients

React dashboards

---

# 15. feedback-service

## Purpose

Continuous learning.

## Responsibilities

- User feedback
- Accuracy tracking
- Detection improvements
- Model evaluation

Outputs

Learning events

---

# 16. notification-service

## Purpose

Enterprise notifications.

## Responsibilities

- Email alerts
- Teams notifications
- Security alerts
- Operational alerts

Events

Policy violations

System failures

High risk requests

---

# Shared Library

Purpose

Reusable infrastructure.

Contains

Authentication

Authorization

Logging

Configuration

Telemetry

Exceptions

Validation

Database helpers

Azure SDK wrappers

Constants

Utilities

Forbidden

Business logic

PII detection

Policies

Tokenization

LLM routing

---

# Service Ownership Matrix

| Service | Owns Business Logic | Own Database | REST API | Events | External Integration |
|----------|--------------------|-------------|----------|--------|----------------------|
| email-agent | Yes | Yes | Yes | Yes | Graph API |
| document-agent | Yes | Yes | Yes | Yes | Azure Storage |
| ocr-service | Yes | Yes | Yes | Yes | Azure AI DI |
| pii-engine | Yes | Yes | Yes | Yes | Presidio/spaCy |
| classification-engine | Yes | Yes | Yes | Yes | Internal |
| policy-engine | Yes | Yes | Yes | Yes | OPA |
| tokenization-service | Yes | Yes | Yes | Yes | Internal |
| token-vault | Yes | Yes | Yes | No | Key Vault |
| prompt-firewall | Yes | Yes | Yes | Yes | Internal |
| llm-gateway | Yes | Yes | Yes | Yes | Azure OpenAI |
| response-validator | Yes | Yes | Yes | Yes | Internal |
| rehydration-service | Yes | Yes | Yes | Yes | Token Vault |
| audit-service | Yes | Yes | Yes | Yes | Azure Monitor |
| dashboard-api | Yes | Yes | Yes | No | Frontend |
| feedback-service | Yes | Yes | Yes | Yes | Internal |
| notification-service | Yes | Yes | Yes | Yes | Email/Teams |

---

# Cross-Service Rules

No service may:

- Access another service's database
- Modify another service's data
- Reuse another service's internal code
- Assume another service's responsibility

All communication must occur through published APIs or events.

---

# Success Criteria

The microservice architecture is successful when:

- Every responsibility belongs to exactly one service
- Services are independently deployable
- Services scale independently
- No circular dependencies exist
- Domain boundaries remain intact
- New services can be added without modifying existing domains

---

End of Document
