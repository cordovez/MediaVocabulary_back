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
    sentence_objects = list(doc.sents) # making it a list allows you to access: sentences[2]
    sentence_texts = [str(sentence) for sentence in sentence_objects ]
    total_sentences = len(sentence_texts)
    
    ents_set = {(ent.text, ent.label_) for ent in doc.ents}
    ents_list = [{"entity":text, "label":label} for text, label in ents_set]
    
    return {"total_sentences": total_sentences, "entities": ents_list}
 



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


