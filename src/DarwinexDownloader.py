# library to connect with Darwinex
import ftplib
# https://docs.python.org/es/3.10/library/tempfile.html
import tempfile
# Library to decompress log data
import gzip
# Pandas library to manage data
import pandas as pd
# Library to manage time
from datetime import date, timedelta
# Library to os manage
import os


# main class
class DarwinexDownloader:
	''' Class to download data from Darwinex'''

	# Initialization
	def __init__(self, user, password):
		''' Params
        :user: ftp username
        :password: ftp password
        :return: class
        :rtype: DarwinexDownloader
        '''
		self.user = user
		self.passw = password
		
		
		self.ftp = ftplib.FTP('tickdata.darwinex.com', self.user, self.passw)

	def download(self, ticker, date_start, date_end, frecuency):
		''' Params
        :ticker: Ticker's name to download
        :date_start: start date with format dd-mm-yyyy
		:date_end: End date with format dd-mm-yyyy
        :return: ohlc data
        :rtype: dataframe
        '''
		# Create a temp folder
		tmpdirname = 'tempDataFolder'
		with tempfile.TemporaryDirectory() as tmpdirname:
			# Preparo las fechas para trabajar más fácil con ellas
			start_split = date_start.split("-")
			end_split = date_end.split("-")
			start_datetime = date(int(start_split[2]), int(start_split[1]), int(start_split[0]))
			end_datetime = date(int(end_split[2]), int(end_split[1]), int(end_split[0]))

			# Calculo la diferencia entre las fechas para ir hacíando el bucle
			# que va descargar todos los datos
			delta = end_datetime - start_datetime
			for i in range(delta.days + 1):
				day = start_datetime + timedelta(days=i)
				# Pongo para que descargue todas las horas para casos de divisas
				# Si no encuentra el fichero (al ser una acción normal) continua
				for i in range(24):
					hora = str(i).rjust(2, '0')
					try:
						download_file = ticker+"_BID_"+str(day.year)+"-"+str(day.month).rjust(2, '0')+"-"+str(day.day).rjust(2, '0')+"_"+hora+".log.gz"
						self.ftp.retrbinary("RETR /"+ticker+"/"+download_file ,open(tmpdirname+"/"+download_file, 'wb').write)
					except:
						pass
			
			onlyfiles = [f for f in os.listdir(tmpdirname) if os.path.isfile(os.path.join(tmpdirname, f))]

			appended_data = []

			for stock_file in onlyfiles:
				with open(tmpdirname+"/"+stock_file, 'rb') as fd:
					gzip_fd = gzip.GzipFile(fileobj=fd)
					appended_data.append(pd.read_csv(gzip_fd,names=["Date","Price","Size"]))
			
			df_stock = pd.concat(appended_data)
			df_stock['Date'] = pd.to_datetime(df_stock['Date'],unit='ms')
		
		# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
		df_stock = df_stock.set_index('Date')
		stock_ohlc = df_stock['Price'].resample(frecuency).ohlc()
		stock_ohlc['Volume'] = df_stock['Size'].resample(frecuency).sum()

		return stock_ohlc.dropna()





