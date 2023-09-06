class Post():
    POSTS=[
        {'id':1,'title':'montitre'},
        {'id':2,'title':'mon title'}
    ]

    @classmethod
    def all(cls):
        return cls.POSTS

    @classmethod
    def find(cls, id):
        return cls.POSTS[int(id)-1]

