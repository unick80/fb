import json
import requests
import hashlib
import uuid
from selenium import webdriver
from time import sleep
import random

response = requests.get('https://line11.bkfon-resources.com/live/currentLine/ru')
try:
  json = response.json()
except:
  json="Error parser json"
  exit()
else:
  jsports = json['sports']
  sports = {}
  for i in range(len(jsports)):
    if "Футбол" in jsports[i]['name']:
      sports[jsports[i]['id']] = jsports[i]['name']
  events = json['events']
  gamers = {}
  for i in range(len(events)):
    sportId = events[i]['sportId']
    place = events[i]['place']
    if (sportId in sports) and (place == "live"):
      try:
        team1 = events[i]['team1']
      except:
        team1 = ""
      try:
        team2 = events[i]['team2']
      except:
        team2 = ""
      id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()
      gamer_name = team1+" - "+team2
      gamers[id] = gamer_name
  print(gamers)
driver = webdriver.Chrome()
driver.get("https://www.fonbet.ru/live/")
sleep(5)
btn_search = driver.find_element_by_class_name("search")
btn_search.click()
input_search = driver.find_element_by_class_name("search__input--DF661")
ok = 0
while ok==0:
  key = random.choice(list(gamers.keys()))
  gamer_name = gamers[key]
  driver.execute_script('arguments[0].value = "";', input_search)
  input_search.send_keys(gamer_name)
  print(gamer_name)
  sleep(5)
  try:
    result_search = driver.find_element_by_class_name("search-result__event-name--3Qfnn")
  except:
    pass
  else:
    ok=1
    result_search.click()
  sleep(5)
