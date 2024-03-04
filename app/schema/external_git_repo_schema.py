from pydantic import BaseModel


class GitHubCheckerSchema(BaseModel):
    score: int
    is_popular: bool


class ExternalRepoPopularityResponseSchema(BaseModel):
    score: int
    is_popular: bool
