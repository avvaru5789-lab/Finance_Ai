# AI Financial Coach - Developer Guide

> **Purpose:** This guide helps you understand the project structure, navigate folders, understand data flow, and know exactly where to make changes for different tasks.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Complete Folder Structure](#complete-folder-structure)
3. [Data Flow Architecture](#data-flow-architecture)
4. [Folder-by-Folder Guide](#folder-by-folder-guide)
5. [How to Navigate for Common Tasks](#how-to-navigate-for-common-tasks)
6. [Understanding Dependencies](#understanding-dependencies)
7. [Development Workflow](#development-workflow)

---

## Project Overview

This is a **production-grade multi-agent AI system** that:
- Accepts bank statements (PDF/CSV)
- Extracts financial data using DeepSeek-OCR
- Runs parallel AI agent analysis via LangGraph
- Produces structured financial strategies

**Key Principle:** Separation of concerns
- **Tools** = Deterministic logic (math, parsing)
- **Agents** = AI reasoning (strategy, insights)
- **Backend** = API orchestration
- **Frontend** = User interface

---

## Complete Folder Structure

```
Finance_AI/
│
├── 📁 frontend/                    # React UI - All user-facing components
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   ├── pages/                 # Main application pages
│   │   ├── services/              # API communication
│   │   ├── visualizations/        # Charts & graphs
│   │   ├── hooks/                 # Custom React hooks
│   │   └── utils/                 # Helper functions
│   └── package.json
│
├── 📁 backend/                     # FastAPI Server - API Layer
│   ├── app.py                     # Main FastAPI application
│   ├── routes/                    # API endpoints
│   ├── controllers/               # Business logic
│   ├── schemas/                   # Data validation (Pydantic)
│   ├── middleware/                # Request/response handling
│   └── config/                    # Settings & database
│
├── 📁 agents/                      # AI Agents - Business Logic
│   ├── orchestrator_agent.py     # Master coordinator
│   ├── debt_analyzer_agent.py    # Debt strategy
│   ├── savings_strategy_agent.py # Savings planning
│   ├── budget_optimizer_agent.py # Budget recommendations
│   ├── risk_scoring_agent.py     # Financial health score
│   ├── scenario_simulation_agent.py # What-if analysis
│   └── base_agent.py              # Shared agent utilities
│
├── 📁 tools/                       # Deterministic Tools - No AI
│   ├── ocr_engine.py              # DeepSeek-OCR wrapper
│   ├── table_extractor.py         # Parse OCR into tables
│   ├── transaction_categorizer.py # Rule-based categorization
│   ├── financial_metrics_engine.py # Calculate ratios/metrics
│   └── validation_engine.py       # Data validation
│
├── 📁 langgraph/                   # LangGraph Orchestration
│   ├── graph_definition.py        # Graph structure & routing
│   ├── node_definitions.py        # Agent node wrappers
│   └── state_schema.py            # Shared state schema
│
├── 📁 models/                      # Model Management
│   ├── model_policy.py            # LLM routing logic
│   └── deepseek_loader.py         # Load DeepSeek-OCR
│
├── 📁 data/                        # Data Storage
│   ├── demo_statements/           # Sample PDFs for testing
│   └── processed/                 # Cached analysis results
│
├── 📁 tests/                       # Automated Tests
│   ├── test_tools.py              # Test deterministic tools
│   ├── test_agents.py             # Test agent outputs
│   └── test_api.py                # Test API endpoints
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env                         # Environment variables
├── 📄 README.md                    # Project overview
└── 📄 DEVELOPER_GUIDE.md          # This file
```

---

## Data Flow Architecture

### End-to-End Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER UPLOADS PDF                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                             │
│  FileUpload.jsx → sends file to backend                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│  POST /api/upload → receives file                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TOOLS LAYER (Deterministic)                  │
│  1. ocr_engine.py → Extract text from PDF                       │
│  2. table_extractor.py → Parse transactions                     │
│  3. transaction_categorizer.py → Categorize spending            │
│  4. financial_metrics_engine.py → Calculate metrics             │
│  5. validation_engine.py → Validate data completeness           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                  ┌──────────────────┐
                  │ FinancialState   │  (Structured JSON)
                  └────────┬─────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  LANGGRAPH ORCHESTRATION                        │
│  graph_definition.py → Executes multi-agent workflow            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
              ┌──────────────┴──────────────┐
              │   PARALLEL AGENT EXECUTION  │
              ▼                             ▼
    ┌──────────────────┐        ┌──────────────────┐
    │ Debt Analyzer    │        │ Savings Strategy │
    └────────┬─────────┘        └────────┬─────────┘
              ▼                             ▼
    ┌──────────────────┐        ┌──────────────────┐
    │ Budget Optimizer │        │ Risk Scoring     │
    └────────┬─────────┘        └────────┬─────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                  ┌──────────────────┐
                  │  Aggregator      │
                  │  (Orchestrator)  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Scenario         │
                  │ Simulation       │
                  └────────┬─────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FINAL JSON OUTPUT                            │
│  {                                                              │
│    "executive_summary": "...",                                  │
│    "financial_health_score": {...},                             │
│    "debt_strategy": {...},                                      │
│    "savings_plan": {...},                                       │
│    "budget_optimization": {...}                                 │
│  }                                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MONGODB ATLAS                                │
│  Store analysis result for history                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│  Returns JSON to frontend                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                             │
│  Dashboard.jsx → Renders visualizations                         │
│  HealthGauge.jsx → Shows financial score                        │
│  DebtStrategy.jsx → Shows debt payoff plan                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Folder-by-Folder Guide

### 📁 `tools/` - The Deterministic Layer

> **Purpose:** Handle all non-AI tasks (math, parsing, categorization)
> 
> **When to work here:** Adding new metrics, improving OCR, new categorization rules

#### Files:

**`ocr_engine.py`**
- **What it does:** Loads DeepSeek-OCR model and extracts text from PDFs
- **Key functions:**
  - `load_deepseek_ocr()` - Initialize model
  - `extract_from_pdf(pdf_path)` - OCR entire document
  - `extract_tables(pdf_path)` - Detect tables
- **Dependencies:** `transformers`, `torch`, `pdf2image`
- **When to modify:** If OCR accuracy is poor, or you want to optimize model loading

---

**`table_extractor.py`**
- **What it does:** Converts raw OCR text into structured transaction tables
- **Key functions:**
  - `parse_transaction_table(ocr_output)` - Identify columns (date, description, amount)
  - `normalize_dates(date_str)` - Handle different date formats
  - `extract_amounts(text)` - Parse currency values
- **When to modify:** If transaction parsing fails for certain bank formats

---

**`transaction_categorizer.py`**
- **What it does:** Rule-based categorization (NO AI)
- **Categories:** Housing, Utilities, Food, Transportation, Entertainment, etc.
- **Logic:** Keyword matching (e.g., "Netflix" → Subscriptions)
- **When to modify:** Adding new categories or improving accuracy

---

**`financial_metrics_engine.py`**
- **What it does:** Calculates all financial ratios and metrics
- **Key metrics:**
  - Cash flow, savings rate, debt-to-income ratio
  - Liquidity ratio, expense volatility
- **IMPORTANT:** All calculations are deterministic (no LLM calls)
- **When to modify:** Adding new financial metrics or ratios

---

**`validation_engine.py`**
- **What it does:** Validates data completeness and consistency
- **Checks:**
  - Schema compliance (all required fields present)
  - Mathematical consistency (debits = credits)
  - Range checks (savings rate 0-100%)
  - Agent output conflicts
- **When to modify:** Adding new validation rules

---

### 📁 `agents/` - The AI Reasoning Layer

> **Purpose:** AI-powered financial strategy and insights
>
> **When to work here:** Changing recommendations, improving strategies, adding new analysis types

#### Files:

**`base_agent.py`**
- **What it does:** Shared utilities for all agents
- **Includes:**
  - OpenRouter API setup
  - Prompt templates
  - Response parsing
  - Error handling
- **When to modify:** Changing LLM provider or adding shared agent logic

---

**`orchestrator_agent.py`**
- **What it does:** Master coordinator - validates state, delegates to sub-agents, aggregates results
- **Flow:**
  1. Validate `FinancialState` is complete
  2. Trigger parallel agent execution
  3. Collect outputs
  4. Detect conflicts between agents
  5. Generate executive summary
- **When to modify:** Changing orchestration logic or adding new agents to the graph

---

**`debt_analyzer_agent.py`**
- **What it does:** Analyzes debt and recommends payoff strategy
- **Input:** Debt accounts, interest rates, minimum payments, available cash flow
- **Output:**
  - Strategy (avalanche vs snowball)
  - Payoff schedule
  - Interest saved
  - Debt-free date
- **When to modify:** Improving debt strategy recommendations

---

**`savings_strategy_agent.py`**
- **What it does:** Recommends savings allocation
- **Output:**
  - Emergency fund target
  - Monthly savings amount
  - Allocation (emergency/short-term/long-term)
  - Timeline to goals
- **When to modify:** Changing savings strategy logic

---

**`budget_optimizer_agent.py`**
- **What it does:** Finds budget inefficiencies and suggests optimizations
- **Output:**
  - Recommended budget by category
  - Reduction opportunities
  - Subscription audit
  - Potential savings
- **When to modify:** Improving budget recommendations

---

**`risk_scoring_agent.py`**
- **What it does:** Calculates financial health score (0-100)
- **Factors:**
  - Emergency fund coverage
  - Debt-to-income ratio
  - Expense volatility
  - Liquidity
  - Savings rate
- **Output:** Score + risk level + explanation + risk flags
- **When to modify:** Adjusting scoring algorithm

---

**`scenario_simulation_agent.py`**
- **What it does:** Simulates financial scenarios (income loss, expense cuts, etc.)
- **Scenarios:**
  - Income loss (3 months)
  - 10% expense reduction
  - Debt consolidation
  - Extra debt payments
- **When to modify:** Adding new scenarios

---

### 📁 `langgraph/` - The Orchestration Layer

> **Purpose:** Defines how agents work together in parallel
>
> **When to work here:** Changing agent execution order, adding new agents, modifying state

#### Files:

**`state_schema.py`**
- **What it does:** Defines the shared state schema used by all agents
- **Contains:**
  - `FinancialState` TypedDict
  - All input data (transactions, debts, income, expenses)
  - All calculated metrics
  - All agent outputs
- **IMPORTANT:** This is the "contract" between all components
- **When to modify:** Adding new fields that agents need to access

---

**`node_definitions.py`**
- **What it does:** Wraps each agent as a LangGraph node
- **Example:**
  ```python
  def debt_analyzer_node(state: FinancialState) -> FinancialState:
      result = debt_analyzer_agent.analyze(state)
      state["debt_strategy"] = result
      return state
  ```
- **When to modify:** Adding new agent nodes

---

**`graph_definition.py`**
- **What it does:** Defines the execution graph
- **Structure:**
  ```
  START → Orchestrator → [Parallel Agents] → Aggregator → Scenario → END
  ```
- **Key features:**
  - Parallel execution for independent agents
  - Error handling per node
  - Graceful degradation
- **When to modify:** Changing execution flow or adding conditional routing

---

### 📁 `backend/` - The API Layer

> **Purpose:** REST API for frontend communication
>
> **When to work here:** Adding new endpoints, changing request/response formats

#### Files:

**`app.py`**
- **What it does:** Main FastAPI application entry point
- **Includes:**
  - CORS middleware
  - Route registration
  - Health check endpoint
- **When to modify:** Adding global middleware or configuration

---

**`routes/upload.py`**
- **Endpoint:** `POST /api/upload`
- **What it does:**
  1. Accepts PDF/CSV file
  2. Triggers OCR extraction
  3. Parses and categorizes transactions
  4. Calculates metrics
  5. Returns `FinancialState` JSON
- **When to modify:** Changing upload logic or supported file types

---

**`routes/analysis.py`**
- **Endpoint:** `POST /api/analyze`
- **What it does:**
  1. Accepts `FinancialState` JSON
  2. Triggers LangGraph orchestration
  3. Returns final analysis JSON
  4. Stores in MongoDB
- **When to modify:** Changing analysis flow or output format

---

**`schemas/financial_schema.py`**
- **What it does:** Pydantic models for request/response validation
- **Models:**
  - `Transaction`
  - `DebtAccount`
  - `FinancialStateInput`
  - `AnalysisResponse`
- **When to modify:** Changing API contracts

---

**`config/database.py`**
- **What it does:** MongoDB Atlas connection setup
- **When to modify:** Changing database configuration

---

### 📁 `frontend/` - The User Interface

> **Purpose:** React-based UI for uploading statements and viewing analysis
>
> **When to work here:** UI changes, new visualizations, styling

#### Key Directories:

**`src/components/`**
- Reusable UI components
- **Key files:**
  - `FileUpload.jsx` - Drag & drop upload
  - `Dashboard.jsx` - Main analysis view
  - `HealthScore.jsx` - Financial health gauge
  - `DebtStrategy.jsx` - Debt payoff plan
  - `SavingsPlan.jsx` - Savings recommendations
  - `ScenarioSimulator.jsx` - Interactive what-if tool

---

**`src/services/api.js`**
- **What it does:** API communication layer
- **Functions:**
  - `uploadStatement(file)` - POST to `/api/upload`
  - `analyzeFinancials(state)` - POST to `/api/analyze`
- **When to modify:** Adding new API calls

---

**`src/visualizations/`**
- Chart components using Recharts or Chart.js
- **Examples:**
  - `CashFlowChart.jsx` - Income vs expenses over time
  - `DebtProjection.jsx` - Debt payoff timeline
  - `HealthGauge.jsx` - Radial gauge for health score

---

### 📁 `models/` - Model Management

**`model_policy.py`**
- **What it does:** Defines which LLM to use for each task
- **Logic:**
  - Cheap model → parsing
  - GPT-4o-mini → financial reasoning
- **When to modify:** Optimizing cost/performance trade-offs

---

**`deepseek_loader.py`**
- **What it does:** Downloads and loads DeepSeek-OCR model
- **When to modify:** Changing model path or version

---

### 📁 `data/` - Data Storage

**`demo_statements/`**
- Sample bank statements for testing
- **Add here:** Your test PDFs/CSVs

---

**`processed/`**
- Cached analysis results
- **Used for:** Avoiding re-processing the same file

---

## How to Navigate for Common Tasks

### Task: "I want to improve OCR accuracy"

**Navigate to:**
1. `tools/ocr_engine.py` - Adjust DeepSeek-OCR configuration
2. `tools/table_extractor.py` - Improve table parsing logic
3. Test with files in `data/demo_statements/`

---

### Task: "I want to add a new financial metric"

**Navigate to:**
1. `tools/financial_metrics_engine.py` - Add calculation function
2. `langgraph/state_schema.py` - Add field to `FinancialState`
3. `agents/` - Update agents to use the new metric
4. `frontend/src/components/Dashboard.jsx` - Display the metric

---

### Task: "I want to change debt strategy recommendations"

**Navigate to:**
1. `agents/debt_analyzer_agent.py` - Modify recommendation logic
2. `frontend/src/components/DebtStrategy.jsx` - Update UI display

---

### Task: "I want to add a new agent"

**Navigate to:**
1. `agents/` - Create new agent file (e.g., `investment_agent.py`)
2. `langgraph/node_definitions.py` - Create node wrapper
3. `langgraph/graph_definition.py` - Add to graph execution
4. `langgraph/state_schema.py` - Add output field
5. `backend/schemas/response_schema.py` - Update response schema
6. `frontend/src/components/Dashboard.jsx` - Display results

---

### Task: "I want to test the system end-to-end"

**Navigate to:**
1. `data/demo_statements/` - Add test PDF
2. `backend/app.py` - Start FastAPI server
3. `frontend/` - Start React dev server
4. Upload file through UI
5. Check MongoDB for stored results

---

## Understanding Dependencies

### Component Dependencies

```
Frontend
  └── depends on → Backend API
                    └── depends on → Tools + LangGraph
                                      ├── Tools
                                      │   └── depends on → DeepSeek-OCR model
                                      └── LangGraph
                                          └── depends on → Agents
                                                            └── depends on → OpenRouter API
```

### Execution Order

1. **Tools** (no dependencies - can run standalone)
2. **Agents** (depend on tools for data input)
3. **LangGraph** (orchestrates agents)
4. **Backend** (calls LangGraph)
5. **Frontend** (calls Backend)

---

## Development Workflow

### Phase 1: Build Tools First
**Why?** Tools have no dependencies and provide the foundation.

**Steps:**
1. Set up environment (`.env`, `requirements.txt`)
2. Download DeepSeek-OCR model
3. Build and test each tool individually
4. Validate with sample PDFs

**Validation:** `pytest tests/test_tools.py`

---

### Phase 2: Build Agents
**Why?** Agents depend on tools but not on each other.

**Steps:**
1. Define `FinancialState` schema
2. Build each agent independently
3. Test with mock financial data

**Validation:** `pytest tests/test_agents.py`

---

### Phase 3: Build LangGraph Orchestration
**Why?** Requires all agents to be functional.

**Steps:**
1. Define graph structure
2. Create node wrappers
3. Test parallel execution

**Validation:** Run graph with sample data

---

### Phase 4: Build Backend API
**Why?** Simple layer that calls LangGraph.

**Steps:**
1. Create FastAPI routes
2. Add file upload handling
3. Connect to MongoDB

**Validation:** `pytest tests/test_api.py`

---

### Phase 5: Build Frontend
**Why?** Final layer with no downstream dependencies.

**Steps:**
1. Build file upload component
2. Create dashboard
3. Add visualizations

**Validation:** Manual testing in browser

---

## Quick Reference: Where to Find Things

| What | Where |
|------|-------|
| **OCR Logic** | `tools/ocr_engine.py` |
| **Transaction Parsing** | `tools/table_extractor.py` |
| **Financial Calculations** | `tools/financial_metrics_engine.py` |
| **Debt Strategy** | `agents/debt_analyzer_agent.py` |
| **Savings Recommendations** | `agents/savings_strategy_agent.py` |
| **Health Score** | `agents/risk_scoring_agent.py` |
| **Agent Execution Flow** | `langgraph/graph_definition.py` |
| **Shared State Schema** | `langgraph/state_schema.py` |
| **API Endpoints** | `backend/routes/` |
| **File Upload** | `backend/routes/upload.py` |
| **Analysis Endpoint** | `backend/routes/analysis.py` |
| **UI Components** | `frontend/src/components/` |
| **API Calls** | `frontend/src/services/api.js` |
| **Charts** | `frontend/src/visualizations/` |
| **Environment Config** | `.env` |
| **Python Dependencies** | `requirements.txt` |
| **Database Setup** | `backend/config/database.py` |
| **LLM Configuration** | `models/model_policy.py` |
| **Test Files** | `data/demo_statements/` |

---

## Common Questions

### Q: Where do I start debugging if the system fails?

**A:** Follow the data flow:
1. Check `tools/ocr_engine.py` logs - Is OCR extracting text?
2. Check `tools/table_extractor.py` - Are transactions parsed?
3. Check `tools/validation_engine.py` - Is data valid?
4. Check `langgraph/graph_definition.py` logs - Are agents executing?
5. Check individual agent outputs - Are they returning valid JSON?

---

### Q: How do I add a new category for transactions?

**A:** 
1. Go to `tools/transaction_categorizer.py`
2. Add category to `CATEGORIES` dict
3. Add keywords to match the category

---

### Q: How do I change the financial health score calculation?

**A:**
1. Go to `agents/risk_scoring_agent.py`
2. Modify scoring logic in the agent's prompt or calculation
3. Test with sample data

---

### Q: How do I visualize a new metric in the UI?

**A:**
1. Ensure metric is in the final JSON output
2. Go to `frontend/src/components/Dashboard.jsx`
3. Add a new component to display the metric
4. (Optional) Create a new chart in `frontend/src/visualizations/`

---

## Summary

This guide provides a complete map of the project. Use it to:
- Understand what each folder/file does
- Navigate quickly to the right component
- Understand dependencies and execution flow
- Debug issues systematically

**Pro tip:** Bookmark this file and refer to it whenever you're unsure where to make changes!
