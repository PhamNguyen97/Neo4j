

class Relation:
    def __init__(self, src_cls, src_id, dst_cls, dst_id, cls, props):
        self.cls = cls
        self.src_cls = src_cls
        self.src_id = src_id
        self.dst_cls = dst_cls
        self.dst_id = dst_id
        self.props = props

    def __repr__(self):
        return f"({self.src_cls} id:{self.src_id}) -[:{self.cls}]-> ({self.dst_cls} id: {self.dst_id})"

    def dict(self):
        output = self.props
        output["cls"] = self.cls
        output["src_cls"] = self.cls
        output["src_id"] = self.src_id
        output["dst_cls"] = self.dst_cls
        output["dst_id"] = self.dst_id
        return output


class PostRel(Relation):
    def __init__(self, src_id, dst_id, post_time):
        super(PostRel, self).__init__("User", src_id, "Post", dst_id, "Post", {"time": post_time})


class CommentRel:
    def __init__(self, user_id, post_id, comment_id):
        self.user_id = user_id
        self.post_id = post_id
        self.user_comment_cls = "Comment"
        self.comment_post_cls = "On"
        self.comment_id = comment_id

    def dict(self):
        output = {
            "user_id": self.user_id,
            "post_id": self.post_id,
            "user_comment_cls": self.user_comment_cls,
            "comment_post_cls": self.comment_post_cls,
            "comment_id": self.comment_id
        }
        return output


class ReplyRel:
    def __init__(self, user_id, reply_id, comment_id):
        self.user_id = user_id
        self.reply_id = reply_id
        self.user_comment_cls = "Reply"
        self.comment_post_cls = "On"
        self.comment_id = comment_id

    def dict(self):
        output = {
            "user_id": self.user_id,
            "reply_id": self.reply_id,
            "user_comment_cls": self.user_comment_cls,
            "comment_post_cls": self.comment_post_cls,
            "comment_id": self.comment_id
        }
        return output


class ReactRel(Relation):
    def __init__(self, user_id, comment_id, reaction):
        super(ReactRel, self).__init__(src_cls="User", src_id=user_id,
                                       dst_cls="Comment", dst_id=comment_id,
                                       cls="Reacted", props={"relation": reaction})
