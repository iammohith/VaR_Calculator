# VaR_Calculator Using Three Different Methodologies From Python CLI

A command-line tool for calculating Value at Risk (VaR) of Indian stocks using three different methodologies. This tool helps investors quantify potential portfolio losses under normal market conditions.

## Features

- Calculates Value at Risk using:
  - Parametric method (Variance-Covariance)
  - Historical simulation
  - Monte Carlo simulation
- Supports stocks from both NSE and BSE exchanges
- Generates comparative visualization of results
- Configurable parameters for confidence level, time horizon, and simulation settings

## Installation

1. Clone the repository:
```bash
git clone https://github.com/iammohith/VaR_Calculator.git
cd VaR_Calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Syntax
```bash
var-calculator [TICKER] [EXCHANGE] [PORTFOLIO_VALUE] [OPTIONS]
```
### Alternative Run Method
```bash
python -m src.cli [TICKER] [EXCHANGE] [PORTFOLIO_VALUE] [OPTIONS]
```

### Required Arguments
| Argument          | Description                         | Example       |
|-------------------|-------------------------------------|---------------|
| `TICKER`          | Stock ticker symbol                 | `RELIANCE`    |
| `EXCHANGE`        | Stock exchange (`NSE` or `BSE`)     | `NSE`         |
| `PORTFOLIO_VALUE` | Portfolio value in INR              | `1000000`     |

### Optional Parameters
| Option              | Description                          | Default Value |
|---------------------|--------------------------------------|---------------|
| `--confidence`      | Confidence level (0.90-0.99)         | 0.95          |
| `--horizon`         | Time horizon in days                 | 1             |
| `--window`          | Historical data window size (days)   | 252           |
| `--simulations`     | Monte Carlo simulations count        | 10000         |

### Example

#### 1.Basic Command:
```bash
var-calculator RELIANCE NSE 1000000 --confidence 0.99 --horizon 5
```
#### 2.Alternative Command:
```bash
python -m src.cli RELIANCE NSE 1000000 --confidence 0.99 --horizon 5
```

#### Sample Output
```
Value at Risk Report:
Parametric Var: ₹48,215.67
Historical Var: ₹52,890.45
Monte Carlo Var: ₹51,327.83

Comparison plot saved as 'var_comparison.png'
```

## File Structure
```
VaR_Calculator_Python_CLI/
├── bin/                       # Executable scripts
│   └── var-calculator         # Main CLI entry point
├── config/                    # Configuration files
│   ├── logging.conf           # Logging configuration
│   └── settings.py            # Default parameters
├── data/                      # Data storage directory
├── docs/                      # Documentation
│   └── README.md              # Syntax
├── src/                       # Source code
│   ├── calculator/            # VaR calculation methods
│   │   ├── historical_var.py  # VaR calculation using Historical method
│   │   ├── monte_carlo_var.py # VaR calculation using Monte Carlo method
│   │   └── parametric_var.py  # VaR calculation using Parametric method
│   ├── core/                  # Core functionality
│   │   ├── data_fetcher.py    # Stock data retrieval
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── risk_report.py     # Report generation
│   └── cli.py                 # Command-line interface
├── requirements.txt           # Python dependencies
├── setup.py                   # Package configuration
└── .gitignore                 # Version control exclusions
```

## Dependencies
- Python 3.7+
- yfinance
- numpy
- pandas
- scipy
- matplotlib

## Limitations
- Currently supports single-stock portfolios only
- Uses daily closing prices for calculations
- Monte Carlo simulation assumes lognormal distribution of returns

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
