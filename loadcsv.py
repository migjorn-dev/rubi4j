# loadcsv
#
# Project: rubi4j
# Version: 1.0 (20.04.2022)
# Author: migjorn-dev
#
# loadcsv uses the neo4j LOAD CSV statement with APOC (Awesome Procedures on Cypher)
# it looks in the neo4j import directory for files of the name
#
# rubi4j.permutation.<nr>.bulk    Format: permutation
# rubi4j.relation.<nr>.bulk       Format: permutation-father,move,perumtation-son
#
# script will establish a constraint for unique permutation nodes
# it creates a node for each permutation (3.674.160)
# after that the relations between them (around 11 Million)
# space in neo4j needed is around 750 MB
#

from neo4j import GraphDatabase
import time

class minicube_neo4j:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    #@unit_of_work(timeout=5)
    def query_load_perm(self, tx, bulkfile):
        query = "LOAD CSV FROM 'file:///" + bulkfile + "' " + \
            "AS line CREATE (a:minicube {permutation: line[0]}) RETURN count(a)"
        return tx.run(query).single().value()

    def load_perm(self, bulkfile):
        with self.driver.session() as session:
            return session.write_transaction(self.query_load_perm, bulkfile)


    def query_load_relation(self, tx, bulkfile):
        query = "LOAD CSV FROM 'file:///" + bulkfile +"' " + \
                "AS row " + \
                "MERGE (p1:minicube {permutation: row[0]}) " + \
                "MERGE (p2:minicube {permutation: row[2]}) " + \
                "WITH p1, p2, row " + \
                "CALL apoc.create.relationship(p1, row[1], {}, p2) YIELD rel " + \
                "RETURN count(rel)"
        return tx.run(query).single().value()
        # guckst du hier (wegen apoc)
        # https://www.markhneedham.com/blog/2016/10/30/neo4j-create-dynamic-relationship-type/

    def load_relation(self, bulkfile):
        with self.driver.session() as session:
            return session.write_transaction(self.query_load_relation, bulkfile)



    def query_permutation_constraint(self, tx):
        return tx.run("CREATE CONSTRAINT ON (n:minicube) ASSERT n.permutation IS UNIQUE").single().value()

    def permutation_constraint(self):
        # define constraint to make sure each permutation is assigned to exactly one node
        with self.driver.session() as session:
            try:
                return session.write_transaction(self.query_permutation_constraint)
            except:
                return -1



if __name__ == "__main__":
    print( f'# open connection ({time.ctime()}' )
    db_feed = minicube_neo4j("bolt://localhost:7687", "neo4j", "rubi4j")
    print( f'# define constraint ({time.ctime()})' )
    db_feed.permutation_constraint()

    count = 0
    while True:
        count += 1
        print( f'# load {count} permutation ({time.ctime()})' )
        try:
            db_feed.load_perm("rubi4j-permutation."+str(count)+".bulk")
        except:
            break

    count = 0
    while True:
        count += 1
        print( f'# load {count} relation 1 ({time.ctime()})' )
        try:
            db_feed.load_relation("rubi4j-relation."+str(count)+".bulk")
        except:
            break
    print( f'# close connection ({time.ctime()})' )
    db_feed.close()


