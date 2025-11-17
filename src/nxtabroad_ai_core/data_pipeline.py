from typing import Iterable, Dict, Any
import pandas as pd


def load_leads_from_csv(path: str) -> Iterable[Dict[str, Any]]:
    """Load lead records from a CSV file and yield dict rows."""
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        yield row.to_dict()