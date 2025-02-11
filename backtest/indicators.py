import pandas as pd
import numpy as np
from numba import jit

# ✅ RSI - Relative Strength Index
@jit(nopython=True)
def calculate_rsi(close, period=14):
    """Aprēķina RSI indikatoru"""
    delta = np.diff(close)
    gains = np.maximum(delta, 0)
    losses = -np.minimum(delta, 0)
    avg_gain = np.convolve(gains, np.ones(period) / period, mode="valid")
    avg_loss = np.convolve(losses, np.ones(period) / period, mode="valid")
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return np.concatenate((np.full(period - 1, np.nan), rsi))

# ✅ MACD - Moving Average Convergence Divergence
def calculate_macd(close, short_period=12, long_period=26, signal_period=9):
    """Aprēķina MACD un signāla līniju"""
    short_ema = pd.Series(close).ewm(span=short_period, adjust=False).mean()
    long_ema = pd.Series(close).ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    return macd.values, signal.values

# ✅ Bollinger Bands
def calculate_bollinger_bands(close, period=20, std_factor=2):
    """Aprēķina Bollinger Bands"""
    sma = pd.Series(close).rolling(window=period).mean()
    std = pd.Series(close).rolling(window=period).std()
    upper_band = sma + (std_factor * std)
    lower_band = sma - (std_factor * std)
    return upper_band.values, lower_band.values

# ✅ ATR - Average True Range
def calculate_atr(high, low, close, period=14):
    """Aprēķina ATR - Average True Range"""
    tr1 = high - low
    tr2 = np.abs(high - close.shift())
    tr3 = np.abs(low - close.shift())
    tr = np.maximum.reduce([tr1, tr2, tr3])
    atr = pd.Series(tr).rolling(window=period).mean()
    return atr.values

# ✅ ADX - Average Directional Index
def calculate_adx(high, low, close, period=14):
    """Aprēķina ADX - Average Directional Index"""
    plus_dm = np.where(high.diff() > low.diff(), high.diff(), 0)
    minus_dm = np.where(low.diff() > high.diff(), low.diff(), 0)
    tr = calculate_atr(high, low, close, period)
    plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).sum() / tr)
    minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).sum() / tr)
    dx = 100 * np.abs((plus_di - minus_di) / (plus_di + minus_di))
    adx = pd.Series(dx).rolling(window=period).mean()
    return adx.values

# ✅ Stochastic Oscillator
def calculate_stochastic_oscillator(high, low, close, period=14):
    """Aprēķina Stochastic Oscillator"""
    lowest_low = low.rolling(window=period).min()
    highest_high = high.rolling(window=period).max()
    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d = k.rolling(window=3).mean()
    return k.values, d.values

# ✅ Volume Moving Average
def calculate_volume_ma(volume, period=20):
    """Aprēķina Volume Moving Average"""
    return volume.rolling(window=period).mean().values

# ✅ VWAP - Volume Weighted Average Price
def calculate_vwap(high, low, close, volume):
    """Aprēķina VWAP - Volume Weighted Average Price"""
    typical_price = (high + low + close) / 3
    vwap = (typical_price * volume).cumsum() / volume.cumsum()
    return vwap.values

# ✅ SuperTrend
def calculate_supertrend(high, low, close, atr_period=10, multiplier=3):
    """Aprēķina SuperTrend indikatoru"""
    atr = calculate_atr(high, low, close, atr_period)
    upper_band = ((high + low) / 2) + (multiplier * atr)
    lower_band = ((high + low) / 2) - (multiplier * atr)
    supertrend = np.where(close > upper_band, lower_band, upper_band)
    return supertrend

# ✅ Ichimoku Cloud
def calculate_ichimoku(high, low, close):
    """Aprēķina Ichimoku Cloud"""
    tenkan_sen = (high.rolling(window=9).max() + low.rolling(window=9).min()) / 2
    kijun_sen = (high.rolling(window=26).max() + low.rolling(window=26).min()) / 2
    senkou_span_a = (tenkan_sen + kijun_sen) / 2
    senkou_span_b = (high.rolling(window=52).max() + low.rolling(window=52).min()) / 2
    chikou_span = close.shift(-26)
    return tenkan_sen.values, kijun_sen.values, senkou_span_a.values, senkou_span_b.values, chikou_span.values
