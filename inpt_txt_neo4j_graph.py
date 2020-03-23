#!/usr/bin/env python
# coding: utf-8

# In[2]:


# This program accepts input text from user and display in visual format

#Importing important libraries
import spacy
from spacy import displacy
from arango import ArangoClient


# In[3]:


# Arango connection and login to database
client = ArangoClient(hosts = 'http://localhost:8529') # Connecting to local web interphase of arango database
db = client.db('test', username = 'nagendra', password = '1432') #Login to arango db with existing user nagendra


# In[4]:


db.graphs()


# In[5]:


#db.delete_graph('sent2graph')


# In[6]:


#Creating graph if it dose not present
if db.has_graph("sent2graph"):
    sent2graph = db.graph("sent2graph")
else:
    sent2graph = db.create_graph("sent2graph")


# In[7]:


#delete_edge_definition('entity', purge=True)
#db.delete_collection('entity')


# In[8]:


#Create edge definitions if not exists
if not sent2graph.has_edge_definition('entity'):
    entity = sent2graph.create_edge_definition(
        edge_collection = 'entity',
        from_vertex_collections = ['sents'],
        to_vertex_collections = ['ents']
    )


# In[9]:


#Loading spacy library and it's component
nlp = spacy.load("en_core_web_sm")
nlp.pipeline
nlp.pipe_names    


# In[35]:


#print(nlp.Defaults.stop_words)
print(len(nlp.Defaults.stop_words))
nlp.Defaults.stop_words.add('male')
print(len(nlp.Defaults.stop_words))
print(nlp.vocab['male'].is_stop)
nlp.Defaults.stop_words.remove('male')
print(len(nlp.Defaults.stop_words))


# In[34]:


from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab)
#print(matcher)
pattern1 = [{'LOWER':'solarpower'}]
pattern2 = [{'LOWER':'solar'},{'LOWER':'power'}]
pattern3 = [{'LOWER':'solar'},{'IS_PUNCT':True},{'LOWER':'power'}]
matcher.add('SolarPower', None, pattern1, pattern2, pattern3)
doc1 = nlp(u'The Solar Power industry continues to grow as demand for solarpower increases. Solar-power cars are gaining popularity.')
found_matches = matcher(doc1)
print(found_matches)
for match_id, start, end in found_matches:
    string_id = nlp.vocab.strings[match_id]
    span = doc1[start:end]
    print(match_id, string_id, start, end, span.text)
    
pattern4 = [{'LOWER':'solar'},{'IS_PUNCT':True, 'OP':'*'},{'LOWER':'power'}]
matcher.add('SolarPower', None, pattern1, pattern4)
found_matches_sp = matcher(doc1)
print(found_matches_sp)
for match_id, start, end in found_matches_sp:
    string_id = nlp.vocab.strings[match_id]
    span = doc1[start:end]
    print(match_id, string_id, start, end, span.text)


# In[10]:


#Getting input 
#doc = nlp(input("Please enter the sentences of your choice to visualize: "))
mystring = "He was a one-eyed, one-horned, flying, purple people-eater.Autonomous cars shift insurance liability toward manufacturers. Apple to build a Hong Kong factory for $6 million."
doc = nlp(mystring)
print(len(doc))
print(len(doc.vocab))


# In[11]:


# Printing sentence, different words and properties, entitie and noun chunks
entity = sent2graph.edge_collection('entity')
sents = sent2graph.vertex_collection('sents')
ents = sent2graph.vertex_collection('ents')

for sent in doc.sents:
    print(sent)
    sk = sents.insert({'sentence': str(sent)})
    #sent_key = k['_key']
    #print(sents.sentence.keys())
    #uttr = sent
    #for token in sent:
    #    print(token.text, '\t', token.lemma, '\t', token.lemma_, '\t', str(spacy.explain(token.lemma_)), '\t',
    #          token.pos, '\t', token.pos_, '\t', str(spacy.explain(token.pos_)), '\t', 
    #          token.dep, '\t', token.dep_, '\t', str(spacy.explain(token.dep_)), '\t', 
    #          token.tag, '\t', token.tag_, '\t', str(spacy.explain(token.tag_)))
    
    #print("********************************")
        
    for ent in sent.ents:
        print(ent.text+' - '+ent.label_+' - '+str(spacy.explain(ent.label_)))
        ent = ent.text+' - '+ent.label_+' - '+str(spacy.explain(ent.label_))
        ek = ents.insert({'entity': str(ent)})
        #ent_key = ek['_key']
                 
        entity.insert({'_from': sk['_id'], '_to': ek['_id']})
        
    #print("********************************")
    
    #for chunk in sent.noun_chunks:
    #    print(chunk.text)
    
    sent_traverse = sent2graph.traverse(
        start_vertex=sk['_id'],
        direction='outbound',
        strategy='bfs',
        edge_uniqueness='global',
        vertex_uniqueness='global',
    )


# In[12]:


displacy.render(doc, style='ent', jupyter=True)


# In[13]:


displacy.render(doc, style='dep', jupyter=True, options={'distance': 110})


# In[14]:


displacy.serve(doc, style='dep')


# In[ ]:




