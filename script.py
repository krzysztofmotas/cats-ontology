import json
import random
from datetime import datetime, timedelta

CAT_NAMES = ["Mruczek", "Adelka", "Urwis", "Elton", "Ozi", "Kajtula", "Klakier", "Zuzia", "Fruto", "Rudy", "Gacek", "Kropka", "Mania", "Zgredek", "Bonifacy"]
FOODS = ["Salmon", "Chicken", "Turkey", "Beef", "Tuna", "Shrimp", "Sardines"]
SLEEP_PLACES = ["Box", "Windowsill", "Hammock", "Sink", "Wardrobe"]
TOYS = ["Feather", "Mouse", "Ball", "Laser"]
ACTIONS = ["climbing-the-wardrobe", "hunting-shadows", "sleeping-in-the-sink"]
ACCESSORIES = ["Sweater", "Blanket", "Collar", "Bandana"]
DISLIKES = ["Vacuum-Cleaner", "Water", "Doorbell", "Rustle", "Dust"]

def get_article(word):
    return "an" if word[0].lower() in "aeiou" else "a"

def normalize_str(name):
    if name == "Iran (Persia)":
        return "Iran"

    parts = name.strip().replace("-", " ").split()
    return "-".join(part.capitalize() for part in parts)

def get_friendliness_level(value):
    if value >= 5:
        return "very-dog-friendly"
    elif value >= 4:
        return "dog-friendly"
    elif value >= 2:
        return "not very-dog-friendly"
    else:
        return "not dog-friendly"

def get_intelligence_level(value):
    if value >= 5:
        return "very-intelligent"
    elif value >= 4:
        return "intelligent"
    elif value >= 2:
        return "not very-intelligent"
    else:
        return "not intelligent"

def get_energy_level(value):
    if value >= 5:
        return "very-energetic"
    elif value >= 4:
        return "energetic"
    elif value >= 2:
        return "not very-energetic"
    else:
        return "not energetic"

def generate_random_date(start_year=2010, end_year=2025):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_random_individuals(breeds, count=10):
    individuals = []
    
    for _ in range(count):
        breed = random.choice(breeds)
        name = random.choice(CAT_NAMES)
        lines = [
            f"{name} is a cat and has-birthday equal-to {generate_random_date()}.",
            f"{name} has-breed that is {breed}.",
            f"{name} likes-food that is {random.choice(FOODS)}.",
            f"{name} sleeps-in {random.choice(SLEEP_PLACES)}."
        ]

        if random.random() < 0.5:
            lines.append(f"{name} has-favorite-toy that is {random.choice(TOYS)}.")
        if random.random() < 0.4:
            lines.append(f"{name} has-hobby that is {random.choice(ACTIONS)}.")
        if random.random() < 0.3:
            lines.append(f"{name} wears {random.choice(ACCESSORIES)}.")
        if random.random() < 0.3:
            lines.append(f"{name} fears {random.choice(DISLIKES)}.")
        if random.random() < 0.2:
            lines.append(f"{name} enjoys {random.choice(ACTIONS)}.")

        individuals.append("\n".join(lines))
    
    return individuals

def to_ace(cat_data):
    lines = []
    breed_name = normalize_str(cat_data['name'])
    lines.append(f"{breed_name} is a breed.")

    if cat_data.get('hairless') == 1:
        lines.append(f"{breed_name} is a hairless-cat.")
    if cat_data.get('natural') == 1:
        lines.append(f"{breed_name} is a natural-breed.")
    if cat_data.get('rare') == 1:
        lines.append(f"{breed_name} is a rare-breed.")

    if 'origin' in cat_data:
        lines.append(f"{breed_name} has-origin that is {normalize_str(cat_data['origin'])}.")

    if 'life_span' in cat_data:
        min_years, max_years = cat_data['life_span'].split("-")
        lines.extend([
            f"{breed_name} has-life-span at-least {min_years.strip()} years.",
            f"{breed_name} has-life-span at-most {max_years.strip()} years."
        ])

    if 'temperament' in cat_data:
        for trait in [t.strip() for t in cat_data["temperament"].split(",")]:
            lines.append(f"{breed_name} has-temperament that is {trait.replace(' ', '-').lower()}.")

    if 'lap' in cat_data:
        lines.append(f"{breed_name} has{'-' if cat_data['lap'] else '-no-'}lap.")
    
    if 'hypoallergenic' in cat_data:
        lines.append(f"{breed_name} is {'a' if cat_data['hypoallergenic'] else 'not a'} hypoallergenic.")

    if 'intelligence' in cat_data:
        lines.append(f"{breed_name} is {get_intelligence_level(cat_data['intelligence'])}.")
    if 'energy_level' in cat_data:
        lines.append(f"{breed_name} is {get_energy_level(cat_data['energy_level'])}.")
    if 'dog_friendly' in cat_data:
        lines.append(f"{breed_name} is {get_friendliness_level(cat_data['dog_friendly'])}.")

    lines.append(f"{breed_name} is an {'in' if cat_data['indoor'] == 1 else 'out'}door-cat.")

    return "\n".join(lines)

def main():
    input_path = "breeds.json"
    output_path = "cats.encnl"

    # Wczytanie danych wejściowych
    with open(input_path, "r", encoding="utf-8") as f:
        cats = json.load(f)

    print(f"Znaleziono {len(cats)} ras kotów.")

    # Pobranie liczby ras do wyeksportowania
    try:
        limit = int(input("Ile chcesz wyeksportować do Fluent Editora? "))
    except ValueError:
        limit = len(cats)
        print(f"Nieprawidłowa wartość, przyjęto {limit}.")

    selected_cats = cats[:limit]

    # Przygotowanie sekcji krajów pochodzenia
    origins = {normalize_str(c['origin']) for c in selected_cats if 'origin' in c}
    origin_definitions = "\n".join(sorted(f"{o} is a country." for o in origins)) + "\n"

    # Budowanie zawartości pliku ACE
    ace_blocks = [
        "Title: 'Ontologia ras kotów'.\nAuthor: 'Krzysztof Motas'.\n",

        "Part-1: 'Podstawowe definicje'.\nEvery breed is a cat.\n" + "\n".join([
            *[f"{normalize_str(f)} is a food." for f in FOODS],
            *[f"{normalize_str(s)} is an object." for s in SLEEP_PLACES],
            *[f"{normalize_str(t)} is a toy." for t in TOYS],
            *[f"{normalize_str(a)} is an action." for a in ACTIONS],
            *[f"{normalize_str(ac)} is an accessory." for ac in ACCESSORIES],
            *[f"{normalize_str(d)} is an object." for d in DISLIKES]
        ]),

        "\nPart-2: 'Kraje pochodzenia'.\n" + origin_definitions,

        "Part-3: 'Opisy ras'.\n" + "\n\n".join(to_ace(cat) for cat in selected_cats),

        "\nPart-4: 'Przykładowe koty'.\n" + "\n\n".join(
            generate_random_individuals(
                [normalize_str(c['name']) for c in selected_cats],
                count=15
            )
        )
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ace_blocks))

    print(f"\nZapisano {limit} ras do pliku: {output_path}")
    print("Otwórz Fluent Editor, wklej zawartość pliku i uruchom Reasoner.")

if __name__ == "__main__":
    main()