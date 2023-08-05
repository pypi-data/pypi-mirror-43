# coding=UTF-8
"""
从tushare中下载常用指数的日线数据存储到基金评价分析的数据库中
"""
import tushare as ts
from guosen.data import data_api
from WindPy import w
import datetime
import time
import math


def index_data_init():
    data_api.connect_sql()
    data_api.execute('use db_fund_info;')
    data_api.execute('truncate t_index_data;')
    data_api.close_sql()


def save_index_data(sql_statement):
    data_api.connect_sql()
    data_api.execute('use db_fund_info;')
    data_api.execute(sql_statement)
    data_api.close_sql()


def get_sql_statement(benchmark_name, benchmark_code, benchmark_data):
    sql_statement = []
    for i in range(len(benchmark_data)):
        temp_date = benchmark_data.iat[i, 0]
        temp_close = benchmark_data.iat[i, 2]
        sql_statement.append(str((benchmark_name, benchmark_code, temp_date, temp_close)))

    return "insert into t_index_data values " + ','.join(sql_statement)


def gen_sql_statement(name, code, times, datas):
    sql_statement = []
    for i in range(len(times)):
        temp_date = times[i]
        temp_close = datas[i]
        sql_statement.append(str((name, code, temp_date, temp_close)))

    return "insert into t_index_data values" + ','.join(sql_statement)


def save_wind_sw_industry_data():
    start_date = '2017-01-01'
    end_date = datetime.datetime.today().strftime("%Y%m%d")

    wind_industry_data = w.wset("sectorconstituent", "date=" + end_date + ";sectorid=a39901011g000000")
    wind_industry_code_to_name = dict(zip(wind_industry_data.Data[1], wind_industry_data.Data[2]))

    wind_industry_codes = ','.join(wind_industry_code_to_name.keys())

    wind_industry_price_data = w.wsd(wind_industry_codes, "close", start_date, end_date, "")

    if wind_industry_price_data.ErrorCode != 0:
        print("save_wind_sw_industry_data 下载数据异常，错误代码：" + wind_industry_price_data.ErrorCode)
        return

    times = wind_industry_price_data.Times
    times = [temp_time.strftime("%Y-%m-%d") for temp_time in times]

    price_datas = wind_industry_price_data.Data
    wind_codes = wind_industry_price_data.Codes

    num = len(price_datas)
    for i in range(num):
        temp_price_data = price_datas[i]
        wind_industry_code = wind_codes[i]
        wind_industry_name = wind_industry_code_to_name[wind_industry_code]

        save_index_data(gen_sql_statement(wind_industry_name, wind_industry_code, times, temp_price_data))


def sava_wind_amt_data():
    start_date = '2017-01-01'
    end_date = datetime.datetime.today().strftime("%Y-%m-%d")

    wind_code = "881001.WI"

    market_data = w.wsd(wind_code, "amt,turn", start_date, end_date, "PriceAdj=F")

    if market_data.ErrorCode != 0:
        print("sava_wind_amt_data 下载数据异常，错误代码：" + market_data.ErrorCode)
        return

    times = market_data.Times
    times = [temp_time.strftime("%Y-%m-%d") for temp_time in times]

    amt_datas = market_data.Data[0]
    turnover_datas = market_data.Data[1]

    num = len(times)
    sql_statement = []
    for i in range(num):
        temp_amt_data = amt_datas[i]
        temp_turnover_data = turnover_datas[i]
        temp_date = times[i]

        if math.isnan(temp_amt_data) or math.isnan(temp_turnover_data):
            continue

        sql_statement.append(str(("万得全A", wind_code, temp_date, temp_amt_data, temp_turnover_data)))

    sql_statement = "insert into t_market_data values " + ','.join(sql_statement)

    data_api.connect_sql()
    data_api.execute('use db_fund_info;')
    data_api.execute('truncate t_market_data;')
    data_api.close_sql()

    save_index_data(sql_statement)


def load_data():
    index_data_init()

    stk_code = '000905'
    stk_name = '中证500'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '000300'
    stk_name = '沪深300'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '000001'
    stk_name = '上证综指'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '399001'
    stk_name = '深圳成指'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '399005'
    stk_name = '中小板指'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '399006'
    stk_name = '创业板指'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '000016'
    stk_name = '上证50'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '000903'
    stk_name = '中证100'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '000852'
    stk_name = '中证1000'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))


if __name__ == '__main__':
    time_start = time.time()

    w.start()
    # load_data()
    # save_wind_sw_industry_data()
    sava_wind_amt_data()
    w.close()

    time_end = time.time()
    print('totally cost', time_end - time_start)
    print("update index data complete!")
