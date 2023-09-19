from fastapi import HTTPException, status
from models.media_models import Independent, LATimes, SMH, TheGuardian
import spacy
import timeit
import string
import re

nlp = spacy.load('en_core_web_trf')

# Dictionary Dispatch pattern:
MEDIA = {
    'guardian' : TheGuardian,
    'independent' : Independent,
    'latimes' : LATimes,
    'smh' : SMH,
}

async def find_article(source, article_id):
    """ 
    function takes a source ("guardian" for example) and the document "_id"
    to do a basic text analysis of that text, using spacy.
    """
    if source not in MEDIA:
        raise ValueError("Unknown Media")
    data = await MEDIA[source].get(article_id)
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    article = data.content.replace("\n", " ")
    
    return article

    
async def analyse_text(source, article_id):
    """ 
    Function passes the values of 'source' and 'article_id' and passes them to another function that retrieves the text of the found document.
    
    The text will be analysed within with Spacy.
    """
    text = await find_article(source, article_id)
    
    doc = nlp(text)
    
    total_sentences = parse_sentences(doc)
    ents_list = parse_entities(doc)
    verbs, adverbs, adjectives = parse_pos(doc)
    phrasal_verbs = find_phrasal_verbs(doc)
    
    return {"sentences": {"total_sentences": total_sentences},
            "entities": ents_list,
            "pos": {"verb_count": len(verbs), "verbs": verbs, 
                    "adverb_count": len(adverbs), "adverbs": adverbs,
                    "adjective_count": len(adjectives),"adjectives": adjectives},
            "phrasal_verbs": phrasal_verbs}
 

def parse_sentences(doc):
    """ 
    Function takes a Spacy object 'doc' and parse it to find and analyse 
    at sentence level.
    """
    sentence_objects = list(doc.sents) 
    # making it a list allows you to access: sentences[2]
    
    sentence_texts = [str(sentence) for sentence in sentence_objects ]
    total_sentences = len(sentence_texts)
    
    return total_sentences 


def parse_entities(doc):
    """ 
    Function takes a Spacy object 'doc' and parse it to find entities.
    """
    
    ents_set = {(ent.text, ent.label_) for ent in doc.ents}
    ents_list = [{"entity":text, "label":label} for text, label in ents_set]
    return ents_list


def parse_pos(doc):
    """ 
    Function takes a Spacy object 'doc' and parses it to find verbs, adverbs, 
    and adjectives.
    
    Two 'for' loops take care of compound adjectives like "post-op" 
    that are separated at the '-'. 
    """
    exclude_glyphs = [ '”', '‘', '“', '’']
    
     # Create a set of punctuation characters to exclude
    exclude_punctuation = set(string.punctuation)
    
    # set comprehension to avoid duplicates, wrapped in a list()
    for token in doc:
        if token.text not in exclude_glyphs and token.text not in exclude_punctuation:
            verbs = list({token.text for token in doc if token.pos_=='VERB'})
            adverbs = list({token.text for token in doc if token.pos_=='ADV'})
            adjectives = list({token.text for token in doc if token.pos_=='ADJ'})
        

    # rejoin hyphenated adjectives 
    # example: [... "post", "-", "op" ...] becomes [... "post-op" ...]         
    for i in range(len(adjectives) - 1):
        if adjectives[i+1] == "-":
            adjectives.append(adjectives[i ] + "-" + adjectives[i + 2])
            
    # and remove separated ones    
    for i in range(len(adjectives) - 1, -1, -1):
        if adjectives[i]== "-":
            adjectives.pop(i) 
            adjectives.pop(i) 


    return verbs, adverbs, adjectives



def find_phrasal_verbs(doc):
    """ 
    Function takes a Spacy object 'doc' and parse it to find phrasal verbs. 
    This is not a trained model.
    """

    common_particles = ["around", "at", "away", "down", "in", "off", 
                        "on", "out", "over", "round", "up", "after", "into", "for"]
    phrasal_verbs = []
    for i in range(len(doc) - 1):
        token = doc[i]
        next_token = doc[i + 1]
            
        # unseparated
        if token.pos_ == "VERB" and next_token.text in common_particles and token.lemma_ != "’":
            phrasal_verbs.append(f"{token.text} {next_token.text}")
    
    for i in range(len(doc) - 3):
        token = doc[i]
        next_token = doc[i +1]
        second_next_token = doc[i + 2]
            
        # separated
        if token.pos_ == "VERB" and second_next_token.text in common_particles and token.lemma_ != "’":
            phrasal_verbs.append(f"{token.text} {next_token.text} {second_next_token.text}")
    
    

            
    
    return phrasal_verbs 
    
async def  aggregate_content(source):
    """
    Function concatenates the text from the ten articles return from the 
    source passed as an argument.
    """
    # list_of_sources = [{"source":"guardian" , "mongo_model": TheGuardian},
    #                    {"source":"independent" , "mongo_model": Independent},
    #                    {"source":"latimes" , "mongo_model": LATimes},
    #                    {"source":"smh" , "mongo_model": SMH}]
    
    if source in MEDIA:
        content = [doc.content for doc in await MEDIA[source].find().to_list()]
    
    # if source in {"guardian", "latimes", "independent", "smh"}:
    #     mongo_model = next(item["mongo_model"] for item in list_of_sources 
    #                         if item["source"] == source)
    #     content = [doc.content for doc in await mongo_model.find().to_list()]
        if not content:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # return content
        aggregated_content = " ".join(content)
        return aggregated_content

    else:
        return None

    # aggregated_content = await aggregate_func()

    # return aggregated_content
 

async def analyse_aggregated_text(text):
    """ 
    Function passes the values of 'source' and 'article_id' and passes them 
    to another function that retrieves the text of the found document.
    
    The text will be analysed within with Spacy.
    """
    joined_text = " ".join(text)
    doc = nlp(joined_text)  
    
    total_sentences = parse_sentences(doc)
    ents_list = parse_entities(doc)
    verbs, adverbs, adjectives = parse_pos(doc)
    phrasal_verbs = find_phrasal_verbs(doc)
   
    return {
        "verbs": verbs,
        "adverbs": adverbs,
        "adjectives": adjectives,
        "phrasal_verbs": phrasal_verbs,
        "total_sentences": total_sentences,
        "entities": ents_list
    }
    