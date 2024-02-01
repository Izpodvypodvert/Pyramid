from fastapi import APIRouter, Depends, HTTPException, status
from typing import Type

from app.utils.exceptions import OpenAPIDocExtraResponse
from app.users.models import User
from app.users.dependencies import current_user


class BaseRouter[T, S, G, V]:
    """
    Generic base router class for creating CRUD API routes.
    The class automatically sets up standard routes for getting all items, getting a single item by ID,
    creating a new item, updating an existing item, and deleting an item.

    Parameters:
    - model (Type[T]): The Pydantic model representing the resource for read operations.
    - model_create (Type[G]): The Pydantic model for creating a new resource.
    - model_update (Type[V]): The Pydantic model for updating an existing resource.
    - service (Type[S]): The service class providing the CRUD operations for the resource.
    - prefix (str): The URL prefix for the routes (e.g., "/items").
    - tags (List[str]): Tags associated with the routes for API documentation.
    """

    def __init__(
        self,
        model: Type[T],
        model_create: Type[G],
        model_update: Type[V],
        service: Type[S],
        prefix: str,
        tags: list[str],
    ):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.model = model
        self.model_create = model_create
        self.model_update = model_update
        self.service = service
        self.responses = {
            401: {"model": OpenAPIDocExtraResponse},
            404: {"model": OpenAPIDocExtraResponse},
        }

        self._create_routes()

    def _create_routes(self):
        @self.router.get("/", response_model=list[self.model])
        async def get_items(service: self.service, user: User = Depends(current_user)):
            return await service.get_all(user)

        @self.router.get("/{item_id}", response_model=self.model)
        async def get_item(
            item_id: int, service: self.service, user: User = Depends(current_user)
        ):
            item = await service.get_by_id(item_id, user)
            return item

        @self.router.post("/", response_model=self.model, responses=self.responses)
        async def create_item(
            item: self.model_create,
            service: self.service,
            user: User = Depends(current_user),
        ):
            new_item = await service.create(item, user)
            return new_item

        @self.router.put("/{item_id}", responses=self.responses)
        async def update_item(
            item_id: int,
            item: self.model_update,
            service: self.service,
            user: User = Depends(current_user),
        ):
            await service.update(item_id, item, user.id, user.is_superuser)
            return {"message": f"Item has been successfully updated"}

        @self.router.delete(
            "/{item_id}",
            responses=self.responses,
            status_code=status.HTTP_204_NO_CONTENT,
        )
        async def delete_item(
            item_id: int, service: self.service, user: User = Depends(current_user)
        ):
            deleted_count = await service.delete(item_id, user.id, user.is_superuser)
            if deleted_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Item not found or unauthorized access",
                )
