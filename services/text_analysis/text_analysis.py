from fastapi import HTTPException, status
from models.media_models import Independent, LATimes, SMH, TheGuardian
import spacy

nlp = spacy.load('en_core_web_trf')

async def find_article(source, article_id):
    """ 
    function takes a source ("guardian" for example) and the document "_id"
    to do a basic text analysis of that text, using spacy.
    """
    if source == "guardian":
        article = await TheGuardian.get(article_id)
    elif source == "latimes":
        article = await LATimes.get(article_id)
    elif source == "independent":
        article = await Independent.get(article_id)
    elif source == "smh":
        article = await SMH.get(article_id)
    else:
        article =  None
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return article.content.replace("\n", " ")
    
async def analyse_text(source, article_id):
    text = await find_article(source, article_id)
    
    doc = nlp(text)
    
    total_sentences = parse_sentences(doc)
    ents_list = parse_entities(doc)
    verbs, adverbs, adjectives = parse_pos(doc)
    phrasal_verbs = find_phrasal_verbs(doc)
    
    # return phrasal_verbs
    # return {"verbs": verbs, "adverbs": adverbs, "adjectives": adjectives }
    # return {"total_sentences": total_sentences, "entities": ents_list}
    return {"sentences": {"total_sentences": total_sentences},
            "entities": ents_list,
            "pos": {"verb_count": len(verbs), "verbs": verbs, 
                    "adverb_count": len(adverbs), "adverbs": adverbs,
                    "adjective_count": len(adjectives),"adjectives": adjectives},
            "phrasal_verbs": phrasal_verbs}
 

def parse_sentences(doc):
    sentence_objects = list(doc.sents) # making it a list allows you to access: sentences[2]
    sentence_texts = [str(sentence) for sentence in sentence_objects ]
    total_sentences = len(sentence_texts)
    
    return total_sentences, 
def parse_entities(doc):
    ents_set = {(ent.text, ent.label_) for ent in doc.ents}
    ents_list = [{"entity":text, "label":label} for text, label in ents_set]
    return ents_list
def parse_pos(doc):
    verbs = []
    adverbs = []
    adjectives =[]
    
    for token in doc:
        if token.pos_ == "VERB":
            if token.text not in verbs:
                verbs.append({"verb": token.text, "lemma":token.lemma_})
        elif token.pos_ == "ADV":
            if token.text not in adverbs:
                adverbs.append(token.text)
        elif token.pos_ == "ADJ":
                if token.text not in adjectives:
                    adjectives.append(token.text)

    # example: [... "post", "-", "op" ...] becomes [... "post-op" ...]         
    for i in range(len(adjectives) - 1):
        if adjectives[i+1] == "-":
            adjectives.append(adjectives[i ] + "-" + adjectives[i + 2])
            
    for i in range(len(adjectives) - 1, -1, -1):
        if adjectives[i]== "-":
            adjectives.pop(i) 
            adjectives.pop(i) 


    return verbs, adverbs, adjectives

def find_phrasal_verbs(doc):
    common_particles = ["around", "at", "away", "down", "in", "off", 
                        "on", "out", "over", "round", "up"]
    phrasal_verbs = []
    for i in range(len(doc) - 1):
        token = doc[i]
        next_token = doc[i + 1]
        if token.pos_ == "VERB" and next_token.text in common_particles and token.lemma_ != "’":
            phrasal_verbs.append(f"{token.text} {next_token.text}")
    return phrasal_verbs  
    
async def  aggregate_content(source):
    if source == "guardian":
        content =  [doc.content for doc in await TheGuardian.find().to_list()]
    elif source == "latimes":
        content =  [doc.content for doc in await LATimes.find().to_list()]
    elif source == "independent":
        content =  [doc.content for doc in await Independent.find().to_list()]
    elif source == "smh":
        content =  [doc.content for doc in await SMH.find().to_list()]
    else:
        content =  None

    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return content

    
    aggregated_content = " ".join(content)
    
    return aggregated_content
