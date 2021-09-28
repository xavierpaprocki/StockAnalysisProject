import pandas as pd
import requests


def stockanalysis_to_df(symbol):
    result = dict()
    balance_sheet = 'https://stockanalysis.com/stocks/' + symbol + '/financials/balance-sheet/'
    income_statement = 'https://stockanalysis.com/stocks/' + symbol + '/financials/'
    cash_flow = 'https://stockanalysis.com/stocks/' + symbol + '/financials/cash-flow-statement/'
    sheets = [balance_sheet, income_statement, cash_flow]
    payload = {'data': 'quarterly'}
    for sheet in sheets:
        r = requests.post(sheet, data=payload)
        txt = r.text
        data_start = txt.find("\"quarterly\"") + 13
        data_end = txt.find("},\"trailing\"")
        data = txt[data_start:data_end]
        split = data.split('],\"')
        for line in split:
            items = line.split(':')
            key = items[0][:-1]
            if key == '"datekey':
                key = 'datekey'
            result[key] = []
            if key != 'bvps':
                values = items[1][1:].split(',')
            else:
                values = items[1][1:-1].split(',')
            for entry in values:
                if key != 'datekey':
                    try:
                        entry = float(entry)
                    except ValueError as _:
                        entry = 0
                result[key].append(entry)
    df = pd.DataFrame.from_dict(result)
    df = df.set_index('datekey')
    df.to_csv('scratch.csv')
    return df


def main():
    # this input will be run differently one way or another
    # id like it to be after the original call or something
    print('Input stock symbol')
    symbol = input()
    financial_data = stockanalysis_to_df(symbol)
    return financial_data


if __name__ == '__main__':
    main()