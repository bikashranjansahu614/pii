# Enterprise AI Trust Gateway

# Repository Structure

Version: 1.0

Status: FINAL

Classification: PERMANENT

---

# Purpose

This document defines the permanent repository structure for the Enterprise AI Trust Gateway.

Every AI agent must follow this structure.

No folder may be renamed.

No folder may be relocated.

No new top-level folder may be created unless explicitly approved.

---

# Repository Strategy

The project follows a MONOREPO architecture.

Repository Name

enterprise-ai-trust-gateway

The repository contains all services, frontend applications, shared libraries, infrastructure, documentation, and AI context.

Services remain independently deployable.

Each service owns its own lifecycle.

---

# Root Structure

enterprise-ai-trust-gateway/

├── AI_CONTEXT/
├── TASKS/
├── services/
├── shared/
├── frontend/
├── infrastructure/
├── database/
├── docs/
├── tests/
├── scripts/
├── configs/
├── tools/
├── .github/
├── .devcontainer/
├── .vscode/
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
└── .editorconfig

---

# AI_CONTEXT

Purpose

Permanent project knowledge.

Contains

Architecture

Coding standards

Security

Technology

Repository rules

Development workflow

AI agents always read this first.

---

# TASKS

Purpose

Implementation roadmap.

One markdown file per implementation task.

Example

TASK-0001.md

TASK-0002.md

TASK-0003.md

Tasks are immutable after completion.

---

# services/

Contains every backend microservice.

Each service is independently deployable.

Each service has its own

API

Database

Tests

Dockerfile

Documentation

Deployment

Configuration

---

# Service List

services/

email-agent/

document-agent/

ocr-service/

pii-engine/

classification-engine/

policy-engine/

tokenization-service/

token-vault/

llm-gateway/

prompt-firewall/

response-validator/

rehydration-service/

audit-service/

dashboard-api/

feedback-service/

notification-service/

---

# Standard Service Structure

service-name/

src/

api/

routers/

dependencies/

middleware/

core/

config/

logging/

security/

models/

schemas/

repositories/

services/

clients/

events/

workers/

database/

migrations/

tests/

unit/

integration/

contract/

performance/

docs/

deploy/

Dockerfile

requirements.txt

README.md

.env.example

---

# shared/

Purpose

Reusable infrastructure.

Contains

authentication/

authorization/

configuration/

database/

logging/

middleware/

exceptions/

events/

messaging/

schemas/

telemetry/

validation/

security/

constants/

utilities/

azure/

No business logic belongs here.

---

# frontend/

Purpose

React applications.

Structure

frontend/

apps/

executive-dashboard/

operations-dashboard/

security-dashboard/

governance-dashboard/

privacy-dashboard/

analytics-dashboard/

shared-ui/

Each application is independently buildable.

Shared components reside in shared-ui.

---

# infrastructure/

Purpose

Infrastructure as Code.

Contains

docker/

helm/

kubernetes/

terraform/

azure/

azure-devops/

monitoring/

grafana/

prometheus/

scripts/

Infrastructure changes occur only here.

---

# database/

Purpose

Shared database assets.

Contains

schemas/

migrations/

functions/

views/

indexes/

seeds/

Only database artifacts belong here.

---

# docs/

Purpose

Project documentation.

Contains

architecture/

api/

deployment/

operations/

security/

developer-guide/

user-guide/

adr/

diagrams/

hackathon/

---

# tests/

Purpose

Cross-service testing.

Contains

unit/

integration/

contract/

performance/

security/

e2e/

Each service also maintains its own local tests.

---

# scripts/

Purpose

Automation.

Contains

Build scripts

Deployment scripts

Migration scripts

Utility scripts

Development tools

No business logic.

---

# configs/

Purpose

Shared configuration.

Contains

Environment templates

Feature flags

Application settings

Shared configuration files

---

# tools/

Purpose

Developer tooling.

Contains

Code generators

Migration utilities

Formatting tools

Validation tools

Documentation generators

---

# Repository Rules

There is exactly one Git repository.

No nested Git repositories.

No duplicated shared code.

Business logic never belongs in shared.

Services never access another service database.

Shared libraries never depend on services.

Frontend never accesses databases directly.

Infrastructure never contains application code.

Documentation never contains implementation.

AI_CONTEXT is always the source of truth.

---

# Dependency Direction

AI_CONTEXT

↓

Shared

↓

Services

↓

Frontend

Infrastructure supports every layer.

Documentation describes every layer.

Tests validate every layer.

---

# Build Order

Shared

↓

Infrastructure

↓

Services

↓

Frontend

↓

System Tests

---

# File Naming

Folders

kebab-case

Python

snake_case.py

TypeScript

PascalCase.tsx

Environment

UPPER_SNAKE_CASE

Docker

Dockerfile

Helm

Chart.yaml

Terraform

snake_case.tf

Documentation

UPPERCASE_WITH_UNDERSCORES.md

---

# Repository Principles

Single Source of Truth

Convention over Configuration

Independent Deployability

Infrastructure as Code

Documentation First

Security by Default

Automation First

Testability

Maintainability

Scalability

---

# Success Criteria

The repository is considered valid when

Every service follows the standard layout.

Every developer can locate files immediately.

AI agents never invent folder structures.

Infrastructure remains isolated.

Business logic remains isolated.

Shared code remains reusable.

Repository remains consistent.

---

End of Document
