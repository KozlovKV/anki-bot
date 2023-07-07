def empty_protected_read(model, instance_id):
    instance = model.get_or_none(id=instance_id)
    if not instance:
        raise IndexError
    return instance


def user_protected_read(model, user_id, instance_id):
    instance = empty_protected_read(model, instance_id)
    if int(instance.user_id) != user_id:
        raise PermissionError
    return instance
