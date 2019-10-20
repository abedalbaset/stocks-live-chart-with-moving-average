import urllib.request, json
import pandas as pd
import matplotlib.pyplot as plt
import time
import plotly.graph_objects as go
from plotly import tools
import chart_studio.plotly as py
import plotly.express as px
import pandas as pd
fig=plt.figure()
Time=100 #time that we want to show

while(True):
 #uplode data from website in Json type
 with urllib.request.urlopen("https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count="+str(Time)+"&granularity=M1") as url:
     data = json.loads(url.read().decode())
     #print (data)
 df = pd.DataFrame(data['candles'])
 #print(df)

 #find minimum
 min=[]
 for index, row in df.iterrows():
  if ((row['openBid'])>(row['closeBid'])):
      min.append((row['closeBid']))
  else:
      min.append((row['openBid']))
 #print('min = ',min)
 #find demand
 absl=[]
 for index, row in df.iterrows():
   temp=abs(row['openBid']-row['closeBid'])
   absl.append(temp/2)
 #print('absl =',absl)
 demand=[]
 for i in range(len(min)):
     demand.append(absl[i]+min[i])
 #print('demand =',demand)
 # Find moving average
 def moving_average(N,mylist):
  cumsum, moving_aves = [0], []
  for i, x in enumerate(mylist, 1):
   cumsum.append(cumsum[i-1] + mylist[i-1])
   if i>=N:
     moving_ave = (cumsum[i] - cumsum[i-N])/N
     #can do stuff with moving_ave here
     moving_aves.append(moving_ave)
  return(moving_aves)
 MA1=moving_average(8,demand)
 MA2=moving_average(16,demand)
 MA3=moving_average(40,demand)
 #print("MA for N=8",len(MA1),MA1)
 #print("MA for N=16 , ",MA2)
 #print("MA for N=40 , ",MA3)

 timedf=df['time']
 print('hadehea',timedf)
 timee=Time-1
 fig1 = go.Figure(data=[go.Candlestick(x=df['time'],
                 open=df['openBid'], high=df['highBid'],
                 low=df['lowBid'], close=df['closeBid'],name="EURUSD"),
               go.Scatter(x=df.loc[7:timee,'time'],y=MA1,name="moving avg=8"),
               go.Scatter(x=df.loc[15:timee,'time'],y=MA2,name="moving avg=16"),
               go.Scatter(x=df.loc[39:timee,'time'],y=MA3,name="moving avg=40")
                      ])


 fig1.update_layout(xaxis_rangeslider_visible=False)

 fig1.show()
 time.sleep(60) #update after one minute


