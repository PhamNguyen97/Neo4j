import pandas as pd


class Node:
    def __init__(self, cls, props):
        self.cls = cls
        self.props = props
        self.preprocess_props()
        self.id = 0

    def to_insert_query_string(self):
        pass

    def preprocess_props(self):
        for key, value in list(self.props.items()):
            if isinstance(value, str):
                value = value.replace("'", "`").replace('"', "``")
                self.props[key] = value
            else:
                if isinstance(value, list):
                    print(value)
                if pd.isna(value):
                    del self.props[key]

    def __repr__(self):
        return f"{self.cls} | {self.props}"

    def dict(self):
        output = self.props
        output["cls"] = self.cls
        output["id"] = str(self.id)
        return output


class PostNode(Node):
    def __init__(self, props):
        super(PostNode, self).__init__("Post", props)
        self.id = str(props["post_id"])
        self.post_id = props["post_id"]
        self.post_time = props["time"]

    @property
    def post_rel(self):
        return {
            "post_time": self.post_time
        }

    def dict(self):
        output = self.props
        output["cls"] = self.cls
        output["id"] = str(self.id)
        output["post_id"] = self.post_id
        output["post_time"] = self.post_time
        return output


class Comment(Node):
    def __init__(self, props):
        super(Comment, self).__init__("Comment", props)
        self.id = props["comment_id"]
        self.comment_time = props.get("comment_time")

    def dict(self):
        output = self.props
        output["cls"] = self.cls
        output["id"] = str(self.id)
        output["comment_time"] = self.comment_time
        return output


class UserNode(Node):
    def __init__(self, props):
        super(UserNode, self).__init__("User", props)
        self.id = props["user_id"]

    def dict(self):
        output = self.props
        output["cls"] = self.cls
        output["id"] = str(self.id)
        return output
