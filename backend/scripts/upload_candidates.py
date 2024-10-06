import datetime as dt
import typing as tp
import random
from dataclasses import dataclass
from tqdm import tqdm
import json
import asyncpg
import asyncio
import os


filename = "./backend/data/vacancy.json"
with open(filename, "r", encoding="utf-8") as file:
    data = json.load(file)


def get_direction():
    # 14139 - разработка,
    # 14142 - аналитика,
    # 14151 - бэк офис,
    # 14172 - дизайн,
    # 14160 - информационная безопасность
    # 14148 - Инфраструктура
    # 14163 - производство и сервисное обслуживание
    # 14166 - развитие бизнеса и консалтинг
    # 14145 - тестирование
    # 14169 - управление продуктами
    # 14154 - управление проектами

    return random.choice(
        [
            "разработка",
            "аналитика",
            "бэк офис",
            "дизайн",
            "информационная безопасность",
            "инфраструктура",
            "производство и сервисное обслуживание",
            "развитие бизнеса и консалтинг",
            "тестирование",
            "управление продуктами",
        ]
    )


vacancy_titles = {
    "разработка": [
        "Python разработчик",
        "Java разработчик",
        "Go разработчик",
        "Frontend разработчик",
    ],
    "аналитика": [
        "Бизнес-аналитик",
        "Системный аналитик",
        "Data Analyst",
        "Product Analyst",
    ],
    "бэк офис": [
        "Офис-менеджер",
        "Администратор офиса",
        "Секретарь",
        "Координатор офиса",
    ],
    "дизайн": [
        "UI/UX дизайнер",
        "Графический дизайнер",
        "Веб-дизайнер",
        "Моушн-дизайнер",
    ],
    "информационная безопасность": [
        "Специалист по ИБ",
        "Аналитик ИБ",
        "Инженер по ИБ",
        "Консультант по ИБ",
    ],
    "инфраструктура": [
        "Системный администратор",
        "DevOps инженер",
        "Сетевой инженер",
        "Инженер по инфраструктуре",
    ],
    "производство и сервисное обслуживание": [
        "Инженер по обслуживанию",
        "Техник по ремонту",
        "Сервисный инженер",
        "Производственный инженер",
    ],
    "развитие бизнеса и консалтинг": [
        "Бизнес-консультант",
        "Консультант по развитию бизнеса",
        "Менеджер по развитию бизнеса",
        "Консультант по консалтингу",
    ],
    "тестирование": [
        "Тестировщик ПО",
        "QA инженер",
        "Автоматизатор тестирования",
        "Специалист по тестированию",
    ],
    "управление продуктами": [
        "Продуктовый менеджер",
        "Менеджер по продукту",
        "Product Owner",
        "Product Lead",
    ],
}


def get_url():
    return random.choice(["hh.ru", "avito.ru", "habr.ru"])


def get_area(direction: str) -> str:
    return random.choice(vacancy_titles[direction])


def get_city():
    return random.choice(["москва", "нижний новгород", "минск", "санкт-петербург"])


@dataclass
class Candidate:
    first_name: str
    last_name: str
    dob: dt.date
    city: str
    country: str
    spezialization: str
    education: list[dict]
    candidate_skills: list[id:int]
    description: str
    experience: list[dict]
    cv_url: str
    raw_json: dict
    src: str


def get_unique_key_skills(data) -> set:
    skills = set()
    for vacancy in data:
        for resume in vacancy["failed_resumes"]:
            try:
                skills.update(resume["key_skills"].split(", "))
            except Exception as e:
                pass
    return skills


def candidate_from_dict(data: dict) -> Candidate:
    first_name = data["first_name"]
    last_name = data["last_name"]
    try:
        experience = data["experienceItem"]
    except:
        experience = {}
    try:
        education = (data["educationItem"],)
    except:
        education = {}
    try:
        dob = dt.datetime.strptime(data["birth_date"], "%Y-%m-%d")
    except:
        dob = dt.datetime.strptime(
            f"{random.randint(1970,2000)}-{random.randint(1,12)}-{random.randint(1,25)}",
            "%Y-%m-%d",
        )
    description = ""
    if data["about"] != None:
        description = data["about"]

    return Candidate(
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        country=data["country"],
        spezialization=get_direction(),
        city=data["city"],
        education=education,
        candidate_skills=random.sample(range(1, 1500), random.randint(3, 6)),
        description=description,
        experience=experience,
        cv_url="https://drive.google.com",
        raw_json=data,
        src=get_url(),
    )


def get_candidates(data) -> list:
    candidates = []
    for vacancy in data:
        for candidate in vacancy["failed_resumes"]:
            candidates.append(candidate_from_dict(candidate))
        for candidate in vacancy["confirmed_resumes"]:
            candidates.append(candidate_from_dict(candidate))
    return candidates


async def upload_skills_to_postgres(skills: set, db_url: str):
    conn = await asyncpg.connect(dsn=db_url)
    try:
        for skill in tqdm(skills):
            try:
                await conn.execute(
                    """
                INSERT INTO skills(name) VALUES($1)
                """,
                    skill,
                )
            except:
                pass
    finally:
        await conn.close()


async def get_skill_ids(db_url):
    conn = await asyncpg.connect(dsn=db_url)
    skills_ids = []
    try:

        rows = await conn.fetch(
            """
        SELECT id from skills;
        """,
        )
        skills_ids = [int(dict(row)["id"]) for row in rows]

    finally:
        await conn.close()
    return skills_ids


async def upload_candidates_to_postgres(candidates: list[Candidate], db_url: str):
    avaliable_skills = set(await get_skill_ids(db_url))
    conn = await asyncpg.connect(dsn=db_url)

    try:
        for candidate in tqdm(candidates):
            try:
                candidate_id = await conn.fetch(
                    """
                        INSERT INTO candidates(
                            first_name, last_name, dob, city, country,spezialization, education, description, experience, cv_url, raw_json, src
                        ) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12) returning id;
                        """,
                    candidate.first_name,
                    candidate.last_name,
                    candidate.dob,
                    candidate.city,
                    candidate.country,
                    candidate.spezialization,
                    json.dumps(candidate.education),
                    candidate.description,
                    json.dumps(candidate.experience),
                    candidate.cv_url,
                    json.dumps(candidate.raw_json),
                    candidate.src,
                )
                for skill in candidate.candidate_skills:
                    if not skill in avaliable_skills:
                        continue
                    await conn.execute(
                        """
                            INSERT INTO candidate_skills(candidate_id, skill_id) VALUES($1, $2)
                            """,
                        int(candidate_id[0]["id"]),
                        int(skill),
                    )
            except:
                pass
    finally:
        await conn.close()


# Example usage
async def main():
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    db_url = "postgresql://postgre:postgre-pass@46.138.243.191:55446/dev"
    skills = get_unique_key_skills(data)
    candidates = get_candidates(data)
    await upload_skills_to_postgres(skills, db_url)
    await upload_candidates_to_postgres(candidates, db_url)


asyncio.run(main())
