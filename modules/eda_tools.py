import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def set_plotting_style():
    """Sets a clean, professional aesthetic."""
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams['figure.dpi'] = 100

def prepare_eda_df(df):
    """
    Consolidates winner and loser stats into a single long-format DataFrame.
    Includes a 'Player_Type' label to allow for deeper analysis if needed.
    """
    # Define the columns we want to extract
    w_cols = {'w_1st_win_pct': 'first_serve_pct', 'w_2nd_win_pct': 'second_serve_pct', 'w_ace': 'aces'}
    l_cols = {'l_1st_win_pct': 'first_serve_pct', 'l_2nd_win_pct': 'second_serve_pct', 'l_ace': 'aces'}
    
    # Process Winners
    winners = df[['surface'] + list(w_cols.keys())].rename(columns=w_cols)
    winners['outcome'] = 'Winner'
    
    # Process Losers
    losers = df[['surface'] + list(l_cols.keys())].rename(columns=l_cols)
    losers['outcome'] = 'Loser'
    
    # Combine and remove any rows with missing serve data
    combined = pd.concat([winners, losers], axis=0).dropna()
    return combined

def plot_surface_analysis(df):
    """
    Generates a single figure with two subplots. 
    By not returning the 'fig' object at the end, we prevent double-plotting.
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    order = ['Clay', 'Hard', 'Grass']
    
    # Subplot 1: 1st Serve Win %
    sns.boxplot(ax=axes[0], x='surface', y='first_serve_pct', data=df, order=order, hue='surface', legend=False)
    axes[0].set_title('1st Serve Win % by Surface', fontweight='bold', fontsize=14)
    axes[0].set_ylabel('Win % (Decimal)')
    
    # Subplot 2: Aces Distribution (using a Boxplot for better outlier visibility)
    sns.boxplot(ax=axes[1], x='surface', y='aces', data=df, order=order, hue='surface', legend=False)
    axes[1].set_title('Aces per Match by Surface', fontweight='bold', fontsize=14)
    axes[1].set_ylabel('Number of Aces')
    
    plt.tight_layout()
    plt.show() # Explicitly show
    plt.close() # Close to free memory and prevent duplicate output

def get_stats_summary(df):
    """Returns a clean summary table."""
    return df.groupby('surface')[['first_serve_pct', 'aces']].agg(['count', 'mean', 'std']).round(3)