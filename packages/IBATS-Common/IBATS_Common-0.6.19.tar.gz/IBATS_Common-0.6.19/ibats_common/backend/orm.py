# -*- coding: utf-8 -*-
"""
Created on 2017/10/9
@author: MG
"""
from datetime import datetime, timedelta
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean, SmallInteger, Date, Time, func
from sqlalchemy.dialects.mysql import DOUBLE, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from pandas import Timedelta
from ibats_common.backend import engines
from ibats_common.utils.db import with_db_session, get_db_session
from ibats_common.common import Action, Direction
from ibats_common.utils.mess import str_2_date, pd_timedelta_2_timedelta, date_2_str, datetime_2_str, date_time_2_str
import logging
from collections import defaultdict
import warnings

engine_ibats = engines.engine_ibats
BaseModel = declarative_base()
# 每一次实务均产生数据库插入或更新动作（默认：否）
UPDATE_OR_INSERT_PER_ACTION = False
_key_idx = defaultdict(lambda: defaultdict(int))


def idx_generator(key1, key2):
    idx = _key_idx[key1][key2]
    idx += 1
    _key_idx[key1][key2] = idx
    return idx


class StgRunInfo(BaseModel):
    """策略运行信息"""

    __tablename__ = 'stg_run_info'
    stg_run_id = Column(Integer, autoincrement=True, primary_key=True)
    stg_name = Column(String(300))
    dt_from = Column(DateTime())
    dt_to = Column(DateTime())
    run_mode = Column(SmallInteger)
    stg_params = Column(String(5000))
    strategy_handler_param = Column(String(1000))
    md_agent_params_list = Column(String(5000))
    trade_agent_params_list = Column(String(5000))


class OrderDetail(BaseModel):
    """订单信息"""

    __tablename__ = 'order_detail'
    stg_run_id = Column(Integer, primary_key=True)
    order_idx = Column(Integer, primary_key=True)
    trade_agent_key = Column(String(40))
    order_dt = Column(DateTime)
    order_date = Column(Date)  # 对应行情数据中 ActionDate
    order_time = Column(Time)  # 对应行情数据中 ActionTime
    order_millisec = Column(Integer, default=0, server_default='0')  # 对应行情数据中 ActionMillisec
    direction = Column(TINYINT)  # -1：空；1：多
    action = Column(Integer)  # 0：关：1：开
    symbol = Column(String(30))
    order_price = Column(DOUBLE)
    order_vol = Column(DOUBLE)  # 订单量

    def __init__(self, stg_run_id=None, trade_agent_key=None, order_dt=None, order_date=None, order_time=None,
                 order_millisec=0, direction=None, action=None, symbol=None, order_price=0, order_vol=0):
        self.stg_run_id = stg_run_id
        self.order_idx = None if stg_run_id is None else idx_generator(stg_run_id, OrderDetail)
        self.trade_agent_key = trade_agent_key
        self.order_dt = date_time_2_str(order_date, order_time) if order_dt is None else order_dt
        self.order_date = order_date
        self.order_time = order_time
        self.order_millisec = order_millisec
        self.direction = direction.value if isinstance(direction, Direction) else direction
        self.action = action.value if isinstance(action, Action) else action
        self.symbol = symbol
        self.order_price = order_price
        self.order_vol = order_vol

    def __repr__(self):
        return f"<OrderDetail(stg_run_id='{self.stg_run_id}' idx='{self.order_idx}', " \
               f"trade_agent_key={self.trade_agent_key}, direction='{Direction(self.direction)}', " \
               f"action='{Action(self.action)}', symbol='{self.symbol}', order_price='{self.order_price}', " \
               f"order_vol='{self.order_vol}')>"

    @staticmethod
    def remove(stg_run_id: int):
        """
        仅作为调试工具使用，删除指定 stg_run_id 相关的 order_detail
        :param stg_run_id: 
        :return: 
        """
        with with_db_session(engine_ibats) as session:
            # session.execute('DELETE FROM order_detail WHERE stg_run_id=:stg_run_id',
            #                 {'stg_run_id': stg_run_id})
            session.query(OrderDetail).filter(OrderDetail.stg_run_id == stg_run_id).delete()
            session.commit()


class TradeDetail(BaseModel):
    """记录成交信息"""
    __tablename__ = 'trade_detail'
    stg_run_id = Column(Integer, primary_key=True)
    trade_idx = Column(Integer, primary_key=True)  # , comment="成交id"
    trade_agent_key = Column(String(40))
    order_idx = Column(Integer)  # , comment="对应订单id"
    order_price = Column(DOUBLE)  # , comment="原订单价格"
    order_vol = Column(DOUBLE)  # 订单量 , comment="原订单数量"
    trade_dt = Column(DateTime)  # 对应行情数据中 ActionDate
    trade_date = Column(Date)  # 对应行情数据中 ActionDate
    trade_time = Column(Time)  # 对应行情数据中 ActionTime
    trade_millisec = Column(Integer)  # 对应行情数据中 ActionMillisec
    direction = Column(TINYINT)  # -1：空；1：多
    action = Column(Integer)  # 0：关：1：开
    symbol = Column(String(30))
    trade_price = Column(DOUBLE)  # , comment="成交价格"
    trade_vol = Column(DOUBLE)  # 订单量 , comment="成交数量"
    margin = Column(DOUBLE, server_default='0')  # 保证金 , comment="占用保证金"
    commission = Column(DOUBLE, server_default='0')  # 佣金、手续费 , comment="佣金、手续费"

    def __init__(self, stg_run_id=None, trade_agent_key=None, order_idx=None, order_price=None, order_vol=None,
                 trade_dt=None, trade_date=None, trade_time=None, trade_millisec=0, direction=None, action=None,
                 symbol=None, trade_price=None, trade_vol=None, margin=None, commission=None):
        self.stg_run_id = stg_run_id
        self.trade_idx = None if stg_run_id is None else idx_generator(stg_run_id, TradeDetail)
        self.trade_agent_key = trade_agent_key
        self.order_idx = order_idx
        self.order_price = order_price
        self.order_vol = order_vol
        self.trade_dt = date_time_2_str(trade_date, trade_time) if trade_dt is None else trade_dt
        self.trade_date = trade_date
        self.trade_time = trade_time
        self.trade_millisec = trade_millisec
        self.direction = direction
        self.action = action
        self.symbol = symbol
        self.trade_price = trade_price
        self.trade_vol = trade_vol
        self.margin = margin
        self.commission = commission

    def set_trade_time(self, value):
        if isinstance(value, Timedelta):
            # print(value, 'parse to timedelta')
            self.trade_time = timedelta(seconds=value.seconds)
        else:
            self.trade_time = value

    @staticmethod
    def remove(stg_run_id: int):
        """
        仅作为调试工具使用，删除指定 stg_run_id 相关的 trade_detail
        :param stg_run_id: 
        :return: 
        """
        with with_db_session(engine_ibats) as session:
            # session.execute('DELETE FROM trade_detail WHERE stg_run_id=:stg_run_id',
            #                 {'stg_run_id': stg_run_id})
            # session.query(PosStatusInfo).filter(PosStatusInfo.stg_run_id.in_([3, 4])).delete(False)  # 仅供实例
            session.query(TradeDetail).filter(TradeDetail.stg_run_id == stg_run_id).delete()
            session.commit()

    @staticmethod
    def create_by_order_detail(order_detail: OrderDetail):
        symbol = order_detail.symbol
        order_price, order_vol = order_detail.order_price, order_detail.order_vol
        # stg_run_id = order_detail.stg_run_id

        # TODO: 增加滑点、成交比例、费率、保证金比例等参数，该参数将和在回测参数中进行设置
        # instrument_info = Config.instrument_info_dic[symbol]
        # multiple = instrument_info['VolumeMultiple']
        # margin_ratio = instrument_info['LongMarginRatio']
        multiple, margin_ratio = 1, 1
        margin = order_vol * order_price * multiple * margin_ratio
        commission = 0
        trade_detail = TradeDetail(stg_run_id=order_detail.stg_run_id,
                                   trade_agent_key=order_detail.trade_agent_key,
                                   order_idx=order_detail.order_idx,
                                   trade_date=order_detail.order_date,
                                   trade_time=order_detail.order_time,
                                   trade_millisec=order_detail.order_millisec,
                                   direction=order_detail.direction,
                                   action=order_detail.action,
                                   symbol=symbol,
                                   order_price=order_price,
                                   order_vol=order_vol,
                                   trade_price=order_price,
                                   trade_vol=order_vol,
                                   margin=margin,
                                   commission=commission
                                   )
        if UPDATE_OR_INSERT_PER_ACTION:
            with with_db_session(engine_ibats, expire_on_commit=False) as session:
                session.add(trade_detail)
                session.commit()
        return trade_detail


class PosStatusDetail(BaseModel):
    """
    持仓状态数据
    当持仓状态从有仓位到清仓时（position>0 --> position==0），计算清仓前的浮动收益，并设置到 floating_pl 字段最为当前状态的浮动收益
    在调用 create_by_self 时，则需要处理一下，当 position==0 时，floating_pl 直接设置为 0，避免引起后续计算上的混淆
    2018-11-02 当仓位多空切换时（1根K线内多头反手转空头），则浮动收益继续保持之前数字
    """
    __tablename__ = 'pos_status_detail'
    stg_run_id = Column(Integer, primary_key=True)  # 对应回测了策略 StgRunID 此数据与 AccSumID 对应数据相同
    pos_status_detail_idx = Column(Integer, primary_key=True)
    trade_agent_key = Column(String(40))
    trade_idx = Column(Integer)  # , comment="最新的成交id"
    trade_dt = Column(DateTime)  # 每个订单变化生成一条记录 此数据与 AccSumID 对应数据相同
    trade_date = Column(Date)  # 对应行情数据中 ActionDate
    trade_time = Column(Time)  # 对应行情数据中 ActionTime
    trade_millisec = Column(Integer)  # 对应行情数据中 ActionMillisec
    direction = Column(TINYINT)
    symbol = Column(String(30))
    position = Column(DOUBLE, default=0.0)
    avg_price = Column(DOUBLE, default=0.0)  # 所持投资品种上一交易日所有交易的加权平均价
    cur_price = Column(DOUBLE, default=0.0)
    floating_pl = Column(DOUBLE, default=0.0)
    floating_pl_chg = Column(DOUBLE, default=0.0)
    floating_pl_cum = Column(DOUBLE, default=0.0)
    margin = Column(DOUBLE, default=0.0)
    margin_chg = Column(DOUBLE, default=0.0)
    position_date = Column(Date, default=0)
    logger = logging.getLogger(f'<Table:{__tablename__}')

    def __repr__(self):
        return f"<PosStatusDetail(id='{self.pos_status_detail_idx}', trade_agent_key={self.trade_agent_key}," \
               f" update_dt='{datetime_2_str(self.trade_dt)}', trade_idx='{self.trade_idx}', symbol='{self.symbol}', " \
               f"direction='{self.direction}', position='{self.position}', avg_price='{self.avg_price}')>"

    def __init__(self, stg_run_id=None, trade_agent_key=None, trade_idx=None, trade_dt=None,
                 trade_date=None, trade_time=None, trade_millisec=None, direction=None, symbol=None, position=None,
                 avg_price=None, cur_price=None, floating_pl=0, floating_pl_chg=0, floating_pl_cum=0,
                 margin=0, margin_chg=0, position_date=None):
        self.stg_run_id = stg_run_id
        self.pos_status_detail_idx = None if stg_run_id is None else idx_generator(stg_run_id, PosStatusDetail)
        self.trade_agent_key = trade_agent_key
        self.trade_idx = trade_idx
        self.trade_dt = date_time_2_str(trade_date, trade_time) if trade_dt is None else trade_dt
        self.trade_date = trade_date
        self.trade_time = trade_time
        self.trade_millisec = trade_millisec
        self.direction = direction
        self.symbol = symbol
        self.position = position
        self.avg_price = avg_price
        self.cur_price = cur_price
        self.floating_pl = floating_pl
        self.floating_pl_chg = floating_pl_chg
        self.floating_pl_cum = floating_pl_cum
        self.margin = margin
        self.margin_chg = margin_chg
        self.position_date = position_date
        # 记录上一状态的浮动收益，用于在计算仓位多空切换时前一状态的浮动收益
        # self.floating_pl_last = floating_pl_last

    @staticmethod
    def create_by_trade_detail(trade_detail: TradeDetail):
        direction, action, instrument_id = trade_detail.direction, trade_detail.action, trade_detail.symbol
        # trade_price, trade_vol, trade_idx = trade_detail.trade_price, trade_detail.trade_vol, trade_detail.trade_idx
        # trade_date, trade_time, trade_millisec = trade_detail.trade_date, trade_detail.trade_time, trade_detail.trade_millisec
        # stg_run_id = trade_detail.stg_run_id
        if action == int(Action.Close):
            raise ValueError('trade_detail.action 不能为 close')
        pos_status_detail = PosStatusDetail(stg_run_id=trade_detail.stg_run_id,
                                            trade_agent_key=trade_detail.trade_agent_key,
                                            trade_idx=trade_detail.trade_idx,
                                            trade_dt=trade_detail.trade_dt,
                                            trade_date=trade_detail.trade_date,
                                            trade_time=trade_detail.trade_time,
                                            trade_millisec=trade_detail.trade_millisec,
                                            direction=trade_detail.direction,
                                            symbol=trade_detail.symbol,
                                            position=trade_detail.trade_vol,
                                            avg_price=trade_detail.trade_price,
                                            cur_price=trade_detail.trade_price,
                                            margin=0,
                                            margin_chg=0,
                                            floating_pl=0,
                                            floating_pl_chg=0,
                                            floating_pl_cum=0,
                                            position_date=trade_detail.trade_date
                                            )
        if UPDATE_OR_INSERT_PER_ACTION:
            # 更新最新持仓纪录
            with with_db_session(engine_ibats, expire_on_commit=False) as session:
                session.add(pos_status_detail)
                session.commit()
        return pos_status_detail

    def update_by_trade_detail(self, trade_detail: TradeDetail):
        """
        创建新的对象，根据 trade_detail 更新相关信息
        :param trade_detail:
        :return: 
        """
        # 复制前一个持仓状态
        pos_status_detail = self.create_by_self()
        direction, action, symbol = trade_detail.direction, trade_detail.action, trade_detail.symbol
        trade_price, trade_vol, trade_idx = trade_detail.trade_price, trade_detail.trade_vol, trade_detail.trade_idx

        # 获取合约信息
        # instrument_info = Config.instrument_info_dic[symbol]
        # multiple = instrument_info['VolumeMultiple']
        # margin_ratio = instrument_info['LongMarginRatio']
        multiple, margin_ratio = 1, 1

        # 计算仓位、方向、平均价格
        pos_direction_last, position_last, avg_price_last = self.direction, self.position, self.avg_price
        if pos_direction_last == direction:
            if action == Action.Open:
                # 方向相同：开仓：加仓；
                pos_status_detail.avg_price = \
                    (position_last * avg_price_last + trade_price * trade_vol) / (position_last + trade_vol)
                pos_status_detail.position = position_last + trade_vol
            else:
                # 方向相同：关仓：减仓；
                if trade_vol > position_last:
                    raise ValueError("当前持仓%d，平仓%d，错误" % (position_last, trade_vol))
                elif trade_vol == position_last:
                    # 清仓前计算浮动收益
                    # 未清仓的情况将在下面的代码中统一计算浮动收益
                    if pos_status_detail.direction == Direction.Long:
                        pos_status_detail.floating_pl = (trade_price - avg_price_last) * position_last * multiple
                    else:
                        pos_status_detail.floating_pl = (avg_price_last - trade_price) * position_last * multiple

                    pos_status_detail.avg_price = 0
                    pos_status_detail.position = 0

                else:
                    pos_status_detail.avg_price = (position_last * avg_price_last - trade_price * trade_vol) / (
                            position_last - trade_vol)
                    pos_status_detail.position = position_last - trade_vol
        elif position_last == 0:
            pos_status_detail.avg_price = trade_price
            pos_status_detail.position = trade_vol
            pos_status_detail.direction = direction
        else:
            # 方向相反
            raise ValueError("当前仓位：%s %d手，目标操作：%s %d手，请先平仓在开仓" % (
                "多头" if pos_direction_last == Direction.Long else "空头", position_last,
                "多头" if direction == Direction.Long else "空头", trade_vol,
            ))
            # if position == trade_vol:
            #     # 方向相反，量相同：清仓
            #     pos_status_detail.avg_price = 0
            #     pos_status_detail.position = 0
            # else:
            #     holding_amount = position * avg_price
            #     trade_amount = trade_price * trade_vol
            #     position_rest = position - trade_vol
            #     avg_price = (holding_amount - trade_amount) / position_rest
            #     if position > trade_vol:
            #         # 减仓
            #         pos_status_detail.avg_price = avg_price
            #         pos_status_detail.position = position_rest
            #     else:
            #         # 多空反手
            #         self.logger.warning("%s 持%s：%d -> %d 多空反手", self.symbol,
            #                             '多' if direction == int(Direction.Long) else '空', position, position_rest)
            #         pos_status_detail.avg_price = avg_price
            #         pos_status_detail.position = position_rest
            #         pos_status_detail.direction = Direction.Short if direction == int(Direction.Short) else Direction.Long

        # 设置其他属性
        pos_status_detail.cur_price = trade_price
        pos_status_detail.trade_dt = trade_detail.trade_dt
        pos_status_detail.trade_date = trade_detail.trade_date
        pos_status_detail.trade_time = trade_detail.trade_time
        pos_status_detail.trade_millisec = trade_detail.trade_millisec

        # 计算 floating_pl margin
        position_cur = pos_status_detail.position
        # cur_price = pos_status_detail.cur_price
        avg_price_last = pos_status_detail.avg_price
        pos_status_detail.margin = position_cur * trade_price * multiple * margin_ratio
        # 如果当前仓位不为 0 则计算浮动收益
        if position_cur > 0:
            if pos_status_detail.direction == Direction.Long:
                pos_status_detail.floating_pl = (trade_price - avg_price_last) * position_cur * multiple
            else:
                pos_status_detail.floating_pl = (avg_price_last - trade_price) * position_cur * multiple
        # 如果前一状态仓位为 0,  且不是多空切换的情况，则保留上一状态的浮动收益
        if self.position == 0 and self.trade_dt != trade_detail.trade_dt:
            pos_status_detail.margin_chg = pos_status_detail.margin
            pos_status_detail.floating_pl_chg = pos_status_detail.floating_pl
        else:
            pos_status_detail.margin_chg = pos_status_detail.margin - self.margin
            pos_status_detail.floating_pl_chg = pos_status_detail.floating_pl - self.floating_pl

        pos_status_detail.floating_pl_cum += pos_status_detail.floating_pl_chg

        if UPDATE_OR_INSERT_PER_ACTION:
            # 更新最新持仓纪录
            with with_db_session(engine_ibats, expire_on_commit=False) as session:
                session.add(pos_status_detail)
                session.commit()
        return pos_status_detail

    def create_by_self(self):
        """
        创建新的对象
        若当前对象持仓为0（position==0），则 浮动收益部分设置为0
        :return: 
        """
        position = self.position
        pos_status_detail = PosStatusDetail(stg_run_id=self.stg_run_id,
                                            trade_agent_key=self.trade_agent_key,
                                            trade_idx=self.trade_idx,
                                            trade_dt=self.trade_dt,
                                            trade_date=self.trade_date,
                                            trade_time=self.trade_time,
                                            trade_millisec=self.trade_millisec,
                                            direction=self.direction,
                                            symbol=self.symbol,
                                            position=position,
                                            avg_price=self.avg_price,
                                            cur_price=self.cur_price,
                                            floating_pl=self.floating_pl if position > 0 else 0,
                                            floating_pl_cum=self.floating_pl_cum,
                                            margin=self.margin,
                                            # floating_pl_last=self.floating_pl,
                                            )
        return pos_status_detail

    @staticmethod
    def remove(stg_run_id: int):
        """
        仅作为调试工具使用，删除指定 stg_run_id 相关的 pos_status_detail
        :param stg_run_id: 
        :return: 
        """
        with with_db_session(engine_ibats) as session:
            # session.execute('DELETE FROM pos_status_detail WHERE stg_run_id=:stg_run_id',
            #                 {'stg_run_id': stg_run_id})
            session.query(PosStatusDetail).filter(PosStatusDetail.stg_run_id == stg_run_id).delete()
            session.commit()
        # PosStatusInfo.query.filter


class TradeAgentStatusDetail(BaseModel):
    """持仓状态数据"""
    __tablename__ = 'trade_agent_status_detail'
    stg_run_id = Column(Integer, primary_key=True)  # 对应回测了策略 StgRunID 此数据与 AccSumID 对应数据相同
    trade_agent_status_detail_idx = Column(Integer, primary_key=True)
    trade_agent_key = Column(String(40))
    trade_dt = Column(DateTime)
    trade_date = Column(Date)  # 对应行情数据中 ActionDate
    trade_time = Column(Time)  # 对应行情数据中 ActionTime
    trade_millisec = Column(Integer)  # 对应行情数据中 ActionMillisec
    available_cash = Column(DOUBLE, default=0.0)  # 可用资金, double
    curr_margin = Column(DOUBLE, default=0.0)  # 当前保证金总额, double
    close_profit = Column(DOUBLE, default=0.0)
    position_profit = Column(DOUBLE, default=0.0)
    floating_pl_cum = Column(DOUBLE, default=0.0)
    fee_tot = Column(DOUBLE, default=0.0)
    balance_tot = Column(DOUBLE, default=0.0)

    def __init__(self, stg_run_id=None, trade_agent_key=None,
                 trade_dt=None, trade_date=None, trade_time=None, trade_millisec=None,
                 available_cash=None, curr_margin=None, close_profit=None, position_profit=None, floating_pl_cum=None,
                 fee_tot=None, balance_tot=None):
        self.stg_run_id = stg_run_id
        self.trade_agent_status_detail_idx = None if stg_run_id is None else idx_generator(
            stg_run_id, TradeAgentStatusDetail)
        self.trade_agent_key = trade_agent_key
        self.trade_dt = date_time_2_str(trade_date, trade_time) if trade_dt is None else trade_dt
        self.trade_date = trade_date
        self.trade_time = trade_time
        self.trade_millisec = trade_millisec
        self.available_cash = available_cash
        self.curr_margin = curr_margin
        self.close_profit = close_profit
        self.position_profit = position_profit
        self.floating_pl_cum = floating_pl_cum
        self.fee_tot = fee_tot
        self.balance_tot = balance_tot

    @staticmethod
    def create(stg_run_id, trade_agent_key, init_cash: int, md: dict):
        """
        根据 md 及 初始化资金 创建对象，默认日期为当前md数据-1天
        :param stg_run_id:
        :param trade_agent_key:
        :param init_cash: 
        :param md: 
        :return: 
        """
        warnings.warn('该函数为范例函数，需要根据实际情况改写', UserWarning)
        trade_date = str_2_date(md['ActionDay']) - timedelta(days=1)
        trade_time = pd_timedelta_2_timedelta(md['ActionTime'])
        trade_millisec = int(md.setdefault('ActionMillisec', 0))
        trade_price = float(md['close'])
        acc_status_detail = TradeAgentStatusDetail(stg_run_id=stg_run_id,
                                                   trade_agent_key=trade_agent_key,
                                                   trade_date=trade_date,
                                                   trade_time=trade_time,
                                                   trade_millisec=trade_millisec,
                                                   available_cash=init_cash,
                                                   balance_tot=init_cash,
                                                   )
        if UPDATE_OR_INSERT_PER_ACTION:
            # 更新最新持仓纪录
            with with_db_session(engine_ibats, expire_on_commit=False) as session:
                session.add(acc_status_detail)
                session.commit()
        return acc_status_detail

    def create_by_self(self):
        """
        创建新的对象，默认前一日持仓信息的最新价，等于下一交易日的结算价（即 AvePrice）
        :return: 
        """
        trade_agent_status_detail = TradeAgentStatusDetail(stg_run_id=self.stg_run_id,
                                                           trade_agent_key=self.trade_agent_key,
                                                           trade_date=self.trade_date,
                                                           trade_time=self.trade_time,
                                                           trade_millisec=self.trade_millisec,
                                                           available_cash=self.available_cash,
                                                           curr_margin=self.curr_margin,
                                                           close_profit=self.close_profit,
                                                           position_profit=self.position_profit,
                                                           floating_pl_cum=self.floating_pl_cum,
                                                           fee_tot=self.fee_tot,
                                                           balance_tot=self.balance_tot
                                                           )
        return trade_agent_status_detail

    def update_by_pos_status_detail(self, pos_status_detail_dic, md: dict):
        """
        根据 持仓列表更新账户信息
        :param pos_status_detail_dic:
        :return: 
        """
        warnings.warn('该函数为范例函数，需要根据实际情况改写', UserWarning)
        trade_agent_status_detail = self.create_by_self()
        # 更新日期、时间
        trade_date = md['ActionDay']
        trade_time = pd_timedelta_2_timedelta(md['ActionTime'])
        trade_millisec = int(md.setdefault('ActionMillisec', 0))

        available_cash_chg = 0
        curr_margin = 0
        close_profit = 0
        position_profit = 0
        floating_pl_chg = 0
        margin_chg = 0
        floating_pl_cum = 0
        for instrument_id, pos_status_detail in pos_status_detail_dic.items():
            curr_margin += pos_status_detail.margin
            if pos_status_detail.position == 0:
                close_profit += pos_status_detail.floating_pl
            else:
                position_profit += pos_status_detail.floating_pl
            floating_pl_chg += pos_status_detail.floating_pl_chg
            margin_chg += pos_status_detail.margin_chg
            floating_pl_cum += pos_status_detail.floating_pl_cum

        available_cash_chg = floating_pl_chg - margin_chg
        trade_agent_status_detail.curr_margin = curr_margin
        # # 对于同一时间，平仓后又开仓的情况，不能将close_profit重置为0
        # if trade_date == trade_date_last and trade_time == trade_time_last and trade_millisec == trade_millisec_last:
        #     trade_agent_status_detail.close_profit += close_profit
        # else:
        # 一个单位时段只允许一次，不需要考虑上面的情况
        trade_agent_status_detail.close_profit = close_profit

        trade_agent_status_detail.position_profit = position_profit
        trade_agent_status_detail.available_cash += available_cash_chg
        trade_agent_status_detail.floating_pl_cum = floating_pl_cum
        trade_agent_status_detail.balance_tot = trade_agent_status_detail.available_cash + curr_margin

        trade_agent_status_detail.trade_date = trade_date
        trade_agent_status_detail.trade_time = trade_time
        trade_agent_status_detail.trade_millisec = trade_millisec
        if UPDATE_OR_INSERT_PER_ACTION:
            # 更新最新持仓纪录
            with with_db_session(engine_ibats, expire_on_commit=False) as session:
                session.add(trade_agent_status_detail)
                session.commit()
        return trade_agent_status_detail


class StgRunStatusDetail(BaseModel):
    """记录每一单位时刻 所有trade_agent_detail 状态汇总"""
    __tablename__ = 'stg_run_status_detail'
    stg_run_id = Column(Integer, primary_key=True)  # 对应回测了策略 StgRunID 此数据与 AccSumID 对应数据相同
    stg_run_status_detail_idx = Column(Integer, primary_key=True)
    trade_dt = Column(DateTime)
    trade_date = Column(Date)  # 对应行情数据中 ActionDate
    trade_time = Column(Time)  # 对应行情数据中 ActionTime
    trade_millisec = Column(Integer)  # 对应行情数据中 ActionMillisec
    available_cash = Column(DOUBLE, default=0.0)  # 可用资金, double
    curr_margin = Column(DOUBLE, default=0.0)  # 当前保证金总额, double
    close_profit = Column(DOUBLE, default=0.0)
    position_profit = Column(DOUBLE, default=0.0)
    floating_pl_cum = Column(DOUBLE, default=0.0)
    fee_tot = Column(DOUBLE, default=0.0)
    balance_tot = Column(DOUBLE, default=0.0)

    def __init__(self, stg_run_id=None,
                 trade_dt=None, trade_date=None, trade_time=None, trade_millisec=None,
                 available_cash=None, curr_margin=None, close_profit=None, position_profit=None, floating_pl_cum=None,
                 fee_tot=None, balance_tot=None):
        self.stg_run_id = stg_run_id
        self.stg_run_status_detail_idx = None if stg_run_id is None else idx_generator(
            stg_run_id, StgRunStatusDetail)
        self.trade_dt = date_time_2_str(trade_date, trade_time) if trade_dt is None else trade_dt
        self.trade_date = trade_date
        self.trade_time = trade_time
        self.trade_millisec = trade_millisec
        self.available_cash = available_cash
        self.curr_margin = curr_margin
        self.close_profit = close_profit
        self.position_profit = position_profit
        self.floating_pl_cum = floating_pl_cum
        self.fee_tot = fee_tot
        self.balance_tot = balance_tot

    @staticmethod
    def create_by_trade_agent_status_detail_list(stg_run_id, trade_agent_status_detail_list):
        """通过 trade_agent_status_detail_list 更新当前 stg_run_detail 状态"""
        data_len = len(trade_agent_status_detail_list)
        if data_len == 0:
            return None

        stg_run_id = stg_run_id
        trade_dt, trade_date, trade_time, trade_millisec = None, None, None, None
        available_cash, curr_margin, close_profit, position_profit = 0, 0, 0, 0
        floating_pl_cum, fee_tot, balance_tot = 0, 0, 0
        for detail in trade_agent_status_detail_list:
            if trade_dt is None or trade_dt < detail.trade_dt:
                trade_dt = detail.trade_dt
                trade_date = detail.trade_date
                trade_time = detail.trade_time
                trade_millisec = detail.trade_millisec

            available_cash += 0 if detail.available_cash is None else detail.available_cash
            curr_margin += 0 if detail.curr_margin is None else detail.curr_margin
            close_profit += 0 if detail.close_profit is None else detail.close_profit
            position_profit += 0 if detail.position_profit is None else detail.position_profit
            floating_pl_cum += 0 if detail.floating_pl_cum is None else detail.floating_pl_cum
            fee_tot += 0 if detail.fee_tot is None else detail.fee_tot
            balance_tot += 0 if detail.balance_tot is None else detail.balance_tot

        stg_run_status_detail = StgRunStatusDetail(
            stg_run_id=stg_run_id,
            trade_dt=trade_dt,
            trade_date=trade_date,
            trade_time=trade_time,
            trade_millisec=trade_millisec,
            available_cash=available_cash,
            curr_margin=curr_margin,
            close_profit=close_profit,
            position_profit=position_profit,
            floating_pl_cum=floating_pl_cum,
            fee_tot=fee_tot,
            balance_tot=balance_tot,
        )
        return stg_run_status_detail


def init():
    from ibats_common.utils.db import alter_table_2_myisam
    BaseModel.metadata.create_all(engine_ibats)
    alter_table_2_myisam(engine_ibats)
    print("所有表结构建立完成")


if __name__ == "__main__":
    init()
    # 创建user表，继承metadata类
    # Engine使用Schama Type创建一个特定的结构对象
    # stg_info_table = Table("stg_info", metadata, autoload=True)
