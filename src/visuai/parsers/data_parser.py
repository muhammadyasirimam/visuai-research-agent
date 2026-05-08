"""
Data Parser - Handles loading data from various sources.

Author: Muhammad Yasir Imam
"""

import os
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np

from ..core.config import Config


class DataParser:
    """Parser for various data formats."""

    def __init__(self, config: Config):
        self.config = config

    def load(self, source: str, **kwargs) -> pd.DataFrame:
        """Load data from file path or URL.

        Args:
            source: File path or URL
            **kwargs: Additional arguments for specific loaders

        Returns:
            pandas DataFrame
        """
        if not os.path.exists(source):
            raise FileNotFoundError(f"File not found: {source}")

        # Check file size
        file_size_mb = os.path.getsize(source) / (1024 * 1024)
        if file_size_mb > self.config.max_file_size_mb:
            raise ValueError(f"File size ({file_size_mb:.1f} MB) exceeds maximum ({self.config.max_file_size_mb} MB)")

        ext = os.path.splitext(source)[1].lower()

        if ext == ".csv":
            return self._load_csv(source, **kwargs)
        elif ext in [".xlsx", ".xls"]:
            return self._load_excel(source, **kwargs)
        elif ext == ".json":
            return self._load_json(source, **kwargs)
        elif ext == ".parquet":
            return self._load_parquet(source, **kwargs)
        elif ext in [".hdf5", ".h5"]:
            return self._load_hdf5(source, **kwargs)
        elif ext in [".txt", ".tsv"]:
            return self._load_tsv(source, **kwargs)
        elif ext in [".db", ".sqlite"]:
            return self._load_sqlite(source, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _load_csv(self, path: str, **kwargs) -> pd.DataFrame:
        """Load CSV file."""
        defaults = {"encoding": "utf-8", "low_memory": False}
        defaults.update(kwargs)
        return pd.read_csv(path, **defaults)

    def _load_excel(self, path: str, **kwargs) -> pd.DataFrame:
        """Load Excel file."""
        sheet_name = kwargs.get("sheet_name", 0)
        return pd.read_excel(path, sheet_name=sheet_name)

    def _load_json(self, path: str, **kwargs) -> pd.DataFrame:
        """Load JSON file."""
        orient = kwargs.get("orient", "records")
        return pd.read_json(path, orient=orient)

    def _load_parquet(self, path: str, **kwargs) -> pd.DataFrame:
        """Load Parquet file."""
        return pd.read_parquet(path, **kwargs)

    def _load_hdf5(self, path: str, **kwargs) -> pd.DataFrame:
        """Load HDF5 file."""
        key = kwargs.get("key", "data")
        return pd.read_hdf(path, key=key)

    def _load_tsv(self, path: str, **kwargs) -> pd.DataFrame:
        """Load TSV file."""
        return pd.read_csv(path, sep="\t", **kwargs)

    def _load_sqlite(self, path: str, **kwargs) -> pd.DataFrame:
        """Load from SQLite database."""
        import sqlite3
        query = kwargs.get("query", "SELECT * FROM data")
        conn = sqlite3.connect(path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get comprehensive data summary."""
        summary = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().mean() * 100).to_dict(),
        }

        # Numeric summary
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            summary["numeric_summary"] = numeric_df.describe().to_dict()

        # Categorical summary
        cat_df = df.select_dtypes(include=["object", "category"])
        if not cat_df.empty:
            summary["categorical_summary"] = {
                col: {
                    "unique_count": df[col].nunique(),
                    "top_values": df[col].value_counts().head(5).to_dict()
                }
                for col in cat_df.columns
            }

        return summary
