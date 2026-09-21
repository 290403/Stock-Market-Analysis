-- ============================================================
-- STOCK MARKET PERFORMANCE & RISK ANALYSIS
-- SQL ANALYSIS FILE
-- Database: PostgreSQL
-- ============================================================


-- ============================================================
-- 1. TECHNICAL ANALYSIS
-- Table: technical_summary
-- ============================================================

-- View complete technical summary
SELECT *
FROM technical_summary;


-- Stocks with the highest total return
SELECT
    "Stock",
    "Total Return %",
    "RSI",
    "MACD",
    "MACD Signal",
    "30D Volatility",
    "Max Drawdown %",
    "Support",
    "Resistance"
FROM technical_summary
ORDER BY "Total Return %" DESC;


-- Stocks with the highest volatility
SELECT
    "Stock",
    "30D Volatility"
FROM technical_summary
ORDER BY "30D Volatility" DESC;


-- Stocks with the lowest maximum drawdown
SELECT
    "Stock",
    "Max Drawdown %"
FROM technical_summary
ORDER BY "Max Drawdown %" DESC;


-- Stocks with RSI above 70
SELECT
    "Stock",
    "RSI"
FROM technical_summary
WHERE "RSI" > 70
ORDER BY "RSI" DESC;


-- Stocks with RSI below 30
SELECT
    "Stock",
    "RSI"
FROM technical_summary
WHERE "RSI" < 30
ORDER BY "RSI" ASC;


-- Compare current price with support and resistance
SELECT
    "Stock",
    "Latest Price",
    "Support",
    "Resistance",
    ("Latest Price" - "Support") AS "Distance From Support",
    ("Resistance" - "Latest Price") AS "Distance From Resistance"
FROM technical_summary
ORDER BY "Stock";


-- ============================================================
-- 2. BENCHMARK ANALYSIS
-- Table: benchmark_comparison
-- ============================================================

-- Complete benchmark comparison
SELECT *
FROM benchmark_comparison;


-- Stocks ranked by relative performance against Nifty 50
SELECT
    "Stock",
    "Stock Return %",
    "Nifty Return %",
    "Relative Performance %",
    "Beta"
FROM benchmark_comparison
ORDER BY "Relative Performance %" DESC;


-- Stocks that outperformed Nifty 50
SELECT
    "Stock",
    "Stock Return %",
    "Nifty Return %",
    "Relative Performance %",
    "Beta"
FROM benchmark_comparison
WHERE "Relative Performance %" > 0
ORDER BY "Relative Performance %" DESC;


-- Stocks that underperformed Nifty 50
SELECT
    "Stock",
    "Stock Return %",
    "Nifty Return %",
    "Relative Performance %",
    "Beta"
FROM benchmark_comparison
WHERE "Relative Performance %" < 0
ORDER BY "Relative Performance %" ASC;


-- Stocks with Beta greater than 1
SELECT
    "Stock",
    "Beta"
FROM benchmark_comparison
WHERE "Beta" > 1
ORDER BY "Beta" DESC;


-- Stocks with Beta below 1
SELECT
    "Stock",
    "Beta"
FROM benchmark_comparison
WHERE "Beta" < 1
ORDER BY "Beta" ASC;


-- ============================================================
-- 3. FUNDAMENTAL ANALYSIS
-- Table: fundamental_analysis
-- ============================================================

-- Complete fundamental analysis
SELECT *
FROM fundamental_analysis;


-- Compare valuation metrics
SELECT
    "Stock",
    "P/E",
    "P/B"
FROM fundamental_analysis
ORDER BY "P/E" ASC;


-- Compare Return on Equity
SELECT
    "Stock",
    "ROE %"
FROM fundamental_analysis
WHERE "ROE %" IS NOT NULL
ORDER BY "ROE %" DESC;


-- Compare Debt-to-Equity
SELECT
    "Stock",
    "Debt/Equity"
FROM fundamental_analysis
WHERE "Debt/Equity" IS NOT NULL
ORDER BY "Debt/Equity" ASC;


-- Compare revenue growth
SELECT
    "Stock",
    "Revenue Growth %"
FROM fundamental_analysis
WHERE "Revenue Growth %" IS NOT NULL
ORDER BY "Revenue Growth %" DESC;


-- Compare profit growth
SELECT
    "Stock",
    "Profit Growth %"
FROM fundamental_analysis
WHERE "Profit Growth %" IS NOT NULL
ORDER BY "Profit Growth %" DESC;


-- Compare dividend yield
SELECT
    "Stock",
    "Dividend Yield %"
FROM fundamental_analysis
WHERE "Dividend Yield %" IS NOT NULL
ORDER BY "Dividend Yield %" DESC;


-- Fundamental comparison of all stocks
SELECT
    "Stock",
    "Sector",
    "P/E",
    "P/B",
    "ROE %",
    "Debt/Equity",
    "Revenue Growth %",
    "Profit Growth %",
    "Dividend Yield %"
FROM fundamental_analysis
ORDER BY "Stock";


-- ============================================================
-- 4. STOCK SCORECARD
-- Table: stock_scorecard
-- ============================================================

-- Complete scorecard
SELECT *
FROM stock_scorecard;


-- View score components
SELECT
    "Rank",
    "Stock",
    "Valuation Score",
    "Quality Score",
    "Momentum Score",
    "Overall Score"
FROM stock_scorecard
ORDER BY "Rank";


-- Compare overall scores
SELECT
    "Stock",
    "Overall Score"
FROM stock_scorecard
ORDER BY "Overall Score" DESC;


-- Compare valuation scores
SELECT
    "Stock",
    "Valuation Score"
FROM stock_scorecard
ORDER BY "Valuation Score" DESC;


-- Compare quality scores
SELECT
    "Stock",
    "Quality Score"
FROM stock_scorecard
ORDER BY "Quality Score" DESC;


-- Compare momentum scores
SELECT
    "Stock",
    "Momentum Score"
FROM stock_scorecard
ORDER BY "Momentum Score" DESC;


-- ============================================================
-- 5. RELATIVE PERFORMANCE
-- Table: relative_performance
-- ============================================================

-- Complete relative performance matrix
SELECT *
FROM relative_performance;


-- Average relative performance by stock
SELECT
    "Stock",
    AVG("Stock Return %") AS "Average Stock Return",
    AVG("Nifty Return %") AS "Average Nifty Return",
    AVG("Relative Performance %") AS "Average Relative Performance"
FROM benchmark_comparison
GROUP BY "Stock"
ORDER BY "Average Relative Performance" DESC;


-- ============================================================
-- 6. CORRELATION ANALYSIS
-- Table: stock_correlation
-- ============================================================

-- Complete correlation matrix
SELECT *
FROM stock_correlation;


-- ============================================================
-- 7. INDIVIDUAL STOCK ANALYSIS
-- ============================================================

-- ------------------------------------------------------------
-- RELIANCE INDUSTRIES
-- Table: reliance
-- ------------------------------------------------------------

-- Highest closing price
SELECT
    "Date",
    "Close"
FROM reliance
ORDER BY "Close" DESC
LIMIT 1;


-- Lowest closing price
SELECT
    "Date",
    "Close"
FROM reliance
ORDER BY "Close" ASC
LIMIT 1;


-- Highest daily return
SELECT
    "Date",
    "Close",
    "Daily Return"
FROM reliance
WHERE "Daily Return" IS NOT NULL
ORDER BY "Daily Return" DESC
LIMIT 10;


-- Lowest daily return
SELECT
    "Date",
    "Close",
    "Daily Return"
FROM reliance
WHERE "Daily Return" IS NOT NULL
ORDER BY "Daily Return" ASC
LIMIT 10;


-- Highest trading volume
SELECT
    "Date",
    "Volume"
FROM reliance
ORDER BY "Volume" DESC
LIMIT 10;


-- Highest volatility periods
SELECT
    "Date",
    "30D Volatility"
FROM reliance
WHERE "30D Volatility" IS NOT NULL
ORDER BY "30D Volatility" DESC
LIMIT 10;


-- ------------------------------------------------------------
-- ONGC
-- ------------------------------------------------------------

SELECT
    "Date",
    "Close"
FROM ongc
ORDER BY "Close" DESC
LIMIT 1;


SELECT
    "Date",
    "Close"
FROM ongc
ORDER BY "Close" ASC
LIMIT 1;


SELECT
    "Date",
    "Close",
    "Daily Return"
FROM ongc
WHERE "Daily Return" IS NOT NULL
ORDER BY "Daily Return" DESC
LIMIT 10;


SELECT
    "Date",
    "Close",
    "Daily Return"
FROM ongc
WHERE "Daily Return" IS NOT NULL
ORDER BY "Daily Return" ASC
LIMIT 10;


SELECT
    "Date",
    "Volume"
FROM ongc
ORDER BY "Volume" DESC
LIMIT 10;


SELECT
    "Date",
    "30D Volatility"
FROM ongc
WHERE "30D Volatility" IS NOT NULL
ORDER BY "30D Volatility" DESC
LIMIT 10;


-- ------------------------------------------------------------
-- BPCL
-- ------------------------------------------------------------

SELECT
    "Date",
    "Close"
FROM bpcl
ORDER BY "Close" DESC
LIMIT 1;


SELECT
    "Date",
    "Close"
FROM bpcl
ORDER BY "Close" ASC
LIMIT 1;


SELECT
    "Date",
    "Close",
    "Daily Return"
FROM bpcl
WHERE "Daily Return" IS NOT NULL
ORDER BY "Daily Return" DESC
LIMIT 10;


SELECT
    "Date",
    "Close",
    "Daily Return"
FROM bpcl
WHERE "Daily Return" IS NOT NULL
ORDER BY "Daily Return" ASC
LIMIT 10;


SELECT
    "Date",
    "Volume"
FROM bpcl
ORDER BY "Volume" DESC
LIMIT 10;


SELECT
    "Date",
    "30D Volatility"
FROM bpcl
WHERE "30D Volatility" IS NOT NULL
ORDER BY "30D Volatility" DESC
LIMIT 10;


-- ------------------------------------------------------------
-- IOC
-- ------------------------------------------------------------

SELECT
    "Date",
    "Close"
FROM ioc
ORDER BY "Close" DESC
LIMIT 1;


SELECT
    "Date",
    "Close"
FROM ioc
ORDER BY "Close" ASC
LIMIT 1;


SELECT
    "Date",
    "Close",
    "Daily Return"
FROM ioc
WHERE "Daily Return" IS NOT NULL
ORDER BY "Daily Return" DESC
LIMIT 10;


SELECT
    "Date",
    "Close",
    "Daily Return"
FROM ioc
WHERE "Daily Return" IS NOT NULL
ORDER BY "Daily Return" ASC
LIMIT 10;


SELECT
    "Date",
    "Volume"
FROM ioc
ORDER BY "Volume" DESC
LIMIT 10;


SELECT
    "Date",
    "30D Volatility"
FROM ioc
WHERE "30D Volatility" IS NOT NULL
ORDER BY "30D Volatility" DESC
LIMIT 10;


-- ============================================================
-- 8. YEARLY PERFORMANCE
-- ============================================================

-- Reliance yearly average return
SELECT
    EXTRACT(YEAR FROM "Date") AS "Year",
    AVG("Daily Return") AS "Average Daily Return"
FROM reliance
WHERE "Daily Return" IS NOT NULL
GROUP BY EXTRACT(YEAR FROM "Date")
ORDER BY "Year";


-- ONGC yearly average return
SELECT
    EXTRACT(YEAR FROM "Date") AS "Year",
    AVG("Daily Return") AS "Average Daily Return"
FROM ongc
WHERE "Daily Return" IS NOT NULL
GROUP BY EXTRACT(YEAR FROM "Date")
ORDER BY "Year";


-- BPCL yearly average return
SELECT
    EXTRACT(YEAR FROM "Date") AS "Year",
    AVG("Daily Return") AS "Average Daily Return"
FROM bpcl
WHERE "Daily Return" IS NOT NULL
GROUP BY EXTRACT(YEAR FROM "Date")
ORDER BY "Year";


-- IOC yearly average return
SELECT
    EXTRACT(YEAR FROM "Date") AS "Year",
    AVG("Daily Return") AS "Average Daily Return"
FROM ioc
WHERE "Daily Return" IS NOT NULL
GROUP BY EXTRACT(YEAR FROM "Date")
ORDER BY "Year";


-- ============================================================
-- 9. MOVING AVERAGE ANALYSIS
-- ============================================================

-- Reliance latest moving averages
SELECT
    "Date",
    "Close",
    "MA20",
    "MA50"
FROM reliance
ORDER BY "Date" DESC
LIMIT 10;


-- ONGC latest moving averages
SELECT
    "Date",
    "Close",
    "MA20",
    "MA50"
FROM ongc
ORDER BY "Date" DESC
LIMIT 10;


-- BPCL latest moving averages
SELECT
    "Date",
    "Close",
    "MA20",
    "MA50"
FROM bpcl
ORDER BY "Date" DESC
LIMIT 10;


-- IOC latest moving averages
SELECT
    "Date",
    "Close",
    "MA20",
    "MA50"
FROM ioc
ORDER BY "Date" DESC
LIMIT 10;


-- ============================================================
-- 10. MOMENTUM ANALYSIS
-- ============================================================

-- Reliance RSI and MACD
SELECT
    "Date",
    "RSI",
    "MACD",
    "MACD Signal",
    "MACD Histogram"
FROM reliance
ORDER BY "Date" DESC
LIMIT 20;


-- ONGC RSI and MACD
SELECT
    "Date",
    "RSI",
    "MACD",
    "MACD Signal",
    "MACD Histogram"
FROM ongc
ORDER BY "Date" DESC
LIMIT 20;


-- BPCL RSI and MACD
SELECT
    "Date",
    "RSI",
    "MACD",
    "MACD Signal",
    "MACD Histogram"
FROM bpcl
ORDER BY "Date" DESC
LIMIT 20;


-- IOC RSI and MACD
SELECT
    "Date",
    "RSI",
    "MACD",
    "MACD Signal",
    "MACD Histogram"
FROM ioc
ORDER BY "Date" DESC
LIMIT 20;


-- ============================================================
-- 11. SUPPORT & RESISTANCE
-- ============================================================

SELECT
    "Date",
    "Close",
    "Support 20D",
    "Resistance 20D"
FROM reliance
ORDER BY "Date" DESC
LIMIT 20;


SELECT
    "Date",
    "Close",
    "Support 20D",
    "Resistance 20D"
FROM ongc
ORDER BY "Date" DESC
LIMIT 20;


SELECT
    "Date",
    "Close",
    "Support 20D",
    "Resistance 20D"
FROM bpcl
ORDER BY "Date" DESC
LIMIT 20;


SELECT
    "Date",
    "Close",
    "Support 20D",
    "Resistance 20D"
FROM ioc
ORDER BY "Date" DESC
LIMIT 20;


-- ============================================================
-- END OF STOCK ANALYSIS SQL
-- ============================================================