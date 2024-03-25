from fastapi import Depends, HTTPException, status
from app.users.dependencies import current_user
from app.users.models import User
from app.utils.router import BaseRouter


class BaseRouterWithUser(BaseRouter):

    def _create_routes(self):
        @self.router.get("/", response_model=list[self.model])
        async def get_items(service: self.service, user: User = Depends(current_user)):
            return await service.get_all(user)

        @self.router.get("/{parent_id}", response_model=list[self.model])
        async def get_items_by_parent_id(parent_id: int, service: self.service,  user: User = Depends(current_user)):
            return await service.get_all_by_id(user, parent_id)
        
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
