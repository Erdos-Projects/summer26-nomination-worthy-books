import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import pickle
from pathlib import Path

def load_tags():
    '''
    Returns the master list of valid tags from the tidy_book_tags notebook
    '''

    # copied from the tidy_book_tags file
    canonical_tag_map = {

        "science fict": ["sf"],
        "scienc fict": ["sf"],
        "sciense fict": ["sf"],
        "scifi": ["sf"],
        "printsf": ["sf"],
        "hard sf": ["sf", "hard sf"],
        "hard science fict": ["sf", "hard sf"],
        "science fiction  fantasi": ["sf", "fantasi"],
        "science fiction fantasi": ["sf", "fantasi"],
        "science fantasi": ["sf", "fantasi"],
        "sf romanc": ["sf", "rom"],
        "scifi rom": ["sf", "rom"],
        "sf rom": ["sf", "rom"],
        "military sf": ["militari", "sf"],
        "juvenile sf": ["ya", "sf"],
        "youngadult sf": ["ya", "sf"],
        "teen science fict": ["ya", "sf"],
        "middle grades science fict": ["ya", "sf"],
        "speculative fict": ["sf"],
        "space st": ["space travel"],
        "space opu": ["space travel"],
        "interplanetary travel": ["space travel"],
        "interplanetary voyag": ["space travel"],
        "space coloni": ["space travel"],
        "generation ship": ["space travel"],
        "space warfar": ["space travel", "militari"],
        "space pir": ["space travel", "adventur"],
        "star war": ["space travel"],
        "star trek the original seri": ["space travel"],
        "star trek": ["space travel"],
        "doctor who fictitious charact": ["sf", "alien"],
        "alien invas": ["alien"],
        "first contact": ["alien"],
        "alien artifact": ["alien"],
        "humanalien encount": ["alien"],
        "war with alien": ["alien"],
        "alien perspect": ["alien"],
        "martian": ["alien"],
        "extraterrestrial b": ["alien"],
        "aliens": ["alien"],
        "dyson spher": ["sf"],
        "terraform": ["sf"],
        "antigrav": ["sf"],
        "megaengin": ["sf"],
        "technolog": ["sf"],
        "nanotechnolog": ["sf"],
        "scienc": ["sf"],
        "climate chang": ["apocalyps"],
        "ecolog": ["apocalyps"],
        "post apocalypt": ["apocalyps"],
        "postapocalypt": ["apocalyps"],
        "apocalypt": ["apocalyps"],
        "end of the world": ["apocalyps"],
        "cosy catastroph": ["apocalyps"],
        "disast": ["apocalyps"],
        "pandem": ["apocalyps"],
        "epidem": ["apocalyps"],
        "plagu": ["apocalyps"],
        "diseas": ["apocalyps"],

        "fantasy": ["fantasi"],
        "fantezi": ["fantasi"],
        "fantasy fict": ["fantasi"],
        "epic": ["epic fantasi"],
        "high fantasi": ["epic fantasi"],
        "heroic fantasi": ["epic fantasi"],
        "quest": ["epic fantasi"],
        "progression fantasi": ["epic fantasi"],
        "magician": ["magic"],
        "wizard": ["magic"],
        "witch": ["magic"],
        "druid": ["magic"],
        "alchemi": ["magic"],
        "necromanc": ["magic"],
        "magic school": ["magic"],
        "cozy fantasi": ["fantasi", "lightheart"],
        "humorous fantasi": ["fantasi", "funni"],
        "fantasyhummi": ["fantasi"],
        "christian fantasi": ["fantasi", "religion"],
        "religious fantasi": ["fantasi", "religion"],
        "fantasy litrpg": ["litrpg"],
        "faeri": ["fantasy creatur", "fairy tal"],
        "fairi": ["fantasy creatur", "fairy tal"],
        "fa": ["fantasy creatur"],
        "elf": ["fantasy creatur"],
        "dwarf": ["fantasy creatur"],
        "troll": ["fantasy creatur"],
        "goblin": ["fantasy creatur"],
        "gargoyl": ["fantasy creatur"],
        "siren": ["fantasy creatur"],
        "mermaid": ["fantasy creatur"],
        "unicorn": ["fantasy creatur"],
        "mythical creatur": ["fantasy creatur"],
        "dragons  mythical creatur": ["dragon", "fairy tal", "fantasy creatur"],
        "dragonl": ["dragon", "fantasy creatur"],
        "fairy tale inspir": ["fairy tal"],
        "folk tal": ["fairy tal"],
        "cinderella": ["fairy tal"],
        "the sleeping beauti": ["fairy tal"],
        "beauty and the beast": ["fairy tal"],
        "mytholog": ["fairy tal"],
        "greek mytholog": ["fairy tal"],
        "norse mytholog": ["fairy tal"],
        "celtic": ["fairy tal"],
        "legend": ["fairy tal"],
        "folklor": ["fairy tal"],
        "retold fairy tal": ["fairy tal"],
        "retel": ["fairy tal"],
        "mythical": ["fairy tal"],
        "discworld": ["fantasi"],
        "propheci": ["fantasi"],
        "secret": ["fantasi"],

        # --- Alternative Realities & Timelines ---
        "parallel world": ["parallel univers"],
        "transdimension": ["parallel univers"],
        "portalg": ["parallel univers"],
        "time loop": ["time travel"],
        "time slip": ["time travel"],
        "time travel rom": ["rom", "time travel"],
        "timetravel rom": ["time travel", "rom"],
        "hitler win": ["alternate histori"],
        "alternative histories fict": ["alternate histori"],
        "alternate world": ["alternate histori"],
        "secret histori": ["alternate histori"],
        "alternate univers": ["alternate histori"],
        "lost world": ["lost rac"],
        "lost rac": ["lost rac"],
        "atlanti": ["lost rac"],

        # --- Cyber, Tech & Gaming ---
        "computer gam": ["video gam"],
        "gamebook": ["video gam"],
        "game": ["video gam"],
        "virtual r": ["video gam"],
        "transhuman": ["cyberpunk"],
        "posthuman": ["cyberpunk"],
        "android": ["robot"],
        "cyborg": ["robot"],
        "artificial intellig": ["robot"],
        "comput": ["robot"],

        # --- Horror, Ghosts & Dark Themes ---
        "horreur": ["horror"],
        "read horror": ["horror"],
        "body horror": ["horror"],
        "horror tal": ["horror"],
        "gothic horror": ["gothic"],
        "scari": ["horror"],
        "terror": ["horror"],
        "lovecraftian": ["horror"],
        "cannib": ["horror"],
        "monster": ["horror"],
        "sea monst": ["horror"],
        "bizarro": ["weird"],
        "haunted hous": ["ghost"],
        "ghost stori": ["ghost"],
        "afterlif": ["ghost"],

        # --- Paranormal & Shifters ---
        "paranormal  urban": ["supernatur"],
        "paranormal powers": ["supernatur"],
        "paranormal mystery": ["supernatur"],
        "paranormal mysteri": ["supernatur"],
        "paranormal thril": ["supernatur"],
        "paranormal fict": ["supernatur"],
        "paranormal pow": ["supernatur"],
        "paranorm": ["supernatur"],
        "paranormal": ["supernatur"],
        "supernatural thril": ["supernatur"],
        "occult detect": ["supernatur", "mysteri"],
        "shapeshift": ["shapechang"],
        "shifter": ["shapechang"],
        "lycanthropi": ["werewolf"],
        "dragon shift": ["shapechang", "dragon"],
        "voodoo": ["supernatur"],
        "demonolog": ["demon"],
        "satan": ["supernatur"],
        "devil": ["supernatur"],
        "hell": ["supernatur"],
        "possess": ["supernatur"],
        "vike": ["supernatur"],
        "god": ["supernatur"],
        "longev": ["supernatur"],
        "reincarn": ["supernatur"],
        "resurrect": ["supernatur"],

        "romanc": ["rom"],
        "romant": ["rom"],
        "love stori": ["paranormal rom"],
        "love": ["paranormal rom"],
        "fated m": ["paranormal rom"],
        "manwoman relationship": ["paranormal rom"],
        "paranormal romance stori": ["paranormal rom"],
        "paranormal romance stories": ["paranormal rom"],
        "paranormal erotic romance": ["paranormal rom"],
        "paranormal erotic rom": ["paranormal rom"],
        "fantasyrom": ["fantasy rom"],
        "romantic fantasi": ["fantasy rom"],
        "romantasi": ["fantasy rom"],
        "vampire rom": ["vampir", "rom"],
        "dark rom": ["dark", "rom"],
        "mm romanc": ["lgbtq"],
        "erotica": ["erot"],
        "gay erotica": ["lgbtq", "erot"],
        "erotic stori": ["erot"],
        "steami": ["erot"],
        "sex": ["erot"],
        "harem": ["erot"],
        "reverse harem": ["erot"],
        "enemies to lov": ["rom"],
        "slow burn": ["rom"],
        "forced proxim": ["rom"],
        "interpersonal rel": ["rom"],
        "marriag": ["rom"],

        "thriller  suspens": ["thriller"],
        "suspens": ["thriller"],
        "suspenseful": ["thriller"],
        "suspense": ["thriller"],
        "technothril": ["thriller"],
        "conspiraci": ["thriller"],
        "intrigu": ["thriller"],
        "kidnap": ["thriller"],
        "serial kil": ["thriller"],
        "abduct": ["thriller"],
        "paranormal suspens": ["supernatur", "thriller"],
        "thriller  suspensescience fiction  fantasi": ["thriller", "sf", "fantasi"],
        "detective and mystery stori": ["mysteri"],
        "murder mysteri": ["mysteri"],
        "murder": ["mysteri"],
        "private investig": ["mysteri"],
        "detect": ["mysteri"],
        "crime": ["mysteri"],
        "spy": ["mysteri"],
        "spi": ["mysteri"],
        "espionag": ["mysteri"],
        "assassin": ["mysteri"],
        "missing person": ["mysteri"],
        "cozy mysteri": ["mysteri", "lightheart"],
        "futuristic mysteri": ["near futur", "mysteri"],
        "sherlock holm": ["mysteri"],
        "action  adventur": ["adventur"],
        "actionadventur": ["adventur"],
        "action": ["adventur"],
        "aventur": ["adventur"],
        "aventure": ["adventur"],
        "adventurers": ["adventur"],
        "aventura": ["adventur"],
        "adventurous": ["adventur"],
        "adventure plot": ["adventur"],
        "misadventures": ["adventur"],
        "adventures": ["adventur"],
        "adventure stori": ["adventur"],
        "adventure and adventur": ["adventur"],
        "fantastic adventur": ["adventur"],
        "planetary adventur": ["adventur"],
        "sea adventur": ["adventur"],
        "pirat": ["adventur"],
        "escap": ["adventur"],
        "rescu": ["adventur"],
        "surviv": ["adventur"],
        "explor": ["adventur"],
        "travel": ["adventur"],
        "martial art": ["adventur"],
        "choose your own adventur": ["adventur"],
        "fix up": ["adventur"],

        "slow burn": ["slowpac"],
        "first person point of view": ["first person"],

        "dystopia": ["dystopian"],
        "dystopias": ["dystopian"],
        "dystopium": ["dystopian"],
        "utopium": ["dystopian"],

        "psychic ": ["psy pow"],
        "psychic": ["psy pow"],
        "telepathi": ["psy pow"],
        "precognit": ["psy pow"],
        "clairvoy": ["psy pow"],
        "esp": ["psy pow"],
        "telekinesi": ["psy pow"],
        "mind control": ["psy pow"],
        "body swap": ["psy pow"],
        "teleport": ["psy pow"],
        "invis": ["psy pow"],
        "memori": ["psy pow"],
        "amnesium": ["psy pow"],
        "clone": ["genetic engin"],
        "mutant": ["genetic engin"],
        "evolut": ["genetic engin"],
        "cryogen": ["genetic engin"],
        "suspended anim": ["genetic engin"],
        "scientist": ["genetic engin"],
        "mad scientist": ["genetic engin"],
        "drug": ["genetic engin"],

        "strong female characters": ["female lead"],
        "strong female charact": ["female lead"],
        "female protagonist": ["female lead"],
        "female main charact": ["female lead"],
        "female warrior": ["female lead"],
        "woman": ["female lead"],
        "written by woman": ["female author"],
        "lgbt": ["lgbtq"],
        "gay": ["lgbtq"],
        "lesbian": ["lgbtq"],
        "queer": ["lgbtq"],
        "bisexu": ["lgbtq"],
        "transgend": ["lgbtq"],
        "nonbinary gend": ["lgbtq"],
        "sapphic": ["lgbtq"],

        "young adult": ["ya"],
        "youngadult": ["ya"],
        "teen  young adult": ["ya"],
        "youngadult fict": ["ya"],
        "juvenile fict": ["ya"],
        "young adult fict": ["ya"],
        "juvenil": ["ya"],
        "teenag": ["ya"],
        "teen": ["ya"],
        "boarding school": ["ya"],
        "young adult fantasi": ["ya", "fantasi"],
        "youngadultfantasi": ["ya", "fantasi"],
        "youngadult fantasi": ["ya", "fantasi"],
        "teen fantasi": ["ya", "fantasi"],
        "juvenile fantasi": ["ya", "fantasi"],
        "teen urban fantasi": ["ya", "urban fantasi"],
        "juvenile urban fantasi": ["ya", "urban fantasi"],
        "youngadult animal fantasi": ["ya", "animal fantasi"],
        "young adult urban fantasi": ["ya", "urban fantasi"],
        "youngadult historical fantasi": ["ya", "historical fantasi"],
        "teen historical fantasi": ["ya", "historical fantasi"],
        "youngadult horror": ["ya", "horror"],
        "youngadult vampir": ["ya", "vampir"],
        "youngadult timetravel": ["ya", "time travel"],
        "juvenile timetravel": ["time travel", "ya"],
        "child": ["childrens stori"],
        "na driven": ["adult"],

        # --- Settings, Regions & Cultural History ---
        "american fict": ["american"],
        "united st": ["american"],
        "new york c": ["american"],
        "californium": ["american"],
        "san francisco": ["american"],
        "new orlean": ["american"],
        "native american": ["american"],
        "african american": ["american"],
        "london": ["england"],
        "great britain": ["england"],
        "uk": ["england"],
        "scotland": ["england"],
        "ireland": ["england"],
        "english fict": ["england"],
        "english": ["england"],
        "franc": ["contemporari"],
        "china": ["contemporari"],
        "japan": ["contemporari"],
        "egypt": ["contemporari"],
        "africa": ["contemporari"],
        "south africa": ["contemporari"],
        "mexico": ["contemporari"],
        "canada": ["contemporari"],
        "canadian fict": ["contemporari"],
        "thailand": ["contemporari"],
        "antarctica": ["contemporari"],
        "australium": ["contemporari"],
        "future australium": ["contemporari"],
        "indium": ["contemporari"],
        "spanish": ["contemporari"],
        "african": ["contemporari"],
        "african speculative fict": ["contemporari"],
        "histor": ["histori"],
        "historical fict": ["histori"],
        "prehistor": ["histori"],
        "western": ["histori"],
        "weird west": ["histori"],
        "victorian": ["histori"],
        "noir": ["histori"],
        "cold war": ["histori"],
        "civil war": ["histori"],
        "world war iu": ["histori"],
        "historical fantasy rom": ["historical fantasi", "fantasy rom"],
        "arthurian fantasi": ["historical fantasi"],
        "arthurian rom": ["historical fantasi", "rom"],
        "archeolog": ["histori"],
        "archaeolog": ["histori"],
        "military fantasi": ["militari", "fantasi"],
        "imaginary wars and battl": ["militari", "fantasi"],
        "interstellar war": ["militari", "space travel"],
        "revolut": ["militari"],
        "rebellion": ["militari"],
        "polit": ["militari"],
        "empir": ["militari"],
        "colon": ["space travel", "coloni"],
        "lost coloni": ["space travel", "coloni"],

        # --- Narrative Tone & Themes ---
        "humor": ["funni"],
        "satir": ["funni"],
        "parodi": ["funni"],
        "comic": ["funni"],
        "hummi": ["funni"],
        "insan": ["sad"],
        "suicid": ["sad"],
        "death": ["sad"],
        "reveng": ["sad"],
        "betray": ["sad"],
        "cold": ["sad"],
        "alcohol": ["sad"],
        "good and evil": ["social commentari"],
        "social critic": ["social commentari"],
        "social cla": ["social commentari"],
        "racism": ["social commentari"],
        "slaveri": ["social commentari"],
        "genocid": ["social commentari"],
        "cur": ["social commentari"],
        "surreal": ["reflect"],
        "philosophi": ["reflect"],
        "psycholog": ["reflect"],
        "literature  fiction": ["literari"],
        "literature  fict": ["literari"],
        "literatur": ["literari"],
        "literary fict": ["literari"],
        "literary fantasi": ["literari", "fantasi"],
        "metafict": ["literari"],
        "dream": ["reflect"],
        "fate": ["reflect"],
        "coming of ag": ["friendship"],
        "famili": ["friendship"],
        "sibl": ["famili"],
        "brother": ["famili"],
        "brothers and sist": ["famili"],
        "twin": ["famili"],
        "orphan": ["famili"],
        "christian fict": ["religion"],
        "christian": ["religion"],
        "futuristic": ["near futur"],
        "far futur": ["near futur"],
        "distant futur": ["near futur"],
        "futuristic rom": ["near futur", "rom"],
        "wish": ["hope"],
        "cozy mysteri": ["mysteri", "lightheart"],

        # --- Animals & Core Habitats ---
        "cat": ["anim"],
        "dog": ["anim"],
        "hors": ["anim"],
        "rat": ["anim"],
        "mous": ["anim"],
        "spider": ["anim"],
        "dolphin": ["anim"],
        "dinosaur": ["anim"],
        "insect": ["anim"],
        "talking anim": ["anim", "fairy tal"],
        "anthropomorph": ["anim"],
        "selki": ["anim"],
        "forest": ["interesting setting"],
        "desert": ["interesting setting"],
        "water": ["interesting setting"],
        "sea": ["interesting setting"],
        "small town": ["interesting setting"],
        "circu": ["interesting setting"],
        "librari": ["interesting setting"],
        "hollow earth": ["sf"],
        "basebal": ["interesting setting"],
        "sport": ["interesting setting"],

        # --- Arts, Media & Fallbacks ---
        "music": ["art"],
        "poetri": ["art"],
        "food": ["art"],
        "invent": ["sf"],
        'interstellar travel': ["space travel"],
        "mar": ["space travel"],
        "hard sf": ["sf"], 
        'adult': [],
        'polous': [],
        'contemporary fantasi': ["fantasi", "contemporari"],
        'youngadult ghost stori': ["ya", "paranorm"],
        'parallel univers': ["alternate histori"],
        'life on other planet': ["alien"],
        'middle grades fantasi': ["ya", "fantasi"],
        'moon': ["space travel"],
        'fiction in english': [],
        'literature  fictionscience fiction  fantasi' : ["sf", "literari", "fantasi"],
        'gay rom': ["lgbtq"],
        'geni': ["fairy tal"],
        'angry robot' : ["robot"],
        'christian sf': ["sf", "religion"],
        'fantasy  science fict': ["sf", "fantasi"],
        'mf' : ["rom"],
        'juvenile mysteri': ['ya', 'mysteri'],
        'christma': ["religion"],
        'cult': ["religion"],
        'overpopul': ['apocalyps'],
        'british dystopium': ['dystopia', 'england'],
        'cozi': ["lightheart"],
        'venu': ["space travel"],
        'asteroid': ["space travel"],
        'airship': ["space travel"],
        'faster than light travel': ["space travel"],
        'family secret': ['famili'],
        'imaginary plac': ["interesting setting"],
        'only human': ['social commentari'],
        'femin': ['social commentari'],
        'ident': ['social commentari'],
        'youngadult rom': ['ya', 'rom'],
        'enhanced intellig': ['robot'],
        'nuclear war': ['militari'],
        'ai': ['robot'],
        'galactic empir': ['militari', 'space travel', "coloni"],
        'spiritu': ['reflect', 'religion'],
        'surveil': ['dystopia'],
        'higher intellig': ['genetic engin'],
            'youngadult supernatur': ['ya', 'paranorm'],
        'sword  sorceri': ['sword sorceri'],
        'book': []
    }

    tags = set()

    for l in canonical_tag_map.values():
        for t in l:
            tags.add(t)

    tags = list(tags)

    return np.array(tags)


def load_transformer():
    '''
    Load the locally saved transformer and returns it
    '''
    BASE_DIR = Path(__file__).resolve().parent
    BASE_DIR = str(BASE_DIR)

    file = open(BASE_DIR + '/../../../exploratory-data-analysis/sentence_encoding/transformer.pkl', 'rb')

    transformer = pickle.load(file)

    file.close()

    return transformer


def encode_tags():
    '''
    Encode the master list of tags via the transformer we have
    '''
    tags = load_tags()
    transformer = load_transformer()

    return transformer.encode(tags)

def tag_dictionary():
    '''
    Returns the dictionary of mapping between the actual tag name and its embedded vector
    '''
    tags = load_tags()
    tags_encoded = encode_tags()

    return {tags[i] : tags_encoded[i] for i in range(len(tags))} # already checked that this is correct upto some floating point errors


def encode_books(books : pd.DataFrame, transformer : SentenceTransformer) -> pd.DataFrame:
    '''
    Input:
        books: DataFrame containing all the book data.
               In particular, books should contain a column called
               book_synopsis
        transformer: Magical transformer that takes in texts and spits out a vector
    Returns:
        books with all the synopsis encoded by the transformer
    '''

    transformer = load_transformer()

    # Drop all the missing values, so we don't have to deal with books without synopses.
    # This shouldn't be a problem because books without synopses are unlikely to be winners anyways.
    # Additionally, we have a decently large dataset even without all the null entries.
    books = books.dropna()

    #synopses = np.array(books.book_synopsis)

    books['encoded_synopsis'] = books.book_synopsis.apply(transformer.encode)

    return books

def tag_description(encoded_description : np.ndarray, transformer, encoded_tags) -> np.ndarray:
    '''
    Input:
        encoded_description: Vector of the book synopsis/description encoded by the transformer
        transformer: Load this in for performance reasons
        encoded_tags: Loaded for performance reasons
    Output:
        Array of similarities to the book description with the tags
    '''
    
    return transformer.similarity(encoded_description, encoded_tags)[0].numpy()


def tag_books(books : pd.DataFrame, transformer : SentenceTransformer, tags_encoded : np.ndarray) -> pd.DataFrame():
    """
    Inputs:
        books: DataFrame with books with already encoded synopses
        transformer: included for performance and modularity purposes
        tags_encoded: included for performance and modularity purposes

    Returns:
        books with a new column called auto_tags which contains the similarity between 
        the booksynopsis and encoded tags 
    """

    books['auto_tags'] = books.encoded_synopsis.apply(lambda x : tag_description(x, transformer, tags_encoded))

    return books