# Enterprise AI Trust Gateway

# Technology & Coding Standards

Version: 1.0

Status: FINAL

Classification: PERMANENT

---

# Purpose

This document defines the mandatory technology stack, engineering principles, coding conventions, dependency rules, testing standards and code quality requirements.

Every generated source file must comply.

These standards are immutable unless explicitly changed by project architects.

---

# Approved Technology Stack

## Backend

Language

Python 3.12

Framework

FastAPI

Validation

Pydantic v2

ORM

SQLAlchemy 2.x

Database Migration

Alembic

Dependency Management

Poetry

Testing

pytest

pytest-asyncio

pytest-cov

Linting

Ruff

Formatting

Black

Type Checking

mypy

---

## Frontend

React 19

TypeScript

Vite

Material UI

React Router

TanStack Query

React Hook Form

Zod

Axios

ESLint

Prettier

Vitest

---

## Database

PostgreSQL

Redis

Azure Storage

---

## Cloud

Microsoft Azure

Azure OpenAI

Azure AI Document Intelligence

Azure Key Vault

Azure Service Bus

Azure Event Grid

Microsoft Graph API

Azure Monitor

Application Insights

Microsoft Entra ID

---

## Infrastructure

Docker

Docker Compose

Kubernetes

Helm

Terraform

Azure DevOps Pipelines

---

# Clean Architecture

Every service follows

Presentation Layer

↓

Application Layer

↓

Domain Layer

↓

Infrastructure Layer

Dependencies always point inward.

---

# SOLID Principles

Every implementation must follow

Single Responsibility

Open/Closed

Liskov Substitution

Interface Segregation

Dependency Inversion

---

# Repository Pattern

Repositories

Only access persistence.

Never contain business logic.

Only return domain entities or DTOs.

---

# Service Layer

Business logic belongs only in

/services

Never inside

Routes

Repositories

Schemas

Models

Middleware

---

# API Layer

Routes must

Validate requests

Call services

Return responses

Handle HTTP concerns only

Never implement business rules.

---

# DTO Rules

Request DTO

Response DTO

Internal DTO

Event DTO

Audit DTO

DTOs must be immutable whenever possible.

---

# Pydantic Standards

Always use

BaseModel

Field()

Annotated

ConfigDict

Strict typing

Never use

dict

Any

Untyped payloads

---

# Type Safety

Mandatory

Type hints

Return types

Generic typing

Protocols where appropriate

Avoid

typing.Any

Dynamic typing

---

# Async Rules

All I/O operations

Must be async.

Examples

Database

Redis

Azure

HTTP

Messaging

Filesystem

Never block the event loop.

---

# Error Handling

Every service must implement

Domain exceptions

Validation exceptions

Infrastructure exceptions

HTTP exception mapping

Global exception middleware

Never expose

Stack traces

Internal errors

Secrets

---

# Logging

Use structured JSON logging.

Every log contains

timestamp

level

service

environment

correlation_id

trace_id

request_id

user_id (if available)

message

exception (if present)

---

# Configuration

Configuration is immutable.

Load once at startup.

Validation is mandatory.

Environment variables only.

Production secrets

Azure Key Vault.

---

# Naming Standards

Python

Files

snake_case.py

Functions

snake_case

Variables

snake_case

Classes

PascalCase

Constants

UPPER_SNAKE_CASE

Private methods

_prefix

---

# API Naming

URLs

/api/v1/

Use kebab-case.

Example

/api/v1/document-processing

---

# Database Naming

Schemas

snake_case

Tables

snake_case_plural

Columns

snake_case

Indexes

idx_table_column

Constraints

pk_

fk_

uq_

---

# Comments

Explain WHY.

Never explain WHAT.

Avoid redundant comments.

Prefer expressive code.

---

# Docstrings

Every public class

Every public function

Every API

Every shared module

Must include

Purpose

Parameters

Returns

Raises

Examples (when appropriate)

Google Style.

---

# Imports

Order

1 Standard Library

2 Third-party

3 Shared Library

4 Local Application

No wildcard imports.

---

# Dependency Rules

Allowed

Application

↓

Domain

↓

Infrastructure

Forbidden

Infrastructure

↓

Presentation

Routes

↓

Repositories

Repositories

↓

Routes

---

# Testing Standards

Minimum

90% coverage

Every service includes

Unit Tests

Integration Tests

Contract Tests

Performance Tests (critical paths)

Security Tests (critical modules)

---

# Code Quality Gates

Before merge

Black

Ruff

mypy

pytest

OpenAPI generation

Security scan

Dependency scan

---

# Performance Standards

Async everywhere

Connection pooling

Batch operations

Pagination

Streaming for large files

Avoid N+1 queries

No SELECT *

---

# Security Standards

Input validation

Output encoding

Parameterized queries

JWT validation

TLS only

Secrets from Key Vault

No plaintext credentials

No secrets in logs

---

# Forbidden Practices

No global mutable state

No business logic in routes

No business logic in middleware

No direct SQL in routes

No duplicated utilities

No hardcoded URLs

No hardcoded credentials

No TODOs

No placeholder implementations

No commented-out code

---

# Definition of Production Ready

A feature is production-ready only if it

Compiles

Passes all tests

Has documentation

Has OpenAPI

Has Docker support

Has Helm manifests

Has health endpoints

Has telemetry

Has logging

Has security validation

Has configuration

Has CI validation

---

# Success Criteria

The coding standards are successful when

Every service looks consistent.

Every developer follows the same patterns.

AI-generated code is indistinguishable from human-written enterprise code.

Code remains maintainable, testable and secure.

---

End of Document
