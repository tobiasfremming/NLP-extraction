import spacy
from spacy.matcher import Matcher

from spacy.tokens import Token

def extract_svo(sent):
    # find the main verb
    root = next((t for t in sent if t.dep_ == "ROOT"), None)
    if not root: 
        return None

    # subjects = children of ROOT with subj- deps
    subs = [w for w in root.lefts if w.dep_.endswith("subj")]
    objs = [w for w in root.rights if w.dep_.endswith("obj")]

    def expand(tok):
        # find a noun_chunk that covers tok
        for nc in sent.noun_chunks:
            if tok in nc:
                return nc.text
        return tok.text

    if subs and objs:
        return expand(subs[0]), root.lemma_, expand(objs[0])
    return None


def print_entities(doc, nlp):

    # Print named entities
    for ent in doc.ents:
        print(f"{ent.text:20}  {ent.label_}  [{ent.start_char}:{ent.end_char}]")

    # Print dependency arcs sentence by sentence
    print("\n=== Dependency Parse ===")
    for i, sent in enumerate(doc.sents, 1):
        print(f"\nSentence {i}: {sent.text}")
        for token in sent:
            # token.dep_: dependency label; token.head: the "governor"
            print(f"  {token.text:12} → {token.head.text:12}  ({token.dep_})")

    for id, sent in enumerate(doc.sents):
        print(f'Sentence {id+1}: {extract_entity_pairs(sent)}')
  
    for id, sent in enumerate(doc.sents):
        print(f'Sentence {id+1}: {extract_relation(sent, nlp)}')
        
    for id, sent in enumerate(doc.sents):  
        entity_pair = extract_entity_pairs(sent)
        print(f'Triple {id+1}: ({entity_pair[0]}, {extract_relation(sent, nlp)}, {entity_pair[1]})')
        
import re
def split_clauses(text: str):
    # a very simple splitter. make it smarter
    return re.split(r'\s*(?:, and|;| but| and)\s*', text)

def extract_entity_pairs(sent):
    head = ''
    tail = ''

    prefix = ''             # variable for storing compound noun phrases
    prev_token_dep = ''     # dependency tag of previous token in the sentence
    prev_token_text = ''    # previous token in the sentence


    for token in sent:
        # if it's a punctuation mark, do nothing and move on to the next token
        if token.dep_ == 'punct': # TODO remove thi when parsing multiple sentences at once
            continue

        # Condition #1: subj is the head entity
        if token.dep_.find('subj') == True:
            head = f'{prefix} {token.text}'

            # Reset placeholder variables, to be reused by succeeding entities
            prefix = ''
            prev_token_dep = ''
            prev_token_text = ''      

        # Condition #2: obj is the tail entity
        if token.dep_.find('obj') == True:
            tail = f'{prefix} {token.text}'
            
        # Condition #3: entities may be composed of several tokens
        if token.dep_ == "compound":
            # if the previous word was also a 'compound' then add the current word to it
            if prev_token_dep == "compound":
                prefix = f'{prev_token_text} {token.text}'
            # if not, then this is the first token in the noun phrase
            else:
                prefix = token.text

        # Placeholders for compound cases.      
        prev_token_dep = token.dep_
        prev_token_text = token.text

    return [head.strip(), tail.strip()]


  


def extract_relation(sent, nlp):

    # Rule-based pattern matching class
    matcher = Matcher(nlp.vocab)

    # define the patterns according to the dependency graph tags 
    pattern = [{'DEP':'ROOT'},                # verbs are often root
            {'DEP':'prep','OP':"?"},
            {'DEP':'attr','OP':"?"},
            {'DEP':'det','OP':"?"},
            {'DEP':'agent','OP':"?"}] 

    matcher.add("relation",[pattern]) 

    matches = matcher(sent)
    k = len(matches) - 1

    span = sent[matches[k][1]:matches[k][2]] 

    return(span.text)



  

    
if __name__ == "__main__":

#     # 1) Load model & text
    nlp = spacy.load("en_core_web_sm")
    text = (
        "Like other tyrannosaurids, Tyrannosaurus was a bipedal carnivore with a massive skull balanced by a long, heavy tail. "
        "Relative to its large and powerful hind limbs, the forelimbs of Tyrannosaurus were short but unusually powerful for their size, and they had two clawed digits. "
        "The most complete specimen measures 12.3–12.4 m (40–41 ft) in length, but according to most modern estimates, Tyrannosaurus could have exceeded sizes of 13 m (43 ft) in length, 3.7–4 m (12–13 ft) in hip height, and 8.8 t (8.7 long tons; 9.7 short tons) in mass."
        "Although some other theropods might have rivaled or exceeded Tyrannosaurus in size, it is still among the largest known land predators, with its estimated bite force being the largest among all terrestrial animals. "
        "By far the largest carnivore in its environment, Tyrannosaurus rex was most likely an apex predator, preying upon hadrosaurs, juvenile armored herbivores like ceratopsians and ankylosaurs, and possibly sauropods. Some experts have suggested the dinosaur was primarily a scavenger. "
        "The question of whether Tyrannosaurus was an apex predator or a pure scavenger was among the longest debates in paleontology. " 
        "Most paleontologists today accept that Tyrannosaurus was both a predator and a scavenger." 
    )
   
    
    doc = nlp(text)
    entity_pairs = extract_entity_pairs(doc)
    relation = extract_relation(doc, nlp)
    print_entities(doc, nlp)
    
    for sent in nlp(text).sents:
        print(f'Sentence: {sent.text}')
        entity_pair = extract_entity_pairs(sent)
        print(f'Entity Pair: {entity_pair}')
        relation = extract_relation(sent, nlp)
        print(f'Relation: {relation}')
        print(f'Triple: ({entity_pair[0]}, {relation}, {entity_pair[1]})')


    # import textacy.extract

    # for sent in nlp(text).sents:
    #     for subj, verb, obj in textacy.extract.subject_verb_object_triples(sent):
    #         print(subj, verb, obj)
            
    # # [they] [had] [digits]
    # # [Tyrannosaurus] [could, have, exceeded] [sizes]
    # # [theropods] [might, have, rivaled] [Tyrannosaurus]
    # # [theropods] [exceeded] [Tyrannosaurus]
    
    import textacy.extract

for sent in nlp(text).sents:
    triples = textacy.extract.subject_verb_object_triples(sent)
    for subj, verb, obj in triples:
        print("SVO:", subj, verb, obj)
        
        
        

# kan kanskje bruke openrefine https://openrefine.org/