from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import Url


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


class UrlShortener(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, url_in: schemas.UrlCreate) -> Url:
        url_model = Url(**url_in.model_dump())
        url_model.original_url = str(url_model.original_url)
        self.session.add(url_model)
        await self.session.commit()
        await self.session.refresh(url_model)

        return url_model

    async def get(
            self,
            url_id: int
    ) -> Url | None:
        statement = select(Url).where(Url.id == url_id)

        return await self.session.scalar(statement=statement)

    async def get_by_code(
            self,
            url_code: str
    ) -> Url | None:
        statement = select(Url).where(Url.code == url_code)

        return await self.session.scalar(statement=statement)

    async def get_by_url(
            self,
            url: str
    ) -> Url | None:
        statement = select(Url).where(Url.original_url == url)

        return await self.session.scalar(statement=statement)

    async def update(
            self,
            url_id: int,
            url_update_in: schemas.UrlUpdate
    ) -> Url | None:
        url_model = await self.get(url_id=url_id)
        statement = update(Url).where(Url.id == url_id).values(
            **url_update_in.model_dump(exclude_none=True)
        )
        await self.session.execute(statement=statement)
        await self.session.commit()

        return url_model

    async def delete(self, url_id: int) -> int:
        await self.session.execute(delete(Url).where(Url.id == url_id))
        await self.session.commit()

        return url_id
