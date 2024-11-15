import FinanceDataReader as fdr

code = '005930'

fdr_data = fdr.DataReader(code)

print(fdr_data)