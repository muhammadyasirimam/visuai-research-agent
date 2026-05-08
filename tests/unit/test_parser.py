"""
Unit tests for data parser.

Author: Muhammad Yasir Imam
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os

from visuai.parsers.data_parser import DataParser
from visuai.core.config import Config


@pytest.fixture
def config():
    return Config()


class TestDataParser:
    """Test DataParser functionality."""

    def test_initialization(self, config):
        parser = DataParser(config)
        assert parser.config == config

    def test_load_csv(self, config):
        parser = DataParser(config)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('a,b,c\n1,2,3\n4,5,6\n')
            temp_path = f.name

        try:
            df = parser.load(temp_path)
            assert isinstance(df, pd.DataFrame)
            assert df.shape == (2, 3)
            assert list(df.columns) == ['a', 'b', 'c']
        finally:
            os.unlink(temp_path)

    def test_load_unsupported_format(self, config):
        parser = DataParser(config)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write('test')
            temp_path = f.name

        try:
            with pytest.raises(ValueError):
                parser.load(temp_path)
        finally:
            os.unlink(temp_path)

    def test_get_data_summary(self, config):
        parser = DataParser(config)
        df = pd.DataFrame({
            'num1': [1, 2, 3, 4, 5],
            'num2': [1.1, 2.2, 3.3, 4.4, 5.5],
            'cat': ['A', 'B', 'A', 'C', 'B']
        })

        summary = parser.get_data_summary(df)

        assert summary["shape"] == (5, 3)
        assert "columns" in summary
        assert "numeric_summary" in summary
        assert "categorical_summary" in summary
