from flask import Flask, render_template, request
from historic import all_cards_priv, all_sets_priv, historic_cards, txt_deck_to_mtga

import pprint
pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)

cards = all_cards_priv()
sets  = all_sets_priv()

historicCards = historic_cards(cards, sets)

@app.route('/')
def query():
   return render_template('txt_deck_to_mtga.html')

@app.route('/converted', methods = ['POST'])
def response():
  pp.pprint(request.__dict__)
  mtga_deck = txt_deck_to_mtga(request.form['deck'], historicCards)
  return render_template('converted.html', result={'mtga_deck': mtga_deck})

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 7551, debug = False)
