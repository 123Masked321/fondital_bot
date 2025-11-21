from os import getenv
from typing import List

import asyncpg
from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_ADDRESS = getenv("DB_ADDRESS")
DB_NAME = getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}"


class Database:
    ALLOWED_TABLES = {
        'boiler_brands',
        'boiler_types',
        'boiler_errors',
        'boiler_models',
        'boiler_instructions',
        'users',
    }

    ALLOWED_COLUMNS = {
        'boiler_brands': {
            'brand_name',
            'description_uk',
            'photo_path',
        },
        'boiler_types': {
            'type_name',
            'description_uk',
            'photo_path',
        },
        'boiler_errors': {
            'brand_id',
            'error_code',
            'description_uk',
            'photo_path',
        },
        'boiler_models': {
            'brand_id',
            'type_id',
            'model_name',
            'description_uk'
            'photo_path',
        },
        'boiler_instructions': {
            'model_id',
            'doc_type',
            'lang',
            'doc_path',
            'access',
        },
        'users': {
            'telegram_id',
            'lang',
            'role',
            'fullname',
            'area',
            'phone',
            'username',
            'city',
            'category',
        },
    }

    def __init__(self):
        self.pool = None
        self.DATABASE_URL = DATABASE_URL

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.DATABASE_URL)

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def user_exists(self, user_id: int) -> bool:
        query = "SELECT EXISTS (SELECT 1 FROM users WHERE telegram_id = $1)"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, user_id)

    async def register_user(self, username: str, chat_id: int, lang: str, role: str, fullname: str,
                            area: str, city: str, category: str, phone: str, processed: bool) -> None:
        query = """INSERT INTO users (username, telegram_id, lang, role, fullname, area, city, category, phone, processed) 
               VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, username, chat_id, lang, role, fullname, area, city, category, phone, processed)

    async def update_user(self, chat_id: int, role: str, fullname: str, area: str, city: str,
                          category: str, phone: str, processed: bool) -> None:
        query = """UPDATE users SET role = $2, fullname = $3, area = $4, city = $5, category = $6, phone = $7, processed = $8
               WHERE telegram_id = $1"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, chat_id, role, fullname, area, city, category, phone, processed)

    async def get_admins(self) -> list[str]:
        query = """SELECT telegram_id FROM users WHERE role = 'admin'"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query)

    async def get_user_data(self, telegram_id: int):
        query = "SELECT role, fullname, area, phone, city, category FROM users WHERE telegram_id = $1"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, telegram_id)

    # async def update_lang_user(self, user_id: int, lang: str):
    #     query = "UPDATE users SET lang = $1 WHERE telegram_id = $2"
    #     async with self.pool.acquire() as conn:
    #         await conn.execute(query, lang, user_id)
    #
    # async def get_lang_user(self, user_id: int):
    #     query = "SELECT lang FROM users WHERE telegram_id = $1"
    #     async with self.pool.acquire() as conn:
    #         return await conn.fetchval(query, user_id)

    async def get_role_user(self, user_id: int):
        query = "SELECT role FROM users WHERE telegram_id = $1"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, user_id)

    async def check_processed_spec(self, user_id: int):
        query = "SELECT processed FROM users WHERE telegram_id = $1"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, user_id)

    async def get_boiler_brands(self):
        query = "SELECT brand_name, id AS brand_id FROM boiler_brands"
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
            return [(row["brand_name"], row["brand_id"]) for row in rows]

    async def get_details_brand(self, brand_id: int):
        query = f"""SELECT bb.description_uk, bb.photo_path
        FROM boiler_brands AS bb
        WHERE bb.id = $1 """
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, brand_id)

    async def get_boiler_types(self):
        query = "SELECT type_name, id AS type_id FROM boiler_types"
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
            return [(row["type_name"], row["type_id"]) for row in rows]

    async def get_details_type(self, type_id: int):
        query = f"""SELECT bt.description_uk, bt.photo_path
        FROM boiler_types AS bt
        WHERE bt.id = $1 """
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, type_id)

    async def get_models(self, brand_id: id, type_id: id):
        query = """SELECT bm.model_name , bm.id AS model_id
        FROM boiler_models AS bm 
        WHERE bm.brand_id = $1 AND bm.type_id = $2"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, brand_id, type_id)
            return [(row["model_name"], row["model_id"]) for row in rows]

    async def get_details_model(self, model_id: int):
        query = f"""SELECT bm.description_uk, bm.photo_path
        FROM boiler_models AS bm
        WHERE bm.id = $1 """
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, model_id)

    async def get_errors(self, brand_id: id) -> list[tuple[str, int]]:
        query = """
            SELECT be.error_code, be.id AS error_id
            FROM boiler_errors AS be
            WHERE be.brand_id = $1
            ORDER BY (regexp_replace(be.error_code, '\\D','','g'))::int
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, brand_id)
            return [(row["error_code"], row["error_id"]) for row in rows]

    async def get_details_error(self, error_id: int):
        query = f"""SELECT be.error_code, be.description_uk, be.photo_path
        FROM boiler_errors AS be
        WHERE be.id = $1"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, error_id)

    async def get_instructions(self, model_id: int):
        query = f"""SELECT bi.doc_type, bi.id AS doc_id
        FROM boiler_instructions AS bi
        WHERE bi.model_id = $1 AND bi.lang = 'uk'"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, model_id)
            return [(row["doc_type"], row["doc_id"]) for row in rows]

    async def get_path_photo_brand(self, brand_id: int):
        query = f"""SELECT photo_path 
        FROM boiler_brands 
        WHERE id = $1"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, brand_id)

    async def get_path_photo_type(self, type_id: int):
        query = f"""SELECT photo_path 
        FROM boiler_types
        WHERE id = $1"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, type_id)

    async def get_path_photo_error(self, error_id: int):
        query = f"""SELECT photo_path 
        FROM boiler_errors
        WHERE id = $1"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, error_id)

    async def get_path_photo_model(self, model_id: int):
        query = f"""SELECT photo_path 
        FROM boiler_models 
        WHERE id = $1"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, model_id)

    async def get_instruction(self, file_id: int):
        query = f"""SELECT doc_path, doc_type, access as role FROM 
        boiler_instructions 
        WHERE id = $1"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, file_id)

    async def count_file(self, path: str):
        query = f"""SELECT SUM(count) as total FROM (
        SELECT COUNT(*) as count 
        FROM boiler_models WHERE photo_path = $1
        UNION ALL
        SELECT COUNT(*) as count 
        FROM boiler_errors WHERE photo_path = $1
        UNION ALL
        SELECT COUNT(*) as count 
        FROM boiler_instructions WHERE doc_path = $1
    ) AS counts"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, path)

    async def get_count_users(self):
        query = """SELECT COUNT(*) FROM users"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query)

    async def get_info_specs(self, area: str, category: str):
        query = "SELECT * FROM users WHERE role = 'spec' AND area = $1 AND category = $2 AND processed = TRUE"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, area, category)

    async def get_spec_form(self):
        query = "SELECT * FROM users WHERE role = 'spec' AND processed = FALSE LIMIT 1"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query)

    async def get_count_forms(self):
        query = "SELECT count(*) FROM users WHERE role = 'spec' AND processed = FALSE"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query)

    async def update_answer_form(self, role: str, processed: bool, user_id: int):
        query = "UPDATE users SET role = $1, processed = $2 WHERE telegram_id = $3"
        async with self.pool.acquire() as conn:
            await conn.execute(query, role, processed, user_id)

    async def create_boiler_brand(self, brand_name: str, description_uk: str, description_ru: str, photo_path: str):
        query = """INSERT INTO boiler_brands (brand_name, description_uk, description_ru, photo_path)
         VALUES ($1, $2, $3, $4)"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, brand_name, description_uk, description_ru, photo_path)

    async def update_boiler_brand(
            self,
            brand_id: int,
            brand_name: str = None,
            description_uk: str = None,
            description_ru: str = None,
            photo_path: str = None):
        query = """UPDATE boiler_brands SET 
                    brand_name = COALESCE($2, brand_name),
                    description_uk = COALESCE($3, description_uk),
                    description_ru = COALESCE($4, description_ru),
                    photo_path = COALESCE($5, photo_path)
                   WHERE id = $1"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, brand_id, brand_name, description_uk, description_ru, photo_path)

    async def delete_boiler_brand(self, brand_id: int):
        query = """DELETE FROM boiler_brands WHERE id = $1"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, brand_id)

    async def create_boiler_type(self, type_name: str, description_uk: str, description_ru: str, photo_path: str):
        query = """INSERT INTO boiler_types (type_name, description_uk, description_ru, photo_path)
         VALUES ($1, $2, $3, $4)"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, type_name, description_uk, description_ru, photo_path)

    async def delete_boiler_type(self, type_id: int):
        query = """DELETE FROM boiler_types WHERE id = $1"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, type_id)

    async def create_boiler_model(self, brand_id: int, type_id: int, model_name: str, description_uk: str,
                                  description_ru: str, photo_path: str):
        query = """INSERT INTO boiler_models (brand_id, type_id, model_name, description_uk, description_ru, photo_path)
         VALUES ($1, $2, $3, $4, $5, $6)"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, brand_id, type_id, model_name, description_uk, description_ru, photo_path)

    async def delete_boiler_model(self, model_id: int):
        query = """DELETE FROM boiler_models WHERE id = $1"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, model_id)

    async def create_boiler_error(
            self,
            brand_id: int,
            error_code: str,
            description_uk: str,
            description_ru: str,
            photo_path: str):
        query = """INSERT INTO boiler_errors (brand_id, error_code, description_uk, description_ru, photo_path)
         VALUES ($1, $2, $3, $4, $5)"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, brand_id, error_code, description_uk, description_ru, photo_path)

    async def delete_boiler_error(self, error_id: int):
        query = """DELETE FROM boiler_errors WHERE id = $1"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, error_id)

    async def create_boiler_instruction(
            self,
            model_id: int,
            doc_type: str,
            lang: str,
            doc_path: str,
            access: str):
        query = """INSERT INTO boiler_instructions (model_id, doc_type, lang, doc_path, access)
         VALUES ($1, $2, $3, $4, $5)"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, model_id, doc_type, lang, doc_path, access)

    async def delete_boiler_instruction(self, instruction_id: int):
        query = """DELETE FROM boiler_instructions WHERE id = $1"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, instruction_id)

    # async def delete_from_table(self, table: str, instruction_id: int):
    #     if table not in self.ALLOWED_TABLES:
    #         raise ValueError(f"Неприпустима таблиця: {table}")
    #
    #     query = f"""UPDATE {table} WHERE id = $1"""
    #     async with self.pool.acquire() as conn:
    #         await conn.execute(query, instruction_id)

    async def update_table(self, table: str, column: str, value: any, record_id: int):
        if table not in self.ALLOWED_TABLES:
            raise ValueError(f"Неприпустима таблиця: {table}")

        if column not in self.ALLOWED_COLUMNS.get(table,set()):
            raise ValueError(f"Неприпустимий стовбець: {column}")

        query = f"""UPDATE {table}
         SET {column} = $1
         WHERE telegram_id = $2"""
        async with self.pool.acquire() as conn:
            await conn.execute(query, value, record_id)