import graphene

from graphene_django import DjangoObjectType, DjangoListField 
from .models import Post, Comment


class PostType(DjangoObjectType): 
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    all_post = graphene.List(PostType)
    post = graphene.Field(PostType, post_id=graphene.Int())

    def resolve_all_post(self, info, **kwargs):
        return Post.objects.all()

    def resolve_post(self, info, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except:
            return None
    

class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    publish_date = graphene.String()
    author = graphene.String() 


class CreatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        createPost_instance = Post( 
            title=post_data.title,
            description=post_data.description,
            publish_date=post_data.publish_date,
            author=post_data.author
        )
        createPost_instance.save()
        return CreatePost(post=createPost_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        try:
            updatePost_instance = Post.objects.get(pk=post_data.id)
        except:
            raise Exception(f"Post with ID {post_data.id} does not exist.")

        if updatePost_instance:
            updatePost_instance.title = post_data.title
            updatePost_instance.description = post_data.description
            updatePost_instance.publish_date = post_data.publish_date
            updatePost_instance.author = post_data.author
            updatePost_instance.save()

            return UpdatePost(post=updatePost_instance)
        return UpdatePost(post=None)


class CommentInput(graphene.InputObjectType):
    post_id = graphene.ID()
    text = graphene.String()
    author = graphene.String()


class CreateComment(graphene.Mutation):
    class Arguments:
        comment_data = CommentInput(required=True)

    comment = graphene.Field(CommentType)

    @staticmethod
    def mutate(self, info, comment_data=None):
        try:
            post = Post.objects.get(pk=comment_data.post_id)
        except Post.DoesNotExist:
            raise Exception(f"Post with ID {comment_data.post_id} does not exist.")

        comment_instance = Comment( 
            post = post,
            text = comment_data.text,
            author = comment_data.author
        )
        comment_instance.save()
        return CreateComment(comment=comment_instance)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        try:
            comment_instance = Comment.objects.get(pk=id)
            comment_instance.delete()
            return DeleteComment(success=True)
        except:
            return DeleteComment(success=False)
    

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)