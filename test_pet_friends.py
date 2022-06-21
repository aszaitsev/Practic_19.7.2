from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем возможность получения ключа с корректными данными"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print(' Status cod =', status)
    assert 'key' in result
    print(result)


def test_not_get_api_key_with_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем невозможность получения ключа с некорректным email"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    print(' Status cod =', status)


def test_not_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем невозможность получения ключа с некорректным password"""

    # Запрашиваем ключ api
    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    print(' Status cod =', status)


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем возможность получения списка моих питомцев с корректным ключом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) > 0
    print(' Status cod =', status)


def test_not_get_all_pets_with_invalid_key(filter=''):
    """Проверяем невозможность получения списка моих питомцев с некорректным ключом"""

    # Неверный api сохраняем в переменую auth_key
    auth_key = {'key': 'e8b6a5c108c9d82f8ffea6e4d385848ff3188b0fb7bd3a3ba0ab63er'}

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    print(' Status cod =', status)


def test_add_new_pet_with_valid_data(name='Peach', animal_type='dog',
                                     age='3', pet_photo='images/dog.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_not_add_new_pet_with_invalid_key(name='Peach', animal_type='dog',
                                     age='3', pet_photo='images/dog.jpg'):
    """Проверяем невозможность добавить питомца с не верным ключом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Не верный api сохраняем в переменую auth_key
    auth_key = {'key': 'e8b6a5c108c9d82f8ffea6e4d385848ff3188b0fb7bd3a3ba0ab63er'}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    print(' Status cod =', status)


def test_not_add_photo_new_pet_with_invalid_format_photo(name='Peach', animal_type='dog',
                                     age='3', pet_photo='images/dog.png'):
    """Проверяем невозможность добавления фото у нового питомца если формат фото не верный"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] == ''


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Frank", "Собакен", "3", "images/dog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_not_deleted_self_pet_with_invalid_key():
    """Проверяем невозможность удаления питомца с не верным ключом """

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Frank", "Собакен", "3", "images/dog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление, но уже с некорректным ключем
    pet_id = my_pets['pets'][0]['id']
    auth_key = {'key': 'e8b6a5c108c9d82f8ffea6e4d385848ff3188b0fb7bd3a3ba0ab63er'}
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 403
    assert status == 403
    print(' Status cod =', status)


def test_successful_update_self_pet_info(name='Big', animal_type='Boss', age=100):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_not_update_self_pet_info_with_invalid_key(name='Big', animal_type='Boss', age=100):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        auth_key = {'key': 'e8b6a5c108c9d82f8ffea6e4d385848ff3188b0fb7bd3a3ba0ab63er'}
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 403
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

