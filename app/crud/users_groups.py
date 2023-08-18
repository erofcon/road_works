from app.models.database import database
from app.models import users_groups as users_groups_model
from app.schemas import users_groups as users_groups_schemas


async def create_related_users_groups(users_groups: users_groups_schemas.UsersGroupsBaseCreate):
    query = users_groups_model.users_groups.insert().values(
        user_id=users_groups.user_id,
        group_id=users_groups.group_id
    )

    try:
        return await database.execute(query=query)
    except Exception:
        return False
