'''
Add by Cyan
Wed Jan  6 16:07:11 CST 2021
'''
#!/bin/env python3
import os


'''
'''
class DependsGraph:
    '''
    Depends Graph
    each node is an application of brew
    '''
    class Node:
        '''
        Graph node 
        each node has several root nodes, and several child nodes
        '''
        def __init__(self, app_name: str):
            self.name = app_name
            self.pre = set()
            self.suc = set()

        def __str__(self):
            ss = f"{self.name}:\n\t["
            for node in self.pre:
                ss += f"{node.name} "
            ss += "]\n\t("
            for node in self.suc:
                ss += f"{node.name} "
            ss += ")"

            return ss

        @classmethod
        def instance(cls, app_name: str, depends: list):
            node = cls(app_name)
            for name in depends:
                suc = cls(name)
                suc.pre = {node}
                node.suc.add(suc)

            return node

    
    def __init__(self):
        self.root = DependsGraph.Node('')
        self.nodes = {}

    def add_node(self, new_node: Node):
        new_name = new_node.name
        for node in new_node.suc:
            if node.name not in self.nodes:
                self.nodes[node.name] = node
            self.nodes[node.name].pre.add(new_node)

        if new_name not in self.nodes:
            self.nodes[new_name] = new_node
        else:
            self.nodes[new_name].pre |= new_node.pre

    def make_root(self):
        for node in self.nodes.values():
            if len(node.pre) == 0:
                node.pre.add(self.root)

    def get_depends(self, app_name):
        if app_name not in self.nodes:
            return []
        return [node.name for node in self.nodes[app_name].suc]

    def get_base(self, app_name):
        if app_name not in self.nodes:
            return []
        return [node.name for node in self.nodes[app_name].pre]

    def __str__(self):
        ss = ""
        for node in self.nodes.values():
            ss += f"{node}\n"
        return ss

    @classmethod
    def instance(cls):
        graph = cls()

        with os.popen("brew deps --installed") as f:
            for line in f.readlines():
                line = line.strip()
                # print(line)
                app_names = line.split()
                app = app_names[0][:-1]
                dep_apps = app_names[1:] if len(app_names) > 1 else []

                node = DependsGraph.Node.instance(app, dep_apps)
                graph.add_node(node)

                # print(node)

        graph.make_root()
        return graph


