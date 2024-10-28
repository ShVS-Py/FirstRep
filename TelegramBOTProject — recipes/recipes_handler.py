import random
import aiohttp
import asyncio
import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from translatepy import Translator

router = Router()
translator = Translator()

class RecipeSearch(StatesGroup):
    choosing_category = State()
    showing_recipes = State()

@router.message(Command("category_search_random"))
async def category_search_random(message: Message, state: FSMContext):
    logging.info(f"Текущее состояние: {await state.get_state()}")
    try:
        args = message.text.split(" ")
        num_recipes = int(args[1]) if len(args) > 1 else 3

        await state.set_data({"num_recipes": num_recipes})
        url = "https://www.themealdb.com/api/json/v1/1/list.php?c=list"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        if 'meals' not in data:
            await message.answer("Не удалось получить категории. Попробуй позже.")
            return

        categories = [category['strCategory'] for category in data['meals']]
        logging.info("Полученные категории: %s", categories)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=category, callback_data=f"category_{category}")]
                for category in categories])

        await message.answer("Выбери категорию:", reply_markup=keyboard)
        await state.set_state(RecipeSearch.choosing_category)

    except Exception as e:
        logging.error(f"Ошибка в /category_search_random: {e}")
        await message.answer(f"Произошла ошибка: {e}")

@router.callback_query(lambda callback: callback.data.startswith("category_"))
async def choose_category(callback_query: types.CallbackQuery, state: FSMContext):
    category = callback_query.data.split("_")[1]
    data = await state.get_data()
    num_recipes = data.get("num_recipes", 3)

    logging.info(f"Выбранная категория: {category}")

    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    if 'meals' not in data or data['meals'] is None:
        await callback_query.message.answer("Нет рецептов в данной категории. Попробуй другую.")
        return

    meals = random.choices(data['meals'], k=min(num_recipes, len(data['meals'])))
    recipe_ids = [meal['idMeal'] for meal in meals]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=meal['strMeal'], callback_data=f"recipe_{meal['idMeal']}")]
            for meal in meals])

    await callback_query.message.answer("Случайные рецепты:", reply_markup=keyboard)
    await state.update_data(recipe_ids=recipe_ids)
    await state.set_state(RecipeSearch.showing_recipes)

@router.callback_query(lambda c: c.data.startswith('recipe_'))
async def show_recipe_details(callback_query: types.CallbackQuery, state: FSMContext):
    recipe_id = callback_query.data.split("_")[1]
    async with aiohttp.ClientSession() as session:
        recipe = await fetch_recipe(session, recipe_id)

    if 'meals' in recipe and recipe['meals']:
        recipe_data = recipe['meals'][0]
        instructions = recipe_data['strInstructions']
        ingredients = [
            f"{recipe_data[f'strIngredient{i}']} - {recipe_data[f'strMeasure{i}']}"
            for i in range(1, 21) if recipe_data[f'strIngredient{i}']
        ]

        translated_instructions = translator.translate(instructions, "Russian").result
        translated_ingredients = [translator.translate(ingredient, "Russian").result for ingredient in ingredients]

        recipe_text = f"{recipe_data['strMeal']}\n\nРецепт:\n{translated_instructions}\n\nИнгредиенты:\n" + "\n".join(translated_ingredients)
        await callback_query.message.answer(recipe_text)
    else:
        await callback_query.answer("Не удалось получить данные для этого рецепта.")

async def fetch_recipe(session, recipe_id):
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}"
    logging.info(f"id: {recipe_id}")
    async with session.get(url) as response:
        return await response.json()
