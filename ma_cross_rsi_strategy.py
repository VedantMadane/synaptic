
"""
NautilusTrader MA Crossover + RSI Strategy
Based on the Synaptic Trading evaluation requirements.
"""

from decimal import Decimal
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.data import BarType, Bar
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.orders import MarketOrder
from nautilus_trader.indicators.average.sma import SimpleMovingAverage
from nautilus_trader.indicators.rsi import RelativeStrengthIndex
from nautilus_trader.model.instruments import Instrument


class MACrossRSIConfig(StrategyConfig):
    """Configuration for MA Crossover + RSI strategy."""
    
    instrument_id: str
    bar_type: str
    fast_ma_period: int = 20
    slow_ma_period: int = 50
    rsi_period: int = 14
    rsi_oversold: int = 30
    rsi_overbought: int = 70
    trade_size: float = 1.0


class MACrossRSIStrategy(Strategy):
    """
    A strategy that combines moving average crossover with RSI filtering.
    
    Trading Rules:
    - Buy when: Fast MA crosses above Slow MA AND RSI < 70 (not overbought)
    - Sell when: Fast MA crosses below Slow MA AND RSI > 30 (not oversold)
    - Close all positions at end of day (EOD flat)
    """
    
    def __init__(self, config: MACrossRSIConfig) -> None:
        super().__init__(config)
        
        # Configuration
        self.instrument_id = InstrumentId.from_str(config.instrument_id)
        self.bar_type = BarType.from_str(config.bar_type)
        self.trade_size = Decimal(str(config.trade_size))
        
        # RSI thresholds
        self.rsi_oversold = config.rsi_oversold
        self.rsi_overbought = config.rsi_overbought
        
        # Create indicators
        self.fast_ma = SimpleMovingAverage(config.fast_ma_period)
        self.slow_ma = SimpleMovingAverage(config.slow_ma_period)
        self.rsi = RelativeStrengthIndex(config.rsi_period)
        
        # State tracking for crossover detection
        self.previous_fast_ma = None
        self.previous_slow_ma = None
        
        self.instrument: Instrument | None = None
    
    def on_start(self) -> None:
        """Actions to be performed on strategy start."""
        self.instrument = self.cache.instrument(self.instrument_id)
        if self.instrument is None:
            self.log.error(f"Could not find instrument for {self.instrument_id}")
            self.stop()
            return
        
        # Register indicators for automatic updates
        self.register_indicator_for_bars(self.bar_type, self.fast_ma)
        self.register_indicator_for_bars(self.bar_type, self.slow_ma)
        self.register_indicator_for_bars(self.bar_type, self.rsi)
        
        # Subscribe to bars
        self.subscribe_bars(self.bar_type)
        
        self.log.info(f"Strategy started for {self.instrument_id}")
        self.log.info(f"Fast MA: {self.fast_ma.period}, Slow MA: {self.slow_ma.period}, RSI: {self.rsi.period}")
    
    def on_bar(self, bar: Bar) -> None:
        """
        Actions to be performed when a bar is received.
        
        Uses only PREVIOUS bar values to avoid look-ahead bias.
        """
        # Wait for warm-up period (need enough data for indicators)
        if not self.indicators_initialized():
            return
        
        # Get current indicator values
        fast_ma_value = self.fast_ma.value
        slow_ma_value = self.slow_ma.value
        rsi_value = self.rsi.value
        
        # Detect crossovers using previous values
        if self.previous_fast_ma is not None and self.previous_slow_ma is not None:
            
            # Bullish crossover: Fast MA crosses above Slow MA
            if (self.previous_fast_ma <= self.previous_slow_ma and 
                fast_ma_value > slow_ma_value and 
                rsi_value < self.rsi_overbought):
                
                if self.portfolio.is_flat(self.instrument_id):
                    self.log.info(f"BUY signal - Fast MA crossed above Slow MA, RSI: {rsi_value:.2f}")
                    self.buy()
                elif self.portfolio.is_net_short(self.instrument_id):
                    self.log.info(f"BUY signal - Reversing short position, RSI: {rsi_value:.2f}")
                    self.close_all_positions(self.instrument_id)
                    self.buy()
            
            # Bearish crossover: Fast MA crosses below Slow MA
            elif (self.previous_fast_ma >= self.previous_slow_ma and 
                  fast_ma_value < slow_ma_value and 
                  rsi_value > self.rsi_oversold):
                
                if self.portfolio.is_flat(self.instrument_id):
                    self.log.info(f"SELL signal - Fast MA crossed below Slow MA, RSI: {rsi_value:.2f}")
                    self.sell()
                elif self.portfolio.is_net_long(self.instrument_id):
                    self.log.info(f"SELL signal - Reversing long position, RSI: {rsi_value:.2f}")
                    self.close_all_positions(self.instrument_id)
                    self.sell()
        
        # Store current values for next bar
        self.previous_fast_ma = fast_ma_value
        self.previous_slow_ma = slow_ma_value
    
    def indicators_initialized(self) -> bool:
        """Check if all indicators have enough data."""
        return (self.fast_ma.initialized and 
                self.slow_ma.initialized and 
                self.rsi.initialized)
    
    def buy(self) -> None:
        """Submit a market buy order."""
        order: MarketOrder = self.order_factory.market(
            instrument_id=self.instrument_id,
            order_side=OrderSide.BUY,
            quantity=self.instrument.make_qty(self.trade_size),
        )
        self.submit_order(order)
    
    def sell(self) -> None:
        """Submit a market sell order."""
        order: MarketOrder = self.order_factory.market(
            instrument_id=self.instrument_id,
            order_side=OrderSide.SELL,
            quantity=self.instrument.make_qty(self.trade_size),
        )
        self.submit_order(order)
    
    def on_stop(self) -> None:
        """Actions to be performed when strategy is stopped."""
        # Close all positions (EOD flat requirement)
        self.cancel_all_orders(self.instrument_id)
        self.close_all_positions(self.instrument_id)
        self.unsubscribe_bars(self.bar_type)
        
        self.log.info("Strategy stopped - All positions closed")
    
    def on_reset(self) -> None:
        """Reset all indicators."""
        self.fast_ma.reset()
        self.slow_ma.reset()
        self.rsi.reset()
        self.previous_fast_ma = None
        self.previous_slow_ma = None
