[English](README_EN.md) | [中文](README.md)

# Time Series Model Analysis and Diagnostic Tool

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

A professional tool for time series model analysis and diagnostics, providing AR model stationarity checks and MA model invertibility checks.

## 🚀 Features

### Core Features

- **AR Model Stationarity Check**: Test the stationarity condition of autoregressive models
- **MA Model Invertibility Check**: Test the invertibility condition of moving average models
- **Characteristic Root Analysis**: Calculate the roots of the characteristic polynomial and determine their positions
- **Stability Margin Analysis**: Quantitatively analyze the degree of model stability
- **Modification Suggestions**: Provide adjustment suggestions for models that do not meet the conditions

### Usage Modes

- **Python Library**: Can be imported and used as a Python package
- **Command Line Tool**: User-friendly CLI interface
- **Batch Processing**: Supports batch model analysis and comparison

## 📦 Installation

### Using uv (Recommended)

```bash
uv add time-series-model-analysis-and-diagnostic-tool
```

### Using pip

```bash
pip install time-series-model-analysis-and-diagnostic-tool
```

### From Source

```bash
git clone https://github.com/zym9863/time-series-model-analysis-and-diagnostic-tool.git
cd time-series-model-analysis-and-diagnostic-tool
uv sync
```

## 🔧 Quick Start

### Command Line Usage

#### AR Model Stationarity Check

```bash
# Basic check
tsdiag stationarity -c "0.5,-0.3"

# With analysis and suggestions
tsdiag stationarity -c "0.8,0.15" --analysis --suggest

# Check non-stationary model
tsdiag stationarity -c "1.1" --suggest
```

#### MA Model Invertibility Check

```bash
# Basic check
tsdiag invertibility -c "0.5,-0.3"

# With analysis and suggestions
tsdiag invertibility -c "0.8,0.15" --analysis --suggest
```

#### ARMA Model Comprehensive Check

```bash
# Check both AR and MA parts
tsdiag check --ar "0.5,-0.3" --ma "0.4,0.2"
```

#### View Usage Examples

```bash
tsdiag examples
```

### Python Library Usage

#### Basic Usage

```python
import tsdiag

# AR model stationarity check
ar_result = tsdiag.stationarity_check([0.5, -0.3])
print(f"Is the model stationary: {ar_result.is_stationary}")
print(f"Characteristic roots: {[root.magnitude for root in ar_result.roots]}")

# MA model invertibility check
ma_result = tsdiag.invertibility_check([0.5, -0.3])
print(f"Is the model invertible: {ma_result.is_invertible}")
```

#### Advanced Features

```python
import tsdiag

# Use advanced API
diagnostic = tsdiag.TSModelDiagnostic()

# Check ARMA model
ar_result, ma_result = diagnostic.check_arma_model(
    ar_coefficients=[0.5, -0.3],
    ma_coefficients=[0.4, 0.2]
)

# Get summary
summary = diagnostic.get_summary()
print(summary)

# Quick check (returns boolean only)
is_stationary = tsdiag.quick_ar_check([0.5, -0.3])
is_invertible = tsdiag.quick_ma_check([0.4, 0.2])
```

#### Batch Analysis

```python
import tsdiag

# Batch AR model analysis
ar_models = [
    [0.5],
    [1.1],
    [0.5, -0.3]
]
results = tsdiag.batch_stationarity_check(ar_models)

for result in results:
    print(f"{result['model_name']}: {result['is_stationary']}")

# Model comparison
ma_models = [[0.5], [1.1], [0.3]]
comparison = tsdiag.compare_ma_models(ma_models)
print(f"Invertibility rate: {comparison['invertibility_rate']}")
```

## 📊 Theoretical Background

### AR Model Stationarity

AR(p) model: $X_t = \phi_1 X_{t-1} + \phi_2 X_{t-2} + \cdots + \phi_p X_{t-p} + \varepsilon_t$

**Stationarity Condition**: All roots of the characteristic equation $1 - \phi_1 z - \phi_2 z^2 - \cdots - \phi_p z^p = 0$ must be outside the unit circle.

### MA Model Invertibility

MA(q) model: $X_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2} + \cdots + \theta_q \varepsilon_{t-q}$

**Invertibility Condition**: All roots of the characteristic equation $1 + \theta_1 z + \theta_2 z^2 + \cdots + \theta_q z^q = 0$ must be outside the unit circle.

## 📖 Documentation

### Input Formats

Coefficients can be input in various formats:

- **List**: `[0.5, -0.3, 0.1]`
- **numpy array**: `np.array([0.5, -0.3, 0.1])`
- **String**: `"0.5,-0.3,0.1"` or `"0.5 -0.3 0.1"`

### Output Results

#### StationarityResult

```python
@dataclass
class StationarityResult:
    is_stationary: bool              # Whether stationary
    roots: List[RootInfo]           # Characteristic root info
    ar_coefficients: List[float]    # AR coefficients
    characteristic_polynomial: List[float]  # Characteristic polynomial coefficients
    message: str                    # Result message
```

#### InvertibilityResult

```python
@dataclass
class InvertibilityResult:
    is_invertible: bool             # Whether invertible
    roots: List[RootInfo]           # Characteristic root info
    ma_coefficients: List[float]    # MA coefficients
    characteristic_polynomial: List[float]  # Characteristic polynomial coefficients
    message: str                    # Result message
```

### Risk Levels

- **low**: All roots far from the unit circle (distance > 0.1)
- **medium**: Roots close to the unit circle (0 < distance ≤ 0.1)
- **high**: Roots inside or on the unit circle (distance ≤ 0)

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=tsdiag

# Run a specific test file
uv run pytest tests/test_core.py -v
```

## 📝 Examples

### Common AR Models

```python
import tsdiag

# AR(1) model examples
models = {
    "Stationary": [0.5],
    "Non-stationary": [1.1],
    "Unit root": [1.0],
    "Boundary case": [0.99]
}

for name, coeffs in models.items():
    result = tsdiag.stationarity_check(coeffs)
    print(f"{name}: {result.is_stationary}")
```

### Common MA Models

```python
import tsdiag

# MA(1) model examples
models = {
    "Invertible": [0.5],
    "Non-invertible": [1.1],
    "Unit root": [1.0],
    "Boundary case": [0.99]
}

for name, coeffs in models.items():
    result = tsdiag.invertibility_check(coeffs)
    print(f"{name}: {result.is_invertible}")
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Thanks to all contributors
- Based on classic time series analysis theory
- Uses NumPy for numerical computation
- Uses Click for CLI construction
