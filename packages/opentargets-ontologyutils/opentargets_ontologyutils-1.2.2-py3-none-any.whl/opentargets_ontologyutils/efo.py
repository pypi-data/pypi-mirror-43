from __future__ import print_function

import logging
import collections

import rdflib

from opentargets_ontologyutils.rdf_utils import OntologyClassReader,merge_classes_paths

logger = logging.getLogger(__name__)


"""
Loads EFO from the URI provided into the ontology class reader object
returns nothing
"""
def load_open_targets_disease_ontology(ocr, efo_uri):

    logger.debug("load_open_targets_disease_ontology...")
    ocr.load_ontology_graph(efo_uri)

    ocr.get_deprecated_classes(obsoleted_in_version=True)

    # disease, phenotype, measurement, biological process, function
    #these are the parts of EFO that we want to slim to
    ocr.classes_paths = {}
    for root in [ 'http://www.ebi.ac.uk/efo/EFO_0000408', #disease
            'http://www.ebi.ac.uk/efo/EFO_0000651', #phenotype
            'http://www.ebi.ac.uk/efo/EFO_0001444', #measurement
            'http://purl.obolibrary.org/obo/GO_0008150', #biological_process
            'http://www.ifomis.org/bfo/1.1/snap#Function']: #function

        ocr.load_ontology_classes(base_class=root)
        classes_paths = ocr.get_classes_paths(root_uri=root, level=0)
        ocr.classes_paths = merge_classes_paths(ocr.classes_paths, classes_paths)
    logger.debug("Found %d classes", len(ocr.current_classes.keys()))


    #discover the therapeutic areas that are labelled in the ontology
    therapeutic_areas = tuple(find_therapeutic_areas(ocr.rdf_graph))
    logger.debug("Found %d therapeutic areas", len(therapeutic_areas))

    #combine a dictionary of which therapeutic areas each term is in
    ocr.therapeutic_labels = collections.defaultdict(list)
    ocr.therapeutic_uris = collections.defaultdict(list)
    for uri in ocr.classes_paths:
        #check if this uri is a therapeutic area itself
        if uri in therapeutic_areas:
            label = ocr.current_classes[uri]
            if label not in ocr.therapeutic_labels[uri]:
                ocr.therapeutic_labels[uri].append(label)
                ocr.therapeutic_uris[uri].append(uri)
        #follow all paths to root and check if therapeutic area
        for path in ocr.classes_paths[uri]['all']:
            for entry in path:
                if entry['uri'] in therapeutic_areas:
                    label = ocr.current_classes[entry['uri']]
                    if label not in ocr.therapeutic_labels[uri]:
                        ocr.therapeutic_labels[uri].append(label)
                        ocr.therapeutic_uris[uri].append(entry['uri'])


"""
Generator of the therapeutic areas labelled in the rdf graph of efo
"""
def find_therapeutic_areas(rdf_graph):
    in_subset = rdflib.term.URIRef('http://www.geneontology.org/formats/oboInOwl#inSubset')
    therapeutic_area_label = rdflib.term.Literal('therapeutic_area')
    for s in rdf_graph.subjects(in_subset,therapeutic_area_label):
        therapeutic_area = str(s)
        logger.debug("found therapeutic area: %s", therapeutic_area)
        yield therapeutic_area
