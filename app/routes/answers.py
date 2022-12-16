import os
import shutil
from datetime import datetime

from fastapi import HTTPException, APIRouter, Depends, UploadFile, File, status

from app.crud import users as users_crud
from app.crud import answers as answers_crud
from app.crud import answer_images as answer_images_crud
from app.schemas import users as users_schemas
from app.schemas import answers as answer_schemas
from app.schemas import answer_images as answer_images_schemas

router = APIRouter()


@router.post('/create_answer')
async def create_answer(answer: answer_schemas.AnswersCreate = Depends(), files: list[UploadFile] | None = File(None),
                        current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    answer_id = await answers_crud.create_answer(answer=answer, creator_id=current_user.id)
    if not answer_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if files:
        try:
            file_path = f'static/answer_images/{datetime.now().strftime("%Y-%m-%d")}'
            if not os.path.isdir(file_path):
                os.makedirs(file_path)

            for file in files:
                file_name = f'{file_path}/{file.filename}'
                if file.content_type in ['image/jpeg', 'image/png']:
                    with open(file_name, 'wb') as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    await answer_images_crud.create_answer_images(
                        answer=answer_images_schemas.AnswerImagesCreate(url=file_name, answer_id=answer_id))
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)
