
# Enterprise AI Trust Gateway

# Event Driven Architecture

Version: 1.0

Status: FINAL

Classification: PERMANENT

---

# Purpose

This document defines the event-driven communication model for the Enterprise AI Trust Gateway.

It specifies:

- Synchronous communication
- Asynchronous communication
- Event ownership
- Event lifecycle
- Message contracts
- Retry strategy
- Dead Letter Queue strategy
- Event versioning
- Idempotency
- Correlation and tracing

Every service must follow these standards.

---

# Communication Principles

The platform uses two communication models.

## Synchronous

Protocol

REST

HTTPS

OpenAPI

Used for

Immediate request/response operations.

Examples

Dashboard → Audit Service

Dashboard → Notification Service

Gateway → Token Vault

---

## Asynchronous

Platform

Azure Service Bus

Azure Event Grid

Used for

Long-running workflows

Notifications

Document processing

OCR

Audit

Feedback

Analytics

Background processing

---

# Event Design Principles

Every event

Must have a single producer.

May have multiple consumers.

Must be immutable.

Must be versioned.

Must include metadata.

Must include timestamps.

Must include correlation identifiers.

Must never contain raw secrets.

Must never contain plaintext PII.

---

# Event Envelope

Every event contains

event_id

event_type

event_version

occurred_at

correlation_id

trace_id

producer

payload

metadata

---

# Event Versioning

Use Semantic Versioning.

Examples

document.received.v1

document.received.v2

pii.detected.v1

tokenization.completed.v1

Older consumers must continue to function.

Breaking changes require a new version.

---

# Correlation

Every request entering the platform receives

Correlation ID

Trace ID

These identifiers travel through every service.

They are mandatory.

---

# Idempotency

Consumers must safely process duplicate events.

Requirements

Duplicate detection

Safe retries

No duplicate business effects

No duplicate audit records

---

# Retry Strategy

Transient failures

Retry

Permanent failures

Dead Letter Queue

Retry Policy

Exponential Backoff

Maximum Retries

5

After maximum retries

Move message to DLQ

---

# Dead Letter Queue

Every queue has a DLQ.

Failed messages remain available for investigation.

No failed message is discarded.

---

# Event Categories

Document Events

Security Events

Processing Events

AI Events

Audit Events

Notification Events

Feedback Events

System Events

---

# Document Events

Producer

email-agent

document-agent

Events

document.received.v1

document.validated.v1

document.failed.v1

Consumers

ocr-service

audit-service

notification-service

---

# OCR Events

Producer

ocr-service

Events

ocr.completed.v1

ocr.failed.v1

Consumers

pii-engine

audit-service

---

# PII Events

Producer

pii-engine

Events

pii.detected.v1

pii.not_found.v1

Consumers

classification-engine

audit-service

---

# Classification Events

Producer

classification-engine

Events

classification.completed.v1

classification.failed.v1

Consumers

policy-engine

---

# Policy Events

Producer

policy-engine

Events

policy.allowed.v1

policy.blocked.v1

policy.review.v1

Consumers

tokenization-service

notification-service

audit-service

---

# Tokenization Events

Producer

tokenization-service

Events

tokenization.completed.v1

tokenization.failed.v1

Consumers

prompt-firewall

token-vault

audit-service

---

# Prompt Firewall Events

Producer

prompt-firewall

Events

prompt.approved.v1

prompt.blocked.v1

Consumers

llm-gateway

audit-service

notification-service

---

# LLM Events

Producer

llm-gateway

Events

llm.requested.v1

llm.completed.v1

llm.failed.v1

Consumers

response-validator

audit-service

---

# Response Validation Events

Producer

response-validator

Events

response.validated.v1

response.rejected.v1

Consumers

rehydration-service

audit-service

---

# Rehydration Events

Producer

rehydration-service

Events

response.rehydrated.v1

Consumers

audit-service

dashboard-api

---

# Audit Events

Producer

Every service

Events

audit.record.created.v1

Consumers

dashboard-api

analytics

---

# Notification Events

Producer

notification-service

Events

notification.sent.v1

notification.failed.v1

---

# Feedback Events

Producer

feedback-service

Events

feedback.received.v1

feedback.processed.v1

---

# Event Routing

Azure Service Bus

Handles

Reliable delivery

Commands

Work queues

Background jobs

Azure Event Grid

Handles

Broadcast events

Notifications

System integration

Multiple subscribers

---

# Event Ordering

Ordering is guaranteed only where explicitly required.

Business logic must not depend on global ordering.

---

# Payload Design Rules

Payloads must contain

Business identifiers

Metadata

References

Never include

Secrets

Passwords

Access tokens

Plaintext PII

Large binary documents

Use references for large files.

---

# Observability

Every event produces

Logs

Metrics

Traces

Audit records

Correlation IDs

Latency metrics

Failure metrics

---

# Security

Events are encrypted in transit.

Events are authenticated.

Authorization applies to publishers and subscribers.

Sensitive values must be tokenized before publication.

---

# Success Criteria

The messaging architecture is successful when

Every event has one producer.

Events are immutable.

Events are versioned.

Duplicate processing is safe.

Failures are recoverable.

Tracing is complete.

No sensitive data leaks into the event bus.

---

End of Document
