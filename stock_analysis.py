import yfinance as yf
import pandas as pd
import numpy as np

# ==========================================
# 1. SETTINGS
# ==========================================

TICKER = "RELIANCE.NS"

START_DATE = "2000-01-01"
END_DATE = None   # None = download up to the latest available date


# ==========================================
# 2. DOWNLOAD DATA
# ==========================================

print(f"Downloading data for {TICKER}...")

df = yf.download(
    TICKER,
    start=START_DATE,
    end=END_DATE,
    interval="1d",
    auto_adjust=False,
    progress=True
)


# ==========================================
# 3. CLEAN COLUMN NAMES
# ==========================================

# yfinance may return MultiIndex columns
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.reset_index()

# Rename columns
df.columns = [str(col).strip() for col in df.columns]

# Make sure Date is datetime
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date
df = df.sort_values("Date").reset_index(drop=True)


# ==========================================
# 4. REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates(subset=["Date"])


# ==========================================
# 5. HANDLE MISSING VALUES
# ==========================================

print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Remove rows where essential price data is missing
df = df.dropna(subset=["Open", "High", "Low", "Close", "Volume"])


# ==========================================
# 6. CALCULATE DAILY RETURN
# ==========================================

df["Daily Return"] = df["Close"].pct_change() * 100


# ==========================================
# 7. CALCULATE MOVING AVERAGES
# ==========================================

df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()


# ==========================================
# 8. CALCULATE 30-DAY VOLATILITY
# ==========================================

df["30D Volatility"] = (
    df["Daily Return"]
    .rolling(window=30)
    .std()
)


# ==========================================
# 9. CALCULATE CUMULATIVE RETURN
# ==========================================

df["Cumulative Return"] = (
    (1 + df["Daily Return"] / 100)
    .cumprod() - 1
)

df["Cumulative Return %"] = (
    df["Cumulative Return"] * 100
)


# ==========================================
# 10. CALCULATE MAXIMUM DRAWDOWN
# ==========================================

df["Running Maximum"] = df["Close"].cummax()

df["Drawdown"] = (
    (df["Close"] - df["Running Maximum"])
    / df["Running Maximum"]
) * 100


# ==========================================
# 11. DISPLAY BASIC INFORMATION
# ==========================================

print("\n==========================================")
print("STOCK DATA SUMMARY")
print("==========================================")

print(f"Ticker: {TICKER}")
print(f"Start Date: {df['Date'].min().date()}")
print(f"End Date: {df['Date'].max().date()}")
print(f"Number of Rows: {len(df)}")
print(f"Number of Columns: {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


# ==========================================
# 12. SAVE CLEANED DATA
# ==========================================

output_file = "RELIANCE_analyzed.csv"

df.to_csv(output_file, index=False)

print(f"\nCleaned data saved to: {output_file}")


# ==========================================
# 13. FINAL CHECK
# ==========================================

print("\nFinal missing values:")
print(df.isnull().sum())

print("\nData download and cleaning completed successfully!")

