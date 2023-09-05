import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

def getCMBWLRate():
    CMBWL_BuyHKD = None
    CMBWL_BuyUSD = None

    cmburl = 'https://www.cmbwinglungbank.com/ibanking/CnCoFiiTtrateDsp.jsp'
    response = requests.get(cmburl)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'width': '660'})
    rows = table.find_all('tr')
    # Extracting the needed values
    for row in rows:
        cells = row.find_all('td', {'class': 'wl_tabletxt1'})
        if cells:
            if '離岸' in cells[0].get_text().strip():
                CMBWL_BuyHKD = round(1 / float(cells[1].get_text().strip()), 4)
            if '美元' in cells[0].get_text().strip():
                CMBWL_BuyUSD = round(float(cells[2].get_text().strip()), 4)

    return CMBWL_BuyHKD, CMBWL_BuyUSD

def getHSBCRate():
    url = 'https://rbwm-api.hsbc.com.hk/pws-hk-hase-rates-papi-prod-proxy/v1/fxnotes-exchange-rates'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-HK',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    HSBCHK_BuyUSD = None
    HSBCHK_BuyHKD = None

    for item in data['fxnoteExchangeRates']:
        if item['ccyDisplayCode'] == 'USD':
            HSBCHK_BuyUSD = float(item['noteSellRate'])
            HSBCHK_BuyUSD = round(HSBCHK_BuyUSD, 4)
        if item['ccyDisplayCode'] == 'CNY':
            HSBCHK_BuyHKD = float(item['noteBuyRate'])
            HSBCHK_BuyHKD = round(1 / HSBCHK_BuyHKD, 4)
        if HSBCHK_BuyUSD is not None and HSBCHK_BuyHKD is not None:
            break

    return HSBCHK_BuyUSD, HSBCHK_BuyHKD

def getBOCHKRate():
    BOCHK_BuyHKD = None
    BOCHK_BuyUSD = None

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    data_usd = {
        'bean.rateType': 1,
        'bean.depCurrency': 'HKD',
        'bean.withdrCurrency': 'USD'
    }
    
    response_usd = requests.post('https://www.bochk.com/whk/calculator/realTimeRate/realTimeRate-getRealTimeRate.action', headers=headers, data=data_usd)
    BOCHK_BuyUSD = float(response_usd.text.strip('"'))

    data_hkd = {
        'bean.rateType': 1,
        'bean.depCurrency': 'CNY',
        'bean.withdrCurrency': 'HKD'
    }
    
    response_hkd = requests.post('https://www.bochk.com/whk/calculator/realTimeRate/realTimeRate-getRealTimeRate.action', headers=headers, data=data_hkd)
    BOCHK_BuyHKD = round(1 / float(response_hkd.text.strip('"')), 4)

    return BOCHK_BuyHKD, BOCHK_BuyUSD

def getHKBEARate():
    HKBEA_BuyHKD = None
    HKBEA_BuyUSD = None

    url = 'https://www.hkbea.com/cgi-bin/rate_ttfx.jsp'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if cells:
            if 'CNH' in cells[0].get_text().strip():
                HKBEA_BuyHKD = round(1 / (float(cells[2].get_text().strip())) * 100, 4)
            if 'USD' in cells[0].get_text().strip():
                HKBEA_BuyUSD = round((float(cells[3].get_text().strip()) / 100), 4)

    return HKBEA_BuyHKD, HKBEA_BuyUSD

def getICBCAISARate():
    ICBCASIA_BuyHKD = None
    ICBCASIA_BuyUSD = None
    
    url = 'http://papi.icbc.com.cn/rest/currencies/asia/foreign'
    response = requests.get(url)
    data = response.json()

    for item in data['data']:
        if item['currename'] == 'CNY':
            ICBCASIA_BuyHKD = round((1 / float(item['buyrate'])), 4)
        if item['currename'] == 'USD':
            ICBCASIA_BuyUSD = round(float(item['salrate']), 4) 

    return ICBCASIA_BuyHKD, ICBCASIA_BuyUSD

@app.route('/')
def index():
    HSBCHK_BuyUSD, HSBCHK_BuyHKD = getHSBCRate()
    CMBWL_BuyHKD, CMBWL_BuyUSD = getCMBWLRate()
    BOCHK_BuyHKD, BOCHK_BuyUSD = getBOCHKRate()
    HKBEA_BuyHKD, HKBEA_BuyUSD = getHKBEARate()
    ICBCASIA_BuyHKD, ICBCASIA_BuyUSD = getICBCAISARate()
    
    rates = [
        {'Bank': 'HSBC(HK)', 'BuyUSD': HSBCHK_BuyUSD, 'BuyHKD': HSBCHK_BuyHKD},
        {'Bank': 'CMB (WL)', 'BuyUSD': CMBWL_BuyUSD, 'BuyHKD': CMBWL_BuyHKD},
        {'Bank': 'BOC (HK)', 'BuyUSD': BOCHK_BuyUSD, 'BuyHKD': BOCHK_BuyHKD},
        {'Bank': 'BEA (HK)', 'BuyUSD': HKBEA_BuyUSD, 'BuyHKD': HKBEA_BuyHKD},
        {'Bank': 'ICBC (ASIA)', 'BuyUSD': ICBCASIA_BuyUSD, 'BuyHKD': ICBCASIA_BuyHKD}
    ]
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return render_template('index.html', rates=rates, current_time=current_time)

@app.route('/raw')
def raw_data():
    HSBCHK_BuyUSD, HSBCHK_BuyHKD = getHSBCRate()
    CMBWL_BuyHKD, CMBWL_BuyUSD = getCMBWLRate()
    BOCHK_BuyHKD, BOCHK_BuyUSD = getBOCHKRate()
    HKBEA_BuyHKD, HKBEA_BuyUSD = getHKBEARate()
    ICBCASIA_BuyHKD, ICBCASIA_BuyUSD = getICBCAISARate()

    rates = {
        'HSBCHK': {'BuyUSD': HSBCHK_BuyUSD, 'BuyHKD': HSBCHK_BuyHKD},
        'CMBWL': {'BuyUSD': CMBWL_BuyUSD, 'BuyHKD': CMBWL_BuyHKD},
        'BOCHK': {'BuyUSD': BOCHK_BuyUSD, 'BuyHKD': BOCHK_BuyHKD},
        'BEAHK': {'BuyUSD': HKBEA_BuyUSD, 'BuyHKD': HKBEA_BuyHKD},
        'ICBCASIA': {'BuyUSD': ICBCASIA_BuyUSD, 'BuyHKD': ICBCASIA_BuyHKD}
    }
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({'rates': rates, 'last_updated': current_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)