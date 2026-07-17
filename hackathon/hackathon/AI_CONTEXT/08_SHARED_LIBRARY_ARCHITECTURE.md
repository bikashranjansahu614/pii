# Enterprise AI Trust Gateway

# Shared Library Architecture

Version: 1.0

Status: FINAL

Classification: PERMANENT

---

# Purpose

This document defines the architecture, responsibilities, ownership and boundaries of the shared library.

The shared library exists to eliminate infrastructure duplication across microservices.

It must NEVER contain business logic.

---

# Objectives

Provide reusable infrastructure.

Provide standardized implementations.

Reduce duplicated code.

Improve consistency.

Simplify maintenance.

Improve developer productivity.

---

# Shared Library Principles

Shared contains only infrastructure.

Business logic NEVER belongs here.

Domain rules NEVER belong here.

Policies NEVER belong here.

PII detection NEVER belongs here.

Prompt processing NEVER belongs here.

Tokenization NEVER belongs here.

LLM logic NEVER belongs here.

Shared is technology-focused.

Services are business-focused.

---

# Directory Structure

shared/

authentication/

authorization/

azure/

configuration/

constants/

database/

events/

exceptions/

logging/

messaging/

middleware/

monitoring/

schemas/

security/

telemetry/

utilities/

validation/

---

# Module Responsibilities

## authentication/

Purpose

Authentication framework.

Contains

JWT validation

OAuth2 helpers

Entra ID integration

Authentication middleware

Token parsing

Claims extraction

Forbidden

Authorization logic

Business roles

Permissions

---

## authorization/

Purpose

Authorization framework.

Contains

Permission evaluation

Role evaluation

Policy decorators

Authorization middleware

Forbidden

Business policies

Domain permissions

---

## azure/

Purpose

Azure SDK wrappers.

Contains

Key Vault client

Blob Storage client

Service Bus client

Event Grid client

Application Insights client

Azure OpenAI client

Document Intelligence client

Graph API client

Rules

Every Azure SDK wrapper must expose an interface.

No service uses SDKs directly.

---

## configuration/

Purpose

Centralized configuration.

Contains

Settings

Environment loading

Secret loading

Configuration validation

Configuration caching

Rules

Configuration is immutable after startup.

Secrets always come from Azure Key Vault in production.

---

## constants/

Purpose

Global constants.

Contains

HTTP constants

Header names

Media types

Event names

Configuration keys

Environment names

Never place business constants here.

---

## database/

Purpose

Database infrastructure.

Contains

Database session factory

Connection pooling

Transaction helpers

Base model

Repository interfaces

Migration helpers

Health checks

Forbidden

Business repositories

Queries

Domain models

---

## events/

Purpose

Shared event definitions.

Contains

Base event

Event envelope

Metadata

Correlation ID

Trace ID

Serialization

Versioning

Forbidden

Business events

---

## exceptions/

Purpose

Exception hierarchy.

Contains

BaseException

ValidationException

ConfigurationException

AuthenticationException

AuthorizationException

DatabaseException

AzureException

SerializationException

HTTPException wrappers

Global exception handlers

---

## logging/

Purpose

Enterprise logging.

Contains

JSON logger

Logger factory

Correlation ID

Structured logging

Log enrichment

Request logging

Performance logging

Rules

Every service uses the same logger.

---

## messaging/

Purpose

Messaging abstraction.

Contains

Publisher

Subscriber

Queue abstraction

Topic abstraction

Retry helpers

Dead Letter helpers

Serialization

Forbidden

Business workflows

---

## middleware/

Purpose

Shared middleware.

Contains

Request logging

Correlation ID

Trace ID

Timing

Authentication

Request validation

Response headers

Compression

Rate limiting

---

## monitoring/

Purpose

Monitoring helpers.

Contains

Health checks

Readiness

Liveness

Metrics registration

Diagnostic utilities

---

## schemas/

Purpose

Shared DTOs.

Contains

Pagination

Problem Details

Error responses

Success responses

Health responses

Audit metadata

Request metadata

Response metadata

Forbidden

Business DTOs

---

## security/

Purpose

Security utilities.

Contains

Encryption

Hashing

AES

Key management

Random generators

Secure comparison

Forbidden

Business security decisions

---

## telemetry/

Purpose

Observability.

Contains

OpenTelemetry

Metrics

Tracing

Instrumentation

Azure Monitor integration

Application Insights integration

---

## utilities/

Purpose

General utilities.

Contains

Date utilities

UUID helpers

JSON helpers

File helpers

String helpers

Collection helpers

Retry helpers

Clock abstraction

---

## validation/

Purpose

Reusable validators.

Contains

Email validation

UUID validation

Date validation

Header validation

Pagination validation

Common request validation

Forbidden

Business validation

PII validation

Policy validation

---

# Dependency Rules

Shared modules may depend on

Python standard library

Third-party infrastructure libraries

Other shared modules

Shared modules may NEVER depend on

Any service

Any business logic

Any domain model

Frontend

---

# Dependency Graph

configuration

↓

logging

↓

telemetry

↓

database

↓

middleware

↓

authentication

↓

authorization

↓

messaging

↓

utilities

Services depend on shared.

Shared never depends on services.

---

# Versioning

Shared follows Semantic Versioning.

Breaking changes require major versions.

Every service must pin compatible versions.

---

# Testing

Every shared module includes

Unit tests

Integration tests where applicable

Performance tests for critical modules

Static analysis

Security scanning

---

# Documentation

Every shared module contains

README

Public API documentation

Usage examples

Configuration guide

---

# Performance

Shared libraries must

Avoid unnecessary allocations

Be thread-safe where required

Support asynchronous execution

Minimize startup time

Avoid global mutable state

---

# Security

Every shared component must

Support secure defaults

Never expose secrets

Validate inputs

Produce structured logs

Emit telemetry

Use least privilege

---

# Forbidden

The shared library must NEVER contain

Business logic

PII detection

Classification

Policy evaluation

Tokenization

Prompt Firewall logic

LLM routing

OCR

Audit business rules

Notification logic

Feedback logic

Any domain-specific implementation

---

# Success Criteria

The shared library is successful when

Infrastructure code is never duplicated.

Business logic remains inside services.

Every service shares common infrastructure.

Every module is independently testable.

Services remain loosely coupled.

---

End of Document
