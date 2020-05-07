def oddities():
  return {
# HA
    "Inexorable Tide": {"set": "SOM", "number": 35},
    "Hypnotic Specter": {"set": "M10", "number": 100},
    "Virulent Plague": {"set": "DTK", "number": 125},
    "Kiln Fiend": {"set": "ROE", "number": 153},
    "Waste Not": {"set": "M15", "number": 122},
    "Pack Rat": {"set": "RTR", "number": 73},
    "Phyrexian Arena": {"set": "8ED", "number": 152},
    "Forgotten Cave": {"set": "ONS", "number": 317},
    "Tendrils of Corruption": {"set": "M10", "number": 114},
    "Bojuka Bog": {"set": "WWK", "number": 132},
    "Cryptbreaker": {"set": "EMN", "number": 86},
    "Dragonmaster Outcast": {"set": "WWK", "number": 81},
    "Goblin Ruinblaster": {"set": "ZEN", "number": 127},
    "Brain Maggot": {"set": "JOU", "number": 62},
    "Barren Moor": {"set": "ONS", "number": 312},
    "Distant Melody": {"set": "MOR", "number": 32},
    "Merrow Reejerey": {"set": "LRW", "number": 74},
    "Thalia, Guardian of Thraben": {"set": "DKA", "number": 24},
    "Nyx-Fleece Ram": {"set": "JOU", "number": 18},
    "Sigil of the Empty Throne": {"set": "CONF", "number": 18},
    "Lonely Sandbar": {"set": "ONS", "number": 320},
    "Kinsbaile Cavalier": {"set": "MOR", "number": 15},
    "Treasure Hunt": {"set": "WWK", "number": 42},
    "Serra Ascendant": {"set": "M11", "number": 28},
    "Soul Warden": {"set": "M10", "number": 34},
    "Goblin Matron": {"set": "MH1", "number": 129},
    "Ranger of Eos": {"set": "ALA", "number": 21},
    "Hidetsugu's Second Rite": {"set": "SOK", "number": 102},
    "Tranquil Thicket": {"set": "ONS", "number": 326},
    "Elvish Visionary": {"set": "ORI", "number": 175},
    "Fauna Shaman": {"set": "M11", "number": 172},
    "Ancestral Mask": {"set": "MMQ", "number": 229},
    "Imperious Perfect": {"set": "LRW", "number": 220},
    "Terravore": {"set": "ODY", "number": 278},
    "Meddling Mage": {"set": "ARB", "number": 8},
    "Maelstrom Pulse": {"set": "ARB", "number": 92},
    "Burning-Tree Emissary": {"set": "GTC", "number": 216},
    "Knight of the Reliquary": {"set": "CONF", "number": 113},
    "Captain Sisay": {"set": "INV", "number": 237},
    "Ghost Quarter": {"set": "ISD", "number": 240},
    "Ornithopter": {"set": "M10", "number": 216},
    "Mind Stone": {"set": "WTH", "number": 153},
    "Darksteel Reactor": {"set": "DST", "number": 114},
    "Platinum Angel": {"set": "M10", "number": 218},
  }

def promo_oddities():
  return {
# PANA
    "The Gitrog Monster": {"set": "SOI", "number": 245},
    "Talrand, Sky Summoner": {"set": "M13", "number": 72},
    "Rhys the Redeemed": {"set": "SHM", "number": 237},
    "Bladewing the Risen": {"set": "SCG", "number": 136},
  }

def discrepancies(x):
  if x == "CON_": # IDK how could I have debugged it faster even sober.
    return "CONF"
  else:
    return x
