import pandas as pd
import json
import re

DATA_PATH = "data/data.xlsx"
datetime_re = re.compile(r": datetime.datetime\((.*?)\)")


def preprocess(comment):
    comment = comment.replace('" FHD', "`` FHD").replace("'", '"').replace('" ', "' ").replace(": None", ": null")
    datetime_strings = datetime_re.findall(comment)
    for datetime_string in datetime_strings:
        comment = comment.replace(f": datetime.datetime({datetime_string})",
                                  f': "datetime.datetime({datetime_string})"')
    try:
        comment = json.loads(comment)
    except:
        return []
    return comment


def get_user_data(comment):
    return comment.get("commenter_id"), comment.get("commenter_name"), comment.get("commenter_url")


data = pd.read_excel(DATA_PATH)
user_data_old = data[["user_id","username","user_url"]]

comment_full = list(data["comments_full"])
comment_full = [preprocess(comment) for comment in comment_full]
comment_users = []
for comments in comment_full:
    for comment in comments:
        user_data = get_user_data(comment)
        comment_users.append(user_data)
        for reply in comment["replies"]:
            user_data = get_user_data(reply)
            comment_users.append(user_data)

comment_users = pd.DataFrame(comment_users, columns=["user_id", "username", "user_url"])
user_data = pd.concat([user_data_old, comment_users], axis=0)

user_data.to_csv("user_data.text.csv")



