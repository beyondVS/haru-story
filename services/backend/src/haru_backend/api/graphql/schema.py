import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def service_status(self) -> str:
        return "ok"


schema = strawberry.Schema(query=Query)
