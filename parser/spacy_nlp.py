import spacy
from spacy.matcher import Matcher
import re

def extract_svo(sent):
    # 1) find the ROOT verb
    root = next((tok for tok in sent if tok.dep_ == "ROOT"), None)
    if not root:
        return None

    # 2) find nominal subject & object among the root’s children
    subj = [w for w in root.lefts  if w.dep_.endswith("subj")]
    obj  = [w for w in root.rights if w.dep_.endswith("obj")]

    # helper: return the full noun_chunk covering tok, if any
    def to_span(tok):
        for nc in sent.noun_chunks:
            if tok in nc:
                return nc.text
        return tok.text

    if subj and obj:
        return (to_span(subj[0]), root.lemma_, to_span(obj[0]))
    return None


def print_svos(doc):
    for i, sent in enumerate(doc.sents, 1):
        # Optionally split long clauses:
        for clause in re.split(r'\s*(?:, and|;| but| and)\s*', sent.text):
            subdoc = doc.vocab.make_doc(clause)
            subdoc = doc.__class__(subdoc.vocab)(clause)  # re-parse
            svo = extract_svo(subdoc)
            if svo:
                subj, verb, obj = svo
                print(f"Sentence {i!r}, clause {clause!r} → SVO: ({subj!r}, {verb!r}, {obj!r})")


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    text = (
        "By far the largest carnivore in its environment, "
        "Tyrannosaurus rex was most likely an apex predator, "
        "preying upon hadrosaurs, juvenile armored herbivores ..."
    )
    doc = nlp(text)
    print_svos(doc)
