from utils.db_api.db_commands import create_new_user


def check_activation_code(code, user_name, user_tg_id):
    if code == '123':
        await create_new_user(user_name, user_tg_id)