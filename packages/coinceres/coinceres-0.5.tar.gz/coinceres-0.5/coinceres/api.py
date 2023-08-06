# -*- coding: utf-8 -*-
from coinceres.http_client import HttpRequest
from coinceres.sign import SignMixin


class APIClient(HttpRequest, SignMixin):
    """Http客户端"""

    def __init__(self, api_key=None, secret_key=None, host='open.coinceres.com', url='api/v1'):
        """
        :param api_key:
        :param secret_key:
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.url = self.join_url("http:/", host, url)

    @staticmethod
    def _error_handler(r):
        data = r.json()
        if r.status_code != 200:
            raise ValueError(data.get('message'))
        if data.get('code') != '200':
            raise ValueError(data.get('message'))
        return data.get('data')

    @staticmethod
    def _error_handler_market(r):
        data = r.json()
        if r.status_code != 200:
            raise ValueError(data.get('message'))
        if data.get('code') is None:
            return data
        raise ValueError(data.get('message'))

    def contract_info(self, exchange: str, contract: str = None):
        """
        獲取交易所內各幣對基本信息
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :param contract: 幣對或合約名稱
        :return:
        """
        data = {
            "exchange": exchange
        }
        if contract is not None:
            data.update(contract=contract)
        return self._error_handler(self._do_get(api="basic/contracts", data=data))

    def account(self, exchange: str = None):
        """
        獲取帳號信息
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :return:
        """
        data = None
        if exchange is not None:
            data = {
                "exchange": exchange
            }
        return self._error_handler(self._do_get(api="trade/account", data=data))

    def order_info(self, system_oid: str = None, status: int = None, exchange: str = None, contract: str = None):
        """
        查詢訂單詳情
        :param system_oid: 系统生成订单号，逗号分隔，最多可查询15个
        :param status: 订单状态
        :param exchange: 交易所名稱
        :param contract: 幣對或合約名稱
        :return:
        """
        data = dict()
        if system_oid is not None:
            data.update(system_oid=system_oid)
        if status is not None:
            data.update(status=status)
        if exchange is not None:
            data.update(exchange=exchange)
        if contract is not None:
            data.update(contract=contract)
        if not data:
            data = None
        return self._error_handler(self._do_get("trade/order", data=data))

    def _order(self, exchange: str, contract: str, entrust_vol: str, entrust_bs: str, future_dir: str,
               lever: str, price_type: str, entrust_price: str = None, profit_value: str = None,
               stop_value: str = None, client_oid: str = None):
        payload = {
            "exchange": exchange,
            "contract": contract,
            "price_type": price_type,
            "entrust_vol": entrust_vol,
            "entrust_bs": entrust_bs,
            "future_dir": future_dir,
            "lever": lever,
        }
        if entrust_price is not None:
            payload.update(entrust_price=entrust_price)
        if profit_value is not None:
            payload.update(profit_value=profit_value)
        if stop_value is not None:
            payload.update(stop_value=stop_value)
        if client_oid is not None:
            payload.update(client_oid=client_oid)
        return self._error_handler(self._do_post("trade/input", data=payload))

    def market_order(self, exchange: str, contract: str, entrust_vol: str, entrust_bs: str, future_dir: str,
                     lever: str, entrust_price: str = None, profit_value: str = None, stop_value: str = None,
                     client_oid: str = None):
        """
        創建市價訂單
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :param contract: 幣對或合約名稱
        :param entrust_vol: 交易量
        :param entrust_bs: 交易方向 "buy"/"sell"
        :param future_dir: "open"/"close"
        :param lever: 槓桿倍數
        :param entrust_price: 委託價格
        :param profit_value: 止盈价,合约必传
        :param stop_value: 止损价，合约必传
        :param client_oid: 来源标记
        :return:
        """
        return self._order(exchange, contract, entrust_vol, entrust_bs, future_dir, lever, "market",
                           entrust_price, profit_value, stop_value, client_oid)

    def limit_order(self, exchange: str, contract: str, entrust_vol: str, entrust_bs: str, future_dir: str,
                    lever: str, entrust_price: str, profit_value: str = None, stop_value: str = None,
                    client_oid: str = None):
        """
        創建限價訂單
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :param contract: 幣對或合約名稱
        :param entrust_vol: 交易量
        :param entrust_bs: 交易方向 "buy"/"sell"
        :param future_dir: "open"/"close"
        :param lever: 槓桿倍數
        :param entrust_price: 委託價格
        :param profit_value: 止盈价,合约必传
        :param stop_value: 止损价，合约必传
        :param client_oid: 来源标记
        :return:
        """
        return self._order(exchange, contract, entrust_vol, entrust_bs, future_dir, lever, "limit",
                           entrust_price, profit_value, stop_value, client_oid)

    def delete_order(self, system_oid: str):
        """
        取消訂單
        :param system_oid: 訂單號
        :return:
        """
        payload = {
            "system_oid": system_oid
        }
        return self._error_handler(self._do_delete("trade/order", data=payload))

    def close_order(self, exchange: str, contract: str, price_type: str, entrust_vol: str, entrust_bs: str,
                    entrust_price: str = None, deal_id: str = None, client_oid: str = None, close_rule: str = None):
        """
        平仓
        :param exchange: 交易所名称
        :param contract: 合约名称
        :param price_type: 市价：market 限价： limit
        :param entrust_vol: 委托量，限价买、卖、市价卖是数量，市价买是金额
        :param entrust_bs: 买：buy 卖：sell
        :param entrust_price: 委托价格， 限价必传
        :param deal_id: 平仓持仓号，合约平仓需指定的持仓单号
        :param client_oid: 客户端标识
        :param close_rule: 平仓规则
        :return:
        """
        payload = dict(
            exchange=exchange,
            contract=contract,
            price_type=price_type,
            entrust_vol=entrust_vol,
            entrust_bs=entrust_bs
        )
        if entrust_price is not None:
            payload.update(entrust_price=entrust_price)
        if deal_id is not None:
            payload.update(deal_id=deal_id)
        if client_oid is not None:
            payload.update(client_oid=client_oid)
        if close_rule is not None:
            payload.update(close_rule=close_rule)
        return self._error_handler(self._do_post("trade/close", data=payload))

    def open_contract(self, exchange: str = None, contract: str = None, position_dir: str = None):
        """
        查询合约持仓信息
        :param exchange: 交易所名称
        :param contract: 合约名称
        :param position_dir: 持仓方向，多: "buy"/空: "sell"
        :return:
        """
        data = dict()
        if exchange is not None:
            data.update(exchange=exchange)
        if contract is not None:
            data.update(contract=contract)
        if position_dir is not None:
            data.update(position_dir=position_dir)
        if not data:
            data = None
        return self._error_handler(self._do_get("trade/position", data=data))

    def transaction(self, exchange: str, contract: str, count: int):
        """
        查询成交纪录
        :param exchange: 交易所名称
        :param contract: 币币交易对或合约名称
        :param count: 查询数量 最大50
        :return:
        """
        data = dict(
            exchange=exchange,
            contract=contract,
            count=count
        )
        return self._error_handler(self._do_get("trade/trans", data=data))

    def kline(self, exchange: str, contract: str, duration: str, begin: str = None, end: str = None, size: int = None):
        """

        :param exchange: 交易所名称
        :param contract: 币币交易对或合约名称
        :param duration: 请求周期类型(1m.5m.15m.30m.1h.4h.1d)
            duration表示周期，1m.5m.15m.30m表示1分钟线.5分钟线.15分钟线.30分钟线，1h.4h表示1小时线.4小时线，1d表示日线
        :param begin: 请求开始时间(时间戳)
        :param end: 请求结束时间(时间戳)
        :param size: 请求根数
            如果begin 和end都填写了，则size忽略，如果begin和size填写了，end没有填写，则表示从begin开始向后请求多少根，
            如果end和size填写了，begin没有填写，则表示向前请求多少根。
        :return:
        """
        data = dict(
            exchange=exchange,
            contract=contract,
            duration=duration,
        )
        if begin:
            data.update(begin=begin)
        if end:
            data.update(end=end)
        if size:
            data.update(size=size)
        return self._error_handler_market(self._do_get("market/candle", data=data))

    def trade(self, exchange: str, contract: str, begin: str = None, end: str = None, size: int = None):
        data = dict(
            exchange=exchange,
            contract=contract,
        )
        if begin:
            data.update(begin=begin)
        if end:
            data.update(end=end)
        if size:
            data.update(size=size)
        return self._error_handler_market(self._do_get("market/trade", data=data))

    def depth(self, exchange: str, contract: str):
        data = dict(
            exchange=exchange,
            contract=contract,
        )
        return self._error_handler_market(self._do_get("market/depth10", data=data))

    def tick(self, exchange: str, contract: str):
        data = dict(
            exchange=exchange,
            contract=contract,
        )
        return self._error_handler_market(self._do_get("market/tick", data=data))
