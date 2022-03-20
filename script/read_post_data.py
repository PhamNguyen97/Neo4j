import pandas as pd

from models.node import PostNode, UserNode
from models.relation import PostRel


def get_post_data(data_frame=None) -> [PostNode]:
    if data_frame is None:
        data_frame = pd.read_excel("data/data.xlsx")
    data = data_frame.copy()
    data.drop("comments_full", axis=1, inplace=True)
    data.drop("with", axis=1, inplace=True)
    data.drop("reactors", axis=1, inplace=True)
    data.drop("post_text", axis=1, inplace=True)
    data.dropna(how='all', axis=1, inplace=True)
    post_nodes = []
    for _, row in data.iterrows():
        post_nodes.append(PostNode(props=dict(row)))
    return post_nodes


def get_user_data(data_frame=None) -> [UserNode]:
    if data_frame is None:
        data_frame = pd.read_excel("data/data.xlsx")
    data = data_frame.copy()
    data = data[["user_id", "username", "user_url"]]
    user_nodes = []
    for _, row in data.iterrows():
        user_nodes.append(UserNode(props=dict(row)))
    return user_nodes


def get_post_relations(data_frame=None) -> [PostNode]:
    if data_frame is None:
        data_frame = pd.read_excel("data/data.xlsx")
    data = data_frame.copy()
    relations = []
    for _, row in data.iterrows():
        relations.append(PostRel(src_id=row["user_id"], dst_id=row["post_id"], post_time=row["time"]))
    return relations

