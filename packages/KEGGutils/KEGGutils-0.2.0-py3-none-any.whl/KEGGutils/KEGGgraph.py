import networkx as nx
import logging
import matplotlib.pylab as plt

from KEGGutils.KEGGutils import get_nodes_by_nodetype, populate_graph, connected_components, linked_nodes, graph_measures
from KEGGutils.KEGGapi import keggapi_link



class KEGGgraph(nx.DiGraph):
    
    elements = {}
    pos = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _find_arg_and_kick(self, args, to_find):
        """finds an arg in args using to_find as a substring
        
        Parameters
        ----------
        args : list
            list of args
        to_find : str
            substring to identify the argument
        
        Returns
        -------
        arg: str
            found argument
        newargs: list
            list of arguments without arg
        """

        for arg in args:
            if type(arg) == str:
                if arg.find(to_find) != -1:
                    logging.debug("found {} in args".format(arg))

                    newargs = [argument for argument in args if argument != arg]
                    args = newargs

                    return arg, newargs
        
    def list_by_nodetype(self, nodetype):
        
        nodes_dict = get_nodes_by_nodetype(self, nodetype)
        
        #it's ugly af but removes duplicates in a line
        return list(dict.fromkeys(list(nodes_dict.keys())))
    
    def connected_components(self):
        return connected_components(self)
    
    def linked_nodes(self,node):
        return linked_nodes(self, node)
    
    def graph_measures(self):
        return graph_measures(self)
        
class KEGGlinkgraph(KEGGgraph):
    
    source_db = None
    target_db = None
    
    source_nodes = {}
    target_nodes = {}
    

    def __init__(self, *args, **kwargs):
        
        if "source_db" in kwargs:
            self.source_db = kwargs.pop("source_db")
        if "target_db" in kwargs:
            self.target_db = kwargs.pop("target_db")
            
        super().__init__(*args, **kwargs)
        
        if (self.source_db is not None) and (self.target_db is not None):
            self.graph_init()
        
        
    def graph_init(self):   
        self.name = "{}_to_{}".format(self.source_db, self.target_db)
        
        nodes1, nodes2 = self._get_nodes_from_api(self.source_db, self.target_db)
        
        self.source_nodes = dict.fromkeys(nodes1, self.source_db)
        self.target_nodes = dict.fromkeys(nodes2, self.target_db)
        
        populate_graph(self, nodes1, nodes2, self.source_db, self.target_db)
        
    def _get_nodes_from_api(self, source, target):
        
        nodes1, nodes2 = keggapi_link(source, target, verbose = True)
        
        return nodes1, nodes2
    
    
            
        
    
        