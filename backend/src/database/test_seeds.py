import asyncio
import random

from faker import Faker
from meilisearch_python_sdk import AsyncClient
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from src.database.db import async_session_maker
from src.database.models.user import User, UserRole
from src.database.models.profile import Profile, Like
from src.config import settings

fake = Faker()


async def create_user_profile():
    async with async_session_maker() as session:
        users_data = []
        for _ in range(100):
            users_data.append({
                "email": fake.unique.email(),
                "sub": fake.unique.uuid4(),
                "role": UserRole.user,  # передаем объект роли, если это Enum
                "created_at": fake.date_time_this_year(),
                "updated_at": fake.date_time_this_year(),
            })

        stmt_user = insert(User).values(users_data)
        stmt_user = stmt_user.on_conflict_do_nothing(index_elements=["sub"])

        await session.execute(stmt_user)
        await session.commit()

        result = await session.execute(select(User.id).limit(100))
        user_ids = result.scalars().all()

        profiles_data = []
        for user_id in user_ids:
            profiles_data.append({
                "user_id": user_id,
                "username": fake.user_name(),
                "age": fake.random_int(min=18, max=50),
                "description": fake.text(max_nb_chars=200),
                "avatar_path": fake.image_url(),
                "created_at": fake.date_time_this_year(),
                "updated_at": fake.date_time_this_year(),
            })

        if profiles_data:
            stmt_profile = insert(Profile).values(profiles_data)
            stmt_profile = stmt_profile.on_conflict_do_nothing(index_elements=["user_id"])
            await session.execute(stmt_profile)
            await session.commit()

        print(f"Successfully processed {len(profiles_data)} users and profiles")

async def create_likes(max_likes_per_profile: int = 10):
    """
    Generate random likes for all profiles.
    """
    async with async_session_maker() as session:
        # Get all profile IDs
        result = await session.execute(select(Profile.id))
        profile_ids = result.scalars().all()
        print(f"Total profiles: {len(profile_ids)}")

        likes_data = []
        for liker_id in profile_ids:
            # Random number of likes per profile
            num_likes = random.randint(1, max_likes_per_profile)
            # Choose unique liked profiles excluding self
            possible_likes = list(set(profile_ids) - {liker_id})
            liked_ids = random.sample(possible_likes, min(num_likes, len(possible_likes)))

            for liked_id in liked_ids:
                likes_data.append({
                    "liker_id": liker_id,
                    "liked_id": liked_id,
                })

        if likes_data:
            stmt = insert(Like).values(likes_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=["liker_id", "liked_id"]
            )
            await session.execute(stmt)
            await session.commit()
            print(f"✅ Inserted {len(likes_data)} likes")
        else:
            print("No likes generated.")
async def clear_meili():
    meili = AsyncClient(
        settings.meilisearch.MEILI_URL,
        settings.meilisearch.MEILI_MASTER_KEY,
    )
    index = meili.index("profiles")
    await index.delete_all_documents()
    print("Profile cleared from meili")

async def add_to_meili():
    meili = AsyncClient(
        settings.meilisearch.MEILI_URL,
        settings.meilisearch.MEILI_MASTER_KEY,
    )
    async with async_session_maker() as session:
        result = await session.execute(select(Profile))
        profiles = result.scalars().all()
        print("Profiles in DB:", len(profiles))

    # Формируем документы для Meilisearch
    documents = [
        {
            "id": profile.id,
            "user_id": profile.user_id,
            "username": profile.username,
            "description": profile.description,
            "avatar_path": profile.avatar_path,
        }
        for profile in profiles
    ]

    if documents:
        await meili.index("profiles").delete()
        await meili.create_index(uid="profiles", primary_key="id")
        index = meili.index("profiles")
        # Add documents
        task_info = await index.add_documents(documents)
        print(f"Task enqueued: {task_info.task_uid}")

        print("Waiting for indexing to finish...")
        # Wait for the task
        task = await meili.wait_for_task(task_info.task_uid)

        # --- DEBUGGING BLOCK ---
        if task.status == 'failed':
            print(f"❌ ERROR: {task.error['message']}")
            print(f"Error Code: {task.error['code']}")
        else:
            print(f"✅ Success! Status: {task.status}")
        # -----------------------

        # Fetch documents
        result = await index.get_documents(limit=100)
        print(f"Total found in Meili: {result.total}")
        print(result.results)
    else:
        print("Нет документов для добавления.")

    await meili.aclose()

if __name__ == "__main__":
    async def main():

        await create_user_profile(),
        await create_likes()


    asyncio.run(main())
