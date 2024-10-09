from fastapi import Depends, HTTPException, status
from app.users.dependencies import current_user
from app.users.models import User
from app.utils.router import BaseRouter


class BaseRouterWithUser(BaseRouter):
    """
    A specialized router class that extends BaseRouter with user-dependent CRUD operations.
    It includes user authentication and authorization in all CRUD operations.

    Attributes:
    - model (Type[BaseModel]): The Pydantic model for read operations.
    - model_create (Type[BaseModel]): The Pydantic model for create operations.
    - model_update (Type[BaseModel]): The Pydantic model for update operations.
    - service_dependency (Callable[..., AbstractService]): A callable that provides an instance
      of a service implementing AbstractService.
    - prefix (str): The URL prefix for the router (e.g., "/items").
    - tags (list[str]): Tags for categorizing the routes in API documentation.
    - current_user (User): Dependency that provides the currently authenticated user.
    """

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


class ParentItemRouterWithUser(BaseRouterWithUser):
    """
    A router class that extends BaseRouterWithUser with additional routes for retrieving items
    associated with a specific parent entity, allowing more complex nested structures.

    Methods:
    - get_items_by_parent_id: Retrieves a list of items associated with a given parent ID for the current user.
    """
    def _create_routes(self):
        super()._create_routes()

        @self.router.get("/parent/{parent_id}", response_model=list[self.model])
        async def get_items_by_parent_id(
            parent_id: int, service: self.service, user: User = Depends(current_user)
        ):
            return await service.get_all_by_id(user, parent_id)
