# Local File Organizer (Qwen AI Edition) 🚀

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-qwen3.5:2b-black.svg)](https://ollama.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-brightgreen.svg)](#)

A smart, **100% offline, privacy-first desktop and file organizer** powered by local AI (**Qwen 3.5 2B via Ollama**). Clean up your desktop and messy directories instantly with zero cloud dependencies and zero data leaks.

---

## 🌟 Overview

Tired of desktop clutter and messy download folders? **Local File Organizer** categorizes, renames, and organizes your files into intuitive directories.

- **Dual-Engine Organization:** Choose between lightning-fast **Rule-Based Fast Mode** (instant categorization by file type) and **AI Semantic Mode** (deep document understanding via local LLM).
- **100% Privacy & Zero Cloud Dependency:** Powered entirely on your local machine using **Ollama** and **Qwen 3.5 (2B)**. No files or metadata ever leave your computer.
- **Fail-Safe Operation:** Atomic staging (`.part`), SHA-256 integrity verification, and instant **One-Click Undo** rollback ensure your files are always safe.

---

## 📸 Workflow Preview

### Before: Cluttered Workspace
```text
Desktop/
├── 1.xlsx
├── 12222_777.docx
├── BS.txt
├── IMG_0967.PNG
├── go_bruin.pptx
├── logo.png
├── paper_1col.pdf
├── financial_report.csv
└── project_notes.md
```

### After: Organized & Categorized
```text
Desktop/Organized/
├── financial_and_banking/
│   ├── doc_BS.txt
│   └── doc_financial_report.csv
├── research_papers/
│   └── doc_paper_1col.pdf
├── presentations/
│   └── doc_go_bruin.pptx
├── image_assets/
│   ├── img_logo.png
│   └── img_IMG_0967.PNG
└── office_documents/
    ├── doc_12222_777.docx
    └── doc_project_notes.md
```

---

## ✨ Features

- **⚡ Dual Sorting Engines:**
  - **Fast Rule-Based Mode:** Sorts hundreds of files in milliseconds based on MIME categories and extensions.
  - **AI Semantic Mode:** Uses local `qwen3.5:2b` to read document excerpts and create contextual folders based on actual content.
- **🛠️ Self-Healing Service Detection:** Automatically verifies whether Ollama is running and automatically starts the service in the background if needed. Live UI status badge (`🟢 AI Ready` / `🟡 Starting...` / `🔴 Ollama Missing`).
- **🎨 Dark & Light Theme:** Clean, modern interface supporting instant theme switching.
- **🌐 Bilingual UI:** Full support for both **English** and **Turkish (Türkçe)** with live in-place language switching.
- **🛡️ Data Safety & Rollback:**
  - Moves files with atomic staging and SHA-256 checksum checks.
  - Full Undo logging: Revert any organization action with a single click.
- **🐧 Cross-Platform Ready:**
  - **Windows:** Standalone single executable (`Desktop-Organizer.exe`) — no Python setup required.
  - **Linux:** Native runner (`run_linux.sh`) with automatic environment and dependency management.

---

## 💻 Hardware Requirements

| Component | Minimum (CPU Inference) | Recommended (GPU Accelerated) |
| :--- | :--- | :--- |
| **Processor (CPU)** | 4 Cores (Intel 8th Gen+ / AMD Ryzen 3000+) | 6+ Cores (Intel 11th Gen+ / AMD Ryzen 5000+) |
| **Memory (RAM)** | 8 GB DDR4 | 16 GB DDR4/DDR5 |
| **Graphics (GPU)** | Integrated Graphics (Intel UHD/Iris Xe, AMD Vega) | Dedicated GPU (NVIDIA GTX 1650+ / RTX, AMD RX 6000+) |
| **AI Processing Time** | ~20–45 sec / document | ~3–8 sec / document |
| **Storage** | 3 GB free disk space (for Ollama model) | 3 GB free disk space |

> *Note: Fast Mode has no AI overhead and runs instantly on any hardware.*

---

## 🚀 Quick Start (Pre-Built Release)

### 🪟 Windows:
1. Download `Local-File-Organizer-v1.0.0.zip` from [Releases](https://github.com/ihsan896/Local-File-Organizer-Qwen-Ai-version-/releases).
2. Extract the archive.
3. *(Optional for AI Mode)* Install [Ollama](https://ollama.com) and pull the model:
   ```bash
   ollama pull qwen3.5:2b
   ```
4. Double-click `Desktop-Organizer.exe` to run.

### 🐧 Linux:
1. Download and extract `Local-File-Organizer-v1.0.0.zip`.
2. Open terminal and run:
   ```bash
   chmod +x run_linux.sh
   ./run_linux.sh
   ```
   *(The script checks required dependencies like `python3-tk` and launches the GUI).*

---

## 🛠️ Run from Source (Developers)

```bash
# 1. Clone repository
git clone https://github.com/ihsan896/Local-File-Organizer-Qwen-Ai-version-.git
cd Local-File-Organizer-Qwen-Ai-version-

# 2. Create virtual environment
python -m venv venv

# Windows activate:
.\venv\Scripts\Activate.ps1
# Linux activate:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull local model
ollama pull qwen3.5:2b

# 5. Launch GUI or CLI
python gui.py       # GUI mode
python main.py      # Interactive CLI mode
```

---

## 📂 Supported File Types

- **Documents & Text:** `.pdf`, `.docx`, `.txt`, `.md`
- **Spreadsheets & Data:** `.xlsx`, `.xls`, `.csv`
- **Presentations:** `.pptx`, `.ppt`
- **Images:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`

---

## 🤝 Attribution & Acknowledgements

- **Maintained & Enhanced by:** [Ihsan-AI](https://github.com/ihsan896)
- **Upstream Project:** Forked and enhanced from [QiuYannnn/Local-File-Organizer](https://github.com/QiuYannnn/Local-File-Organizer) (MIT License). Upgraded from legacy Nexa SDK to local Ollama inference, cross-platform packaging, bilingual GUI, and modern dark theme.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Copyright (c) 2026 Ihsan-AI. All rights reserved.  
Original codebase copyright (c) 2024 Yanhao Qiu. See [NOTICE.md](NOTICE.md) for details.
