# strategies.py

from pyalgotrade import strategy
from pyalgotrade import dataseries
from pyalgotrade.technical import ma
import technicalfilters as tf
from pyalgotrade.technical import cross
from pyalgotrade.broker import backtesting


class EMACrossover(strategy.BacktestingStrategy):

    def __init__(self, feed, instruments, cash, ema_length, ema_alpha, commission_scheme, printinfo=False):
        """

        Params:

        commission_scheme: tuple(str, float)
        """
        strategy.BacktestingStrategy.__init__(self, feed, cash)
        print 'PARAMS: len = %d | alpha = %.2f | Commission: %s' % (ema_length, ema_alpha, commission_scheme)

        # We wan't to use adjusted close prices instead of close.
        self.setUseAdjustedValues(True)
        self.printinfo = printinfo
        # Commission
        self.getBroker().setCommission(
            getattr(backtesting, commission_scheme[0])(commission_scheme[1]))

        # Initialize indicators for each instrument.
        self.__closes = {}
        self.__ema = {}
        self.__dt = {}
        self.__zeroseries = {}
        self.__zeroema = {}

        for instrument in instruments:
            self.__closes[instrument] = feed[instrument].getPriceDataSeries()
            self.__ema[instrument] = tf.EMA(
                self.__closes[instrument], ema_length, .1)
            self.__dt[instrument] = tf.Derivative(self.__ema[instrument])
            self.__zeroseries[instrument] = tf.ZeroSeries(
                self.__closes[instrument])
            self.__zeroema[instrument] = ma.EMA(
                self.__zeroseries[instrument], 3)

    def inventory(self, instrument):
        broker = self.getBroker()
        return (broker.getCash(), broker.getShares(instrument))

    def buyamount(self, instrument, price, volume, cash, cashpct):
        full = cash / price
        buyqty = full * cashpct
        if buyqty < 1:
            self.warning('Insufficient cash to buy %s.' % instrument)
        if buyqty > volume:
            self.warning('Coercing volume of %s.' % instrument)
            buyqty = max(volume - 1, 0)
        return buyqty

    def getEMA(self, instrument):
        return self.__ema[instrument]

    def onBars(self, bars):
        for instrument, bar in bars.items():
            infoout = None
            if cross.cross_above(self.__dt[instrument], self.__zeroema[instrument]) > 0:
                # If the derivative crosses above zero (deriv - -> +),
                # buy the instrument.
                now_cash, now_shares = self.inventory(instrument)
                buyqty = self.buyamount(
                    instrument, bar.getClose(), bar.getVolume(), now_cash, .2)
                self.marketOrder(instrument, buyqty)
                infoout = 'Order %d shares of %s @$%.2f. COH $%.2f' % (
                    buyqty, instrument, bar.getClose(), now_cash)

            elif cross.cross_below(self.__dt[instrument], self.__zeroema[instrument]) > 0:
                # If the derivative crosses below zero (deriv + -> -),
                # sell the instrument.
                now_cash, now_shares = self.inventory(instrument)
                if now_shares > 0:
                    # Sell all shares
                    self.marketOrder(instrument, -now_shares)
                    infoout = 'Sell %d shares of %s @$%.2f. COH $%.2f' % (
                        now_shares, instrument, bar.getClose(), now_cash)
            if infoout and self.printinfo:
                self.info(infoout)


class SLTRIXCrossover(strategy.BacktestingStrategy):

    def __init__(self, feed, instruments, cash, shortlen, longlen, a1, a3, printinfo=False):
        strategy.BacktestingStrategy.__init__(self, feed, cash)
        self.printinfo = printinfo
        # We want to use adjusted close prices instead of close.
        self.setUseAdjustedValues(True)

        # Initialize indicators for each instrument.
        self.__closes = {}
        self.__shorttrix = {}
        self.__longtrix = {}

        # Commission
        self.getBroker().setCommission(
            getattr(backtesting, 'FixedPerTrade')(10))

        for instrument in instruments:
            self.__closes[instrument] = feed[instrument].getPriceDataSeries()
            self.__shorttrix[instrument] = tf.TRIX(
                self.__closes[instrument], shortlen, [a1, a1, a1])
            self.__longtrix[instrument] = tf.TRIX(
                self.__closes[instrument], longlen, [a3, a3, a3])

    def inventory(self, instrument):
        broker = self.getBroker()
        return (broker.getCash(), broker.getShares(instrument))

    def buyamount(self, instrument, price, volume, cash, cashpct):
        full = cash / price
        buyqty = full * cashpct
        if buyqty < 1:
            self.warning('Insufficient cash to buy %s.' % instrument)
        if buyqty > volume:
            self.warning('Coercing volume of %s.' % instrument)
            buyqty = max(volume - 1, 0)
        return buyqty

    def getshorttrix(self, instrument):
        return self.__shorttrix[instrument]

    def getlongtrix(self, instrument):
        return self.__longtrix[instrument]

    def onBars(self, bars):
        for instrument, bar in bars.items():
            infoout = None
            if cross.cross_above(self.__shorttrix[instrument],
                                 self.__longtrix[instrument]) > 0:
                # If the derivative crosses above zero (deriv - -> +),
                # buy the instrument.
                now_cash, now_shares = self.inventory(instrument)
                buyqty = self.buyamount(
                    instrument, bar.getClose(), bar.getVolume(), now_cash, .2)
                self.marketOrder(instrument, buyqty)
                infoout = 'Order %d shares of %s @$%.2f. COH $%.2f' % (
                    buyqty, instrument, bar.getClose(), now_cash)

            elif cross.cross_below(self.__shorttrix[instrument],
                                   self.__longtrix[instrument]) > 0:
                # If the derivative crosses below zero (deriv + -> -),
                # sell the instrument.
                now_cash, now_shares = self.inventory(instrument)
                if now_shares > 0:
                    # Sell all shares
                    self.marketOrder(instrument, -now_shares)
                    infoout = 'Sell %d shares of %s @$%.2f. COH $%.2f' % (
                        now_shares, instrument, bar.getClose(), now_cash)
            if infoout and self.printinfo:
                self.info(infoout)


class SLEMACrossover(strategy.BacktestingStrategy):

    def __init__(self, feed, instruments, cash, shortlen, longlen, a1, a3, printinfo=True):
        strategy.BacktestingStrategy.__init__(self, feed, cash)
        self.printinfo = printinfo
        # We want to use adjusted close prices instead of close.
        self.setUseAdjustedValues(True)

        # Initialize indicators for each instrument.
        self.__closes = {}
        self.__shorttrix = {}
        self.__longtrix = {}

        # Commission
        self.getBroker().setCommission(
            getattr(backtesting, 'FixedPerTrade')(10))

        for instrument in instruments:
            self.__closes[instrument] = feed[instrument].getPriceDataSeries()
            self.__shorttrix[instrument] = tf.EMA(
                self.__closes[instrument], shortlen, a1)
            self.__longtrix[instrument] = tf.EMA(
                self.__closes[instrument], longlen, a3)

    def inventory(self, instrument):
        broker = self.getBroker()
        return (broker.getCash(), broker.getShares(instrument))

    def buyamount(self, instrument, price, volume, cash, cashpct):
        full = cash / price
        buyqty = full * cashpct
        if buyqty < 1:
            self.warning('Insufficient cash to buy %s.' % instrument)
        if buyqty > volume:
            self.warning('Coercing volume of %s.' % instrument)
            buyqty = max(volume - 1, 0)
        return buyqty

    def getshorttrix(self, instrument):
        return self.__shorttrix[instrument]

    def getlongtrix(self, instrument):
        return self.__longtrix[instrument]

    def onBars(self, bars):
        for instrument, bar in bars.items():
            infoout = None
            if cross.cross_below(self.__shorttrix[instrument],
                                 self.__longtrix[instrument]) > 0:
                # If the derivative crosses above zero (deriv - -> +),
                # buy the instrument.
                now_cash, now_shares = self.inventory(instrument)
                buyqty = self.buyamount(
                    instrument, bar.getClose(), bar.getVolume(), now_cash, .2)
                self.marketOrder(instrument, buyqty)
                infoout = 'Order %d shares of %s @$%.2f. COH $%.2f' % (
                    buyqty, instrument, bar.getClose(), now_cash)

            elif cross.cross_above(self.__shorttrix[instrument],
                                   self.__longtrix[instrument]) > 0:
                # If the derivative crosses below zero (deriv + -> -),
                # sell the instrument.
                now_cash, now_shares = self.inventory(instrument)
                if now_shares > 0:
                    # Sell all shares
                    self.marketOrder(instrument, -now_shares)
                    infoout = 'Sell %d shares of %s @$%.2f. COH $%.2f' % (
                        now_shares, instrument, bar.getClose(), now_cash)
            if infoout and self.printinfo:
                self.info(infoout)