import requests
import json

from rdflib import *

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Creating a RO-crate entry and serializing it in JSON-LD
schema = Namespace("http://schema.org/")


class RO_crate_abstract:
    """
    An abstract RO-crate class to share common attributes and methods.
    """

    def __init__(self, uri):
        self.uri = uri
        self.graph = ConjunctiveGraph()

    def get_uri(self):
        return self.uri

    def print(self):
        print(self.graph.serialize(format='turtle').decode())

    def serialize_jsonld(self):
        res = requests.get('https://w3id.org/ro/crate/1.0/context')
        ctx = json.loads(res.text)['@id']

        jsonld = self.graph.serialize(format='json-ld', context=ctx)
        print(jsonld.decode())
        self.graph.serialize(destination='ro-crate-metadata.jsonld', format='json-ld', context=ctx)

    def add_has_part(self, other_ro_crate):
        self.graph = self.graph + other_ro_crate.graph
        # TODO add has_part property
        self.graph.add((URIRef(self.get_uri()), schema.hasPart, URIRef(other_ro_crate.get_uri())))


class RO_crate_Root(RO_crate_abstract):
    """
    The root RO-crate.
    """

    def __init__(self):
        RO_crate_abstract.__init__(self, uri='ro-crate-metadata.jsonld')
        self.graph.add((URIRef('ro-crate-metadata.jsonld'), RDF.type, schema.CreativeWork))
        self.graph.add((URIRef('ro-crate-metadata.jsonld'), schema.identifier, Literal('ro-crate-metadata.jsonld')))
        self.graph.add((URIRef('ro-crate-metadata.jsonld'), schema.about, URIRef('./')))


class RO_crate_Person(RO_crate_abstract):
    """
    A person RO-crate.
    """

    def __init__(self, uri):
        RO_crate_abstract.__init__(self, uri)
        self.graph.add((URIRef(uri), RDF.type, schema.Person))


class RO_crate_Contact(RO_crate_Person):
    """
    A person RO-crate.
    """

    def __init__(self, uri, name=None, email=None, ctype=None, url=None):
        RO_crate_Person.__init__(self, uri)
        self.graph.add((URIRef(uri), RDF.type, schema.Person))
        if name:
            self.graph.add((URIRef(uri), schema.name, Literal(name)))
        if email:
            self.graph.add((URIRef(uri), schema.email, Literal(email, datatype=XSD.string)))
        if ctype:
            self.graph.add((URIRef(uri), schema.contactType, Literal(ctype)))
        if url:
            self.graph.add((URIRef(uri), schema.url, Literal(url)))


if __name__ == '__main__':
    # creating a root RO-crate
    root = RO_crate_Root()
    root.print()

    # creating a person RO-crate
    orcid = "https://orcid.org/0000-0003-4929-1219"
    person = RO_crate_Person(orcid)
    person.print()

    # creating a contact RO-crate
    contact = RO_crate_Contact(orcid, name='Laura Rodriguez Navas', ctype='Crazy person')
    contact.print()

    # adding hasPart relation between RO-crates
    root.add_has_part(contact)
    root.print()

    # serializing the output
    root.serialize_jsonld()
