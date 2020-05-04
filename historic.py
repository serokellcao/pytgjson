import json
import os
import pprint
from historic_oddities import oddities, discrepancies
pp = pprint.PrettyPrinter(indent=4)

# We will build a weird monad here, that runs a function
# with a signature f :: PyDict -> (Bool, PyDict)
# and if (fst . f) x == true, then it will append
# (snd . f) x to x before passing the continuation to the next
# function.
#
# Runner of this monad is run_monad_filtermap

# TODO add capabilities so that we can discriminate plain cards object from
# its enriched versions at least on runtime and catch errors quickly

def historic_sets():
  base_sets = [
    "XLN", "RIX", "DOM", "M19", "GRN", "RNA", "WAR",
    "M20", "ELD", "THB", "IKO", "HA1", "HA2"
  ]
  return base_sets
# WE ARE BALLMER PEAKING BOIZ

def historic_cards(cards, sets, fs=[]):
  do = [
    keep_historic_printings,
    add_printings_info_curried(sets),
    oddity_fixup_curried2(oddities(), sets)
  ]
  do.extend(fs)
  return run_monad_filtermap(cards, do)

def histoic_peasant_cards(cards, sets, fs=[]):
  do = [ keep_peasant ]
  do.extend(fs)
  return historic_cards(cards, sets, do)

def txt_deck_to_mtga(deck, mtgaPool):
  def unsplit_maybe(eitherSplitOrWholesome):
    eitherPartsOrWholesome = eitherSplitOrWholesome.split(' // ')
    if len(eitherPartsOrWholesome) == 1:
      return eitherSplitOrWholesome # wholesome
    else:
      pp.pprint(eitherPartsOrWholesome[0])
      return eitherPartsOrWholesome[0] # split

  def mk_mtga_deck_entry(mtgaPool, qan, name):
    return ' '.join(
      [
        qan,
        '(' + get_next_set(mtgaPool, name) + ')',
        get_next_collector_number(mtgaPool, name)
      ]
    )

  mutableDecklist = ['Deck']
  mutableErrors = []
  for qtyAndNameTxt in deck.splitlines():
    if qtyAndNameTxt == 'Sideboard':
      mutableDecklist.extend(['', 'Sideboard'])
      continue
    qtyAndName = qtyAndNameTxt.split(' ', 1)
    if len(qtyAndName) != 2:
      if qtyAndNameTxt:
        mutableErrors.append(qtyAndNameTxt)
      continue
    qty = qtyAndName[0]
    name = unsplit_maybe(qtyAndName[1])
    try:
      mutableDecklist.append(mk_mtga_deck_entry(
        mtgaPool, unsplit_maybe(qtyAndNameTxt), name
      ))
    except:
      mutableErrors.append(qtyAndNameTxt)
      continue
  return ('\n'.join(mutableDecklist), mutableErrors)

def all_cards(source_file):
  fh = open(source_file)
  fc = fh.read()
  fh.close()
  return json.loads(fc)

def all_cards_priv():
  return all_cards(os.path.join('priv', 'AllCards.json'))

def all_sets(source_directory):
  mutableAcc = {}
  for fn in [x for x in os.listdir(source_directory) if x.endswith('.json')]:
    fh = open(os.path.join(source_directory, fn))
    fc = fh.read()
    mutableAcc[(fn.replace('.json', ''))] = json.loads(fc)
    fh.close()
  return mutableAcc

def all_sets_priv():
  return all_sets(os.path.join('priv', 'sets'))

def keep_peasant(card):
  (b, d)   = keep_rarity_curried('common')(card)
  (b1, d1) = keep_rarity_curried('uncommon')(card)
  return ( (b or b1), {} )

def keep_rarity_curried(rarity):
  def keep_rarity(card):
    #pp.pprint(('Keep rarity curried', (card['name'], card['printings'])))
    matchMaybe = next( (x for x in card['printings'] if card['printings_info'][x]['rarity'] == rarity), None )
    return ( (matchMaybe is not None), {} )
  return keep_rarity

def run_monad_filtermap(cards, fs):
  mutableAcc = cards.copy()
  for k in cards:
    for f in fs:
      (b, d) = f( mutableAcc[k] )
      if b:
        mutableAcc[k] = { **mutableAcc[k], **d }
      else:
        del mutableAcc[k]
        break
  #return ('MONAD_FILTERMAP', mutableAcc)
  return mutableAcc

def get_printing_info(card, set, sets):
  return next(x for x in sets[set]['cards'] if x['name'] == card['name'])

def add_printings_info_curried(sets):
  def add_set_info(card):
    #pp.pprint(('add_set_info', (card['name'], card['printings'])))
    mutableAcc = {'printings_info': {}}
    for s in card['printings']:
      mutableAcc['printings_info'][s] = get_printing_info(card, s, sets)
    return (True, mutableAcc)
  return add_set_info

# TODO: Refactor to keep_historic_printings_curried(sets)!
def was_printed_in_sets(card, sets):
  sets1 = [x for x in card['printings'] if x in sets]
  #pp.pprint(('was_printed_in_sets', (card['name'], card['printings']), ('Remaining', sets1)))
  return ( ([] != sets1),
           {'printings': sets1} )

def keep_historic_printings(card):
  return was_printed_in_sets(card, historic_sets())

def oddity_fixup_curried2(oddities, sets):
  def oddity_fixup(card):
    if card['name'] in oddities:
      mutableAcc = {}
      printing   = oddities[card['name']]['set']
      mutableAcc[printing] = get_printing_info(card, printing, sets)
      return ( True,
               {
                  'printings': [ printing ],
                  'printings_info': mutableAcc
                }
              )
    else:
      return ( True, {} )
  return oddity_fixup

def fixup_set_discrepancies_curried(discrepancies_fn):
  def fixup_set_discrepancies(card):
    printings1 = list(map(discrepancies_fn, card['printings']))
    mutableAcc = {}
    for set_name in card['printings_info']:
      mutableAcc[discrepancies_fn(set_name)] = card['printings_info'][set_name]
    return ( True,
             {
               'printings': printings1,
               'printings_info': mutableAcc
             }
           )
  return fixup_set_discrepancies


###################
# Deck processing #
###################

def get_next_set(cards, name):
  return cards[name]['printings'][0]

def get_next_collector_number(cards, name):
  set = cards[name]['printings'][0] # TODO make it faster.
  return cards[name]['printings_info'][set]['number']

def dump_cards(name, cards):
  with open(os.path.join('result', name + '.extended.json'), 'w+') as fh:
    json.dump(cards, fh)
  with open(os.path.join('result', name + '.txt'), 'w+') as fh:
    for k in cards:
      fh.write(k + '\n')

def all_sets_odd_priv():
  sets  = all_sets_priv()
  mutableAcc = {}
  for x in sets:
    #if discrepancies(x) != x:
    #  pp.pprint(["Discrepancy", discrepancies(x), "Set ID", x])
    mutableAcc[discrepancies(x)] = sets[x]
  return mutableAcc

def main():

  cards = all_cards_priv()
  sets  = all_sets_odd_priv()
  #pp.pprint(len(sets['CONF']))
  pp.pprint("Narrowing down to the Historic card pool")
  historicCards = historic_cards(cards, sets)
  results = [('HistoricCards', historicCards)]
  pp.pprint("Making artisan Historic card pools")
  results.extend([
    ('HistoricPeasant',    run_monad_filtermap(historicCards, [keep_peasant])),
    ('HistoricCommons',    run_monad_filtermap(historicCards, [keep_rarity_curried('common')])),
    ('HistoricUncommons',  run_monad_filtermap(historicCards, [keep_rarity_curried('uncommon')])),
  ])
  for (name, cards1) in results:
    pp.pprint([ "Writing", name, "to disk" ])
    dump_cards(name, cards1)

def main2():
  cards = all_cards_priv()
  sets  = all_sets_priv()
  historicCards = historic_cards(cards, sets)
  fh = open(os.path.join('priv', 'deck.txt'))
  deck = fh.read()
  fh.close()
  print(txt_deck_to_mtga(deck, historicCards))

def main3():
  pp.pprint(oddities())

if __name__ == '__main__':
  main()
