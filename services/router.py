def choose_best_model(task, models):
    category = task["categoryId"]
    sub_category = task["subCategory"]

    best_model = None
    best_score = -1

    for model_name, info in models.items():
        score = 0

        categories = info.get("categories", [])
        strengths = info.get("strengths", [])

        if category in categories:
            score += 10

        if sub_category in strengths:
            score += 20

        if score > best_score:
            best_score = score
            best_model = model_name

    return best_model