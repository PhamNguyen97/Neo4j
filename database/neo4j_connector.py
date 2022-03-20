from neo4j import GraphDatabase

from config import Config
from models.node import Node
from models.relation import Relation


class Neo4jConnector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session()

    def close(self):
        self.driver.close()

    def make_query(self, query_func):
        done = False
        # while not done:
        #     try:
        self.session.write_transaction(query_func)
        done = True
        # except Exception as e:
        #     print(f"Cannot make query to db. Error: {e}")
        #     self.session = self.driver.session()

    def drop_all(self):
        def drop_func(tx):
            tx.run("MATCH (n) DETACH DELETE n")
        self.make_query(drop_func)

    def insert_node(self, node: Node):
        def insert_func(tx):
            query_string = "MERGE (n:" + str(node.cls) + " {node_id:" + str(node.id) + "}) "
            for prop, prop_value in node.props.items():
                if isinstance(prop_value, int) or isinstance(prop_value, float):
                    query_string += f" SET n.{prop}={prop_value}"
                else:
                    query_string += f" SET n.{prop}='{prop_value}'"
            tx.run(query_string)
        self.make_query(insert_func)

    def insert_relation(self, rel: Relation):
        def insert_func(tx):
            query_string = "MERGE (n:" + str(rel.src_cls) + " {node_id:" + str(rel.src_id) + "}) " \
                           "MERGE (n1:" + str(rel.dst_cls) + " {node_id:" + str(rel.dst_id) + "}) " \
                           "MERGE (n) -[r:" + str(rel.cls) + "] -> (n1) "
            for prop, prop_value in rel.props.items():
                if isinstance(prop_value, int) or isinstance(prop_value, float):
                    query_string += f" SET r.{prop}={prop_value}"
                else:
                    query_string += f" SET r.{prop}='{prop_value}'"
            tx.run(query_string)
        self.make_query(insert_func)


if __name__ == "__main__":
    config_ = Config()
    greeter = Neo4jConnector(config_.neo4j_uri, config_.neo4j_user, config_.neo4j_password)
    greeter.drop_all()
    greeter.insert_node(Node("AAA", {"ids": 1}))
    greeter.close()
