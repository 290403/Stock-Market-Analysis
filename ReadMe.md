# Stock Market Performance & Risk Analysis

## Project Overview

This project analyzes the historical performance, risk, technical indicators, fundamental metrics, and benchmark performance of selected NSE-listed companies.

The analysis covers four companies:

* Reliance Industries (`RELIANCE.NS`)
* ONGC (`ONGC.NS`)
* Bharat Petroleum Corporation Limited (`BPCL.NS`)
* Indian Oil Corporation Limited (`IOC.NS`)

The Nifty 50 (`^NSEI`) is used as the benchmark for market comparison.

The project combines Python-based data collection, financial data analysis, technical indicators, fundamental analysis, correlation analysis, benchmark comparison, and an explainable stock scorecard.

---

## Objectives

The main objectives of this project are to:

* Analyze historical stock price performance
* Calculate daily and cumulative returns
* Measure historical volatility and maximum drawdown
* Analyze price trends using moving averages
* Calculate RSI, MACD, and Bollinger Bands
* Identify rolling support and resistance levels
* Compare stock performance with the Nifty 50
* Calculate beta and relative performance
* Analyze correlations between selected stocks
* Compare fundamental financial metrics
* Build a transparent and explainable stock scorecard

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* yfinance
* SQL
* Power BI
* CSV

---

## Data Source

Market data is downloaded programmatically using the `yfinance` library.

NSE-listed companies are accessed using the `.NS` ticker suffix.

The stocks analyzed are:

text
RELIANCE.NS
ONGC.NS
BPCL.NS
IOC.NS


The Nifty 50 index is represented by:

text
^NSEI


The analysis starts from January 1, 2000, where historical data is available, and retrieves the latest available daily data when the script is executed.

This project uses historical and latest available daily market data. It is not a real-time trading or tick-data system.

---

# Analysis Performed

## 1. Price Performance Analysis

The project analyzes the following market variables for each stock:

* Open price
* High price
* Low price
* Closing price
* Trading volume
* Daily returns
* Cumulative returns
* 20-day moving average
* 50-day moving average

### Daily Return

text
Daily Return = (Today's Close / Previous Close) - 1


### Cumulative Return

text
Cumulative Return = (Current Close / Initial Close) - 1


---

## 2. Risk Analysis

The project measures historical risk using:

* 30-day rolling volatility
* Maximum drawdown
* Daily return fluctuations
* Trading volume

### Maximum Drawdown

text
Drawdown = Current Price / Running Maximum - 1


Maximum drawdown describes the historical decline from a previous running peak.

---

# Technical Analysis

The project calculates several commonly used technical indicators.

## Moving Averages

* MA20
* MA50

Moving averages are used to describe short- and medium-term price trends.

## Relative Strength Index

A 14-day RSI is calculated to analyze historical price momentum.

## MACD

The Moving Average Convergence Divergence indicator includes:

* MACD line
* Signal line
* Histogram

## Bollinger Bands

Bollinger Bands are calculated using:

* 20-day moving average
* Upper band
* Lower band

## Support and Resistance

Rolling 20-day minimum and maximum prices are used as:

* Support
* Resistance

These are historical rolling levels and are not treated as guaranteed future price levels.

---

# Benchmark Analysis

Each selected stock is compared against the Nifty 50.

The benchmark analysis includes:

* Stock total return
* Nifty 50 total return
* Relative performance
* Beta

## Beta

Beta is calculated using daily returns:

text
Beta =
Covariance(Stock Returns, Nifty Returns)
/
Variance(Nifty Returns)


## Relative Performance

text
Relative Performance =
Stock Total Return - Nifty 50 Total Return


This measures the difference between the stock's historical cumulative return and the benchmark's cumulative return over the common analysis period.

---

# Stock Correlation Analysis

Pearson correlation is calculated using the daily returns of the selected stocks.

The correlation matrix helps identify the degree to which the historical daily returns of the selected companies moved together.

Companies included:

* Reliance Industries
* ONGC
* BPCL
* Indian Oil Corporation

---

# Fundamental Analysis

Fundamental metrics are collected using `yfinance` where the required information is available.

The project analyzes:

* P/E Ratio
* P/B Ratio
* Return on Equity
* Debt-to-Equity
* Revenue Growth
* Earnings Growth
* Dividend Yield
* Sector

The selected companies are compared using these financial metrics rather than analyzing each company only in isolation.

Fundamental data availability can vary by company and data source. Missing values are not fabricated.

---

# Explainable Stock Scorecard

A simple scorecard combines three analytical dimensions:

* Valuation
* Quality
* Momentum

## Valuation Score

The valuation component uses:

* P/E
* P/B

Lower valuation multiples receive relatively higher scores within the selected stock universe.

## Quality Score

The quality component uses:

* ROE
* Earnings Growth
* Debt-to-Equity

## Momentum Score

The momentum component uses:

* Relative performance against the Nifty 50
* RSI

## Overall Score

The overall score uses the following weighting:

text
Overall Score =
33% Valuation
+
34% Quality
+
33% Momentum


The score is relative to the selected companies and is intended as a transparent analytical framework rather than a prediction or guaranteed trading signal.

---

# Project Visualizations

## Stock Price and Moving Average Analysis — Reliance Industries

![Reliance Price Analysis](images/reliance_analysis.png)

## Stock Price and Moving Average Analysis — ONGC

![ONGC Price Analysis](images/ongc_analysis.png)

## Stock Price and Moving Average Analysis — BPCL

![BPCL Price Analysis](images/bpcl_analysis.png)

## Stock Price and Moving Average Analysis — Indian Oil Corporation

![IOC Price Analysis](images/ioc_analysis.png)

## Fundamental Analysis Comparison

![Fundamental Analysis](images/fundamental_analysis.png)

## Explainable Stock Scorecard

![Stock Scorecard](images/stock_scorecard.png)

---

# Project Structure

text
Stock-Market_Analysis/
│
├── analysis.py
├── stock_analysis.py
├── requirements.txt
├── README.md
│
├── images/
│   ├── reliance_analysis.png
│   ├── ongc_analysis.png
│   ├── bpcl_analysis.png
│   ├── ioc_analysis.png
│   ├── fundamental_analysis.png
│   └── stock_scorecard.png
│
├── RELIANCE_analyzed.csv
├── ONGC_analyzed.csv
├── BPCL_analyzed.csv
├── IOC_analyzed.csv
│
├── technical_summary.csv
├── fundamental_analysis.csv
├── benchmark_comparison.csv
├── stock_correlation.csv
├── relative_performance.csv
└── stock_scorecard.csv


---

# How to Run the Project

## 1. Clone the Repository

bash
git clone <your-github-repository-url>


## 2. Navigate to the Project Directory

bash
cd Stock-Market_Analysis


## 3. Install Dependencies

bash
pip install -r requirements.txt


## 4. Run the Analysis

bash
python analysis.py


The script downloads the latest available market data, performs the analysis, generates the CSV outputs, and displays the visualizations.

---

# Output Files

| File                       | Description                                     |
| -------------------------- | ----------------------------------------------- |
| `technical_summary.csv`    | Technical and risk metrics                      |
| `fundamental_analysis.csv` | Fundamental financial metrics                   |
| `benchmark_comparison.csv` | Stock versus Nifty 50 comparison                |
| `stock_correlation.csv`    | Correlation between selected stocks             |
| `relative_performance.csv` | Relative performance against Nifty 50           |
| `stock_scorecard.csv`      | Valuation, quality, momentum and overall scores |
| `RELIANCE_analyzed.csv`    | Detailed Reliance analysis                      |
| `ONGC_analyzed.csv`        | Detailed ONGC analysis                          |
| `BPCL_analyzed.csv`        | Detailed BPCL analysis                          |
| `IOC_analyzed.csv`         | Detailed Indian Oil analysis                    |

---

# Key Analytical Questions

This project is designed to answer questions such as:

1. How have the selected stocks performed historically?
2. What levels of historical volatility and drawdown did they experience?
3. How did the selected stocks perform relative to the Nifty 50?
4. How sensitive were the stocks to movements in the Nifty 50?
5. How strongly were the selected stocks correlated?
6. How do the companies differ in valuation and financial quality metrics?
7. How does the explainable scorecard compare the selected companies?

---

# Limitations

* Historical performance does not guarantee future performance.
* Market data availability may vary across companies and periods.
* Fundamental metrics may be unavailable or updated at different times.
* Support and resistance are rolling historical levels rather than guaranteed future price levels.
* The scorecard is a simplified relative comparison.
* The scorecard should not be interpreted as investment advice.
* The project does not attempt to predict future stock prices.
* The analysis is based on the selected stock universe and benchmark.

---

# Author

**Gungun Prajapati**

B.Tech Information Technology

Skills demonstrated:

**Python | SQL | Pandas | NumPy | Data Analysis | Financial Analysis | Power BI | Machine Learning Fundamentals**
