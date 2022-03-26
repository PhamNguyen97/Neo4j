import pandas as pd
from tqdm import tqdm

from config import Config
from script.read_post_data import (
    get_post_data, get_user_data, get_post_relations
)
from database.neo4j_connector import Neo4jConnector


def main():
    config = Config()
    connector = Neo4jConnector(uri=config.neo4j_uri, user=config.neo4j_user, password=config.neo4j_password)

    data = pd.read_excel(config.data_path)
    post_nodes = get_post_data(data)
    user_nodes, comment_nodes, comment_relations, reply_relations = get_user_data(data)
    post_relations = get_post_relations(data)
    # INSERT nodes:
    # for post_node in tqdm(post_nodes):
    #     connector.insert_node(post_node)
    #
    # for user_node in tqdm(user_nodes):
    #     connector.insert_node(user_node)

    for comment_node in tqdm(comment_nodes):
        connector.insert_node(comment_node)

    for post_relation in tqdm(post_relations):
        connector.insert_relation(post_relation)

    for comment_relation in tqdm(comment_relations):
        connector.insert_comment_relation(comment_relation)

    for react_relation in tqdm(reply_relations):
        connector.insert_reply_relation(react_relation)


if __name__ == "__main__":
    main()
