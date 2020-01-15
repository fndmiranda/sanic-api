import aiotask_context as context


def user():
    request = context.get('request')

    schema = {
        'name': {
            'type': 'string', 'required': True
        },
        'email': {
            'type': 'string', 'required': True
        },
        'password': {
            'type': 'string', 'required': True
        },
    }

    if request.method == 'PUT':
        schema.update({
            'password': {
                'type': 'string', 'required': False
            },
        })

    return schema
