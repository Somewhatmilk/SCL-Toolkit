# SCL-Momentum

**An SCL project** — a prototype AI chatbot built during the Operations & Automation internship at
[SCL System Enterprise Pte Ltd](https://www.sclsystem.com.sg/).

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python Version](https://img.shields.io/badge/Python-3.10.13-green.svg)](https://shields.io/)
[![Windows OS](https://img.shields.io/badge/Win_OS-11_(22H2)-green.svg)](https://shields.io/)
[![Mac OS](https://img.shields.io/badge/Mac_OS-Sonoma_14.2_(M1)-green.svg)](https://shields.io/)

---

## About SCL System Enterprise

SCL System Enterprise Pte Ltd is a Singapore-based industrial and electrical equipment supplier
(founded 2000) that has grown from a distributor into an integrated solutions provider. It supports
contractors, manufacturers, and system integrators across South East Asia with:

- **Electrical & Automation Distribution** — components and solutions for power, control, and industrial automation
- **M&E & Automation Works** — electrical/mechanical works, system implementation, automation integration
- **IT & AV Infrastructure** — connected infrastructure for business communications and operations
- **Smart Systems & Operational Technology** — smart workplace, IoT, and alarm management

Serving data centres, commercial buildings, factories, logistics hubs, and government projects,
SCL's mission is to make industrial procurement fast, convenient, and easy. (Sources:
[SCL System website](https://www.sclsystem.com.sg/),
[LinkedIn](https://sg.linkedin.com/company/sclsystemsg))

## What this project is

**Momentum** is a prototype chatbot built with **Streamlit + LangChain** that explores how an
organisation like SCL could answer questions from its own documents using a local, private LLM
pipeline. It was a learning project: RAG (retrieval-augmented generation) over a document store
with a chat UI, running fully on local hardware.

The point was never production readiness — it was to prove the pipeline: ingest documents →
embed → retrieve → answer in a chat interface, entirely offline.

## Sequel / add-on: SCL-Toolkit

After the internship's automation work matured, the day-to-day utilities that grew out of the same
rotation were collected into a separate project:

👉 **[SCL-Toolkit](https://github.com/Somewhatmilk/SCL-Toolkit)** — the practical successor: a
generic contact-list formatter (CSV/JSON/XLSX → clean Excel), a PDF merger (GUI + CLI), and a
WhatsApp bulk sender with dry-run safety. Where Momentum proved the concept, SCL-Toolkit shipped
the tools.

## Getting Started

### Prerequisites

1. **Python** 3.10.13 or higher.
2. **Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Copy the example environment and fill in the values (secrets are **never committed** — see
[`.gitignore`](.gitignore)):

```bash
# .env
PERSIST_DIRECTORY=database
MODEL_TYPE=t5-small
MODEL_PATH=<your_model_path>
EMBEDDINGS_MODEL_NAME=<your_embeddings_model_name>
MODEL_N_CTX=1024
MODEL_N_BATCH=8
TOKEN=<your_token>
TARGET_SOURCE_CHUNKS=4
```

### Run

```bash
streamlit run chatbot.py
```

## Stack

- **Streamlit** — chat UI
- **LangChain** — RAG orchestration
- **transformers / torch** — local embeddings + generation (offline)
- **python-dotenv** — environment config

## License

AGPLv3 — see [LICENSE](LICENSE).
