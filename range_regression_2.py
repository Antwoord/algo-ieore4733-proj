import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas.io.data as web

# step 1: Range Selection
st = dt.datetime(2000,12,1)
en = dt.datetime(2015,1,1)
sp500_tickers_lil = ['AA','AAPL','ABC','ABT','ADBE','ADI','ADM','ADP','ADSK','AEE']
sp500_tickers_joey = ['AA','AAPL','ABC','ABT','ADBE','ADI','ADM','ADP','ADSK','AEE','AEP','AES','AET','AFL','AGN','AIG','AIV','AIZ','AKAM','ALL','AMAT','AMGN','AMP','AMT','AMZN','AN','ANTM','AON','APA','APC','APD','AVB','AVY','AXP','AZO','BA','BAC','BAX','BBBY','BBT','BBY','BCR','BDX','BEN',,'BHI','BIIB','BK','BLL','BMY','BRCM','BSX','BXP','C','CA','CAG','CAH','CAT','CB','CBG','CBS','CCE','CCL','CELG','CHK','CHRW','CI','CINF','CL','CLX','CMA','CMCSA','CME','CMI','CMS','CNP','CNX','COF','COH','COL','COP','COST','CPB','CSCO','CSX','CTAS','CTL','CTSH','CTXS','CVS','CVX','D','DD','DE','DFS','DGX','DHI','DHR','DIS','DOV','DOW','DRI','DTE','DUK','DVN','EA','EBAY','ECL','ED','EFX','EIX','EL','EMC','EMN','EMR','EOG','EQR','ESRX','ETFC','ETN','ETR','EXC','EXPD','EXPE','F','FCX','FDX','FE','FIS','FISV','FITB','FLR','FOXA','FTR','GAS','GD','GE','GILD','GIS','GLW','GME','GOOGL','GPC','GPS','GS','GT','GWW','HAL','HAR','HAS','HBAN','HD','HES','HIG','HOG','HON','HOT','HPQ','HRB','HST','HSY','HUM','IBM','ICE','IFF','INTC','INTU','IP','IPG','ITW','JCI','JEC','JNJ','JNPR','JPM','JWN','K','KEY','KIM','KLAC','KMB','KO','KR','KSS','L','LB','LEG','LEN','LH','LLL','LLTC','LLY','LM','LMT','LNC','LOW','LUK','LUV','M','MAR','MAS','MAT','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','MHFI','MKC','MMC','MMM','MO','MON','MRK','MRO','MS','MSFT','MSI','MTB','MU','MUR','MYL','NBL','NEE','NEM','NI','NKE','NOC','NOV','NSC','NTAP','NTRS','NUE','NVDA','NWL','OMC','ORCL','OXY','PAYX','PBI','PCAR','PCG','PCL','PCP','PDCO','PEG','PEP','PFE','PFG','PG','PGR','PH','PHM','PKI','PLD','PNC','PNW','POM','PPG','PPL','PRU','PSA','PX','QCOM','R','RAI','RF','RHI','RL','ROK','RRC','RTN','SBUX','SCHW','SE','SEE','SHW','SLB','SNA','SNDK','SO','SPG','SPLS','SRE','STI','STJ','STT','STZ','SWK','SYK','SYMC','SYY','T','TAP','TDC','TE','TGT','THC','TIF','TJX','TMK','TMO','TROW','TRV','TSN','TSO','TSS','TWX','TXN','TXT','UNH','UNM','UNP','UPS','USB','UTX','VAR','VFC','VIAB','VLO','VMC','VNO','VRSN','VZ','WAT','WBA','WFC','WFM','WHR','WM','WMB','WMT','WU','WY','WYN','XEL','XL','XLNX','XOM','XRX','YHOO','YUM','ZBH','ZION']

spy = web.get_data_yahoo('SPY',start = st,end = en)['Adj Close']
spy_data = spy.resample("M",how = 'last').pct_change()

regr_coefs = []

dataset = sp500_tickers_joey
#dataset = ['AA']

for ticker in dataset:
    try:
        data = web.get_data_yahoo(ticker, start=st, end=en).resample("M",how = 'last')['Adj Close']
    except:
        print(ticker, "error")
        continue
        
    data_pct = data.pct_change().dropna()

    #returns = pd.DataFrame(index = data.index,columns = [1,2,3,4,5,6,7,8,9,10,11,12,'spy'])

    returns = {}
    for i in range(12,len(data_pct.index)):
        today = data_pct.index[i]
        yesterday = data_pct.index[i-1]
        returns[today] = {}
        for lag in range(1,13):
            lagged_date = data_pct.index[i-lag-1]
            returns[today][lag] = data[yesterday]/data[lagged_date]-1.0

    for x in returns:
        print x, returns[x][1], returns[x][2], returns[x][3]
    #for i in range(1,13):
    #    if i in [1,2,3,4,5,6,7,8,9,10,11,12]:
    #        returns[i] = ((data.shift(1)/data.shift(i+1))-1)/i
    #    else:
    #       returns[i] = 0.0

    returns = pd.DataFrame(returns).T
    returns['spy'] = spy_data

    #returns  = returns.ix[14:]
    data_p = data_pct.ix[12:] #[-len(returns):].copy()

    result = sm.OLS(data_p,returns).fit()
    print(result.summary())
    regr_coefs.append(result.params)
    
#print("done")
avg_coefs = np.mean(np.array(regr_coefs),axis=0)
labels = ["1m","2m","3m","4m","5m","6m","7m","8m","9m","10m","11m","12m","spy"]
for x in zip(labels, avg_coefs):
    print(x)

