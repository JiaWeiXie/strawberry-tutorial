import datetime
import typing
import strawberry

from graphql import DirectiveLocation

from app import query, mutation


__all__ = ["schema"]


@strawberry.directive(
    locations=[DirectiveLocation.FIELD],
    name="sensitive",
    description="Replace sensitive text with *",
)
def sensitive_text(value: str) -> str:
    ignore_list = [" ", ",", "，", ".", "。", "!", "?", "！", "？"]
    return "".join([i if i in ignore_list else "*" for i in value])


@strawberry.directive(locations=[DirectiveLocation.FIELD])
def replace(value: str, old: str, new: str):
    return value.replace(old, new)


schema = strawberry.Schema(
    query=query.Query,
    mutation=mutation.Mutation,
    directives=[sensitive_text, replace],
)
