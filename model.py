import os 
from csv import reader
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plot
import numpy as np
import datetime
from operator import itemgetter
from scipy import stats

class Model:
  def __init__(self, fname):
    self.fname = fname
    self.m = {j:i+1 for i,j in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                                'August', 'September', 'October', 'November', 'December'])}
  def save_list(self, li):
    with open(r'max_revnues.txt', 'w') as w:
      for el in li:
        w.write("%s\n" % el)

  def get_revenue(self):
    try:
        with open(self.fname, newline='') as f:
            r = list(reader(f, delimiter=','))[1]
            return [float(r[el][1:].replace(',','')) for el in range(1, len(r), 2)  if r[el][0] =='$']
    except FileNotFoundError as e:
        raise e

  def get_dates(self):
    try:
      with open(self.fname, newline='') as f:
        d = list(reader(f, delimiter=','))[0]
        return [d[el] for el in range(1, len(d), 2) if d[el][0] != 'U' and d[el][0] != '%']
    except FileNotFoundError as e:
      raise e
  
  def get_time(self):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S").replace(':','_')
    return str(current_time)

  def _setup(self,dates, revenue):
    d,ret,datas,dates_num = [],[],[],[]
    for i in dates:
      cra = i.split('[')[0]
      dates_num.append([self.m[cra.split(' ')[0]], int(cra.split(' ')[1])])
    for j, i in enumerate(dates_num):
      d.append([str(i[0]) +'-'+str(i[1])+'-'+str(1), revenue[j]])
      sdate, srev = {}, {}
    for i in d:
        sdate[i[0]] = 1
        srev[i[1]] = 1
    d1, d2 = list(sdate), list(srev)
    for i in zip(d1, d2):
        ret.append(i)
    for el in ret:
        datas.append([el[0], el[1]])
    return datas
   
  def overall_plot(self, dates, revenue):
    plot.plot(dates,revenue)
    plot.show()
    plot.savefig("overall_plot" + self.get_time() +'.jpg')
  
  def quaterly_plot(self, dates, revenue, show=True):
    
    qd = [dates[i] for i in range(0, len(dates), 3)]
    qr = [revenue[i] for i in range(0, len(revenue), 3)]
    plot.plot(qd, qr)
    if show:
          print([i for i in zip(qd, qr)])
    plot.show()
    plot.savefig("quaterly_plot" +self.get_time() +'.jpg' ) 

  def max_revnues(self, r, d):
    return sorted(zip(d, d),key=itemgetter(1))[-d:]

  def overall_linear_regression(self, d, extension=100, verbose=False):
    fig, ax = plot.subplots()
    dates = [x[0] for x in d]#dates are linear so just use len of revenue
    if len(dates) > 30:
      #print(f'Here is the dates and revenue at 0 {dates[0]} {revenue[0]'}
      revenue = [x[1] for x in d]
      print(f'Here is the dates and revenue at 0 {dates[0]} {revenue[0]}')
      bestfit = stats.linregress(range(len(revenue)),revenue)
      equation = str(round(bestfit[0],2)) + "x + " + str(round(bestfit[1],2)) 
      ax.plot(range(len(revenue)), revenue)
      ax.plot(range(len(revenue)), np.poly1d(np.polyfit(range(len(revenue)), revenue, 1))(range(len(revenue))), '--',label=equation)
      for x in range(len(revenue),len(revenue)+extension):
        revenue.append((bestfit[0]*x)+bestfit[1])#mx + c from linear regression found before
        if verbose:
          print(x)
        newdate = dates[-1][0:8]+str(int(dates[-1][-2:])+1)
        dates.append(newdate)
      ax.plot(range(len(revenue)), np.poly1d(np.polyfit(range(len(revenue)), revenue, 1))(range(len(revenue))), ':',label=str(extension)+" day prediction")
      plot.xticks(np.array([]))
      plot.yticks(np.array([]))
      #plot.xticks(range(len(dates)))
      #ax.set_xticklabels(dates)
      plot.legend()
      plot.title("Linear Regression on Revenue Since November 2017")
      plot.show()
      plot.savefig('overall_linear_regression' +self.get_time()+'.jpg')


"""
if len([f.name for f in os.scandir('.') if f.is_file() and f.name =='Month_to_Month_comparison.csv']):
  m = Model()
  revenue = m.get_revenue()
  dates = m.get_dates()
  data = m._setup(dates, revenue)
  overall_linear_regression = m.overall_linear_regression(data)
  max_revenue = m.save_list(data, 10)
"""    
