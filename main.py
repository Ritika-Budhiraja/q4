from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()

    # Read CSV with fallback encodings
    try:
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    except:
        df = pd.read_csv(io.StringIO(content.decode('latin-1')))

    # Normalize column names (remove spaces, lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # Try to find 'category' and 'amount' columns
    category_col = next((col for col in df.columns if 'category' in col), None)
    amount_col = next((col for col in df.columns if 'amount' in col), None)

    if category_col is None or amount_col is None:
        return {"answer": 0.0, "email": "23f1000377@ds.study.iitm.ac.in", "exam": "tds-2025-05-roe"}

    # Clean data
    df[category_col] = df[category_col].astype(str).str.strip().str.lower()
    df[amount_col] = df[amount_col].astype(str).str.replace(',', '').str.strip()

    # Remove invalid/missing values
    df = df[df[amount_col].str.replace('.', '', 1).str.isnumeric()]
    df[amount_col] = df[amount_col].astype(float)

    # Filter "food" category
    total_food = df[df[category_col] == 'food'][amount_col].sum()

    return {
        "answer": round(float(total_food), 2),
        "email": "23f1000377@ds.study.iitm.ac.in",
        "exam": "tds-2025-05-roe"
    }
