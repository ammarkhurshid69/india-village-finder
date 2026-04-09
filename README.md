# 🇮🇳 India Village Finder

A REST API and web interface to explore hierarchical Indian address data — State → District → Sub-district → Village — built on the MDDS government dataset with 5,70,000+ village records.

Built as **Task 2** of my internship at [Bluestock Fintech](https://bluestock.in).

---

## 🚀 Live Demo

> Run locally — see setup below.

![India Village Finder Screenshot](screenshot.png)

---

## ✨ Features

- 🔽 Cascading dropdowns: State → District → Sub-district → Village
- 🔍 Full-text village search across 29 states and 5,70,000+ records
- ⚡ Autocomplete endpoint for fast lookups
- 🌐 Clean REST API with JSON responses
- 📦 Zero database required — runs entirely on CSV + pandas

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| Data | pandas, MDDS Government Dataset |
| Frontend | Vanilla HTML/CSS/JS (served by FastAPI) |
| Data prep | openpyxl, xlrd, odf |

---

## 📁 Project Structure

```
dataset/
├── server.py              # FastAPI app + embedded frontend
├── make_csv.py            # Combines Excel files → india_villages_clean.csv
├── india_villages_clean.csv  # Generated dataset (5,70,000+ rows)
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Install dependencies

```bash
pip install fastapi uvicorn pandas openpyxl xlrd odf
```

### 2. Generate the CSV dataset

Place all state-wise Excel files (Rdir_2011_XX_*.xlsx) in the `dataset/` folder, then run:

```bash
py make_csv.py
```

This generates `india_villages_clean.csv` with columns: `state`, `district`, `sub_district`, `village`.

### 3. Start the server

```bash
py -m uvicorn server:app --reload
```

### 4. Open in browser

```
http://127.0.0.1:8000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| GET | `/states` | List all states |
| GET | `/districts?state=BIHAR` | Districts in a state |
| GET | `/subdistricts?district=Patna` | Sub-districts in a district |
| GET | `/villages?subdistrict=Patna` | Villages in a sub-district |
| GET | `/search?q=rampur` | Search villages by name |
| GET | `/autocomplete?q=ram` | Autocomplete suggestions |

### Example Response

```json
GET /states

{
  "states": [
    "ANDHRA PRADESH",
    "ASSAM",
    "BIHAR",
    ...
  ]
}
```

```json
GET /search?q=rampur

[
  {
    "village": "Rampur",
    "sub_district": "Jewar",
    "district": "Gautam Buddha Nagar",
    "state": "UTTAR PRADESH"
  },
  ...
]
```

---

## 📊 Dataset

- **Source:** MDDS (Metadata and Data Standards) — Government of India
- **Coverage:** 29 states, 600+ districts, 5,000+ sub-districts, 5,70,000+ villages
- **Format:** State-wise Excel files combined into a single cleaned CSV

---

## 👨‍💻 Author

**Ammar Mohammed Khurshid**  
BTech CSE — Sharda University  
Intern @ Bluestock Fintech (April–May 2025)  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/ammarkhurshid69)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/ammarkhurshid69)

---

## 📄 License

MIT License — free to use and modify.
