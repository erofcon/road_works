from datetime import datetime

from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import answers as answers_model
from app.schemas import answers as answers_schemas


async def create_answer(answer: answers_schemas.AnswersCreate, creator_id: int) -> int | bool:
    query = answers_model.answers.insert().values(
        description=answer.description,
        create_datetime=datetime.now(),
        task_id=answer.task_id,
        creator_id=creator_id,
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False
