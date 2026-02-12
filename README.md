Monte Carlo Simulation for Stock Price Forecasting

Overview
This project implements a Monte Carlo simulation to model one-year forward price dynamics using historical volatility estimated from market data. The simulation generates 10,000 stochastic price paths and evaluates expected terminal price and probability of positive return.

Methodology

Historical daily returns computed using yfinance

Annualised volatility estimated from historical data

Geometric Brownian Motion used to simulate price evolution

10,000 simulation paths over 252 trading days

Results

<img width="1500" height="600" alt="monte_carlo_results" src="https://github.com/user-attachments/assets/99498cb1-c049-40bf-94b6-c2f8959b451f" />


Expected 1-year price: £12.58

Probability of price increase: 43.1%

