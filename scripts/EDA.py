import pandas as pd
import talib
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
import matplotlib.pyplot as plt
#import pynance




def LoadData(file_path):
    # Load the data from the file
    df = pd.read_csv(file_path)
    return df
def InspectData(dataFrame):
    return dataFrame.info()
   
def GetShape(df):
    return df.shape
def GetSummary(df):
    return df.describe()
def GetColumns(df):
    return df.columns
def GetColumnNames(df):
    return df.columns.tolist()
def GetColumnTypes(df):
    return df.dtypes
def CheckMissingValue(df):
    return df.isnull().sum()
def RemoveColumn(df):
    return df.drop(columns= ['Unnamed: 0'], inplace=True)
def AddHeadlineLength(df):
    df["headline_length"] = df["headline"].apply(len)
    return df
def GtHeadlineLengthStats(df):
    
    return df['headline_length'].describe()


# Convert a specified column to datetime and set it as the index
def ConvertDdate(df):    
   date_length = df['date'].apply(len)
   # Truncate the 'date' column to a length of 19 characters
   df['date'] = df['date'].str.slice(0, 19)   
   # Convert the 'date' column to datetime format
   df['date'] = pd.to_datetime(df['date'])
    
   return df


# Extract year, month, day, hour, and minute from the 'date' column
def EctractTimeFormat(df):
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df

def ArticlePublishedYearly(df):
    #Extract year and month from the date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Count the number of articles per year and month
    articles_per_month = df.groupby(['year', 'month']).size().reset_index(name='count')

    # Plotting the number of articles per month for each year
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=articles_per_month, x='month', y='count', hue='year', marker='o', palette='tab10')
    plt.title('Number of Articles Published Each Month by Year')
    plt.xlabel('Month')
    plt.ylabel('Number of Articles')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Year')
    plt.grid(True)
    plt.show()

########################################################################


# Histogram of headline lengths
def HeadlineLength(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['headline_length'], bins=50, kde=True)
    plt.title('Distribution of Headline Lengths')
    plt.xlabel('Headline Length')
    plt.ylabel('Frequency')
    plt.show()


# Plot the Relative Strength Index (RSI)
def TopPublisher(df):
    
    top_publishers = df['publisher'].value_counts().head(10)
    plt.figure(figsize=(14, 8))
    sns.barplot(x=top_publishers.index, y=top_publishers.values, palette="viridis")
    plt.xticks(rotation=90)
    plt.title('Top 10 Publishers by Number of Articles')
    plt.xlabel('Publisher')
    plt.ylabel('Number of Articles')
    plt.show()




#Plot number of Articles Published per Year
def YearlyArticlePublished(df):
    plt.figure(figsize=(12, 6))
    articles_per_year = df.groupby('year').size()
    plt.plot(articles_per_year.index, articles_per_year.values, marker='o')
    plt.title('Number of Articles Published per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Articles')
    plt.grid(True)
    plt.show()



def DailyArticlesPublishedEachMonth(df):
    # Filter the DataFrame to include only the year 2017
    df_2017 = df[df['year'] == 2017]
    
    # Loop through each month from January (1) to December (12)
    for month in range(1, 13):
        # Filter the DataFrame for the current month
        df_month = df_2017[df_2017['month'] == month]

        # Count the number of articles per day in the current month
        daily_counts = df_month.groupby('day').size().reset_index(name='count')

        # Create a plot for the current month
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=daily_counts, x='day', y='count', marker='o')
        plt.title(f'Number of Articles Published Per Day in {month}/2017')
        plt.xlabel('Day')
        plt.ylabel('Number of Articles')
        plt.grid(True)
        plt.xticks(range(1, 32))  # Display all possible days on the x-axis
        plt.show()

def ThreeYearJanu(df):
    # Filter data for January of 2017, 2018, and 2019
    years = [2018, 2019, 2020]
    df_filtered = df[df['year'].isin(years) & (df['month'] == 1)]

    # Count the number of articles per day for each year
    daily_counts = df_filtered.groupby(['year', 'day']).size().reset_index(name='count')

    # Plotting the number of articles published per day for January in each year
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=daily_counts, x='day', y='count', hue='year', marker='o')
    plt.title('Number of Articles Published Per Day in January (2018-2020)')
    plt.xlabel('Day')
    plt.ylabel('Number of Articles')
    plt.legend(title='Year')
    plt.grid(True)
    plt.xticks(daily_counts['day'].unique())  # Ensure all days are shown on x-axis
    plt.show()

# Plot distribution of sentiment scores
def SentimentScore(df):
    
    plt.figure(figsize=(12, 6))
    sns.histplot(df['sentiment'], bins=30, kde=True)
    plt.title('Distribution of Sentiment Scores')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show() 


# Plot distribution of the custom sentiment classes.
def SentimentClass(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='sentiment_class', data=df, palette='viridis')
    plt.title('Distribution of Sentiments in Headlines')
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Articles')
    plt.show()  


def PlotDistributions(final_data):
    plt.figure(figsize=(14, 7))
    plt.subplot(2, 2, 1)
    sns.histplot(final_data['Close'], kde=True, bins=30)
    plt.title('Distribution of Closing Prices')
    plt.xlabel('Closing Price')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 2)
    sns.histplot(final_data['average_sentiment_score'], kde=True, bins=30)
    plt.title('Distribution of Sentiment Scores')
    plt.xlabel('Average Sentiment Score')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()

def PlotScatter(final_data):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=final_data, x='average_sentiment_score', y='daily_return')
    plt.title('Sentiment Score vs. Daily Return')
    plt.xlabel('Average Sentiment Score')
    plt.ylabel('Daily Return')

    plt.subplot(1, 2, 2)
    sns.scatterplot(data=final_data, x='average_sentiment_score', y='Close')
    plt.title('Sentiment Score vs. Closing Price')
    plt.xlabel('Average Sentiment Score')
    plt.ylabel('Closing Price')

    plt.tight_layout()
    plt.show()

def PlotHeatmap(final_data):
    correlation_matrix = final_data[['average_sentiment_score', 'daily_return', 'Close']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    plt.show()


def PlotScatterAndHeatmap(final_data):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=final_data, x='average_sentiment_score', y='daily_return')
    plt.title('Sentiment Score vs. Daily Return')
    plt.xlabel('Average Sentiment Score')
    plt.ylabel('Daily Return')

    plt.subplot(1, 2, 2)
    sns.scatterplot(data=final_data, x='average_sentiment_score', y='Close')
    plt.title('Sentiment Score vs. Closing Price')
    plt.xlabel('Average Sentiment Score')
    plt.ylabel('Closing Price')

    plt.tight_layout()
    plt.show()

    correlation_matrix = final_data[['average_sentiment_score', 'daily_return', 'Close']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    plt.show()


def NumArticlePubTime(df):
    # Count the number of articles per date
    articles_per_date = df['date'].value_counts().sort_index()

    # Convert to DataFrame for plotting
    articles_per_date_df = articles_per_date.reset_index()
    articles_per_date_df.columns = ['date', 'count']

    # Plotting the number of articles over time
    plt.figure(figsize=(16, 8))
    sns.lineplot(data=articles_per_date_df, x='date', y='count')
    plt.title('Number of Articles Published Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.show()


# Calculate technical indicators using TA-Lib.
def CalculateTechnicalIndicators(df):
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return df

# Plot stock data with technical indicators.
def PlotStockData(df):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label='Close', color='blue')
    plt.plot(df.index, df['SMA_20'], label='20-day SMA', color='red')
    plt.plot(df.index, df['SMA_50'], label='50-day SMA', color='green')
    plt.title('Stock Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the Relative Strength Index (RSI)
def PlotRSI(df):
    plt.figure(figsize=(14, 5))
    plt.plot(df.index, df['RSI'], label='RSI', color='purple')
    plt.axhline(70, color='red', linestyle='--', label='Overbought')
    plt.axhline(30, color='green', linestyle='--', label='Oversold')
    plt.title('Relative Strength Index (RSI)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot Moving Average Convergence Divergence (MACD).
def PlotMACD(df):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['MACD'], label='MACD', color='blue')
    plt.plot(df.index, df['MACD_signal'], label='MACD Signal', color='red')
    plt.bar(df.index, df['MACD_hist'], label='MACD Histogram', color='gray', alpha=0.3)
    plt.title('MACD and Signal Line')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

def FetchStockData(ticker, period='1y'):
    """Fetch historical stock data using yfinance."""
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(period=period)
    return historical_data

def FinancialMetrics(ticker):
    """Calculate financial metrics using yfinance."""
    metrics = {}
    stock = yf.Ticker(ticker)
    
    # Fetching company information
    info = stock.info
    metrics['PE_Ratio'] = info.get('forwardEps', 'N/A') / info.get('forwardEps', 'N/A') if info.get('forwardEps', None) else 'N/A'
    metrics['Market_Cap'] = info.get('marketCap', 'N/A')
    metrics['Dividend_Yield'] = info.get('dividendYield', 'N/A')
    
    return metrics