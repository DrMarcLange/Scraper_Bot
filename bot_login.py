import functools, itertools
import itertools
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as brave_executable_config
from selenium.webdriver.common.by import By
import time
wait = lambda s: time.sleep(s)

import _config_data
action_sequence = _config_data.get_action_sheet_data()

import datetime
stamp = lambda : str(datetime.datetime.now())[:19]
clear_log = lambda : _config_data.clear_log()
log_row = lambda x: _config_data.append_log_data([x,])
renew_log = lambda : log_row(['BOT','created_at','text','tag','keys','delay','url'])

class Scraper_Bot():
  def __init__(self):
    self.name='The Data Scraper Bot v0.1'
    self.browser_binary='/usr/bin/brave'
    self.executable_path='./chromedriver'

  def __start_new_driver__(self):
    options = webdriver.ChromeOptions()
    options.binary_location=self.browser_binary
    s=brave_executable_config(self.executable_path)
    driver = webdriver.Chrome(options=options, service=s)
    return driver

  @property
  def browser(self):
    try:
      return self._driver
    except:
      self._driver = self.__start_new_driver__()
      return self._driver

  def execute_action_sequence(self,action_sequence):
    _url=min(map(lambda x: x[2],filter(lambda x: x[1]=='_URL',action_sequence))); self.url=_url
    _colnames, action_sequence = action_sequence[0], action_sequence[1:]
    clear_log(); renew_log(); log_row(['v0.1',stamp(),'STARTED PROCESS','n/a','n/a','0',self.url])

    with open('.pass','r') as fi:
      strings=fi.readlines()
    strings=list(map(lambda x: x.strip().split(':'),strings))
    strings=list(filter(lambda x: x[0].lower() in self.url, strings))[0]
    self.username,self.password=strings[1:]

    browser=self.browser #start a controllable browser-instance
    print(action_sequence)
    for text, tag, action, delay in action_sequence:
      log_row(['v0.1',stamp(),text,tag,action,delay,self.url])
      elements=list()
      if tag == '_START':
        print('starting action sequence, START', stamp())
        continue
      if tag == '_DONE':
        print('finished action sequence, DONE!', stamp())
        break #escape the for-loop
      if tag == '_URL':
        print('Going directly to url: ', action)
        browser.get(action); wait(float(delay)); continue
      while len(elements)==0:
        print(text,tag,action,delay)
        print('trying to find elements, waiting ', delay,' s')
        wait(float(delay));
        elements=browser.find_elements(by=By.TAG_NAME,value=tag)
        print('found ',len(elements),' elements')
        if len(elements)>0:
          try:
            print(elements[0].text)
          except:
            continue
          if len(text)>0:
            try:
              elements=list(filter(lambda x: text in x.text, elements))
              print(list(map(lambda x: x.text, elements)))
            except:
              continue #while-loop
          else:
            try:
              print(list(map(lambda x: x.text, elements)))
            except:
              continue #while-loop
          match action:
            case 'L_CLICK':
              try:
                #while-loop (l.57) break, not match break 
                elements[0].click(); break
              except:
                continue
            case 'USER':
              try:
                print('Sending Username: ',self.username)
                elements[0].send_keys(self.username+'\n'); break
              except:
                continue
            case 'PASS':
              try:
                print('Sending Password of length: ', 5*(1+len(self.password)//5))
                elements[1].send_keys(self.password+'\n'); break
              except:
                continue
            case s:
              try:
                print('Sending the string: ', s)
                elements[0].send_keys(s+'\n'); break
              except:
                continue
    ##==Logged In, seeing feed!==##
    return browser

if __name__=='__main__':
  scrbot = Scraper_Bot()
  browser = scrbot.execute_action_sequence(action_sequence)
