import pytest
import yaml
import copy



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
 


def test_load_configmap():
    configmap = load_configmap("./original-configmap.yaml")
    assert configmap["apiVersion"] == "v1"
    assert configmap["kind"] == "ConfigMap"
    assert configmap["metadata"]["name"] == "store-inventory"


def test_load_configmap_wrong_file():
    with pytest.raises(FileNotFoundError):
        load_configmap("wrong-file.yaml")


def test_visit_leaf_nodes_empty():
    initial_configmap = {}
    expected_leaf_nodes = []
    assert visit_leaf_nodes(initial_configmap) == expected_leaf_nodes


def test_visit_leaf_nodes():
    initial_configmap = {
        "apiVersion": "v1",
        "metadata": {
            "name": "store-inventory",
            "annotations": {
                "marketplace.com/comments": "What about chess?"
            },
        },
        "data": {
            "competitive": "300",
        }
    }

    expected_leaf_nodes = [
        ("apiVersion", "v1"),
        ("metadata", "name", "store-inventory"),
        ("metadata", "annotations", "marketplace.com/comments", "What about chess?"),
        ("data", "competitive", "300"),
    ]

    leaf_nodes = visit_leaf_nodes(initial_configmap)
    assert leaf_nodes == expected_leaf_nodes

    
def test_remove_items_in_configmap_that_are_in_filter_list():
    initial_configmap = {
        "apiVersion": "v1",
        "metadata": {
            "name": "store-inventory",
            "annotations": {
                "marketplace.com/comments": "What about chess?",
                "blah": "blah"
            },
        },
        "data": {
            "competitive": "300",
        }
    }
    
    filter_list = {
        "metadata": {
            "annotations": {
                "marketplace.com/comments": None
            },
        },
    }

    remove_items(initial_configmap, filter_list)

    assert initial_configmap == {
        "apiVersion": "v1",
        "metadata": {
            "name": "store-inventory",
            "annotations": {
                "blah": "blah"
            },
        },
        "data": {
            "competitive": "300",
        }
    }




def test_filter_configmap():
    downloaded_configmap = load_configmap("./downloaded-configmap.yaml")
    ignore_list = load_configmap("ignore-list.yaml")
    remove_items(downloaded_configmap, ignore_list)
    assert downloaded_configmap == {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": "store-inventory",
            "namespace": "gamestore",
            "annotations": {
                "marketplace.com/comments": "What about chess?"
            },
            "labels": {},
        },
        "data": {
            "single_player": "20",
            "cooperative": "60",
            "competitive": "300",
        },   
    }



if __name__ == "__main__":
    pytest.main()