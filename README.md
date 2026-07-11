# ☸️ Drishti Chakra (By Team NexAura)
### *Autonomous Industrial R&D & Strategic Intelligence Engine*

[![AMD Instinct™ MI300X](https://img.shields.io/badge/Powered%20By-AMD%20Instinct%E2%84%A2%20MI300X-blue.svg)](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)
[![ROCm™ 6.x](https://img.shields.io/badge/ROCm%E2%84%A2-6.x-red.svg)](https://www.amd.com/en/graphics/servers-solutions-rocm)
[![Gemma-2-9b](https://img.shields.io/badge/Model-Gemma--2--9b-orange.svg)](https://huggingface.co/google/gemma-2-9b)
[![Fireworks AI](https://img.shields.io/badge/API-Fireworks%20AI-purple.svg)](https://fireworks.ai/)

---

## 1. Project Title
**Drishti Chakra (Drishti Apex): Autonomous Industrial R&D Engine**

---

## 2. Short Description (The "Billion-Dollar" Hook)
Drishti Chakra solves the **"$500 Billion Innovation Blindspot"** by utilizing **AMD Instinct™ MI300X GPUs** to perform 6 months of industrial R&D, patent auditing, and technical blueprinting in under 6 minutes.

---

## 3. Long Description (The Professional Pitch)
### The Problem
Global industrial R&D is currently manual, slow, and highly fragmented. This **"Innovation Blindspot"** causes up to 40% of deep-tech and industrial projects to fail due to missed prior-art patent risks, unviable material constraints, or unoptimized supply chains identified too late in the cycle.

### The Solution
**Drishti Chakra** is an autonomous agentic suite (consisting of **Shodh** [Research], **Manthan** [Synthesis], and **Parikshan** [Audit]) that crawls global scientific journals and patent databases to identify market gaps, generates structured engineering specifications, and audits intellectual property viability. For this hackathon, we demonstrated its capabilities on one of the most mathematically challenging physics topics: **Autonomous Anti-Gravity Propulsion Systems (Electrogravitics & Superconductor-based)**.

### The AMD Advantage
Drishti Chakra is custom-built for the **AMD ROCm 6.x** ecosystem. By leveraging the industry-leading **192GB HBM3 memory** and **5.3 TB/s bandwidth** of the **AMD Instinct™ MI300X** (via Fireworks AI), our model loads entire multi-patent corpuses and detailed engineering papers simultaneously without performance bottlenecks. Our **"Deep-Reach" logic** powered by **Gemma-2-9b** enables deep, recursive reasoning steps that ensure no critical engineering bottleneck or patent landmine is overlooked.

### Market Potential
Targeting a fraction of the global $500B enterprise R&D, compliance, and strategic management consulting market, Drishti Chakra functions as a **"Startup-in-a-Box"** for deep-tech founders and industrial pioneers.

---

## 5. How to Deploy and Test

### Prerequisites
- Docker & Docker-Compose installed.
- Fireworks AI API Key (from AMD AI Developer Program).

### Installation Steps

**1. Clone Repository:**
```bash
git clone https://github.com/nexaura-team/drishti-chakra.git
cd drishti-chakra
```

**2. Configure Environment:**
Create a `.env` file in the root directory:
```text
FIREWORKS_API_KEY=your_fireworks_api_key_here
```

**3. Build & Launch (Containerized):**
```bash
docker build -t drishti-chakra .
docker run -p 8501:8501 --env-file .env drishti-chakra
```

**4. Access Dashboard:**
Open `http://localhost:8501` in your browser.

---

### 🧪 Testing the "Unicorn" Logic

1. Wait for the **"Drishti Pulse"** splash screen to finish (or click **Skip Intro ➔**).
2. Enter the prompt:
   ```
   Autonomous Anti-Gravity Propulsion System using YBCO Superconductors
   ```
3. Click **LAUNCH AGENT CYCLE** and observe the terminal-style logs as the Chakra Cycle moves through:
   - 🔍 **Shodh** *(Find)* — Global patent & market gap analysis
   - ⚗️ **Manthan** *(Do)* — Technical blueprint generation using AMD MI300X
   - ✅ **Parikshan** *(Test)* — Freedom-to-Operate legal audit & risk scoring

---

## 6. Technology Stack Details

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit + Custom Glassmorphic CSS |
| **LLM Engine** | Gemma-2-9b via Fireworks AI |
| **GPU Accelerators** | AMD Instinct™ MI300X — ROCm 6.1 |
| **Memory** | 192GB HBM3 @ 5.3 TB/s bandwidth |
| **Containerization** | Docker / Docker-Compose |
| **Environment** | Python 3.11 |

---

## 7. Architecture Overview

```
User Prompt
    │
    ▼
┌─────────────────────────────────────┐
│         DRISHTI CHAKRA ENGINE       │
│  ┌─────────┐ ┌─────────┐ ┌───────┐ │
│  │  SHODH  │→│ MANTHAN │→│PARIK- │ │
│  │ (Find)  │ │  (Do)   │ │SHAN   │ │
│  └─────────┘ └─────────┘ └───────┘ │
│       AMD Instinct™ MI300X          │
│       ROCm 6.1 | Fireworks AI       │
└─────────────────────────────────────┘
    │
    ▼
 Full 5-Section Enterprise Whitepaper
 (Executive Dossier, R&D Blueprint,
  Patent Audit, GTM Strategy, SWOT)
```

---

> **💡 Idea tamari, Shakti AMD ni, ane Drishti amari!**
> *(Your idea, AMD's power, and our vision!)*
>
> — **Team NexAura** | AMD Developer Hackathon 2026

