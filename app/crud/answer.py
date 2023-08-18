from datetime import datetime

from asyncpg.exceptions import DataError

from app.models import user as users_model
from app.models.database import database
from app.models import answer as answers_model
from app.models import answer_images as answer_images_model
from app.schemas import answer as answers_schemas
from app.schemas import user as users_schemas


async def create_answer(answer: answers_schemas.AnswerCreate, creator_id: int) -> int | bool:
    query = answers_model.answer.insert().values(
        description=answer.description,
        create_datetime=datetime.now(),
        task_id=answer.task_id,
        creator_id=creator_id,
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False


async def get_answers(task_id: int):
    answer_query = answers_model.answer.select().where(answers_model.answer.c.task_id == task_id)
    answers = await database.fetch_all(query=answer_query)

    return_answer = []

    for answer in answers:
        one_answer = answers_schemas.AnswerQuery(**answer)

        answer_creator_query = users_model.user.select().where(users_model.user.c.id == answer.creator_id)
        answer_creator = await database.fetch_one(query=answer_creator_query)

        answer_images_query = answer_images_model.answer_images.select(
            answer_images_model.answer_images.c.answer_id == answer.id)
        answer_images = await database.fetch_all(query=answer_images_query)

        one_answer.creator = users_schemas.UserBase(**answer_creator)
        one_answer.answer_images = answer_images

        return_answer.append(one_answer)

    return return_answer


async def get_one_answer(answer_id: int) -> answers_schemas.AnswerQuery:
    answer_query = answers_model.answer.select().where(answers_model.answer.c.id == answer_id)
    answer = await database.fetch_one(query=answer_query)

    one_answer = answers_schemas.AnswerQuery(**answer)

    answer_creator_query = users_model.user.select().where(users_model.user.c.id == answer.creator_id)
    answer_creator = await database.fetch_one(query=answer_creator_query)

    answer_images_query = answer_images_model.answer_images.select(
        answer_images_model.answer_images.c.answer_id == answer.id)
    answer_images = await database.fetch_all(query=answer_images_query)

    one_answer.creator = users_schemas.UserBase(**answer_creator)
    one_answer.answer_images = answer_images

    return one_answer
