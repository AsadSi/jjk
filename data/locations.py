locations = [
    {
        "id": "tokyo_jujutsu_high",
        "slug": "tokyo-jujutsu-high",
        "name": "Tokyo Jujutsu High",
        "jpName": "東京都立呪術高専",
        "type": "Jujutsu School",
        "region": "Tokyo",
        "image": "/static/images/locations/tokyo-high.jpg",
        "description": "One of the two primary jujutsu schools in Japan. Located in Tokyo, it serves as the main setting for the series. Known for producing elite sorcerers.",
        "notablePeople": ["Satoru Gojo", "Yuji Itadori", "Megumi Fushiguro", "Nobara Kugisaki", "Yuta Okkotsu"],
        "significance": "Central hub for main characters and protagonist training ground"
    },
    {
        "id": "kyoto_jujutsu_high",
        "slug": "kyoto-jujutsu-high",
        "name": "Kyoto Jujutsu High",
        "jpName": "京都府立呪術高専",
        "type": "Jujutsu School",
        "region": "Kyoto",
        "image": "/static/images/locations/kyoto-high.jpg",
        "description": "Sister school to Tokyo Jujutsu High. Located in Kyoto, it trains sorcerers in the Kansai region. Rivals with Tokyo school in friendly competitions.",
        "notablePeople": ["Aoi Todo", "Maki Zenin", "Mai Zenin", "Kasmo"],
        "significance": "Introduces rival characters and hosts the Goodwill Event"
    },
    {
        "id": "shibuya",
        "slug": "shibuya",
        "name": "Shibuya",
        "jpName": "渋谷",
        "type": "Urban District",
        "region": "Tokyo",
        "image": "/static/images/locations/shibuya.jpg",
        "description": "A major commercial and entertainment district in Tokyo. Site of one of the most catastrophic battles in the series where cursed spirits initiated their largest operation.",
        "notablePeople": ["Multiple sorcerers", "Mahito", "Sukuna"],
        "significance": "Major arc location, turning point in the story"
    },
    {
        "id": "shinjuku",
        "slug": "shinjuku",
        "name": "Shinjuku",
        "jpName": "新宿",
        "type": "Urban District",
        "region": "Tokyo",
        "image": "/static/images/locations/shinjuku.jpg",
        "description": "Another major district in Tokyo. Hosts the final showdown between the strongest sorcerer and the King of Curses.",
        "notablePeople": ["Satoru Gojo", "Sukuna", "Yuji Itadori"],
        "significance": "Series climax location"
    },
    {
        "id": "jujutsu_society",
        "slug": "jujutsu-society",
        "name": "Jujutsu Society Headquarters",
        "jpName": "呪術廻戦本部",
        "type": "Administrative Center",
        "region": "Undisclosed",
        "image": "/static/images/locations/headquarters.jpg",
        "description": "The central governing body of the jujutsu world. Oversees all sorcerer activities and maintains the balance between curses and society.",
        "notablePeople": ["Council of Elders", "Satoru Gojo"],
        "significance": "Political center of jujutsu world"
    },
    {
        "id": "tokyo_colony_1",
        "slug": "tokyo-colony-1",
        "name": "Tokyo No. 1 Colony",
        "jpName": "東京第1結界",
        "type": "Culling Game Colony",
        "region": "Tokyo",
        "image": "/static/images/locations/colony-1.jpg",
        "description": "One of the Culling Game colonies where sorcerers battle for points and survival. Features challenging terrain and inhabitants.",
        "notablePeople": ["Culling Game participants"],
        "significance": "Major battlefield in Culling Game arc"
    },
    {
        "id": "hidden_inventory_location",
        "slug": "hidden-inventory",
        "name": "Hidden Inventory Mission Sites",
        "jpName": "隠された履歴",
        "type": "Mission Location",
        "region": "Japan",
        "image": "/static/images/locations/mission-site.jpg",
        "description": "Various locations where Gojo and Geto's past mission took place, protecting Riko Amanai from assassins.",
        "notablePeople": ["Satoru Gojo", "Suguru Geto"],
        "significance": "Backstory and character development location"
    },
    {
        "id": "zenin_estate",
        "slug": "zenin-estate",
        "name": "Zenin Clan Estate",
        "jpName": "禅院家の屋敷",
        "type": "Clan Estate",
        "region": "Rural Japan",
        "image": "/static/images/locations/zenin-estate.jpg",
        "description": "The ancestral home of the powerful Zenin clan, one of the three major jujutsu families. Known for harsh training and strict traditions.",
        "notablePeople": ["Zenin family members", "Maki Zenin", "Megumi Fushiguro"],
        "significance": "Character backstory and clan dynamics"
    },
    {
        "id": "cursed_sites",
        "slug": "cursed-sites",
        "name": "Various Cursed Sites",
        "jpName": "呪いの地点",
        "type": "Cursed Locations",
        "region": "Japan",
        "image": "/static/images/locations/cursed-site.jpg",
        "description": "Throughout Japan there are locations with high cursed spirit activity. Sorcerers are often dispatched to cleanse these areas.",
        "notablePeople": ["All sorcerers"],
        "significance": "Recurring mission locations"
    }
]


def get_all_locations():
    return locations


def get_location(slug):
    for location in locations:
        if location["slug"] == slug:
            return location
    return None
