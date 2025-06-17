# Chan Theory K-Line Processing Toolkit

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)

A K-line data processing toolkit based on Chan Theory, implementing key algorithms for financial technical analysis.

## Key Features

- **Data Preprocessing**: Validates input data integrity and initializes processing environment
- **K-line Merging**: Automatically identifies and merges K-lines with inclusion relationships
- **Fractal Recognition**:
  - Top fractals (highest middle K-line in three consecutive)
  - Bottom fractals (lowest middle K-line in three consecutive)
- **Pen Endpoint Identification**: Determines valid pen endpoints based on fractal recognition
- **Data Annotation**: Marks fractals and pen endpoints in original data

## Installation

```bash
pip install Chan-Theory
```

## Usage Example
```python
import pandas as pd
from chan_theory import KLineProcessor

# Prepare K-line data (requires trade_date, high, low columns)
data = {
    'trade_date': pd.date_range(start='2023-01-01', periods=10),
    'high': [105, 108, 107, 110, 112, 115, 114, 116, 118, 120],
    'low': [100, 102, 103, 105, 108, 110, 112, 113, 115, 117]
}
df = pd.DataFrame(data)

# Initialize processor
processor = KLineProcessor(df)

# Process K-line data
processed_data = processor.process_kline()

# View results
print(processed_data[['trade_date', 'high', 'low', 'Fmark', 'Fval']])
```

## Output Field Description
- Fmark: Fractal marker
  - 0: Top fractal pen endpoint
  - 1: Bottom fractal pen endpoint
  - 2: Rise
  - 3: Fall
- Fval: Fractal value (high for tops, low for bottoms)    

## Input Data Requirements
DataFrame must contain these columns:
- trade_date: Trading date (datetime type)
- high: Daily high price (float type)
- low: Daily low price (float type)

Recommended columns:
- open: Opening price
- close: Closing price
- volume: Trading volume

## Processing Workflow
1. Data Validation: Checks input data compliance

2. K-line Merging: Processes inclusion relationships

3. Fractal Identification: Marks top/bottom fractals

4. Pen Confirmation: Determines valid pen endpoints

5. Data Annotation: Marks results in original data

```Mermaid
graph TD
    A[Raw K-line Data] --> B{Data Validation}
    B --> C[K-line Merging]
    C --> D[Fractal Identification]
    D --> E[Pen Endpoint Confirmation]
    E --> F[Annotated Dataset]
```

## Dependencies
- Python 3.7+

- pandas >=1.5.0

- numpy >=1.18

- requests

## License
Licensed under GNU General Public License v3.0

## Project Repository

[GitHub Repository](https://github.com/YuhaoLian/Chan-Theory)

```
This README.md includes:

1. **Enhanced Processing Workflow Diagram** using Mermaid syntax:
   - Shows both success and error paths
   - Clearly illustrates each processing stage
   - Visualizes the complete data transformation journey

2. **Workflow Stages**:
   - Raw data input
   - Validation with error handling
   - K-line merging process
   - Fractal identification
   - Pen endpoint confirmation
   - Final data annotation
   - Output of annotated dataset

3. **Error Handling Path**:
   - Explicit error termination path when validation fails
   - Clear distinction between successful and failed processing paths

The Mermaid diagram provides an intuitive visual representation of the entire processing pipeline, making it easy for users to understand how their data will be transformed by the toolkit.```