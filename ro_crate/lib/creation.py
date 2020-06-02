from rdflib import *
from datetime import datetime

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Creating a RO-crate entry and serializing it in JSON-LD
schema = Namespace("http://schema.org/")

# Writing RDF triples to populate a minimal RO-crate
graph = ConjunctiveGraph()
# graph.bind('foaf', 'http://xmlns.com/foaf/0.1/')
graph.load('https://researchobject.github.io/ro-crate/1.0/context.jsonld', format='json-ld')

# person information
orcid = "https://orcid.org/0000-0003-4929-1219"
graph.add((URIRef(orcid), RDF.type, schema.Person))

# contact information
email = "laura.rodriguez@bsc.es"
graph.add((URIRef(email), RDF.type, schema.ContactPoint))
graph.add((URIRef(email), schema.contactType, Literal('Crazy person')))
graph.add((URIRef(email), schema.name, Literal('Laura Rodriguez Navas')))
graph.add((URIRef(email), schema.email,
           Literal(email, datatype=XSD.string)))
graph.add((URIRef(email), schema.url, Literal(orcid)))

# root metadata
filename = "ro-crate-metadata.jsonld"
graph.add((URIRef(filename), RDF.type, schema.CreativeWork))
graph.add((URIRef(filename), schema.identifier, Literal(filename)))
graph.add((URIRef(filename), schema.about, URIRef('./')))

# Dataset metadata with reference to files
graph.add((URIRef('./'), RDF.type, schema.Dataset))
graph.add((URIRef('./'), schema.name, Literal("workflow outputs")))
graph.add((URIRef('./'), schema.datePublished, Literal(datetime.now().isoformat())))
graph.add((URIRef('./'), schema.author, URIRef(orcid)))
graph.add((URIRef('./'), schema.contactPoint, URIRef(email)))
graph.add((URIRef('./'), schema.description, Literal(
    "this is the description of the workfow description")))
graph.add((URIRef('./'), schema.license, Literal("MIT?")))
graph.add((URIRef('./'), schema.hasPart, (URIRef('./data/provenance.ttl'))))

# Files metadata
graph.add((URIRef('./data/provenance.ttl'), RDF.type, schema.MediaObject))

# print(graph.serialize(format='turtle').decode())
print(graph.serialize(format='json-ld').decode())


import json
import requests

res = requests.get('https://w3id.org/ro/crate/1.0/context')
ctx = json.loads(res.text)['@id']

jsonld = graph.serialize(format='json-ld', context=ctx)
print(jsonld.decode())
graph.serialize(destination='ro-crate-metadata.jsonld', format='json-ld', context=ctx)