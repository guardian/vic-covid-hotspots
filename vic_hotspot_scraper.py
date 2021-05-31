import pandas as pd 
import os 
import time 
from modules.yachtCharter import yachtCharter

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"
output_path = os.path.dirname(__file__) + "/output/"

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

urlo = 'https://www.coronavirus.vic.gov.au/exposure-sites'


listo = []
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
# driver = webdriver.Firefox()
driver.get(urlo)

for i in range(0, 23):
    print(f"Count: {i}")
    html = driver.page_source
    df = pd.read_html(html, attrs = {'class': 'rpl-search-results-table'})[0]
    df = df[['Suburb', 'Site', 'Exposure period', 'Notes',
    'Date added', 'Health advice']]
    
    print(df['Site'])
    df['Site'] = df['Site'].str.replace(r'^Site', '', regex=True).str.strip()
    df['Suburb'] = df['Suburb'].str.replace(r'^Suburb', '', regex=True).str.strip()

    df['Exposure period'] = df['Exposure period'].str.replace(r'^Exposure period', '', regex=True).str.strip()
    df['Notes'] = df['Notes'].str.replace(r'^Notes', '', regex=True).str.strip()
    df['Date added'] = df['Date added'].str.replace(r'^Date added', '', regex=True).str.strip()

    df['Health advice'] = df['Health advice'].str.extract(r'(Anyone .+)', expand=False)
    print(df['Site'])
    
    listo.append(df)

    button = driver.find_element_by_xpath("//button[span[text()='Next page']]")
    button.click()
    time.sleep(2)

final = pd.concat(listo)
final = final.dropna(subset=['Site'])
final = final.drop_duplicates(subset=['Site', 'Exposure period'])

driver.close()

with open(f"{here}/vic_hotspots.csv", "w") as f:
    final.to_csv(f, index=False, header=True)


def makeTable(df):
	
    template = [
            {
                "title": "Victoria Covid Hotspots",
                "subtitle": f"""""",
                "footnote": "",
                "source": "| Sources: Victorian government",
                "yScaleType":"",
                "minY": "0",
                "maxY": "",
                "x_axis_cross_y":"",
                "periodDateFormat":"",
                "margin-left": "50",
                "margin-top": "30",
                "margin-bottom": "20",
                "margin-right": "10"
            }
        ]
    key = []
    # labels = []
    df.fillna("", inplace=True)
    chartData = df.to_dict('records')
    labels = []


    yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"table"}], 
    options=[{"colorScheme":"guardian","format": "scrolling","enableSearch": "TRUE","enableSort": "TRUE"}], chartName="vic_covid_hotspots")

makeTable(final)