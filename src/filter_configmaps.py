import yaml



def load_configmap(file_path):
    """Load a ConfigMap from a file"""
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
    
def visit_leaf_nodes(configmap, ctx=[]):
        '''Visit all leaf nodes of a nested dictionary  
            Return a list containing the path to the leaf node and its value
        '''
        leaf_nodes = []
        for key, value in configmap.items():
            if isinstance(value, dict):
                # print("visiting dict", key, value)
                leaf_nodes.extend(visit_leaf_nodes(value, ctx + [key]))
            else:
                # print("visiting leaf", key, value)
                leaf_nodes.append(tuple(ctx + [key, value]))
        return leaf_nodes


def remove_items(initial_configmap, filter_list):
    """
    Remove items from the initial_configmap based on the filter_list
    """
    filter_items = visit_leaf_nodes(filter_list)

    # for every leaf node in the filter list, remove the corresponding key from the to_be_filtered
    for leaf_node in filter_items:
        # pop the last element from the leaf node
        leaf_node = leaf_node[:-1]
        print("removing", leaf_node)
        # remove the key from the deepcopy
        if(len(leaf_node) == 1):
            initial_configmap.pop(leaf_node[0])
        elif(len(leaf_node) == 2):
            initial_configmap[leaf_node[0]].pop(leaf_node[1])
        elif(len(leaf_node) == 3):
            initial_configmap[leaf_node[0]][leaf_node[1]].pop(leaf_node[2])
        elif(len(leaf_node) == 4):
            initial_configmap[leaf_node[0]][leaf_node[1]][leaf_node[2]].pop(leaf_node[3])
        elif(len(leaf_node) == 5):
            initial_configmap[leaf_node[0]][leaf_node[1]][leaf_node[2]][leaf_node[3]].pop(leaf_node[4])
        else:
            print("Error: leaf node is too deep")
            assert False
 
