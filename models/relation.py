from models.node import UserNode, PostNode


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


class PostRel(Relation):
    def __init__(self, src_id, dst_id, post_time):
        super(PostRel, self).__init__("User", src_id, "Post", dst_id, "Post", {"post_time": post_time})


class CommentId(Relation):
    pass
