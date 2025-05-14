import requests
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detail
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("interactions.log"),  # Logs to file
        logging.StreamHandler()  # Also logs to console
    ]
)

RXNORM_BASE = "https://rxnav.nlm.nih.gov/REST"

def get_rxcui(drug_name):
    url = f"{RXNORM_BASE}/rxcui.json"
    params = {"name": drug_name}
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("idGroup", {}).get("rxnormId", [None])[0]

def get_aliases(rxcui):
    url = f"{RXNORM_BASE}/rxcui/{rxcui}/allProperties.json"
    params = {"prop": "names"}
    response = requests.get(url, params=params)
    data = response.json()
    names = data.get("propConceptGroup", {}).get("propConcept", [])
    logger.info(f"rxNorm Api response: {names}")
    return list({n['propValue'].lower() for n in names if 'propValue' in n})

def resolve_aliases_for(drug_name):
    rxcui = get_rxcui(drug_name)
    if not rxcui:
        logger.info(f"Drug not found: {drug_name}")
        return [drug_name.lower()]
    aliases = get_aliases(rxcui)
    return get_aliases(rxcui)

