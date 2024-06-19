import os
import uuid

from aiogram.filters import Command
import requests
from main import dp, client
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Dispatcher
from aiogram.enums.chat_action import ChatAction
from aiogram.types import Message, Chat, InputFile, FSInputFile
from fsm.states import WaitState
from sources.messages import MESSAGES
from utils.config import API

router = Router()


@router.message(Command('start'))
async def print_answer(message: Message, state: FSMContext):
    chat: Chat = await client.get_chat(message.chat.id)
    if chat.pinned_message:
        if (chat.pinned_message.text.replace(' ', '').replace('\n', '') == MESSAGES['pin_msg']
                .replace(' ', '').replace('\n', '')):
            await message.answer(MESSAGES['start_repeat'])
            return

    pin = await message.answer(MESSAGES['pin_msg'])
    await client.pin_chat_message(chat_id=message.chat.id, message_id=pin.message_id)
    await message.answer(MESSAGES['pin_info'])


@router.message(F.photo)
async def print_answer(message: Message, state: FSMContext):
    photo = message.photo[-1]

    file_info = await client.get_file(photo.file_id)
    file_path = file_info.file_path

    file = await client.download_file(file_path)
    unique_id = uuid.uuid4().hex
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    type_name = os.path.splitext(os.path.basename(file_path))[1]
    path = f'sources/user_data/{base_name}{unique_id}{type_name}'
    with open(path, "wb") as f:
        f.write(file.read())

    files = {'file': open(path, "rb")}
    headers = {'Accept': 'application/json'}
    response = requests.post(API, files=files, headers=headers)
    files['file'].close()

    if response.status_code == 200:
        response_json = response.json()
        image_url = response_json['output']['image']
        results = response_json['output']['results']
        string_results = '· #' + '\n· #'.join(results)
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            base_name = os.path.splitext(os.path.basename(image_url))[0]
            type_name = os.path.splitext(os.path.basename(image_url))[1]
            downloaded_image_path = f'sources/res_imgs/{base_name}{type_name}'
            with open(downloaded_image_path, "wb") as img_file:
                img_file.write(img_response.content)

            await message.answer_photo(
                FSInputFile(path=downloaded_image_path), caption=string_results
            )
        else:
            await message.reply('Ошибка')
    else:
        await message.reply('Ошибка')