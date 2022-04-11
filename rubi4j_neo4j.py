# rubi4j-neo4j
# Version 0.4 (11.4.2022)
# Author Markus Luft
#
# pyhon class to insert minicube permutations into neo4j database

from neo4j import GraphDatabase


class minicube_neo4j:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    #@unit_of_work(timeout=5)
    def create_permutation(self, tx, permutation):
        return tx.run("CREATE (a:minicube {permutation: $permutation, children: $children}) RETURN id(a)",
                      permutation=permutation, children=0).single().value()

    def add_permutation(self, permutation):
        with self.driver.session() as session:
            try:
                # we will get an error if there is a unique constraint in place
                return session.write_transaction(self.create_permutation, permutation)
            except:
                return 0


    def query_number_of_children(self, tx, permutation):
        return tx.run("MATCH (a:minicube {permutation: $permutation}) RETURN a.children",
                      permutation=permutation).single().value()

    def get_number_of_children(self, permutation):
        with self.driver.session() as session:
            # we will get an error if permutation is not a node
            try:
                return session.read_transaction(self.query_number_of_children, permutation)
            except:
                return -1


    def change_permutation_children(self, tx, permutation, children):
        return tx.run("MATCH (a:minicube {permutation: $permutation}) SET a.children=$children RETURN a.id",
                      permutation=permutation, children=children).single().value()

    def increase_permutation_children(self, permutation):
        with self.driver.session() as session:
            # we will get an error if there is no node with this permutation
            children = self.get_number_of_children(permutation)
            children = int(children) + 1
            children = str(children)
            return session.write_transaction(self.change_permutation_children, permutation, children)


    def query_permutation_constraint(self, tx):
        return tx.run("CREATE CONSTRAINT ON (n:minicube) ASSERT n.permutation IS UNIQUE").single().value()

    def permutation_constraint(self):
        # define constraint to make sure each permutation is assigned to exactly one node
        with self.driver.session() as session:
            try:
                return session.write_transaction(self.query_permutation_constraint)
            except:
                return -1


    def query_add_father_son_relation(self, tx, permutation_father, permutation_son, cube_side):
        return tx.run("MATCH (a:minicube {permutation: $permutation_father}), "
                      "(b:minicube {permutation: $permutation_son}) "
                      "CREATE(a) -[r: MOVE{side: $cube_side}]-> (b) "
                      "RETURN r.name",
                      permutation_father=permutation_father,
                      permutation_son=permutation_son,
                      cube_side=cube_side ).single().value()

    def add_father_son_relation(self, permutation_father, permutation_son, cube_side):
        # define relation between to permutations - relation is named by side moved to reach son from father
        with self.driver.session() as session:
            return session.write_transaction(self.query_add_father_son_relation,
                                             permutation_father, permutation_son, cube_side)
