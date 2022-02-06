from py2neo import Graph
import csv

class SmartEQP():
    def __init__(self):
        self.server_host = 'bolt://localhost:7687'
        self.username = 'neo4j'
        self.password = '1234'
        self.graph = Graph(self.server_host, auth=(self.username, self.password))
        self.node_order = {'Fab':0,
                           'Department':1,
                           'Section':2,
                           'Layer':3,
                           'Recipe':4,
                           'Step':5,
                           'Modify_Config':6}
        self.node_information = {'Fab':             {'necessary': ['name'], 'other': ['founder', 'date']},
                                 'Department':      ['name'],
                                 'Section':         ['name'],
                                 'Layer':           ['name'],
                                 'Recipe':          ['name'],
                                 'Step':            ['name'],
                                 'Modify_Config':   ['name']}
        self.relationship = ["has"]

    # check if node exist, not then create node
    def check_and_create_node(self, data, info_key):
        # necessary node information
        node_nes_str = '(n1:%s {' % (info_key)
        for info_name in self.node_information[info_key]['necessary']:
            if info_name == 'name':
                node_nes_str += '%s:%s, ' % ('name', data[info_key])
            else:
                node_nes_str += '%s:%s, ' % (info_name, data[info_name])
        node_nes_str = node_nes_str.rstrip(', ')
        node_nes_str += '})'

        # node information with others information
        node_oths_str = node_nes_str.rstrip('})')
        for info_name in self.node_information[info_key]['other']:
            node_oths_str += '%s:%s, ' % (info_name, data[info_name])
        node_nes_str = node_nes_str.rstrip(', ')
        node_nes_str += '})'

        # run graph
        cyther_str = 'MATCH %s with count(n1) as check' \
                     'WHERE check = 0 CREATE %s' %(node_nes_str, node_oths_str)

        self.graph.run(cyther_str)

    # find node correspond to data information
    def find_node(self, data, info_key, node_name):
        # necessary node information
        node_nes_str = '(%s:%s {' % (node_name, info_key)
        for info_name in self.node_information[info_key]['necessary']:
            if info_name == 'name':
                node_nes_str += '%s:%s, ' % ('name', data[info_key])
            else:
                node_nes_str += '%s:%s, ' % (info_name, data[info_name])
        node_nes_str = node_nes_str.rstrip(', ')
        node_nes_str += '})'

        cyther_str = 'MATCH node_nes_str'
        return cyther_str





if __name__ == '__main__':
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "1234"))
    cypher_str = 'MATCH (n:test) RETURN n'
    data = graph.run(cypher_str).data()
    print(data)
    print(type(data))
    print(len(data))



    # with open(r'D:\neo4j\data\test.csv', newline='') as csvfile:
    #     rows = csv.DictReader(csvfile)
    #
    #     for row in rows:
    #         print(row['Department'], row['Section'])

