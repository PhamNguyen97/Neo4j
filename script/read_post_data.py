import pandas as pd
import re
import json

from models.node import PostNode, UserNode, Comment
from models.relation import PostRel, CommentRel, ReplyRel


datetime_re = re.compile(r": datetime.datetime\((.*?)\)")
re_1 = re.compile(r'([0-9])+"')


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


def parse_comments(comment):
    if not isinstance(comment, float):
        inches = re_1.findall(comment)
        for inch in inches:
            comment = comment.replace(f'{inch}"', f'{inch}``')
        if comment[-2:] != "}]":
            comment += "'}]"
        comment = comment.replace('" FHD', "`` FHD").replace("'", '"').replace('" ', "' ").replace(": None", ": null")
        datetime_strings = datetime_re.findall(comment)
        for datetime_string in datetime_strings:
            comment = comment.replace(f": datetime.datetime({datetime_string})", f': "datetime.datetime({datetime_string})"')
        try:
            comment = json.loads(comment)
        except Exception as e:
            print(e)
            comment = []
            # print(comment)
            # print(comment[32760:32770])
        return comment
    return []


def get_user_data(data_frame=None) -> ([UserNode], [Comment]):
    if data_frame is None:
        data_frame = pd.read_excel("data/data.xlsx")
    data = data_frame.copy()
    comments = data["comments_full"]
    comments = [parse_comments(comment) for comment in comments]
    data = data[["user_id", "username", "user_url", "post_id"]]
    user_nodes = []
    comment_nodes = []
    comment_relations = []
    reply_relations = []
    for (_, row), post_comments in zip(data.iterrows(), comments):
        for comment in post_comments:
            if comment.get("commenter_id") is None:
                continue
            comment_replies = comment.get("replies", [])
            if "comment_reactors" in comment:
                del comment["comment_reactors"]
            if "replies" in comment:
                del comment["replies"]
            if "comment_reactions" in comment:
                del comment["comment_reactions"]

            user_nodes.append(UserNode(props={
                "user_id": comment["commenter_id"],
                "username": comment["commenter_name"],
                "user_url": comment["commenter_url"]
            }))
            comment_nodes.append(Comment(props=comment))
            comment_relations.append(CommentRel(user_id=comment["commenter_id"],
                                                comment_id=comment["comment_id"],
                                                post_id=row["post_id"]))

            for reply_comment in comment_replies:
                user_nodes.append(UserNode(props={
                    "user_id": reply_comment["commenter_id"],
                    "username": reply_comment["commenter_name"],
                    "user_url": reply_comment["commenter_url"]
                }))
                if "comment_reactors" in reply_comment:
                    del reply_comment["comment_reactors"]
                if "comment_reactions" in reply_comment:
                    del reply_comment["comment_reactions"]
                comment_nodes.append(Comment(props=reply_comment))
                reply_relations.append(ReplyRel(user_id=reply_comment["commenter_id"],
                                                reply_id=reply_comment["comment_id"],
                                                comment_id=comment["comment_id"]))

            # for reactor in comment_reactors:
            #     user_nodes.append(UserNode(props={
            #         "user_id": reactor["name"],
            #         "user_url": reactor["link"]
            #     }))
            #     react_relations.append(ReactRel(user_id=comment["commenter_id"],
            #                                     comment_id=comment["comment_id"],
            #                                     reaction=reactor["type"]))
        user_nodes.append(UserNode(props=dict(row)))
    return user_nodes, comment_nodes, comment_relations, reply_relations


def get_post_relations(data_frame=None) -> [PostNode]:
    if data_frame is None:
        data_frame = pd.read_excel("data/data.xlsx")
    data = data_frame.copy()
    relations = []
    for _, row in data.iterrows():
        relations.append(PostRel(src_id=row["user_id"], dst_id=row["post_id"], post_time=row["time"]))
    return relations

