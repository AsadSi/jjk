arcs = [
    {
        "id": "intro",
        "slug": "intro",
        "name": "Introductory Arc",
        "jpName": "序章",
        "description": "The beginning of Yuji's journey. He swallows Sukuna's finger and joins Tokyo Jujutsu High alongside Megumi and Nobara.",
        "significance": "Everything begins",
        "chapters_start": 0,
        "chapters_end": 25,
    },
    {
        "id": "mahito-arc",
        "slug": "mahito-arc",
        "name": "Mahito Arc",
        "jpName": "真人編",
        "description": "The first major antagonist arc where the students face the special-grade curse Mahito and the tragic death of Junpei.",
        "significance": "First real threat",
        "chapters_start": 26,
        "chapters_end": 63,
    },
    {
        "id": "kyoto-goodwill",
        "slug": "kyoto-goodwill",
        "name": "Kyoto Goodwill Event",
        "jpName": "京都府立呪術高等専門学校",
        "description": "A friendly competition between Tokyo and Kyoto Jujutsu High students. Tensions rise when curse users infiltrate the event.",
        "significance": "Rivalry and growth",
        "chapters_start": 64,
        "chapters_end": 90,
    },
    {
        "id": "shibuya",
        "slug": "shibuya",
        "name": "Shibuya Incident",
        "jpName": "渋谷事変",
        "description": "A catastrophic conflict where Jujutsu High faces Kenjaku's forces in Tokyo's Shibuya district. The turning point of the entire series.",
        "significance": "Everything changes here",
        "chapters_start": 91,
        "chapters_end": 155,
    },
    {
        "id": "hidden-inventory",
        "slug": "hidden-inventory",
        "name": "Hidden Inventory",
        "jpName": "懐玉・玉折",
        "description": "The prequel arc revealing Gojo and Geto's past, their friendship, and the seeds of Geto's fall.",
        "significance": "The tragedy begins",
    },
    {
        "id": "culling-game",
        "slug": "culling-game",
        "name": "Culling Game",
        "jpName": "淘汰戦",
        "description": "A deadly tournament orchestrated by Kenjaku where sorcerers and non-sorcerers are forced to compete for survival.",
        "significance": "Megumi's descent",
        "chapters_start": 156,
        "chapters_end": 220,
    },
    {
        "id": "shinjuku-showdown",
        "slug": "shinjuku-showdown",
        "name": "Shinjuku Showdown",
        "jpName": "新宿決戦",
        "description": "The final confrontation where all factions clash in Tokyo's Shinjuku district. The ultimate duel between Sukuna and Gojo.",
        "significance": "The ending begins",
        "chapters_start": 221,
        "chapters_end": 271,
    },
]


def get_arc(slug):
    return next((arc for arc in arcs if arc["slug"] == slug), None)


def get_all_arcs():
    return arcs
