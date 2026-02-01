import pandas as pd
import numpy as np
from typing import Dict, Any

class DataService:
    @staticmethod
    def get_column_statistics(file_content: Any) -> Dict[str, Any]:
        """
        Logic for parsing CSV and calculating numerical stats.
        """
        df = pd.read_csv(file_content)
        
        # Filter for numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return {"error": "No numeric columns found in this CSV."}

        column_name = numeric_df.columns[0]
        data = numeric_df[column_name].values

        return {
            "column_analyzed": column_name,
            "row_count": len(df),
            "mean": float(np.mean(data)),
            "std_dev": float(np.std(data)),
            "max": float(np.max(data)),
            "min": float(np.min(data))
        }