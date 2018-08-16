from rest_framework import permissions

class IsPublicOrGroupMemberOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.visibility == '0' or obj.owner == request.user:
            return True
        else:
            # TODO better roles mechanism
            groups = obj.groupforum_set
            if groups.count() and request.user in groups.first().members:
                return True
            else:
                return False

class IsPublicOrGroupMemberOrOwner(permissions.BasePermission):
    pass


# TODO
class IsGroupModeratorOrOwner(permissions.BasePermission):
    pass


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'content_item'):
            return obj.content_item.owner == request.user
        return obj.owner == request.user
