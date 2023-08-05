import networkx as nx
import matplotlib.pylab as plt
import requests

#%%
# =============================================================================
# ERRORS AND EXCEPTIONS
# =============================================================================
class KeggUtilsGraphException(Exception):
    def __init__(self, graph, msg=None):
        self.graph = graph
        if msg is None:
            # Set some default useful error message
            msg = "There's a problem with graph: %s" % graph #TODO: replace %s with something
            
        super(KeggUtilsGraphException, self).__init__(msg)

        
class NotAKeggGraphError(KeggUtilsGraphException):
    pass
        
class MissingNodetypeError(KeggUtilsGraphException):
    pass

class NoDescendantError(KeggUtilsGraphException):
    def __init__(self, graph, msg = None):
        self.graph = graph
        
        if msg is None:
            msg = "Graph {} has no descendant graph".format(graph.name)
            
        super(NoDescendantError, self).__init__(graph, msg)

class KEGGOnlineError(Exception):
    def __init__(self, request, msg = None):
        self.request = request
        self.url = request.url
        self.status_code = request.status_code
        self.reason = request.reason
        
        if msg is None:
            msg = "Nework Request Error > url: {}, stat. code: {}, description: {}".format(self.url, self.status_code, self.reason)
        super(KEGGOnlineError, self).__init__(msg)
        
        
# =============================================================================
# DOWNLOADING FROM KEGG
# =============================================================================
def get_online_request(url):
    """ Just an errored proxy for requests.get()"""
    
    request = requests.get(url)
    
    if request.ok == False:
        raise KEGGOnlineError(request)
        
    print("done")
    return request

def get_organism_codes():
    """Returns all KEGG Organism name codes """
    
    org_url = "http://rest.kegg.jp/list/organism"
    
    org_codes = []
    print("Downloading KEGG organism list...")
    organism_fulltext = get_online_request(org_url).text
    
    for line in organism_fulltext.splitlines():
        T_identifier, kegg_code, description, hier= line.strip().split('\t')
        org_codes.append(kegg_code)
        
    return org_codes

def kegg_url(target_db, source_db):
    """Returns a KEGG database URL given two categories
    
    Parameters:
        :target_db (str): target category
        :source_db (str): source category
        
        both categories must be valid KEGG categories, see KEGG API Docs
        
    Returns:
        :url (str): url for the corresponding KEGG database
    Example:

        >>> kegg_url("hsa", "disease")
        'http://rest.kegg.jp/link/hsa/disease'

    .. warning:: 
        - gene category is represented with the corresponding KEGG organism code
    
        - target_db and source_db must be valid KEGG <database> names, or valid <org> names, see KEGG API Docs
        """
    db_categories = ["pathway", "brite", "module",
                     "ko", "genome", "vg",
                     "ag", "compound", "glycan", "reaction",
                     "rclass", "enzyme", "network", "variant",
                     "disease", "drug", "dgroup", "environ", "atc",
                     "jtc", "ndc", "yj", "pubmed"]
    
    #don't wanna download list it every time, too heavy
    #it's time for ugly global variables
    #just declaring doesnt actually create it
    global organism_names
    
    try:
        organism_names
    except NameError:
        organism_names = get_organism_codes()
    
    assert target_db != source_db, "Same key for target and source"
    assert all(key in db_categories+organism_names for key in [target_db, source_db]), "Invalid target or source KEGG database key"
            
    url = "http://rest.kegg.jp/link/"+target_db+"/"+source_db
    
    return url   

def get_infos(item, verbose = False):
    """ Prints KEGG infos for a given database item 
    Parameters:
        :item (str): KEGG item you want infos about
        :verbose (Bool), False: if True get full KEGG description, if False get only first 4 lines
            Example:
        """
    
    url = "http://rest.kegg.jp/get/"+item

    infos = get_online_request(url).text
    if verbose == False:
        infos = "\n".join(infos.splitlines()[1:4])
        
    print("Infos on {} from KEGG:\n".format(item))
    print(infos)
    
def kegg_graph(source_db, target_db):
    """Returns a NetworkX Graph for a KEGG target-source database
    
    Parameters:
        :target_db (str): target category
        :source_db (str): source category
        
        both categories must be valid KEGG categories, see KEGG API Docs
        
    Returns:
        :Graph (NetworkX Graph): Graph with nodes of type target_db and source_db
    Example:

        >>> KEGGgraph = gen_graph("hsa", "disease")

        .. note:: gene category is represented with the corresponding KEGG organism code
        """
    
    url = kegg_url(target_db, source_db)
    print("Downloading database {} -> {}...".format(source_db, target_db))
    text = get_online_request(url).text
    
    nodes1 = []
    nodes2 = []
    for line in text.splitlines():
        n1, n2 = line.strip().split('\t')
        nodes1.append(n1)
        nodes2.append(n2)

    graph = nx.Graph()
    populate_graph(graph, nodes1, nodes2, source_db, target_db)
    
    graph.name = "{}_to_{}".format(source_db, target_db)
    
    return graph

def populate_graph(graph, nodes_1, nodes_2, nodetype1, nodetype2):
    """Populates a pre-existing Graph given two list of nodes and two node labels
    
    Parameters:
        :graph (Graph): input graph
        :nodes_1(list): first list of nodes
        :nodes_2(list): second list of nodes
        :nodetype1(str): first nodetype
        :nodetype2(str): second nodetype
        """
    
    for i, nodo in enumerate(nodes_1):
        graph.add_node(nodo, nodetype = nodetype1)
        graph.add_node(nodes_2[i], nodetype = nodetype2)
        graph.add_edge(nodo, nodes_2[i])
        

# =============================================================================
# GRAPH OPERATIONS
# =============================================================================

def has_nodetypes(graph):
    """Populates a pre-existing Graph given two list of nodes and two node labels
    
    Parameters:
        :graph (Graph): input graph
        
    Returns:
        :has_nodetype (bool): that's self explanatory bro
        
    """
    attributes = nx.get_node_attributes(graph, 'nodetype')
    if attributes == {}:
        return False
    else:
        return True

def get_nodetype_nodes(kegg_graph, nodetype):
    """Given a KEGG graph returns list of nodes for a given nodetype
    
    Parameters:
        :kegg_graph (Graph): input graph, has to be generated via gen_graph()
        :nodetype (str): nodetype, is generally a <database> KEGG name
        
    Returns:
        :nodelist (list): list of nodes
    Example:
        >>> KEGG_graph = gen_graph("hsa", "disease")
        >>> nlist = nodelist(KEGG_graph, "hsa")
        >>> nlist[:10]
        ['hsa:7428',
         'hsa:4233',
         'hsa:2271',
         'hsa:201163',
         'hsa:7030',
         'hsa:894',
         'hsa:411',
         'hsa:1075',
         'hsa:2720',
         'hsa:2588']

    .. seealso:: gen_graph()
        """
        
    if nodetype not in get_unique_nodetypes(kegg_graph):
        raise MissingNodetypeError(kegg_graph, "Requested nodetype is missing in graph nodes")
        
    return [n for n in kegg_graph if kegg_graph.node[n]['nodetype'] == nodetype]

def connected_components(graph):
    """ Returns a list of connected components for a given graph, ordered by size"""
    subgraphs = list(nx.connected_component_subgraphs(graph))
    subgraphs = sorted(subgraphs, key=len, reverse=True)
    
    return subgraphs


    
def get_unique_nodetypes(graph):
    """Given a KEGG graph returns list of its unique nodetypes
    
    Parameters:
        :kegg_graph (Graph): input graph, has to be generated via gen_graph()
        
    Returns:
        :nodetypes (list): list of unique nodetypes
    Example:
        >>> KEGG_graph = gen_graph("hsa", "disease")
        >>> nlist = get_unique_nodetypes(KEGG_graph)
        ['disease','hsa']

    .. seealso:: gen_graph()
        """
    if has_nodetypes(graph) == False:
        raise NotAKeggGraphError(graph, "Graph nodes are missing nodetype attribute")
        
    attributes = nx.get_node_attributes(graph, 'nodetype')
    unique_nodetypes = sorted(set(attributes.values()))
    
    return unique_nodetypes


def descendant_graph(graph, nodelist, name = None):
    """Given a KEGG graph and a set of nodes returns graph of descendant nodes    
    Parameters:
        :kegg_graph (Graph): input graph, has to be generated via gen_graph()
        :nodelist (list): list of nodes
        
    Returns:
        :descendant_graph (Graph): graph of descendant nodes
    .. seealso:: gen_graph()
    """
    nodeset = set()
    
    for node in nodelist:
        try:
            nodeset.update(nx.descendants(graph, node))
        except nx.NetworkXError:
            pass
            
    if len(nodeset) == 0:
        raise NoDescendantError(graph)
        
    descendant_graph = nx.subgraph(graph, nodeset)
    
    if name is None:
        name = "desc_of_{}".format(graph.name) 
    
    descendant_graph.name = name
    
    return descendant_graph


def projected_graph(graph, nodelist, multigraph = False):
    """Calculates the prograph     
    Parameters:
        :kegg_graph (Graph): input graph, has to be generated via gen_graph()
        :nodelist (list): list of nodes
        
    Returns:
        :descendant_graph (Graph): graph of descendant nodes
    .. seealso:: gen_graph()
    """
    
    graphnodes_set = set(graph.nodes)
    nodelist_set = set(nodelist)
    
    common_nodes = graphnodes_set & nodelist_set
    
    nodetype = graph.nodes[list(common_nodes)[0]]['nodetype']
    
    disjoint_nodes = nodelist_set - set(get_nodetype_nodes(graph, nodetype))
    
    projected_graph = nx.projected_graph(graph, common_nodes, multigraph)
    
    for dis_node in disjoint_nodes:
        
        projected_graph.add_node(dis_node, nodetype = nodetype)
        
        
    return projected_graph
    
# =============================================================================
# PLOTTING
# =============================================================================
def draw(graph,
         title = None,
         layout = None,
         filename = None,
         return_ax = False):
    """Graph drawing made a bit easier
    
    Parameters:
        :graph (Graph): input graph, has to be generated via gen_graph()
        :layout (str): layout type, choose from 'bipartite_layout',\
        'circular_layout','kamada_kawai_layout','random_layout',\ 'shell_layout',\
        'spring_layout','spectral_layout'
        :filename (str): if a filename is selected saves the plot as filename.png
        :title (str): title for the graph
        :return_ax: if True returns ax for plot
        
    Returns:
        :ax (list): optional ax for the plot


        """
    default_layout = 'spring_layout'
    if layout is None: layout = default_layout
    graph_nodetypes = get_unique_nodetypes(graph)
    
    if len(graph_nodetypes) == 1:
        graph_nodetypes = graph_nodetypes*2
    
    if title is None: title = "{} > {} graph".format(graph_nodetypes[0], graph_nodetypes[1])
    
    layouts = {'bipartite_layout':      nx.bipartite_layout,
             'circular_layout':         nx.circular_layout,
             'kamada_kawai_layout':     nx.kamada_kawai_layout,
             'random_layout':           nx.random_layout,
             'shell_layout':            nx.shell_layout,
             'spring_layout':           nx.spring_layout,
             'spectral_layout':         nx.spectral_layout
             }

    if layout not in layouts:
        print("layout {} not valid: using {} layout".format(layout, default_layout))
        layout = default_layout

    plt.figure()
    
    pos = layouts[layout](graph)
    nx.draw_networkx_nodes(graph,pos,node_size=700)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)
    
    if title is not None:
        plt.title(title)
        
    plt.axis('off')
    
    if filename is not None:
        plt.savefig('output.png')
           
    plt.show()
    
    if return_ax:
        ax = plt.gca()
        
        return ax
        
        
        
        

