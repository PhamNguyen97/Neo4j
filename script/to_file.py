import pandas as pd

from config import Config
from script.read_post_data import (
    get_post_data, get_user_data, get_post_relations
)


def to_df(data):
    keys = list(data[0].keys())
    data = [[item.get(key) for key in keys] for item in data]
    return pd.DataFrame(data, columns=keys)


def main():
    config = Config()

    data = pd.read_excel(config.data_path)
    post_nodes = get_post_data(data)
    user_nodes, comment_nodes, comment_relations, reply_relations = get_user_data(data)
    post_relations = get_post_relations(data)
    print(len(post_nodes))
    print(len(set([p.id for p in post_nodes])))
    # INSERT nodes:
    post_nodes = [item.dict() for item in post_nodes]
    user_nodes = [item.dict() for item in user_nodes]
    comment_nodes = [item.dict() for item in comment_nodes]
    post_relations = [item.dict() for item in post_relations]
    comment_relations = [item.dict() for item in comment_relations]
    reply_relations = [item.dict() for item in reply_relations]

    post_data = to_df(post_nodes)
    print(len(post_data))
    print(len(set(post_data["post_id"])))
    user_nodes = pd.DataFrame(user_nodes)
    comment_nodes = pd.DataFrame(comment_nodes)
    post_relations = pd.DataFrame(post_relations)
    comment_relations = pd.DataFrame(comment_relations)
    reply_relations = pd.DataFrame(reply_relations)

    post_data.to_csv("data/post_data.csv")
    user_nodes.to_csv("data/user_data.csv")
    comment_nodes.to_csv("data/comment_data.csv")
    post_relations.to_csv("data/post_relation.csv")
    comment_relations.to_csv("data/comment_relation.csv")
    reply_relations.to_csv("data/reply_relation.csv")

if __name__ == "__main__":
    main()
