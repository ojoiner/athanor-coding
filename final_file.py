import pandas as pd, numpy as np, math, pandas.io.sql as psql, mysql.connector

#connect to db and select view
cnx = mysql.connector.connect(host="localhost",user="root",passwd="D0lph1n$7",database="futures")
query = "select * from futures_view"

#load query into dataframe
df = psql.read_sql(query, con=cnx)

#index dataframe based on date
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
	dfret_cols = dfret.columns
	boolean_cols = dfret_cols.str.contains(contract_root, regex=False)
	dfret_root_cols = dfret_cols[boolean_cols]
	ann_vols = pd.DataFrame(dfret[dfret_root_cols].std()*math.sqrt(252))
	ann_vols.index.names = ['code_name']
	ann_vols.columns = ['annualized_vol']
	return ann_vols.sort_values(by=['annualized_vol'],axis=0, ascending=False)

#compute largest single day return and date for specified contract_root
def get_largest_single_day_return(contract_root):
	dfret_cols = dfret.columns
	boolean_cols = dfret_cols.str.contains(contract_root, regex=False)
	dfret_root_cols = dfret_cols[boolean_cols]
	dfret_idxmax = pd.DataFrame(dfret[dfret_root_cols].idxmax())
	dfret_max = pd.DataFrame(dfret[dfret_root_cols].max())
	dfret_idxmax.columns = ['date']
	dfret_max.columns = ['single_day_return']
	max_ret_join = pd.merge(dfret_idxmax, dfret_max, right_index=True, left_index=True)
	max_ret_join.index.names = ['code_name']
	return max_ret_join.sort_values(by=['single_day_return'],axis=0, ascending=False)

#compute largest annual return
def get_largest_annual_return(contract_root):
	dfret_cols = dfret.columns
	boolean_cols = dfret_cols.str.contains(contract_root, regex=False)
	dfret_root_cols = dfret_cols[boolean_cols]
	dfret_plus = dfret + 1 #using (1+return) for calculations
	dfret_plus_annual = dfret_plus[dfret_root_cols].groupby([dfret_plus.index.year]).prod()-1
	dfret_annual_max = dfret_plus_ann.max()
	annual_max = pd.DataFrame({'code_name':dfret_annual_max.index, 'annual_return':dfret_annual_max.values})
	return dfreturn.sort_values(by=['annual_return'],axis=0, ascending=False)

#compute annualized return
def get_annualized_return(contract_root):
	dfret_cols = dfret.columns
	boolean_cols = dfret_cols.str.contains(contract_root, regex=False)
	dfret_root_cols = dfret_cols[boolean_cols]
	dfret_plus = dfret + 1 #using (1+return) for calculations
	df_ret_annual = dfretplus[dfret_root_cols].prod() ** (1/(dfretplus[dfret_root_cols].count()/252)) - 1
	df_ret_annual.name = 'annual_return'
	df_ret_annual.index.names = ['code_name']
	return df_ret_annual.sort_values(axis=0, ascending=False)

#compute sharpe ratio
def get_sharpe_ratio(contract_root):
	dfret_cols = dfret.columns
	boolean_cols = dfret_cols.str.contains(contract_root, regex=False)
	dfret_root_cols = dfret_cols[boolean_cols]
	dfret_plus = dfret + 1 #using (1+return) for calculations
	dfret_annual = dfret_plus[dfret_root_cols].prod() ** (1/(dfret_plus[dfret_root_cols].count()/252)) - 1
	dfret_std = dfret[dfret_root_cols].std() * math.sqrt(252)
	dfret_sharpe = (dfret_annual - 0.0244) / dfret_std #using 3-month T-bill rate for risk-free rate
	return dfret_sharpe.sort_values(axis=0, ascending=False)
