# Enterprise AI Trust Gateway

# Database Architecture

Version: 1.0

Status: FINAL

Classification: PERMANENT

---

# Purpose

This document defines the database architecture for the Enterprise AI Trust Gateway.

It specifies:

- Database ownership
- Schema ownership
- Persistence strategy
- Transaction boundaries
- Migration strategy
- Indexing strategy
- Data retention
- Backup and recovery
- Performance guidelines

No implementation may violate these rules.

---

# Database Strategy

The platform uses PostgreSQL as the primary relational database.

Redis is used for caching and temporary state.

Azure Storage stores large binary files.

Azure Key Vault stores secrets.

---

# Logical Database Architecture

One PostgreSQL Server

↓

One PostgreSQL Database

↓

Independent Schema Per Service

Every service owns one schema.

Example

email_agent

document_agent

ocr_service

pii_engine

classification_engine

policy_engine

tokenization_service

token_vault

llm_gateway

prompt_firewall

response_validator

rehydration_service

audit_service

dashboard_api

feedback_service

notification_service

---

# Database Ownership Rules

Each service owns

Tables

Views

Indexes

Functions

Triggers

Sequences

Migrations

No service may

Read another service schema directly.

Modify another service schema.

Share business tables.

Bypass APIs.

---

# Data Ownership

Email Agent

Owns

Email metadata

Processing status

Attachment references

---

Document Agent

Owns

Document metadata

Upload history

Storage references

---

OCR Service

Owns

OCR output

OCR metadata

Processing statistics

---

PII Engine

Owns

Detected entities

Confidence scores

Detection history

---

Classification Engine

Owns

Classification results

Sensitivity labels

Risk categories

---

Policy Engine

Owns

Policy evaluations

Decision history

Policy execution logs

---

Tokenization Service

Owns

Token metadata

Token generation history

Encryption metadata

---

Token Vault

Owns

Secure token mappings

Key references

Access history

---

LLM Gateway

Owns

Model requests

Provider statistics

Token usage

Latency

---

Prompt Firewall

Owns

Prompt analysis

Security findings

Blocked prompts

---

Response Validator

Owns

Validation results

Hallucination scores

Safety checks

---

Rehydration Service

Owns

Rehydration history

Validation references

---

Audit Service

Owns

Audit logs

Trust scores

Compliance records

Immutable events

---

Dashboard API

Owns

Aggregated reporting

Materialized views

Dashboard cache

---

Feedback Service

Owns

Feedback

Ratings

Evaluation metrics

---

Notification Service

Owns

Notification history

Delivery status

Retry history

---

# Transaction Rules

Transactions remain inside one service.

Distributed transactions are forbidden.

Cross-service consistency uses

Events

Retries

Compensation

Eventually Consistent workflows.

---

# Migration Strategy

Every service manages its own migrations.

Migration Tool

Alembic

Migration Rules

Forward only.

Version controlled.

Reviewed.

Repeatable.

Automated.

No manual production changes.

---

# Naming Standards

Schemas

snake_case

Tables

snake_case_plural

Columns

snake_case

Indexes

idx_<table>_<column>

Foreign Keys

fk_<table>_<reference>

Primary Keys

pk_<table>

Unique Constraints

uq_<table>_<column>

---

# Primary Keys

Use UUID v7 for all business entities.

Avoid auto-increment IDs for externally visible entities.

Every table includes

id

created_at

updated_at

created_by

updated_by

---

# Soft Delete

Business tables should support

deleted_at

deleted_by

Hard delete only when legally permitted.

---

# Auditing

Sensitive tables must include

created_at

updated_at

created_by

updated_by

Audit history is maintained by Audit Service.

---

# Index Strategy

Indexes required for

Primary Keys

Foreign Keys

Frequently filtered columns

Search columns

Event identifiers

Correlation IDs

Trace IDs

Avoid unnecessary indexes.

---

# Large Objects

Binary files

PDF

Images

Office Documents

ZIP

Must never be stored in PostgreSQL.

Store only

Reference

Checksum

Metadata

URI

Files reside in Azure Storage.

---

# Caching Strategy

Redis stores

Session cache

Configuration cache

Temporary OCR cache

Rate limiting

Frequently accessed lookups

Redis is not a system of record.

---

# Backup Strategy

Daily full backups.

Point-in-Time Recovery enabled.

Backup verification required.

Regular restore testing required.

---

# Retention Policy

Audit logs

Long-term retention

Feedback

Configurable retention

Temporary processing data

Short retention

Large binary files

Azure Storage lifecycle policies

---

# Performance Guidelines

Connection pooling

Async database access

Prepared statements

Batch processing where appropriate

Pagination for large result sets

Avoid SELECT *

Limit transaction duration

Optimize indexes

Monitor slow queries

---

# Security

Database authentication through Managed Identity where supported.

Secrets stored in Azure Key Vault.

TLS required.

Encryption at rest enabled.

Least privilege database roles.

No shared database users.

---

# Observability

Every database operation emits

Structured logs

Metrics

Query latency

Connection metrics

Failure metrics

Deadlock metrics

---

# Success Criteria

The database architecture is successful when

Every service owns its data.

No service accesses another schema directly.

Migrations are automated.

Data remains secure.

Performance scales.

Backups are recoverable.

Database evolution remains independent.

---

End of Document
