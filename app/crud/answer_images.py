from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import answer_images as answer_images_models
from app.schemas import answer_images as answer_images_schemas


async def create_answer_images(answer: answer_images_schemas.AnswerImagesCreate):
    query = answer_images_models.answer_images.insert().values(
        url=answer.url,
        answer_id=answer.answer_id
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False
