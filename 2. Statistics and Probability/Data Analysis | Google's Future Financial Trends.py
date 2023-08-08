"""
Title: Future Financial Trend Analysis
Author: Jasmine Sharron
Date: 02 August 2023
Purpose: To perform Exploratory Data Analysis (EDA) and inferential statistics on Google's historical financial data.
"""

# Import appropriate libraries
import pandas as pd
from scipy.stats import shapiro, ttest_1samp
from statsmodels.tsa.stattools import adfuller, acf, pacf, plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt


class FinancialDataAnalyzer:
    def __init__(self, filename):
        """Initialize with the data file's name and a placeholder for the data."""
        self.filename = filename
        self.data = None

    def load_data(self):
        """Load financial data from a CSV file."""
        self.data = pd.read_csv(self.filename, index_col=0)

    def calculate_metrics(self):
        """Calculate various financial metrics and indicators for trend analysis."""
        
        # NOTE: Might give NaN values for the first few rows of the DataFrame 
        #       -- need a certain number of data points to start calculating.

        # Moving Averages: Smooth data to identify trends
        self.data['MA10'] = self.data['Close'].rolling(10).mean()   # 10-day moving average
        self.data['MA50'] = self.data['Close'].rolling(50).mean()   # 50-day moving average
        self.data['SMA20'] = self.data['Close'].rolling(20).mean()  # 20-day, for Bollinger Bands
        
        # Moving Standard Deviation: Measures volatility
        self.data['STD10'] = self.data['Close'].rolling(10).std()   # 10-day
        self.data['StdDev'] = self.data['Close'].rolling(20).std()  # 20-day, for Bollinger Bands
        
        # Bollinger Bands: Identifies periods of high or low volatility
        self.data['Upper Band'] = self.data['SMA20'] + (self.data['StdDev'] * 2)
        self.data['Lower Band'] = self.data['SMA20'] - (self.data['StdDev'] * 2)
        
        # Calculate Daily & Cumulative Returns: Provides insights on potential profitability
        self.data['Daily Returns'] = self.data['Close'].pct_change()
        self.data['Cumulative Return'] = (self.data['Close'] / self.data['Close'].iloc[0]) - 1
        
        # Relative Strength Index (RSI): Identifies overbought or oversold conditions
        delta = self.data['Close'].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        average_gain = up.rolling(14).mean()
        average_loss = abs(down.rolling(14).mean())
        rs = average_gain / average_loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # Moving Average Convergence Divergence (MACD): Indicates changes in trend strength, direction, and momentum
        self.data['12 EMA'] = self.data['Close'].ewm(span=12).mean()
        self.data['26 EMA'] = self.data['Close'].ewm(span=26).mean()
        self.data['MACD'] = self.data['12 EMA'] - self.data['26 EMA']

        # Volume Weighted Average Price (VWAP): Provides insights on trend and entry/exit points
        self.data['Cumulative Volume'] = self.data['Volume'].cumsum()
        self.data['Cumulative VWAP'] = (self.data['Close'] * self.data['Volume']).cumsum()
        self.data['VWAP'] = self.data['Cumulative VWAP'] / self.data['Cumulative Volume']

    def visualize_data(self):
        """Calculate various financial metrics and indicators for trend analysis."""
        
        # Set style
        sns.set_style("whitegrid")

        # Plot stock closing price and moving averages
        plt.figure(figsize=(14, 7))
        self.data['Close'].plot(label='Closing Price', alpha=0.8)
        self.data['MA10'].plot(label='10 Day Avg', alpha=0.8)
        self.data['MA50'].plot(label='50 Day Avg', alpha=0.8)
        plt.title('Stock Closing Price and Moving Averages')
        plt.legend()
        plt.show()

        # Plot Bollinger Bands
        plt.figure(figsize=(14, 7))
        self.data['Close'].plot(label='Closing Price', alpha=0.8)
        self.data['Upper Band'].plot(label='Upper Bollinger Band', linestyle='--', alpha=0.8)
        self.data['Lower Band'].plot(label='Lower Bollinger Band', linestyle='--', alpha=0.8)
        plt.title('Bollinger Bands')
        plt.legend()
        plt.show()

        # Plot daily returns
        plt.figure(figsize=(14, 7))
        self.data['Daily Returns'].plot(label='Daily Returns', linestyle='--', alpha=0.8)
        plt.title('Daily Returns')
        plt.legend()
        plt.show()

        # Plot Moving Average Convergence Divergence (MACD) and its signal line
        plt.figure(figsize=(14, 7))
        self.data['MACD'].plot(label='MACD', linestyle='-', alpha=0.8)
        plt.title('MACD (Moving Average Convergence Divergence)')
        plt.legend()
        plt.show()

        # Plot Relative Strength Index (RSI)
        plt.figure(figsize=(14, 7))
        self.data['RSI'].plot(label='RSI', linestyle='-', alpha=0.8)
        plt.axhline(0, linestyle='--', alpha=0.5, color='red')
        plt.axhline(10, linestyle='--', alpha=0.5, color='orange')
        plt.axhline(20, linestyle='--', alpha=0.5, color='green')
        plt.axhline(30, linestyle='--', alpha=0.5, color='blue')
        plt.axhline(70, linestyle='--', alpha=0.5, color='blue')
        plt.axhline(80, linestyle='--', alpha=0.5, color='green')
        plt.axhline(90, linestyle='--', alpha=0.5, color='orange')
        plt.axhline(100, linestyle='--', alpha=0.5, color='red')
        plt.title('RSI (Relative Strength Index)')
        plt.legend()
        plt.show()

    def inferential_statistics(self):
        """Perform inferential statistics to make data-driven conclusions."""
        
        # Convert index to datetime for time series analysis
        self.data.index = pd.to_datetime(self.data.index)
        
        # Descriptive Statistics for Daily Returns: Summary of key statistics
        Calculate descriptive Statistics for daily returns
        print("Descriptive Statistics for Daily Returns:\n", self.data['Daily Returns'].describe())

        # Shapiro-Wilk Test for Normality: Determines if the daily returns are normally distributed
        stat, p = shapiro(self.data['Daily Returns'].dropna())
        if p > 0.05:
            print("Data follows a Normal Distribution.")
        else:
            print("Data does not follow a Normal Distribution.")

        # T-Test:  Checks if the mean return is significantly different from zero
        t_stat, p_val = ttest_1samp(self.data['Daily Returns'].dropna(), 0)
        if p_val < 0.05:
            print("The mean return is statistically different from 0.")
        else:
            print("The mean return is not statistically different from 0.")

        # Calculate Augmented Dickey-Fuller Test for Stationarity: Checks for the stationarity of the time series data. 
        # Non-stationary data can have its mean, variance, and covariance vary over time. 
        result = adfuller(self.data['Close'])
        if result[1] <= 0.05:
            print("The data is stationary.")
        else:
            print("The data is non-stationary. Consider differencing or transformations.")

        # Seasonal Decomposition: Breaks down time series into its trend, seasonal, and residual components
        decomposition = seasonal_decompose(self.data['Close'], model='multiplicative', period=252)
        decomposition.plot()
        plt.show()

        # Autocorrelation and Partial Autocorrelation Plots: Check for patterns in time-lagged data
        fig, ax = plt.subplots(1,2, figsize=(16, 4))
        plot_acf(self.data['Close'].dropna(), lags=40, ax=ax[0])  # Auto-Correlation
        plot_pacf(self.data['Close'].dropna(), lags=40, ax=ax[1], method='ywm')  # Partial Auto-Correlation with specified method
        plt.show()
        

def main():
    # Create an instance of FinancialDataAnalyzer
    analyzer = FinancialDataAnalyzer("GOOGL_2023_08_05.csv")
    
    # Load the data
    analyzer.load_data()
    
    # Calculate the metrics
    analyzer.calculate_metrics()
    print(analyzer.data.head())
    
    # Visualize the data
    analyzer.visualize_data()
    
    # Perform inferential statistics
    analyzer.inferential_statistics()
    
if __name__ == "__main__":
    main()

