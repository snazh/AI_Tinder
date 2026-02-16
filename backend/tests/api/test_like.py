import pytest
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from faker import Faker
from src.database.models.user import User, UserRole
from src.database.models.profile import Profile, Like

fake = Faker()


@pytest.mark.asyncio
async def test_profile_like(client, db_session):
    # --- user1/profile1: liker (ID=1)
    await db_session.execute(
        insert(User)
        .values(email="u1@test.local", sub="dev-u1", role=UserRole.user)
        .on_conflict_do_nothing(index_elements=["id"])  # <-- ВОТ ЭТО
    )

    await db_session.execute(
        insert(Profile)
        .values(user_id=1, username="u1", age=20, description="x", avatar_path="x")
        .on_conflict_do_nothing(index_elements=["user_id"])
    )

    r = await db_session.execute(select(Profile).where(Profile.user_id == 1))
    profile1 = r.scalar_one()

    # --- user2/profile2: liked (ID=2)
    await db_session.execute(
        insert(User)
        .values(email="u2@test.local", sub="dev-u2", role=UserRole.user)
        .on_conflict_do_nothing(index_elements=["sub"])
    )
    r = await db_session.execute(select(User).where(User.sub == "dev-u2"))
    user2 = r.scalar_one()

    await db_session.execute(
        insert(Profile)
        .values(user_id=user2.id, username="u2", age=20, description="x", avatar_path="x")
        .on_conflict_do_nothing(index_elements=["user_id"])

    )
    r = await db_session.execute(select(Profile).where(Profile.user_id == user2.id))
    profile2 = r.scalar_one()

    # IMP: flush not commit
    await db_session.flush()

    # api request
    resp = await client.post(f"/profile/{profile2.id}/like")
    assert resp.status_code in (200, 201), resp.text

    # --- проверяем запись Like ---
    r = await db_session.execute(
        select(Like).where(Like.liker_id == profile1.id, Like.liked_id == profile2.id)
    )
    assert r.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_get_likers(client, db_session):
    users_data = []
    # creating 10 users
    for _ in range(10):
        users_data.append({
            "email": fake.unique.email(),
            "sub": fake.unique.uuid4(),
            "role": UserRole.user,
        })
    stmt_user = insert(User).values(users_data).on_conflict_do_nothing(index_elements=["sub"])
    await db_session.execute(stmt_user)
    await db_session.flush()

    # fetching user_ids
    result = await db_session.execute(select(User.id).limit(100))
    user_ids = result.scalars().all()
    # creating 10 profiles
    profiles_data = []
    for user_id in user_ids:
        profiles_data.append({
            "user_id": user_id,
            "username": fake.user_name(),
            "age": fake.random_int(min=18, max=50),
            "description": fake.text(max_nb_chars=200),
            "avatar_path": fake.image_url(),
        })

    if profiles_data:
        stmt_profile = insert(Profile).values(profiles_data).on_conflict_do_nothing(index_elements=["user_id"])
        await db_session.execute(stmt_profile)
        await db_session.flush()

    result = await db_session.execute(select(Profile.id).limit(100))
    profile_ids = result.scalars().all()
    like_data = []
    liked_profile_id = profile_ids[0]
    profile_ids = profile_ids[1:]
    for profile_id in profile_ids:
        like_data.append({
            "liker_id": profile_id,
            "liked_id": liked_profile_id
        })
    if like_data:
        stmt_like = insert(Like).values(like_data)
        await db_session.execute(stmt_like)
        await db_session.flush()

    # api request
    resp = await client.get(f"/profile/{liked_profile_id}/likers")
    assert resp.status_code in (200, 201), resp.text

    result = await db_session.execute(select(Like.liker_id).where(Like.liked_id == liked_profile_id))
    saved_profile_ids = result.scalars().all()
    print(saved_profile_ids)

    assert saved_profile_ids == profile_ids
