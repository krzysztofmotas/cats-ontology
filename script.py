import json
import random
from datetime import datetime, timedelta

CAT_NAMES = ["Mruczek", "Adelka", "Urwis", "Elton", "Ozi", "Kajtula", "Klakier", "Zuzia", "Rudy", "Gacek", "Kropka", "Mania", "Zgredek", "Bonifacy"]
FOODS = ["Salmon", "Chicken", "Turkey", "Beef", "Tuna", "Shrimp", "Sardines"]
SLEEP_PLACES = ["Box", "Windowsill", "Hammock", "Sink", "Wardrobe"]
TOYS = ["Feather", "Mouse", "Ball", "Laser"]
ACTIONS = ["climbing-the-wardrobe", "hunting-shadows", "sleeping-in-the-sink"]
ACCESSORIES = ["Sweater", "Blanket", "Collar", "Bandana"]
DISLIKES = ["Vacuum-Cleaner", "Water", "Doorbell", "Rustle", "Dust"]

def normalize_str(name):
    if name == "Iran (Persia)":
        return "Iran"

    parts = name.strip().replace("-", " ").split()
    return "-".join(part.capitalize() for part in parts)

def get_friendliness_level(value):
    if value >= 5:
        return "very-child-friendly"
    elif value >= 4:
        return "child-friendly"
    elif value >= 2:
        return "not-very-child-friendly"
    else:
        return "not-child-friendly"

def get_intelligence_level(value):
    if value >= 5:
        return "very-intelligent"
    elif value >= 4:
        return "intelligent"
    elif value >= 2:
        return "not-very-intelligent"
    else:
        return "not-intelligent"

def get_energy_level(value):
    if value >= 5:
        return "very-energetic"
    elif value >= 4:
        return "energetic"
    elif value >= 2:
        return "not-very-energetic"
    else:
        return "not-energetic"

def generate_random_date(start_year=2010, end_year=2025):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_random_individuals(breeds, count=10):
    individuals = []
    used_names = set()

    while len(individuals) < count:
        breed = random.choice(breeds)

        name = random.choice([n for n in CAT_NAMES if n not in used_names])
        used_names.add(name)

        lines = [
            f"{name} is a cat.",
            f"{name} has-birthday equal-to {generate_random_date()}.",
            # f"{name} is a cat and has-birthday equal-to {generate_random_date()}.",
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

def to_cnl(cat_data):
    lines = []
    breed_name = normalize_str(cat_data['name'])

    if cat_data.get('hairless') == 1:
        lines.append(f"{breed_name} is a hairless-cat.")

    lines.append(f"{breed_name} is {'natural-breed' if cat_data.get('natural') == 1 else 'unnatural-breed'}.")

    if 'weight' in cat_data and 'metric' in cat_data['weight']:
        weight = cat_data['weight']['metric']
        if '-' in weight:
            try:
                min_w, max_w = weight.split('-')
                min_w = int(min_w.strip())
                max_w = int(max_w.strip())
                lines.append(f"{breed_name} has-weight-kg greater-or-equal-to {min_w}.")
                lines.append(f"{breed_name} has-weight-kg lower-or-equal-to {max_w}.")
            except ValueError:
                pass

    if cat_data.get('rare') == 1:
        lines.append(f"{breed_name} is a rare-breed.")

    if 'origin' in cat_data:
        origin = normalize_str(cat_data['origin'])
        lines.append(f"{breed_name} has-origin that is {origin}.")

    if 'life_span' in cat_data and '-' in cat_data['life_span']:
        min_years, max_years = cat_data['life_span'].replace(" ", "").split("-")
        lines.append(f"{breed_name} has-life-span-years greater-or-equal-to {min_years}.")
        lines.append(f"{breed_name} has-life-span-years lower-or-equal-to {max_years}.")

    if 'temperament' in cat_data:
        for trait in cat_data["temperament"].split(","):
            lines.append(f"{breed_name} has-temperament equal-to '{trait.strip().lower().replace(' ', '-')}'.")

    if 'lap' in cat_data:
        lines.append(f"{breed_name} has-lap." if cat_data['lap'] else f"{breed_name} has-no-lap.")

    if 'short_legs' in cat_data:
        lines.append(f"{breed_name} has-short-legs." if cat_data['short_legs'] else f"{breed_name} has-no-short-legs.")

    if 'hypoallergenic' in cat_data:
        lines.append(f"{breed_name} is a hypoallergenic." if cat_data['hypoallergenic'] else f"{breed_name} is not a hypoallergenic.")

    if 'intelligence' in cat_data:
        lines.append(f"{breed_name} is {get_intelligence_level(cat_data['intelligence'])}.")

    if 'energy_level' in cat_data:
        lines.append(f"{breed_name} is {get_energy_level(cat_data['energy_level'])}.")

    if 'child_friendly' in cat_data:
        lines.append(f"{breed_name} is {get_friendliness_level(cat_data['child_friendly'])}.")

    if 'indoor' in cat_data:
        lines.append(f"{breed_name} is an {'indoor-cat' if cat_data['indoor'] == 1 else 'outdoor-cat'}.")
    return "\n".join(lines)

def main():
    input_path = "breeds.json"
    output_path = "cats.encnl"
    with open(input_path, "r", encoding="utf-8") as f:
        cats = json.load(f)
    # try:
    #     limit = int(input("Ile chcesz wyeksportować do Fluent Editora? "))
    # except ValueError:
    #     limit = len(cats)
    #     print(f"Nieprawidłowa wartość, przyjęto {limit}.")

    limit = len(cats)

    selected_cats = cats[:limit]
    origins = {normalize_str(c['origin']) for c in selected_cats if 'origin' in c}
    origin_definitions = "\n".join(sorted(f"{o} is a country." for o in origins)) + "\n"
    cnl_parts = [
        # "Namespace: 'http://example.org/cats'.\n",
        "Title: 'Ontologia ras kotów'.\nAuthor: 'Krzysztof Motas'.\n",
          
        "Part-1: 'Kraje pochodzenia'.\n" + origin_definitions,
        # "Part-2: 'Podstawowe definicje'.\n" + "\n".join([
        #     *[f"{normalize_str(f)} is a food." for f in FOODS],
        #     *[f"{normalize_str(s)} is an object." for s in SLEEP_PLACES],
        #     *[f"{normalize_str(t)} is a toy." for t in TOYS],
        #     *[f"{normalize_str(ac)} is an accessory." for ac in ACCESSORIES],
        #     *[f"{normalize_str(d)} is an object." for d in DISLIKES],
        # ]),
        "Part-2: 'Opisy ras'.\n"
        "Every hairless-cat is a breed.\n"
        "Every rare-breed is a breed.\n"
        "Every natural-breed is a breed.\n"
        "Every unnatural-breed is a breed.\n\n"
        + "\n\n".join(to_cnl(cat) for cat in selected_cats),
        "Part-3: 'Przykładowe koty'.\n" + "\n\n".join(
            generate_random_individuals(
                [normalize_str(c['name']) for c in selected_cats],
                count=10
            )
        )
    ]
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(cnl_parts))
    print(f"Zapisano {limit} ras oraz przykładowe koty do pliku: {output_path}")

if __name__ == "__main__":
    main()