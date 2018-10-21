import matplotlib
matplotlib.use('Agg')
import requests
import json
import api_client
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import io
import base64
import pandas as pd
from pandas_datareader import data as web

pos_events = ['All Time High', 'Buyback - Change in Plan Terms', 'Buyback Announcements by Company', 'Buyback Closings by Company', 'Buyback Tranche Update', 'Buyback', 'Transaction Announcements', 'Buyback Transaction Cancellations', 'Buybacks', 'Dividend Affirmations', 'Dividend Increases', 'Dividend Initiation', 'Expansions', 'Special Dividend Announced', 'Stock Splits', 'Person starts a specified role by company', 'Person starts any role by company']
bad_events = ['Bankruptcy', 'Cyberattacks', 'Debt Defaults', 'Delayed Earnings Announcements', 'Discontinued Operations & Downsizings', 'Discontinued Operations/Downsizings', 'Dividend Cancellation', 'Dividend Decreases', 'Delayed SEC Filings', 'Earthquakes by Country', 'Financial Crises', 'Impeachments', 'Lawsuits', 'Leaks', 'Natural Disasters', 'Oversight', 'Penalties', 'Product Outages', 'Product Recalls', 'Political Scandals', 'Political Violence', 'Resignations', 'Regulations', 'Regulatory Agency Inquiries', 'Regulatory Authority - Regulations', 'Terrorism', 'Tornados by Region', 'Person ends a specified role by company', 'Person ends any role by company']

def timeline(search):
  client = api_client.get_pandas_graph_client('https://www.kensho.com/external/v1', '769469f2d24c9203f3fe13666d4358d466c480a9')
  ent = client.search_entities('Equity', search)[0]
  ent_id = ent['entity_id']
  symbol = ent['ticker_name']
  time_id = client.get_related_entities(ent_id, 'EquityTimelines')
  posx = []
  poxy = []
  negx = []
  negy = []
  for t in time_id:
    if t['entity_type'] == 'Timeline':
      if t['timeline_type'] in bad_events:
        for ti in client.get_timeline(t['entity_id']):
          negx.append(ti['event_date'][:ti['event_date'].index('T')])
      elif t['timeline_type'] in pos_events:
        for ti in client.get_timeline(t['entity_id']):
          posx.append(ti['event_date'][:ti['event_date'].index('T')])
  fig, (ax1, ax) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[3, 1]})
  posx = list(map(datetime.datetime.strptime, posx, len(posx)*['%Y-%m-%d']))
  negx = list(map(datetime.datetime.strptime, negx, len(negx)*['%Y-%m-%d']))
  locator = mdates.AutoDateLocator()
  ax.xaxis.set_major_locator(locator)
  ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
  pos_mpl_data = mdates.date2num(posx)
  neg_mpl_data = mdates.date2num(negx)
  # ax.xaxis.set_major_locator(mdates.MonthLocator())
  # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
  ax.hist(pos_mpl_data, bins = max(10, int((pos_mpl_data.max() - pos_mpl_data.min())/300)), color = 'green', alpha = 0.7)
  ax.hist(neg_mpl_data, bins = max(10, int((neg_mpl_data.max() - neg_mpl_data.min())/300)), color = 'red', alpha = 0.7)
  buf = io.BytesIO()
  start,end = mdates.num2date(ax.get_xaxis().get_data_interval()[0]), mdates.num2date(ax.get_xaxis().get_data_interval()[1])
  prices = web.DataReader(symbol, "yahoo", start, end)
  ax1.plot(prices["Adj Close"])
  ax1.set_title('Stock Price')
  ax.set_title('News Summary')
  fig.savefig(buf, format='png')
  buf.seek(0)
  buffer = b''.join(buf)
  b2 = base64.b64encode(buffer)
  fig2=b2.decode('utf-8')
  return fig2

  # print(client.get_related_entities(ent_id, 'EquityTimelines')[2])
  # print(client.get_timeline(time_id)[0])
  # print(client.list_timeline_types())

if __name__ == '__main__':
  timeline('AAPL')
