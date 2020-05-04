from flask import Flask, render_template, request
from historic import all_cards_priv, all_sets_priv, historic_cards, txt_deck_to_mtga

import pprint
import json
pp = pprint.PrettyPrinter(indent=4)
import os

app = Flask(__name__)

# RENAME TO MTGA.JSON # fh = open(os.path.join('result', 'HistoricCards.mtga.json'))
fh = open(os.path.join('result', 'HistoricCards.extended.json'))
fc = fh.read()
fh.close()
historicCards = json.loads(fc)

@app.route('/')
def query():
   return render_template('txt_deck_to_mtga.html')

@app.route('/converted', methods = ['POST'])
def response():
  pp.pprint(request.__dict__)
  mtga_deck = txt_deck_to_mtga(request.form['deck'], historicCards)
  return render_template('converted.html', result={'mtga_deck': mtga_deck})

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 22020, debug = False)
