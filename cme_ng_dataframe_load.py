import pandas as pd, numpy as np, math, pandas.io.sql as psql, mysql.connector

#connect to db and select view
cnx = mysql.connector.connect(host="localhost",user="root",passwd="D0lph1n$7",database="futures")
query = "select * from futures_view"

#load query into dataframe
df = psql.read_sql(query, con=cnx)

#index table based on date
df['date'] = pd.to_datetime(df['datadate'])
df = df.set_index('date')
df.drop(['datadate'], axis=1, inplace=True)

#create returns dataframe
dfret = df / df.shift(1) - 1

#functionality
#full volatility
dfret.std()
#full annualized volatility
dfret.std() * math.sqrt(252)
#trailing 60 day volatility
dfret.rolling(60).std()
#trailing 60 day annualized volatility
dfret.rolling(60).std() * math.sqrt(252)

#compute annual vol from specified contract_root
def get_annual_vol(contract_root):
	dfretcols=dfret.columns
	dfretarray=dfretcols.str.contains(contract_root, regex=False)
	dfretactivecol = dfretcols[dfretarray]
	annvols = pd.DataFrame(dfret[dfretactivecol].std()*math.sqrt(252))
	annvols.index.names = ['code_name']
	annvols.columns = ['annualized_vol']
	return annvols.sort_values(by=['annualized_vol'],axis=0, ascending=False)

#compute largest single day return and date for specified contract_root
def get_largest_single_day_return(contract_root):
	dfretcols2=dfret.columns
	dfretarray=dfretcols2.str.contains(contract_root, regex=False)
	dfretactivecol = dfretcols2[dfretarray]
	dfretidxmax = pd.DataFrame(dfret[dfretactivecol].idxmax())
	dfretmax = pd.DataFrame(dfret[dfretactivecol].max())
	dfretidxmax.columns = ['date']
	dfretmax.columns = ['single_day_return']
	dfretjoin = pd.merge(dfretidxmax, dfretmax, right_index=True, left_index=True)
	dfretjoin.index.names = ['code_name']
	return dfretjoin.sort_values(by=['single_day_return'],axis=0, ascending=False)

#shift by one to get 12/31 figures for annual returns and group by year
dfshift = df.shift(1)
dfshiftann = dfshift.groupby([dfshift.index.year])

#compute product of (1+return) at an annual level
dfretplusann = dfretplus.groupby([dfretplus.index.year]).prod()

#compute 
dfretplusann.prod()

#alternatively
dfretplus = dfret + 1
dfretplus.prod()

#compute largest annual return
def get_largest_annual_return(contract_root):
	dfretcols2=dfret.columns
	dfretarray=dfretcols2.str.contains(contract_root, regex=False)
	dfretactivecol = dfretcols2[dfretarray]
	dfretplus = dfret + 1
	dfretplusann = dfretplus[dfretactivecol].groupby([dfretplus.index.year]).prod()-1
	dfretplusannmax = dfretplusann.max()
	dfreturn = pd.DataFrame({'code_name':dfretplusannmax.index, 'annual_return':dfretplusannmax.values})
	return dfreturn.sort_values(by=['annual_return'],axis=0, ascending=False)

#compute annualized return
def get_annualized_return(contract_root):
	dfretcols2=dfret.columns
	dfretarray=dfretcols2.str.contains(contract_root, regex=False)
	dfretactivecol = dfretcols2[dfretarray]
	dfretplus = dfret + 1
	dfretann = dfretplus[dfretactivecol].prod() ** (1/(dfretplus[dfretactivecol].count()/252)) - 1
	dfretann.name = 'annual_return'
	dfretann.index.names = ['code_name']
	return dfretann.sort_values(axis=0, ascending=False)

#compute sharp ratio
def def get_sharpe_ratio(contract_root):
	dfretcols2=dfret.columns
	dfretarray=dfretcols2.str.contains(contract_root, regex=False)
	dfretactivecol = dfretcols2[dfretarray]
	dfretplus = dfret + 1
	dfretann = dfretplus[dfretactivecol].prod() ** (1/(dfretplus[dfretactivecol].count()/252)) - 1
	dfretstd = dfret[dfretactivecol].std() * math.sqrt(252)
	dfretsharpe = (dfretann - 0.0244) / dfretstd
	return dfretsharpe.sort_values(axis=0, ascending=False)
