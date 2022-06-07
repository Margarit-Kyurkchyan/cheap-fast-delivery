from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from multiprocessing import Process, Manager
from os import environ
import sites

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.from_pyfile('config.py')



@app.route('/')
def index():
    address = request.args.get('address')
    name = request.args.get('name')

    path = app.config['PATH']
    options = webdriver.ChromeOptions()
    options.headless = True
    user_agent = app.config['USER_AGENT']
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(path, options=options)
    driver2 = webdriver.Chrome(path, options=options)
    manager = Manager()
    queue = manager.dict()
    p1 = Process(target=sites.ubereats, args=(driver, address, name, queue))
    p1.start()
    p2 = Process(target=sites.doordash, args=(driver2, address, name, queue))
    p2.start()
    p1.join()
    p2.join()
    driver.quit()
    print('end')
    return jsonify(queue.items())

@app.route('/ubereats')
def ubereats():
    queue = site('ubereats')
    return jsonify(queue)

@app.route('/doordash')
def doordash():
    queue = site('doordash')
    return jsonify(queue)

@app.route('/grubhub')
def grubhub():
    queue = site('grubhub')
    return jsonify(queue)



def site(siteName):
    address = request.args.get('address')
    name = request.args.get('name')
    path = app.config['PATH']
    options = webdriver.ChromeOptions()
    options.headless = True
    queue = {}
    options.add_argument(f"user-agent={app.config['USER_AGENT']}")
    driver = webdriver.Chrome(path, options=options)
    if siteName == 'ubereats':
        sites.ubereats(driver, address, name, queue)
    elif siteName == 'doordash':
        sites.doordash(driver, address, name, queue)
    elif siteName == 'grubhub':
        sites.grubhub(driver, address, name, queue)
    return queue


if __name__ == "__main__":
    app.run(debug=True)
