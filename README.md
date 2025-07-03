# NLP Knowledge Graph Extractor

A rule‑based information extraction pipeline for building graph data from natural language text using [spaCy](https://spacy.io/) transformer models. Extracts Subject–Predicate–Object (SPO) triples and additional factual relations without relying on LLMs, keeping costs low and performance high.

---

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Quickstart](#quickstart)
* [Extraction Pipeline](#extraction-pipeline)

  * [Core SPO Extractor](#core-spo-extractor)
  * [Additional Rules](#additional-rules)
* [Usage](#usage)

* [License](#license)

---

## Features

* Rule‑based extraction of SPO triples (ROOT → subject → object) from text
* Merging of multi‑word entities and noun chunks for accurate spans
* Optional patterns for appositions, conjunctions, prepositional relations, numeric measures, adjectival modifiers, and more
* Fully offline: uses spaCy transformer models (e.g., `en_core_web_trf`)
* No expensive LLM calls required in core pipeline

---

## Prerequisites

* Python 3.8+ (tested on 3.12)
* [spaCy 3.7+](https://spacy.io/) and `en_core_web_trf` model

Optional for advanced patterns:

* AllenNLP or Hugging Face for coreference resolution
* Custom relation extractor models (spaCy v3)

---

## Installation

1. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   # .\venv\Scripts\activate  # Windows PowerShell
   ```

2. **Install dependencies**

   ```bash
   pip install --upgrade pip setuptools wheel
   pip install spacy==3.7.4 spacy-transformers transformers
   python -m spacy download en_core_web_trf
   ```

3. **Configure `requirements.txt`**

   ```text
   spacy==3.7.4
   spacy-transformers
   transformers
   en_core_web_trf
   ```

---

## Quickstart

Load the model and run the basic extractor:

```python
import spacy

nlp = spacy.load("en_core_web_trf")
nlp.add_pipe("merge_entities")
nlp.add_pipe("merge_noun_chunks")
nlp.add_pipe("merge_subtokens")

text = "Tyrannosaurus rex was a massive predator in the Late Cretaceous..."
for sent in nlp(text).sents:
    spo = extract_spo(sent)
    if spo:
        print(spo)
```

---

## Extraction Pipeline

### Core SPO Extractor

1. **ROOT detection**: find the token with `dep_ == "ROOT"`.
2. **Subject**: left children where `"subj"` is in `dep_` (covers `nsubj`, `nsubjpass`).
3. **Object**: right children in (`dobj`, `pobj`, `iobj`, `attr`, `acomp`).
4. **Phrase assembly**: use `tok.subtree` to capture full spans.
5. **Relation**: include auxiliary (`aux`, `auxpass`), negation (`neg`), particles (`prt`) with the verb.



### Additional Rules

* **Appositions (`appos`)**: capture definitions (`X is a Y`).
* **Conjunctions (`conj`)**: split `A and B are C` into separate triples.
* **Prepositions (`prep`→`pobj`)**: extract `X with Y`, `X in Z`, etc.
* **Numeric measures**: detect `like_num` + unit spans → `has_measure`.
* **Adjectival modifiers (`amod`)**: `X is Y` for noun–adjective pairs.
* **Clausal complements (`ccomp`/`xcomp`)**: subordinate clause facts.
* **Relative clauses (`acl`/`relcl`)**: `A that B` patterns.
* **Possessives (`poss`, `nmod:of`)**: `X's Y` or `Y of X` → `X has Y`.
* **Passive voice**: handle `agent` and `nsubjpass`.

Customize by enabling or disabling rules in your notebook.

---



## License

This project is licensed under the MIT License. Feel free to use and modify!
