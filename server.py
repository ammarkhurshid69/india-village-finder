from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "india_villages_clean.csv"
INDEX_PATH = BASE_DIR / "index.html"

# Load CSV and clean
df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.strip()

# ✅ FIX: Remove rows where column value equals column name
# (happens when combine.py repeated the header for each file)
df = df[df["state"] != "state"]
df = df[df["state"] != "State"]
df = df[df["district"] != "district"]

# Clean whitespace in all columns
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# Drop blank/nan state rows
df = df[df["state"].notna() & (df["state"] != "") & (df["state"] != "nan")]
df = df.reset_index(drop=True)

print(f"Loaded {len(df)} rows | States: {df['state'].nunique()}")

# ✅ Serve index.html at root "/"
@app.get("/")
def serve_frontend():
    return FileResponse(INDEX_PATH)

@app.get("/states")
def get_states():
    states = sorted(df["state"].dropna().unique().tolist())
    return {"states": states}

@app.get("/districts")
def get_districts(state: str):
    data = df[df["state"] == state]
    districts = sorted(data["district"].dropna().unique().tolist())
    return {"districts": districts}

@app.get("/subdistricts")
def get_subdistricts(district: str):
    data = df[df["district"] == district]
    subs = sorted(data["sub_district"].dropna().unique().tolist())
    return {"sub_districts": subs}

@app.get("/villages")
def get_villages(subdistrict: str):
    data = df[df["sub_district"] == subdistrict]
    villages = sorted(data["village"].dropna().unique().tolist())
    return {"villages": villages}

@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    if not q.strip():
        return []
    result = df[
        df["village"].str.contains(q.strip(), case=False, na=False)
    ].head(50)
    return result[["village", "sub_district", "district", "state"]].to_dict(orient="records")

@app.get("/autocomplete")
def autocomplete(q: str = Query(..., min_length=1)):
    result = df[
        df["village"].str.startswith(q, na=False)
    ]["village"].drop_duplicates().head(10)
    return {"suggestions": result.tolist()}
