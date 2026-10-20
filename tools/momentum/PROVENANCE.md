# PROVENANCE — SCL-Momentum files in this directory

Merged 2026-10-20 into SCL-Toolkit on branch `merge-momentum` (local only, not pushed).

## Source
- Repo: https://github.com/Somewhatmilk/SCL-Momentum
- Local: C:/Users/somew/repos/SCL-Momentum (untouched — this was a COPY, not a move)
- Source commit: 6a7c65c ("Reframe as SCL project (SCL-Momentum); link SCL-Toolkit as sequel")
- Source branch: main (clean at merge time)

## File mapping (7 tracked files, all present here)
| Source file | Destination | Note |
|---|---|---|
| chatbot.py | chatbot.py | byte-identical |
| Excel Data.py | excel_data.py | renamed: space in filename breaks CLI invocation; byte-identical otherwise |
| config.toml | config.toml | byte-identical; inert at this path (Streamlit loads .streamlit/config.toml) |
| README.md | README.md | original, preserved verbatim |
| LICENSE | LICENSE | AGPLv3 — SCL-Toolkit root LICENSE is GPLv3; both retained alongside their code |
| requirements.txt | requirements.txt | original, for provenance; merged set lives at repo root |
| .gitignore | .gitignore | original, for provenance |

## Not copied
- `secrets.toml`, `.env` — present in the source working tree but git-ignored there
  (verified `git check-ignore`). Never committed, content not touched. Both patterns are
  now added to SCL-Toolkit root .gitignore.
- Anything untracked in the source repo.

## Known status of chatbot.py
Non-runnable prototype as merged: imports `constants.CHROMA_SETTINGS` (constants.py absent
from the source repo), loads google/flan-t5-xxl (~22 GB) at import time, and misuses the
transformers API (`T5ForConditionalGeneration(model_path=..., n_ctx=..., ...)` — those are
LangChain-LLM-style kwargs, not transformers kwargs). Documented in the source README as a
learning/RAG-prototype project, not production code.