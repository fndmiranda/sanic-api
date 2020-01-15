from sanic.views import HTTPMethodView
from sanic.response import json
from cerberus import Validator
from user.validations import user as validation
from user.services import UserService
from user.resources import User as UserResource


class UserListView(HTTPMethodView):
    async def get(self, request):
        data = await UserService().paginate()
        return json(UserResource().collection(data))

    async def post(self, request):
        v = Validator(validation())

        if v.validate(request.json):
            data = await UserService().create(request.json)
            return json(UserResource().make(data), 201)
        else:
            return json(v.errors, 400)


class UserDetailView(HTTPMethodView):
    async def get(self, request, user_id):
        data = await UserService().find_or_404(user_id)

        return json(UserResource().make(data))

    async def put(self, request, user_id):
        v = Validator(validation())

        if v.validate(request.json):
            data = await UserService().update_or_404(user_id, request.json)
            return json(UserResource().make(data))
        else:
            return json(v.errors, 400)

    async def delete(self, request, user_id):
        await UserService().delete_or_404(user_id)
        return json({}, 204)
