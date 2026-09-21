import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# STOCK MARKET ANALYSIS PROJECT
# Technical Analysis + Benchmark + Fundamentals + Scoring
# ============================================================

# ------------------------------------------------------------
# 1. SETTINGS
# ------------------------------------------------------------

STOCKS = {
    "RELIANCE.NS": "Reliance Industries",
    "ONGC.NS": "ONGC",
    "BPCL.NS": "Bharat Petroleum",
    "IOC.NS": "Indian Oil Corporation"
}

BENCHMARK = "^NSEI"
BENCHMARK_NAME = "Nifty 50"

START_DATE = "2000-01-01"

print("=" * 70)
print("STOCK MARKET ANALYSIS PROJECT")
print("=" * 70)


# ============================================================
# 2. DOWNLOAD STOCK DATA
# ============================================================

print("\nDownloading stock data...")

stock_data = {}

for ticker, name in STOCKS.items():

    print(f"Downloading {name} ({ticker})...")

    data = yf.download(
        ticker,
        start=START_DATE,
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    # Handle MultiIndex returned by newer yfinance versions
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    data.columns = [
        str(col).strip()
        for col in data.columns
    ]

    data["Date"] = pd.to_datetime(data["Date"])

    data = data.sort_values("Date")
    data = data.drop_duplicates(subset=["Date"])

    data = data.dropna(
        subset=[
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
    )

    stock_data[ticker] = data

    print(
        f"  {len(data):,} records downloaded"
    )


# ============================================================
# 3. DOWNLOAD NIFTY 50 BENCHMARK
# ============================================================

print("\nDownloading Nifty 50 benchmark...")

nifty = yf.download(
    BENCHMARK,
    start=START_DATE,
    interval="1d",
    auto_adjust=False,
    progress=False
)

if isinstance(nifty.columns, pd.MultiIndex):
    nifty.columns = nifty.columns.get_level_values(0)

nifty = nifty.reset_index()

nifty.columns = [
    str(col).strip()
    for col in nifty.columns
]

nifty["Date"] = pd.to_datetime(nifty["Date"])

nifty = nifty.sort_values("Date")
nifty = nifty.drop_duplicates(subset=["Date"])

nifty = nifty.dropna(subset=["Close"])

print(
    f"Nifty 50 records downloaded: {len(nifty):,}"
)


# ============================================================
# 4. TECHNICAL INDICATORS
# ============================================================

def add_technical_indicators(data):

    df = data.copy()

    # --------------------------------------------------------
    # Daily Return
    # --------------------------------------------------------

    df["Daily Return"] = (
        df["Close"].pct_change() * 100
    )

    # --------------------------------------------------------
    # Moving Averages
    # --------------------------------------------------------

    df["MA20"] = (
        df["Close"]
        .rolling(20)
        .mean()
    )

    df["MA50"] = (
        df["Close"]
        .rolling(50)
        .mean()
    )

    # --------------------------------------------------------
    # 30-Day Volatility
    # --------------------------------------------------------

    df["30D Volatility"] = (
        df["Daily Return"]
        .rolling(30)
        .std()
    )

    # --------------------------------------------------------
    # Cumulative Return
    # --------------------------------------------------------

    df["Cumulative Return"] = (
        (1 + df["Daily Return"] / 100)
        .cumprod()
        - 1
    )

    df["Cumulative Return %"] = (
        df["Cumulative Return"] * 100
    )

    # --------------------------------------------------------
    # Maximum Drawdown
    # --------------------------------------------------------

    df["Running Maximum"] = (
        df["Close"].cummax()
    )

    df["Drawdown"] = (
        (df["Close"] - df["Running Maximum"])
        / df["Running Maximum"]
    ) * 100

    # ========================================================
    # RSI - Relative Strength Index
    # ========================================================

    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = (
        100 - (100 / (1 + rs))
    )

    # ========================================================
    # MACD
    # ========================================================

    ema12 = (
        df["Close"]
        .ewm(span=12, adjust=False)
        .mean()
    )

    ema26 = (
        df["Close"]
        .ewm(span=26, adjust=False)
        .mean()
    )

    df["MACD"] = ema12 - ema26

    df["MACD Signal"] = (
        df["MACD"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    df["MACD Histogram"] = (
        df["MACD"]
        - df["MACD Signal"]
    )

    # ========================================================
    # Bollinger Bands
    # ========================================================

    rolling_mean = (
        df["Close"]
        .rolling(20)
        .mean()
    )

    rolling_std = (
        df["Close"]
        .rolling(20)
        .std()
    )

    df["BB Middle"] = rolling_mean

    df["BB Upper"] = (
        rolling_mean
        + (2 * rolling_std)
    )

    df["BB Lower"] = (
        rolling_mean
        - (2 * rolling_std)
    )

    # ========================================================
    # Support and Resistance
    # ========================================================

    df["Support 20D"] = (
        df["Low"]
        .rolling(20)
        .min()
    )

    df["Resistance 20D"] = (
        df["High"]
        .rolling(20)
        .max()
    )

    return df


# Apply indicators
for ticker in STOCKS:

    stock_data[ticker] = (
        add_technical_indicators(
            stock_data[ticker]
        )
    )


# ============================================================
# 5. TECHNICAL ANALYSIS SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("TECHNICAL ANALYSIS SUMMARY")
print("=" * 70)

technical_summary = []

for ticker, name in STOCKS.items():

    df = stock_data[ticker]

    latest = df.iloc[-1]

    total_return = (
        (df["Close"].iloc[-1]
         / df["Close"].iloc[0])
        - 1
    ) * 100

    max_drawdown = df["Drawdown"].min()

    technical_summary.append({

        "Stock": name,

        "Latest Price":
            latest["Close"],

        "Total Return %":
            total_return,

        "RSI":
            latest["RSI"],

        "MACD":
            latest["MACD"],

        "MACD Signal":
            latest["MACD Signal"],

        "30D Volatility":
            latest["30D Volatility"],

        "Max Drawdown %":
            max_drawdown,

        "Support":
            latest["Support 20D"],

        "Resistance":
            latest["Resistance 20D"]
    })


technical_summary_df = pd.DataFrame(
    technical_summary
)

print(
    technical_summary_df.round(2)
    .to_string(index=False)
)


# ============================================================
# 6. NIFTY 50 RETURNS
# ============================================================

nifty["Daily Return"] = (
    nifty["Close"].pct_change()
)

nifty["Cumulative Return"] = (
    (1 + nifty["Daily Return"])
    .cumprod()
    - 1
)


# ============================================================
# 7. BENCHMARK COMPARISON
# ============================================================

benchmark_results = []

for ticker, name in STOCKS.items():

    stock = stock_data[ticker][
        ["Date", "Close", "Daily Return"]
    ].copy()

    stock["Stock Return"] = (
        stock["Close"].pct_change()
    )

    benchmark = nifty[
        ["Date", "Close", "Daily Return"]
    ].copy()

    benchmark = benchmark.rename(
        columns={
            "Close": "Nifty Close",
            "Daily Return": "Nifty Return"
        }
    )

    merged = pd.merge(
        stock,
        benchmark,
        on="Date",
        how="inner"
    )

    # --------------------------------------------------------
    # Beta
    # --------------------------------------------------------

    covariance = (
        merged["Stock Return"]
        .cov(merged["Nifty Return"])
    )

    benchmark_variance = (
        merged["Nifty Return"]
        .var()
    )

    beta = (
        covariance / benchmark_variance
    )

    # --------------------------------------------------------
    # Relative Performance
    # --------------------------------------------------------

    stock_total_return = (
        (merged["Close"].iloc[-1]
         / merged["Close"].iloc[0])
        - 1
    ) * 100

    nifty_total_return = (
        (merged["Nifty Close"].iloc[-1]
         / merged["Nifty Close"].iloc[0])
        - 1
    ) * 100

    relative_performance = (
        stock_total_return
        - nifty_total_return
    )

    benchmark_results.append({

        "Stock": name,

        "Stock Return %":
            stock_total_return,

        "Nifty Return %":
            nifty_total_return,

        "Relative Performance %":
            relative_performance,

        "Beta":
            beta
    })


benchmark_df = pd.DataFrame(
    benchmark_results
)

print("\n" + "=" * 70)
print("NIFTY 50 BENCHMARK COMPARISON")
print("=" * 70)

print(
    benchmark_df.round(2)
    .to_string(index=False)
)


# ============================================================
# 8. CORRELATION BETWEEN STOCKS
# ============================================================

print("\n" + "=" * 70)
print("STOCK RETURN CORRELATION")
print("=" * 70)

return_data = pd.DataFrame()

for ticker, name in STOCKS.items():

    temp = stock_data[ticker][
        ["Date", "Daily Return"]
    ].copy()

    temp = temp.rename(
        columns={
            "Daily Return": name
        }
    )

    if return_data.empty:

        return_data = temp

    else:

        return_data = pd.merge(
            return_data,
            temp,
            on="Date",
            how="inner"
        )


correlation_matrix = (
    return_data
    .set_index("Date")
    .corr()
)

print(
    correlation_matrix.round(2)
    .to_string()
)


# ============================================================
# 9. FUNDAMENTAL DATA
# ============================================================

print("\n" + "=" * 70)
print("FUNDAMENTAL ANALYSIS")
print("=" * 70)


def safe_number(value):

    if value is None:
        return np.nan

    try:

        value = float(value)

        if np.isfinite(value):
            return value

        return np.nan

    except:

        return np.nan


fundamental_results = []


for ticker, name in STOCKS.items():

    print(f"\nCollecting fundamentals for {name}...")

    stock = yf.Ticker(ticker)

    try:
        info = stock.info

    except Exception as e:

        print(
            f"Could not retrieve info for {ticker}: {e}"
        )

        info = {}


    # --------------------------------------------------------
    # Basic ratios
    # --------------------------------------------------------

    pe = safe_number(
        info.get("trailingPE")
    )

    pb = safe_number(
        info.get("priceToBook")
    )

    roe = safe_number(
        info.get("returnOnEquity")
    )

    debt_to_equity = safe_number(
        info.get("debtToEquity")
    )

    dividend_yield = safe_number(
        info.get("dividendYield")
    )

    revenue_growth = safe_number(
        info.get("revenueGrowth")
    )

    earnings_growth = safe_number(
        info.get("earningsGrowth")
    )


    # --------------------------------------------------------
    # Annual financial statements
    # Used as fallback for growth calculations
    # --------------------------------------------------------

    try:

        income_statement = (
            stock.income_stmt
        )

    except:

        income_statement = pd.DataFrame()


    # Revenue growth fallback
    if (
        pd.isna(revenue_growth)
        and not income_statement.empty
    ):

        try:

            revenue_rows = [
                "Total Revenue",
                "Operating Revenue"
            ]

            revenue_row = None

            for row in revenue_rows:

                if row in income_statement.index:

                    revenue_row = row
                    break

            if revenue_row is not None:

                values = (
                    income_statement
                    .loc[revenue_row]
                    .dropna()
                    .sort_index()
                )

                if len(values) >= 2:

                    latest = float(values.iloc[-1])
                    previous = float(values.iloc[-2])

                    if previous != 0:

                        revenue_growth = (
                            latest / previous - 1
                        )

        except:

            pass


    # Earnings growth fallback
    if (
        pd.isna(earnings_growth)
        and not income_statement.empty
    ):

        try:

            profit_rows = [
                "Net Income",
                "Net Income Common Stockholders"
            ]

            profit_row = None

            for row in profit_rows:

                if row in income_statement.index:

                    profit_row = row
                    break

            if profit_row is not None:

                values = (
                    income_statement
                    .loc[profit_row]
                    .dropna()
                    .sort_index()
                )

                if len(values) >= 2:

                    latest = float(values.iloc[-1])
                    previous = float(values.iloc[-2])

                    if previous != 0:

                        earnings_growth = (
                            latest / previous - 1
                        )

        except:

            pass


    fundamental_results.append({

        "Stock": name,

        "Ticker": ticker,

        "Sector":
            info.get("sector", "N/A"),

        "P/E":
            pe,

        "P/B":
            pb,

        "ROE %":
            roe * 100
            if not pd.isna(roe)
            else np.nan,

        "Debt/Equity":
            debt_to_equity,

        "Revenue Growth %":
            revenue_growth * 100
            if not pd.isna(revenue_growth)
            else np.nan,

        "Profit Growth %":
            earnings_growth * 100
            if not pd.isna(earnings_growth)
            else np.nan,

        "Dividend Yield %":
            dividend_yield * 100
            if not pd.isna(dividend_yield)
            else np.nan
    })


fundamental_df = pd.DataFrame(
    fundamental_results
)

print(
    fundamental_df.round(2)
    .to_string(index=False)
)


# ============================================================
# 10. SECTOR PEER COMPARISON
# ============================================================

print("\n" + "=" * 70)
print("SECTOR PEER COMPARISON")
print("=" * 70)

for sector in fundamental_df["Sector"].dropna().unique():

    sector_data = fundamental_df[
        fundamental_df["Sector"] == sector
    ]

    print(f"\nSector: {sector}")

    print(
        sector_data[
            [
                "Stock",
                "P/E",
                "P/B",
                "ROE %",
                "Debt/Equity",
                "Revenue Growth %",
                "Profit Growth %",
                "Dividend Yield %"
            ]
        ]
        .round(2)
        .to_string(index=False)
    )


# ============================================================
# 11. TRANSPARENT SCORING SYSTEM
# ============================================================

print("\n" + "=" * 70)
print("STOCK SCORECARD")
print("=" * 70)


score_df = fundamental_df.copy()


# ------------------------------------------------------------
# VALUATION SCORE
#
# Lower P/E = better valuation score
# Lower P/B = better valuation score
# ------------------------------------------------------------

def inverse_score(series):

    clean = series.replace(
        [np.inf, -np.inf],
        np.nan
    )

    minimum = clean.min()
    maximum = clean.max()

    if (
        pd.isna(minimum)
        or pd.isna(maximum)
        or maximum == minimum
    ):

        return pd.Series(
            50.0,
            index=series.index
        )

    score = (
        (maximum - clean)
        / (maximum - minimum)
    ) * 100

    return score.fillna(50)


score_df["PE Score"] = inverse_score(
    score_df["P/E"]
)

score_df["PB Score"] = inverse_score(
    score_df["P/B"]
)

score_df["Valuation Score"] = (
    score_df["PE Score"]
    + score_df["PB Score"]
) / 2


# ------------------------------------------------------------
# QUALITY SCORE
#
# Higher ROE = better
# Lower Debt/Equity = better
# Higher profit growth = better
# ------------------------------------------------------------

def normal_score(series):

    clean = series.replace(
        [np.inf, -np.inf],
        np.nan
    )

    minimum = clean.min()
    maximum = clean.max()

    if (
        pd.isna(minimum)
        or pd.isna(maximum)
        or maximum == minimum
    ):

        return pd.Series(
            50.0,
            index=series.index
        )

    score = (
        (clean - minimum)
        / (maximum - minimum)
    ) * 100

    return score.fillna(50)


score_df["ROE Score"] = normal_score(
    score_df["ROE %"]
)

score_df["Profit Growth Score"] = normal_score(
    score_df["Profit Growth %"]
)

score_df["Debt Score"] = inverse_score(
    score_df["Debt/Equity"]
)

score_df["Quality Score"] = (
    score_df["ROE Score"]
    + score_df["Profit Growth Score"]
    + score_df["Debt Score"]
) / 3


# ------------------------------------------------------------
# MOMENTUM SCORE
# Based on relative performance and technical momentum
# ------------------------------------------------------------

momentum_df = benchmark_df[
    [
        "Stock",
        "Relative Performance %",
    ]
].copy()

momentum_df["Relative Performance Score"] = (
    normal_score(
        momentum_df["Relative Performance %"]
    )
)

# Latest RSI
latest_rsi = []

for ticker, name in STOCKS.items():

    latest_rsi_value = (
        stock_data[ticker]["RSI"]
        .dropna()
        .iloc[-1]
    )

    latest_rsi.append({

        "Stock": name,

        "RSI":
            latest_rsi_value
    })


rsi_df = pd.DataFrame(latest_rsi)

momentum_df = pd.merge(
    momentum_df,
    rsi_df,
    on="Stock"
)


# RSI score:
# Values around 50 are treated as neutral.
# This avoids treating extremely high RSI as automatically better.

momentum_df["RSI Score"] = (
    100
    - abs(momentum_df["RSI"] - 50) * 2
)

momentum_df["RSI Score"] = (
    momentum_df["RSI Score"]
    .clip(0, 100)
)


# Final momentum score
momentum_df["Momentum Score"] = (
    momentum_df["Relative Performance Score"]
    * 0.70
    +
    momentum_df["RSI Score"]
    * 0.30
)


# ------------------------------------------------------------
# COMBINE SCORES
# ------------------------------------------------------------

score_df = pd.merge(
    score_df,
    momentum_df[
        [
            "Stock",
            "Momentum Score"
        ]
    ],
    on="Stock",
    how="left"
)


# Overall score
score_df["Overall Score"] = (
    score_df["Valuation Score"] * 0.33
    +
    score_df["Quality Score"] * 0.34
    +
    score_df["Momentum Score"] * 0.33
)


# Rank for presentation
score_df["Rank"] = (
    score_df["Overall Score"]
    .rank(
        ascending=False,
        method="min"
    )
)


scorecard = score_df[
    [
        "Rank",
        "Stock",
        "Valuation Score",
        "Quality Score",
        "Momentum Score",
        "Overall Score"
    ]
].sort_values("Rank")


print(
    scorecard.round(2)
    .to_string(index=False)
)


# ============================================================
# 12. CHART 1 — PRICE + MOVING AVERAGES
# ============================================================

for ticker, name in STOCKS.items():

    df = stock_data[ticker]

    plt.figure(figsize=(14, 6))

    plt.plot(
        df["Date"],
        df["Close"],
        label="Closing Price"
    )

    plt.plot(
        df["Date"],
        df["MA20"],
        label="MA20"
    )

    plt.plot(
        df["Date"],
        df["MA50"],
        label="MA50"
    )

    plt.title(
        f"{name} - Price and Moving Averages"
    )

    plt.xlabel("Date")
    plt.ylabel("Price (₹)")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

    print(
        f"Interpretation — {name}: "
        "The moving averages help identify the stock's "
        "longer-term price trend. When the price remains "
        "above the moving averages, the historical trend "
        "has been relatively stronger; when it falls below "
        "them, the trend has weakened."
    )


# ============================================================
# 13. CHART 2 — RSI
# ============================================================

for ticker, name in STOCKS.items():

    df = stock_data[ticker]

    plt.figure(figsize=(14, 5))

    plt.plot(
        df["Date"],
        df["RSI"],
        label="RSI"
    )

    plt.axhline(
        70,
        linestyle="--",
        label="70"
    )

    plt.axhline(
        30,
        linestyle="--",
        label="30"
    )

    plt.title(
        f"{name} - RSI (14-Day)"
    )

    plt.xlabel("Date")
    plt.ylabel("RSI")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

    print(
        f"Interpretation — {name}: "
        "RSI measures the magnitude of recent price gains "
        "and losses. Readings near the upper range indicate "
        "strong recent upward momentum, while lower readings "
        "indicate weaker recent momentum. RSI should be "
        "treated as a descriptive indicator rather than a "
        "standalone trading signal."
    )


# ============================================================
# 14. CHART 3 — MACD
# ============================================================

for ticker, name in STOCKS.items():

    df = stock_data[ticker]

    plt.figure(figsize=(14, 5))

    plt.plot(
        df["Date"],
        df["MACD"],
        label="MACD"
    )

    plt.plot(
        df["Date"],
        df["MACD Signal"],
        label="Signal"
    )

    plt.axhline(0, linewidth=1)

    plt.title(
        f"{name} - MACD"
    )

    plt.xlabel("Date")
    plt.ylabel("MACD")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

    print(
        f"Interpretation — {name}: "
        "MACD compares short-term and longer-term exponential "
        "moving averages. The relationship between the MACD "
        "and signal line describes changes in historical "
        "momentum."
    )


# ============================================================
# 15. CHART 4 — BOLLINGER BANDS
# ============================================================

for ticker, name in STOCKS.items():

    df = stock_data[ticker]

    plt.figure(figsize=(14, 6))

    plt.plot(
        df["Date"],
        df["Close"],
        label="Close"
    )

    plt.plot(
        df["Date"],
        df["BB Upper"],
        label="Upper Band"
    )

    plt.plot(
        df["Date"],
        df["BB Middle"],
        label="Middle Band"
    )

    plt.plot(
        df["Date"],
        df["BB Lower"],
        label="Lower Band"
    )

    plt.title(
        f"{name} - Bollinger Bands"
    )

    plt.xlabel("Date")
    plt.ylabel("Price (₹)")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

    print(
        f"Interpretation — {name}: "
        "Bollinger Bands show the stock price relative to "
        "its rolling average and historical price variability. "
        "Wider bands indicate greater recent variability, "
        "while narrower bands indicate lower variability."
    )


# ============================================================
# 16. CHART 5 — SUPPORT AND RESISTANCE
# ============================================================

for ticker, name in STOCKS.items():

    df = stock_data[ticker]

    recent = df.tail(500)

    plt.figure(figsize=(14, 6))

    plt.plot(
        recent["Date"],
        recent["Close"],
        label="Close"
    )

    plt.plot(
        recent["Date"],
        recent["Support 20D"],
        label="20D Support"
    )

    plt.plot(
        recent["Date"],
        recent["Resistance 20D"],
        label="20D Resistance"
    )

    plt.title(
        f"{name} - Support and Resistance"
    )

    plt.xlabel("Date")
    plt.ylabel("Price (₹)")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

    print(
        f"Interpretation — {name}: "
        "The rolling support and resistance levels represent "
        "recent 20-trading-day lows and highs. They describe "
        "historical price boundaries and should not be treated "
        "as guaranteed future price levels."
    )


# ============================================================
# 17. CHART 6 — RELATIVE PERFORMANCE VS NIFTY
# ============================================================

comparison = pd.DataFrame()

for ticker, name in STOCKS.items():

    stock = stock_data[ticker][
        ["Date", "Close"]
    ].copy()

    stock["Normalized"] = (
        stock["Close"]
        / stock["Close"].iloc[0]
    ) * 100

    stock = stock[
        ["Date", "Normalized"]
    ]

    stock = stock.rename(
        columns={
            "Normalized": name
        }
    )

    if comparison.empty:

        comparison = stock

    else:

        comparison = pd.merge(
            comparison,
            stock,
            on="Date",
            how="outer"
        )


nifty_comparison = nifty[
    ["Date", "Close"]
].copy()

nifty_comparison["Nifty 50"] = (
    nifty_comparison["Close"]
    / nifty_comparison["Close"].iloc[0]
) * 100

nifty_comparison = nifty_comparison[
    ["Date", "Nifty 50"]
]

comparison = pd.merge(
    comparison,
    nifty_comparison,
    on="Date",
    how="inner"
)

plt.figure(figsize=(14, 7))

for name in STOCKS.values():

    plt.plot(
        comparison["Date"],
        comparison[name],
        label=name
    )

plt.plot(
    comparison["Date"],
    comparison["Nifty 50"],
    label="Nifty 50"
)

plt.title(
    "Relative Performance vs Nifty 50"
)

plt.xlabel("Date")
plt.ylabel("Normalized Value (Base = 100)")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()

print(
    "Interpretation — Relative Performance: "
    "All series are normalized to 100 at the beginning "
    "of the common period. A higher ending value represents "
    "higher cumulative historical performance over that "
    "period relative to the starting value."
)


# ============================================================
# 18. CHART 7 — CORRELATION HEATMAP
# ============================================================

plt.figure(figsize=(9, 7))

plt.imshow(
    correlation_matrix,
    interpolation="nearest",
    aspect="auto"
)

plt.colorbar(
    label="Correlation"
)

plt.xticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(correlation_matrix.index)),
    correlation_matrix.index
)

plt.title(
    "Stock Return Correlation Matrix"
)

plt.tight_layout()

plt.show()

print(
    "Interpretation — Correlation: "
    "Correlation ranges from -1 to +1. Higher positive "
    "values indicate that two stocks' daily returns have "
    "historically moved more closely together, while values "
    "near zero indicate a weaker linear relationship. "
    "Correlation does not establish causation."
)


# ============================================================
# 19. CHART 8 — SCORECARD
# ============================================================

score_plot = scorecard.set_index("Stock")[
    [
        "Valuation Score",
        "Quality Score",
        "Momentum Score"
    ]
]

score_plot.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title(
    "Stock Scorecard"
)

plt.xlabel("Stock")
plt.ylabel("Score (0–100)")

plt.xticks(rotation=45)

plt.legend()

plt.grid(axis="y")

plt.tight_layout()

plt.show()

print(
    "Interpretation — Scorecard: "
    "The scorecard combines valuation, quality and momentum "
    "into transparent component scores. It is a descriptive "
    "framework for comparing the selected stocks, not a "
    "prediction of future returns."
)


# ============================================================
# 20. SAVE RESULTS
# ============================================================

print("\n" + "=" * 70)
print("SAVING RESULTS")
print("=" * 70)


technical_summary_df.to_csv(
    "technical_summary.csv",
    index=False
)

benchmark_df.to_csv(
    "benchmark_comparison.csv",
    index=False
)

correlation_matrix.to_csv(
    "stock_correlation.csv"
)

fundamental_df.to_csv(
    "fundamental_analysis.csv",
    index=False
)

scorecard.to_csv(
    "stock_scorecard.csv",
    index=False
)

comparison.to_csv(
    "relative_performance.csv",
    index=False
)


# Save individual analyzed datasets

for ticker, name in STOCKS.items():

    filename = (
        ticker.replace(".NS", "")
        + "_analyzed.csv"
    )

    stock_data[ticker].to_csv(
        filename,
        index=False
    )


print("\nFiles created:")

print("- technical_summary.csv")
print("- benchmark_comparison.csv")
print("- stock_correlation.csv")
print("- fundamental_analysis.csv")
print("- stock_scorecard.csv")
print("- relative_performance.csv")

for ticker in STOCKS:

    print(
        "- "
        + ticker.replace(".NS", "")
        + "_analyzed.csv"
    )


print("\n" + "=" * 70)
print("PROJECT ANALYSIS COMPLETED")
print("=" * 70)

