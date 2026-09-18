from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load cleaned drug data
df = pd.read_csv("notebooks/cleaned_drug_data.csv")
repurposing_df = pd.read_csv("data/repurposing_data.csv")

@app.get("/")
def home():
    return {"message": "AI Drug Repurposing Backend is running!"}

@app.get("/drugs")
def get_drugs():
    data = df.astype(object).where(pd.notna(df), None)
    return data.to_dict(orient="records")
@app.get("/drugs/search")
def search_drug(brand: str):
    result = df[
        df["brand_name"].fillna("").str.contains(
            brand,
            case=False,
            na=False
        )
    ]

    data = result.astype(object).where(pd.notna(result), None)
    return data.to_dict(orient="records")
@app.get("/drugs/repurpose")
def repurpose_drug(brand: str):

    result = repurposing_df[
        repurposing_df["drug"].fillna("").str.contains(
            brand,
            case=False,
            na=False
        )
    ]

    if result.empty:
        return {
            "drug": brand,
            "results": []
        }

    data = result.astype(object).where(pd.notna(result), None)

    return {
        "drug": brand,
        "results": data.to_dict(orient="records")
    }