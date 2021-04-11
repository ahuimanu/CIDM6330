from barkylib.services import unit_of_work


def bookmarks_view(title: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            """
            SELECT title, url FROM bookmars WHERE title = :title
            """,
            dict(title=title),
        )
    return [dict(r) for r in results]