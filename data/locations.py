locations = [
    {
        "id": "tokyo-high",
        "slug": "tokyo-high",
        "name": "Tokyo Jujutsu High",
        "jpName": "東京呪術高専",
        "description": "The primary school where the main characters train. Home to Gojo and where Yuji, Megumi, and Nobara attend as first-year students.",
        "affiliation": "Jujutsu Society",
        "notableMembers": ["Gojo Satoru", "Yuji Itadori", "Megumi Fushiguro", "Nobara Kugisaki", "Nanami Kento"],
    },
    {
        "id": "kyoto-high",
        "slug": "kyoto-high",
        "name": "Kyoto Jujutsu High",
        "jpName": "京都呪術高専",
        "description": "A rival jujutsu school. Home to sorcerers like Aoi Todo and Maki Zenin.",
        "affiliation": "Jujutsu Society",
        "notableMembers": ["Aoi Todo", "Maki Zenin", "Kasumi Miwa"],
    },
    {
        "id": "shibuya",
        "slug": "shibuya",
        "name": "Shibuya District",
        "jpName": "渋谷",
        "description": "A major Tokyo district that becomes the stage for a catastrophic jujutsu incident. The turning point of the entire series.",
        "affiliation": "Tokyo, Japan",
        "significance": "Major battle location",
    },
    {
        "id": "shinjuku",
        "slug": "shinjuku",
        "name": "Shinjuku District",
        "jpName": "新宿",
        "description": "Another major Tokyo district where the final confrontation between the strongest forces takes place.",
        "affiliation": "Tokyo, Japan",
        "significance": "Final battle location",
    },
    {
        "id": "jujutsu-hq",
        "slug": "jujutsu-hq",
        "name": "Jujutsu Headquarters",
        "jpName": "呪術廻戦本部",
        "description": "The central headquarters of the Jujutsu Society that oversees all sorcerer operations.",
        "affiliation": "Jujutsu Society",
        "notableMembers": ["Gojo Satoru (formerly)", "Leadership Council"],
    },
    {
        "id": "culling-game-arena",
        "slug": "culling-game-arena",
        "name": "Culling Game Arena",
        "jpName": "淘汰戦アリーナ",
        "description": "Multiple locations across Japan transformed into arenas for the deadly Culling Game tournament.",
        "affiliation": "Kenjaku's Territory",
        "significance": "Multi-location tournament",
    },
]


def get_location(slug):
    return next((location for location in locations if location["slug"] == slug), None)


def get_all_locations():
    return locations
