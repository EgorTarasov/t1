import json
import re
import typing as tp

import httpx

T1_EMPLOYER_ID = 4649269
DUCK_DUCK_GO_URL = "https://duckduckgo.com/duckchat/v1/chat"


class HHApi:
    def __init__(
        self,
        api_key: str = "",
        base_url: str = "https://api.hh.ru",
        client: httpx.Client = httpx.Client(),
    ):
        self.__base_url = base_url
        self.__available_directions: set[int] = set(
            [
                14139,
                14142,
                14151,
                14172,
                14160,
                14148,
                14163,
                14166,
                14145,
                14169,
                14154,
            ]
        )
        self.__api_key = api_key
        self.__client: httpx.Client = client
        if api_key:
            self.__client.headers = {"Authorization": f"Bearer {self.__api_key}"}

    @classmethod
    def __map_direction_to_role(self, direction: int) -> list[int]:
        """Сопоставление данных из  query param страницы t1 для hh api"""
        match direction:
            case 14139:
                return [14, 36, 79, 96, 104, 125, 165]
            case 14142:
                return [10, 11, 79, 126, 148, 150, 155, 156, 157, 163, 164]
            case 14151:
                return [
                    1,
                    2,
                    3,
                    6,
                    7,
                    8,
                    9,
                    13,
                    15,
                    16,
                    17,
                    18,
                    19,
                    21,
                    22,
                    23,
                    24,
                    29,
                    31,
                    32,
                    33,
                    35,
                    37,
                    38,
                    39,
                    41,
                    42,
                    43,
                    45,
                    46,
                    50,
                    51,
                    52,
                    55,
                    56,
                    57,
                    58,
                    60,
                    61,
                    64,
                    65,
                    66,
                    67,
                    68,
                    69,
                    70,
                    71,
                    72,
                    74,
                    76,
                    77,
                    81,
                    83,
                    87,
                    88,
                    89,
                    90,
                    91,
                    92,
                    93,
                    94,
                    95,
                    97,
                    98,
                    99,
                    101,
                    102,
                    103,
                    105,
                    106,
                    110,
                    117,
                    118,
                    119,
                    120,
                    122,
                    123,
                    127,
                    129,
                    130,
                    131,
                    132,
                    133,
                    134,
                    135,
                    136,
                    137,
                    138,
                    139,
                    140,
                    142,
                    145,
                    146,
                    147,
                    153,
                    158,
                    159,
                    163,
                    166,
                    167,
                    170,
                    171,
                    172,
                ]
            case 14172:
                return [
                    1,
                    2,
                    3,
                    6,
                    7,
                    8,
                    9,
                    13,
                    15,
                    16,
                    17,
                    18,
                    19,
                    21,
                    22,
                    23,
                    24,
                    29,
                    31,
                    32,
                    33,
                    35,
                    37,
                    38,
                    39,
                    41,
                    42,
                    43,
                    45,
                    46,
                    50,
                    51,
                    52,
                    55,
                    56,
                    57,
                    58,
                    60,
                    61,
                    64,
                    65,
                    66,
                    67,
                    68,
                    69,
                    70,
                    71,
                    72,
                    74,
                    76,
                    77,
                    81,
                    83,
                    87,
                    88,
                    89,
                    90,
                    91,
                    92,
                    93,
                    94,
                    95,
                    97,
                    98,
                    99,
                    101,
                    102,
                    103,
                    105,
                    106,
                    110,
                    117,
                    118,
                    119,
                    120,
                    122,
                    123,
                    127,
                    129,
                    130,
                    131,
                    132,
                    133,
                    134,
                    135,
                    136,
                    137,
                    138,
                    139,
                    140,
                    142,
                    145,
                    146,
                    147,
                    153,
                    158,
                    159,
                    163,
                    166,
                    167,
                    170,
                    171,
                    172,
                ]
            case 14160:
                return [12, 20, 25, 34]
            case 14148:
                return [111, 112, 113, 114, 121, 160]
            case 14163:
                return [
                    4,
                    5,
                    21,
                    27,
                    28,
                    30,
                    31,
                    39,
                    44,
                    46,
                    47,
                    48,
                    49,
                    52,
                    58,
                    59,
                    62,
                    63,
                    67,
                    78,
                    79,
                    80,
                    81,
                    82,
                    84,
                    85,
                    86,
                    100,
                    102,
                    108,
                    109,
                    111,
                    115,
                    128,
                    131,
                    141,
                    143,
                    144,
                    149,
                    151,
                    152,
                    162,
                    168,
                    169,
                    172,
                    173,
                    174,
                ]
            case 14166:
                return [
                    9,
                    11,
                    18,
                    26,
                    35,
                    50,
                    53,
                    54,
                    57,
                    70,
                    71,
                    75,
                    77,
                    91,
                    97,
                    99,
                    105,
                    106,
                    119,
                    122,
                    123,
                    127,
                    129,
                    134,
                    135,
                    136,
                    137,
                    142,
                    154,
                    161,
                    164,
                ]
            case 14145:
                return [48, 12]
            case 14169:
                return [26, 36, 73, 125]
            case 14154:
                return [8, 26, 36, 107, 108, 125]
        return []

    @classmethod
    def vacancies(
        self, direction: int, employer_id: int = T1_EMPLOYER_ID, per_page: int = 1
    ) -> dict[str, tp.Any]:
        """

        Args:
            direction (int):
                14139 - разработка,
                14142 - аналитика,
                14151 - бэк офис,
                14172 - дизайн,
                14160 - информационная безопасность
                14148 - Инфраструктура
                14163 - производство и сервисное обслуживание
                14166 - развитие бизнеса и консалтинг
                14145 - тестирование
                14169 - управление продуктами
                14154 - управление проектами
            employer_id (int, optional):  Defaults to T1_EMPLOYER_ID.
            per_page (int, optional):  Defaults to 0.
        """
        if direction not in self.__available_directions:
            # TODO: custom exception
            raise ValueError(
                f"Invalid direction choose one from: {self.__available_directions}"
            )

        resp = self.__client.get(
            self.__base_url + "/vacancies",
            params={
                "employer_id": 4649269,
                "professional_role": self.__map_direction_to_role(direction),
                "clusters": True,
                "search_field": "name",
                "describe_arguments": True,
            },
        )
        if resp.status_code != 200:
            # TODO: custom exception
            print(resp.status_code)

        return resp.json()


class LLM:
    def __init__(self, llm_chat_url: str):
        self.url = llm_chat_url
        self.client = httpx.Client(
            headers={
                "accept": "text/event-stream",
                "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
                "content-type": "application/json",
                "cookie": "dcm=5",
                "dnt": "1",
                "origin": "https://duckduckgo.com",
                "priority": "u=1, i",
                "referer": "https://duckduckgo.com/",
                "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "x-vqd-4": "4-189727535158365797383025471132521611675",
            }
        )

    @classmethod
    def _assemble_body(
        self,
        prompt: str,
        model: tp.Literal[
            "claude-3-haiku-20240307",
            "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "gpt-4o-mini",
        ] = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    ):
        return {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }

    @classmethod
    def __parse_chunk(self, chunk: str) -> str:
        if len(chunk) == 0:
            return ""
        payload = chunk[5:]
        try:
            return json.loads(payload)["message"]
        except Exception as e:
            print(e, chunk)
            return ""

    @classmethod
    def _email_prompt(self, vacancy_description: str) -> str:
        return f"Помоги написать письмо для рассылки с новой вакансией для компании в формате html, вот описание вакансии: {vacancy_description}"

    @classmethod
    def __parse_html_response(self, response: str) -> str:
        match = re.search(r"```(.*?)```", response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    @classmethod
    def _telegram_prompt(self, vacancy_description: str) -> str:
        return f"Помоги написать пост для рекламы вакансии в соц сети с использованием markdown, вот описание вакансии: {vacancy_description}"

    @classmethod
    def prompt(
        self, post_type: tp.Literal["telegram", "email"], vacancy_description: str
    ) -> str:
        match post_type:
            case "telegram":
                prompt = self._telegram_prompt(vacancy_description)
            case "email":
                prompt = self._email_prompt(vacancy_description)

        response = ""
        with self.client.stream(
            "POST", self.url, json=self._assemble_body(prompt), timeout=120
        ) as r:
            for chunk in r.iter_lines():
                new_data = self.__parse_chunk(chunk)
                response += new_data
        match post_type:
            case "telegram":
                response = response
            case "email":
                response = self.__parse_html_response(response)

        return response
