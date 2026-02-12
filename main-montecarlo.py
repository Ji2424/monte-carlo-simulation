import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
TICKER = "RR.L"        # Rolls-Royce (London)
SIMULATIONS = 10_000   # Multiverses
DAYS_AHEAD = 252       # 1 Year

def plot_simulation_results(price_paths, final_prices, start_price, expected_price):
    """
    Generates two charts and saves them as 'monte_carlo_results.png'
    """
    # Create a figure with 2 subplots (side by side)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # --- Chart 1: The "Spaghetti" Plot (Price Paths) ---
    # We only plot the first 50 paths to keep it readable
    ax1.plot(price_paths[:, :50], alpha=0.6) 
    ax1.axhline(y=start_price, color='black', linestyle='--', label="Start Price")
    ax1.set_title(f"Monte Carlo: First 50 Simulated Paths for {TICKER}")
    ax1.set_ylabel("Price (£)")
    ax1.set_xlabel("Days into Future")
    ax1.legend()

    # --- Chart 2: The Histogram (Distribution of Final Prices) ---
    ax2.hist(final_prices, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    ax2.axvline(x=expected_price, color='red', linestyle='--', linewidth=2, label=f"Avg: £{expected_price:.2f}")
    ax2.axvline(x=start_price, color='black', linestyle='--', linewidth=2, label="Start Price")
    ax2.set_title(f"Distribution of Final Prices (After {DAYS_AHEAD} Days)")
    ax2.set_xlabel("Final Price (£)")
    ax2.set_ylabel("Frequency")
    ax2.legend()

    # Save the file
    plt.tight_layout()
    plt.savefig("monte_carlo_results.png")
    print("\n✅ Graph saved successfully to 'monte_carlo_results.png'")
    # Note: In Codespaces, look at the file explorer on the left to find this image!

def run_monte_carlo():
    # --- STEP 1: GET REAL DATA ---
    print(f"--- 1. Downloading Data for {TICKER} ---")
    stock = yf.Ticker(TICKER)
    history = stock.history(period="1y")
    
    if history.empty:
        print("Error: Could not download data.")
        return

    current_price = history['Close'].iloc[-1]
    
    # Fix Pence vs Pounds
    currency = stock.info.get('currency', 'GBP')
    if currency == 'GBp':
        print(f"   > Detected currency in Pence (GBp). Converting to Pounds...")
        current_price = current_price / 100
    
    print(f"   > Current Price: £{current_price:.2f}")

    # --- STEP 2: CALCULATE VOLATILITY ---
    daily_returns = history['Close'].pct_change().dropna()
    daily_volatility = daily_returns.std()
    annual_volatility = daily_volatility * np.sqrt(252)
    
    print(f"   > Annualized Volatility: {annual_volatility*100:.2f}%")

    # --- STEP 3: RUN SIMULATION ---
    print(f"\n--- 3. Running {SIMULATIONS} Simulations ---")
    
    price_paths = np.zeros((DAYS_AHEAD, SIMULATIONS))
    price_paths[0] = current_price
    
    for t in range(1, DAYS_AHEAD):
        random_shocks = np.random.normal(0, daily_volatility, SIMULATIONS)
        price_paths[t] = price_paths[t-1] * (1 + random_shocks)
        
    # --- STEP 4: RESULTS & PLOTTING ---
    final_prices = price_paths[-1]
    expected_price = np.mean(final_prices)
    
    print(f"\n--- RESULTS ---")
    print(f"Expected Price in 1 Year: £{expected_price:.2f}")
    
    prob_increase = np.sum(final_prices > current_price) / SIMULATIONS
    print(f"Chance of Price Increase: {prob_increase*100:.1f}%")

    # CALL THE NEW PLOTTING FUNCTION
    plot_simulation_results(price_paths, final_prices, current_price, expected_price)

if __name__ == "__main__":
    run_monte_carlo()