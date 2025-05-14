from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import logging
import re
import rxnormApi as rx

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detail
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("interactions.log"),  # Logs to file
        logging.StreamHandler()  # Also logs to console
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

# needed for frontend access
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], #TODO change
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.mount("/static", StaticFiles(directory="frontend"), name="static")

preferred_df = pd.read_csv("../data/ddinter.csv", sep=",", on_bad_lines='skip')
preferred_df['Drug_A'] = preferred_df['Drug_A'].str.lower()
preferred_df['Drug_B'] = preferred_df['Drug_B'].str.lower()
backup_df = pd.read_csv("../data/samwald.csv", sep="\t", on_bad_lines='skip')
backup_df['drug1'] = backup_df['drug1'].str.lower()
backup_df['drug2'] = backup_df['drug2'].str.lower()
logger.info(f"prefdf type = {preferred_df.columns.tolist()} backupdf type = {type(backup_df)}")

# Find interaction in preferred dataset
def find_preferred_interaction(drug1, drug1_aliases, drug2, drug2_aliases):
    logger.info(f"find_preferred_interaction({drug1}, {drug2})")
    result = preferred_df[
        ((preferred_df['Drug_A'] == drug1) & (preferred_df['Drug_B'] == drug2)) |
        ((preferred_df['Drug_A'] == drug2) & (preferred_df['Drug_B'] == drug1))
    ]
    if result.empty:
        for a1 in drug1_aliases:
            for a2 in drug2_aliases:
                    result = preferred_df[
                        ((preferred_df['Drug_A'] == a1) & (preferred_df['Drug_B'] == a2)) |
                        ((preferred_df['Drug_A'] == a2) & (preferred_df['Drug_B'] == a1))
                    ]
                    if not result.empty:
                        logger.info(f"found as alias: {result.iloc[0]}")
                        return result.iloc[0]['Level']
    if not result.empty:
        logger.info(f"found preferred interaction{result.iloc[0]})")
        return result.iloc[0]['Level']
    return None

# Find interaction in backup dataset
def find_backup_interaction(drug1, drug1_aliases, drug2, drug2_aliases):
    logger.info(f"find_backup_interaction({drug1}, {drug2})")
    result = backup_df[
        ((backup_df['object'] == drug1) & (backup_df['precipitant'] == drug2)) |
        ((backup_df['object'] == drug2) & (backup_df['precipitant'] == drug1))
    ]
    if result.empty:
        for a1 in drug1_aliases:
            for a2 in drug2_aliases:
                    result = preferred_df[
                        ((backup_df['object'] == a1) & (backup_df['precipitant'] == a2)) |
                        ((backup_df['object'] == a2) & (backup_df['precipitant'] == a1))
                    ]
                    if not result.empty:
                        logger.info(f"found as alias: {result.iloc[0]}")
                        return result.iloc[0]['Level']
    if not result.empty:
        logger.info(f"found backup interaction{result.iloc[0]} in find_back_up_interaction())")
        if np.isnan(result.iloc[0]['severity']):
            return "Unknown"
        return result.iloc[0]['severity']
    return None


@app.get("/interactions")
def check_interactions(drugs: List[str] = Query(..., min_length=2, max_length=5)):
    logger.info(f"Request for drugs: {drugs}")
    drugs = [d.lower() for d in drugs]
    results = []
    checked_pairs = set()
    n = len(drugs)

    for i in range(n):
        for j in range(i + 1, n):
            d1, d2 = drugs[i], drugs[j]
            d1_aliases, d2_aliases = rx.resolve_aliases_for(d1), rx.resolve_aliases_for(d2)
            logger.info(f"Make api call for: {d1} received: {d1_aliases} and {d2} received: {d2_aliases}")
            pair_key = tuple(sorted([d1,d2]))
            if pair_key in checked_pairs:
                continue
            checked_pairs.add(pair_key)

            interaction = find_preferred_interaction(d1,d1_aliases,d2,d2_aliases)

            if interaction is not None:
                results.append({
                    "drug1": d1,
                    "drug2": d2,
                    "level": interaction,
                    "source": "ddInter",
                    })
            else:
                interaction = find_backup_interaction(d1,d1_aliases,d2,d2_aliases)
                logger.info(f"found backup Interaction {interaction}")


                if interaction is not None :
                    results.append({
                        "drug1": d1,
                        "drug2": d2,
                        "level": interaction,
                        "source": "Samwald",
                        })
                else:
                    results.append({
                        "drug1":d1,
                        "drug2":d2,
                        "level": "unknown",
                        "message": "No interaction found",
                        "source": "none",
                        })
    return {"interactions": results}


# Serve the main HTML file
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")











