import sqlite3
import yfinance
import alpaca_trade_api
import CONFIG

api = alpaca_trade_api.REST(CONFIG.API_KEY, CONFIG.API_SECKEY, CONFIG.LINK, api_version='v2')
clock = api.get_clock()

if clock.is_open:

    connection = sqlite3.connect('test.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT symbol,status FROM apex")
    rows = cursor.fetchall()

    for row in rows:

        if row['status'] == 'active':
            data = yfinance.download(row['symbol'], period='2d', interval='1d')
            data_tail = data[-2:-1]
            del data
            cursor.execute("SELECT _1day_interval FROM apex WHERE symbol = ?", (row))
            jd = cursor.fetchall()
            for sorted_data in data_tail.itertuples():
                cursor.execute(f"""INSERT INTO {jd[0][0]} (date_time, open, high, \
                low, close, adjusted_close,volume) VALUES(
                                                '{sorted_data[0]}',
                                                '{sorted_data[1]}',
                                                '{sorted_data[2]}',
                                                '{sorted_data[3]}',
                                                '{sorted_data[4]}',
                                                '{sorted_data[5]}',
                                                '{sorted_data[6]}')
                """)

        else:
            '''symbol might have been de-listed'''

    connection.commit()
