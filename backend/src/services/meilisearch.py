

# Inside a Docker network, use the service name 'meilisearch'
# If running FastAPI locally (outside Docker), use 'localhost'
from meilisearch_python_sdk import AsyncClient
meili_client: AsyncClient | None = None


async def get_meili_client() -> AsyncClient:
    if meili_client is None:
        raise RuntimeError("Meilisearch client not initialized")
    return meili_client
