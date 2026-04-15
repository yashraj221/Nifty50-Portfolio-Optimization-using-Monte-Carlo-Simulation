import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

tickers = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "BAJFINANCE.NS", "MARUTI.NS", "ICICIBANK.NS",
    "M&M.NS", "SUNPHARMA.NS", "LT.NS"
]

data = yf.download(tickers, start="2022-01-01", end="2026-04-01")["Close"]
print(data.shape)
print(data.head())
print(data.isnull().sum())

# Calculate daily return 
returns = data.pct_change().dropna()

# Calculate annual expected returns and covariance matrix
import numpy as np

annual_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

print("Annual Expected Returns:")
print(annual_returns.round(4))
print("\nCovariance Matrix Shape:", cov_matrix.shape)


# Monte carlo simulation 
num_portfolios = 10000
results = np.zeros((3, num_portfolios))
weights_record = []

for i in range(num_portfolios):
    # Random weights that sum to 1
    weights = np.random.random(10)
    weights = weights / np.sum(weights)
    weights_record.append(weights)

    # Portfolio return 
    port_return = np.dot(weights, annual_returns)

    # Portfolio volatility 
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    # Sharpe ratio (assuming risk-free rate of 6% for India)
    sharpe = (port_return - 0.0525) / port_volatility

    results[0, i] = port_return
    results[1, i] = port_volatility
    results[2, i] = sharpe

print("Simulation completed.")
print(f"Max Sharpe Ratio: {results[2].max():.4f}")
print(f"Min volatility: {results[1].min():.4f}")


# Visualization

# Convert results to dataframe 
results_df = pd.DataFrame({
    'Return': results[0],
    'volatility': results[1],
    'Sharpe': results[2]
})

# Find max Sharpe and min volatility portfolios 
max_sharpe_idx = results[2].argmax()
min_vol_idx = results[1].argmin()

plt.figure(figsize=(12, 7))
scatter = plt.scatter(results[1], results[0],
                      c=results[2], cmap='viridis',
                      alpha=0.5, s=10)
plt.colorbar(scatter, label='Sharpe Ratio')

# Plot max Sharpe Portfolio
plt.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx],
            color='red', marker='*', s=300, label='Max Sharpe Ratio')

# Plot min volatility portfolio 
plt.scatter(results[1, min_vol_idx], results[0, min_vol_idx],
            color='blue', marker='*', s=300, label = 'Min Volatility')

plt.title('Efficient Frontier - Nifty50 Portfolio Optimization (2022-2026)')
plt.xlabel('Portfolio volatiility (Risk)')
plt.ylabel('Portfolio Return')
plt.legend()
plt.tight_layout()
plt.savefig('efficent_frontier.png')
plt.show()

# Get optimal portfolio weights
max_sharpe_weights = weights_record[max_sharpe_idx]
min_vol_weights = weights_record[min_vol_idx]

ticker_names = [t.replace('.NS', '') for t in tickers]

print("\n--- Maximum Sharpe Ration Portfolio ---")
print(f"Return: {results[0, max_sharpe_idx]:.2%}")
print(f"Volatility: {results[1, max_sharpe_idx]:.2%}")
print(f"Sharpe Ratio: {results[2, max_sharpe_idx]:.4f}")
print("\nWeights:")
for ticker, weight in zip(ticker_names, max_sharpe_weights):
    print(f"{ticker}: {weight:.2%}")

print("\n--- Minimum Volatility Portfolio ---")
print(f"Return: {results[0, min_vol_idx]:.2%}")
print(f"Volatility: {results[1, min_vol_idx]:.2%}")
print(f"Sharpe Ratio: {results[2, min_vol_idx]:.4f}")
print("\nWeights:")
for ticker, weight in zip(ticker_names, min_vol_weights):
    print(f"  {ticker}: {weight:.2%}")

# weights visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Max Sharpe weights
ax1.bar(ticker_names, max_sharpe_weights * 100, color='red', alpha=0.7)
ax1.set_title('Maximum Sharpe Ratio Portfolio Weights')
ax1.set_xlabel('Stock')
ax1.set_ylabel('Weight (%)')
ax1.tick_params(axis='x', rotation=45)

# Min Volatility weights
ax2.bar(ticker_names, min_vol_weights * 100, color='blue', alpha=0.7)
ax2.set_title('Minimum Volatility Portfolio Weights')
ax2.set_xlabel('Stock')
ax2.set_ylabel('Weight (%)')
ax2.tick_params(axis='x', rotation=45)

plt.suptitle('Optimal Portfolio Weights - Monte Carlo Simulation', 
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('portfolio_weights.png')
plt.show()