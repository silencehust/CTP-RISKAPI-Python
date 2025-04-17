import time
from datetime import datetime
import csv
from pathlib import Path

import RISK.riskuserapi as riskuserapi

filename=f"broker_deposit{datetime.now().strftime('%Y%m%d')}.csv"

def initCSVFile():
    if not Path(filename).exists():
        with open(filename, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ["自然日期", "当前时间", "当前时间(毫秒)", "经纪公司代码", "会员代码", "交易所代码", "上次结算准备金",
                "当前保证金总额", "平仓盈亏", "期货结算准备金", "入金金额", "出金金额", "可提资金", "基本准备金",
                "冻结的保证金", "交易日期"])

class riskUerApi(riskuserapi.CShfeFtdcRiskUserSpi):
    def __init__(self, risk_front, broker_id, user_id, password):
        super().__init__()
        self.risk_front = risk_front
        self.nRequestID = 0
        self.login = False
        self.api = None
        self.broker_id = broker_id
        self.user_id = user_id
        self.password = password

    def run(self):
        self.api = riskuserapi.CShfeFtdcRiskUserApi.CreateFtdcRiskUserApi()
        self.api.RegisterSpi(self)
        self.api.RegisterFront(self.risk_front)
        self.api.Init()
        time.sleep(1)

    def OnFrontConnected(self):
        print("前置连接成功。")
        req = riskuserapi.CShfeFtdcReqRiskUserLoginField()
        req.BrokerID = self.broker_id
        req.UserID = self.user_id
        req.Password = self.password
        self.nRequestID += 1
        ret = self.api.ReqRiskUserLogin(req, self.nRequestID)
        if ret == 0:
            self.login = True
            print("发送风控用户登录请求成功。")
            initCSVFile()
        else:
            print("发送风控用户登录请求失败。")

    def OnFrontDisconnected(self, nReason: "int") -> "void":
        print(f"前置连接断开。nReason={nReason}")
        self.login = False

    def OnRspRiskUserLogin(self, pRspRiskUserLogin: "CShfeFtdcRspRiskUserLoginField", pRspInfo: "CShfeFtdcRspInfoField",
                           nRequestID: "int", bIsLast: "bool") -> "void":
        if pRspInfo is not None and pRspInfo.ErrorID != 0:
            print(f"风控用户登录失败。错误信息：{pRspInfo.ErrorMsg}")
            return
        print(f"风控用户登录成功。交易日为{pRspRiskUserLogin.TradingDay}")

    def QueryBrokerDeposit(self, exchange_id):
        req = riskuserapi.CShfeFtdcQueryBrokerDepositField()
        req.BrokerID = self.broker_id
        req.ExchangeID = exchange_id
        self.nRequestID += 1
        ret = self.api.ReqRiskQryBrokerDeposit(req, self.nRequestID)
        if ret == 0:
            print("发送查询经纪公司资金请求成功。")
        else:
            print("发送查询经纪公司资金请求失败。")

    def OnRspRiskQryBrokerDeposit(self, pQueryBrokerDeposit: "CShfeFtdcQueryBrokerDepositField",
                                  pRspInfo: "CShfeFtdcRspInfoField", nRequestID: "int", bIsLast: "bool") -> "void":
        if pRspInfo is not None and pRspInfo.ErrorID != 0:
            print(f"查询经纪公司资金失败。错误信息：{pRspInfo.ErrorMsg}")
            return

    def OnRtnBrokerDeposit(self, pBrokerDeposit: "CShfeFtdcBrokerDepositField") -> "void":
        print(
            f"{pBrokerDeposit.ActionDay} {pBrokerDeposit.CurrTime} {pBrokerDeposit.CurrMillisec} 查询经纪公司资金成功。",
            f"经纪公司代码：{pBrokerDeposit.BrokerID}",
            f"会员代码：{pBrokerDeposit.ParticipantID}",
            f"交易所代码：{pBrokerDeposit.ExchangeID}",
            f"上次结算准备金：{pBrokerDeposit.PreBalance}",
            f"当前保证金总额：{pBrokerDeposit.CurrMargin}",
            f"平仓盈亏：{pBrokerDeposit.CloseProfit}",
            f"期货结算准备金：{pBrokerDeposit.Balance}",
            f"入金金额：{pBrokerDeposit.Deposit}",
            f"出金金额：{pBrokerDeposit.Withdraw}",
            f"可提资金：{pBrokerDeposit.Available}",
            f"基本准备金：{pBrokerDeposit.Reserve}",
            f"冻结的保证金：{pBrokerDeposit.FrozenMargin}",
            f"交易日期：{pBrokerDeposit.TradingDay}"
        )
        with open(filename, "a", newline='') as fp:
            writer = csv.writer(fp)
            result = [pBrokerDeposit.ActionDay, pBrokerDeposit.CurrTime, pBrokerDeposit.CurrMillisec,
                      pBrokerDeposit.BrokerID, pBrokerDeposit.ParticipantID, pBrokerDeposit.ExchangeID,
                      pBrokerDeposit.PreBalance, pBrokerDeposit.CurrMargin, pBrokerDeposit.CloseProfit,
                      pBrokerDeposit.Balance, pBrokerDeposit.Deposit, pBrokerDeposit.Withdraw, pBrokerDeposit.Available,
                      pBrokerDeposit.Reserve, pBrokerDeposit.FrozenMargin, pBrokerDeposit.TradingDay]
            writer.writerow(result)


if __name__ == '__main__':
    risk = riskUerApi("tcp://10.10.10.2:11001", "0001", "username", "password")
    risk.run()
    time.sleep(5)
    while risk.login:
        time.sleep(2)
    risk.api.Release()
