# # from google import genai
# # from google.genai import types
# # from dotenv import load_dotenv
# # import os
# # import json

# # # Load environment variables
# # load_dotenv()

# # API_KEY = os.getenv("API_KEY")
# # if not API_KEY:
# #     raise ValueError("API_KEY not found in .env")

# # # Create Gemini client
# # client = genai.Client(api_key=API_KEY)

# # # Load category taxonomy
# # with open("categories.json", "r", encoding="utf-8") as file:
# #     categories = json.load(file)

# # # Create a smaller taxonomy to send to Gemini
# # taxonomy = {
# #     category["id"]: category["subCategories"]
# #     for category in categories["categories"]
# # }

# # # Take user input
# # user_prompt = input("Enter your prompt: ")

# # # Build classification prompt
# # classification_prompt = f"""
# # You are a prompt classification engine.

# # Your task is to classify the user's prompt into EXACTLY ONE
# # category and EXACTLY ONE sub-category from the taxonomy below.

# # Taxonomy:
# # {json.dumps(taxonomy, indent=2)}

# # User Prompt:
# # {user_prompt}

# # Rules:
# # 1. Return ONLY valid JSON.
# # 2. categoryId must be one of the taxonomy keys.
# # 3. subCategory must belong to the selected category.
# # 4. confidence must be a number between 0 and 1.
# # 5. Do not include explanations or markdown.

# # Output format:

# # {{
# #   "categoryId": "CATEGORY_ID",
# #   "subCategory": "SUB_CATEGORY",
# #   "confidence": 0.95
# # }}
# # """

# # # Ask Gemini in JSON mode
# # response = client.models.generate_content(
# #     model="gemini-2.5-flash",
# #     contents=classification_prompt,
# #     config=types.GenerateContentConfig(
# #         response_mime_type="application/json"
# #     )
# # )

# # # Parse JSON response
# # result = json.loads(response.text)

# # print("\nClassification:")
# # print(f"Category     : {result['categoryId']}")
# # print(f"Sub Category : {result['subCategory']}")
# # print(f"Confidence   : {result['confidence']}")

# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# import os
# import json

# # -----------------------------
# # Load environment variables
# # -----------------------------
# load_dotenv()

# API_KEY = os.getenv("API_KEY")
# if not API_KEY:
#     raise ValueError("API_KEY not found in .env")

# # -----------------------------
# # Create Gemini client
# # -----------------------------
# client = genai.Client(api_key=API_KEY)

# # -----------------------------
# # Load categories
# # -----------------------------
# with open("categories.json", "r", encoding="utf-8") as file:
#     categories = json.load(file)

# # -----------------------------
# # Load models
# # -----------------------------
# with open("models.json", "r", encoding="utf-8") as file:
#     models = json.load(file)

# # -----------------------------
# # Create compact taxonomy
# # -----------------------------
# taxonomy = {
#     category["id"]: category["subCategories"]
#     for category in categories["categories"]
# }

# # -----------------------------
# # Get user prompt
# # -----------------------------
# user_prompt = input("Enter your prompt: ")

# # -----------------------------
# # Build classification prompt
# # -----------------------------
# classification_prompt = f"""
# You are a prompt classification engine.

# Classify the user's prompt into EXACTLY ONE category and
# EXACTLY ONE sub-category.

# Available taxonomy:
# {json.dumps(taxonomy, indent=2)}

# User Prompt:
# {user_prompt}

# Rules:
# 1. Return ONLY valid JSON.
# 2. categoryId must be one of the taxonomy keys.
# 3. subCategory must belong to the selected category.
# 4. confidence must be between 0 and 1.
# 5. No markdown.
# 6. No explanations.

# Output format:

# {{
#   "categoryId": "CATEGORY_ID",
#   "subCategory": "SUB_CATEGORY",
#   "confidence": 0.95
# }}
# """

# # -----------------------------
# # Ask Gemini to classify
# # -----------------------------
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=classification_prompt,
#     config=types.GenerateContentConfig(
#         response_mime_type="application/json"
#     )
# )

# classification = json.loads(response.text)

# # -----------------------------
# # Deterministic Model Router
# # -----------------------------
# def choose_best_model(classification, models):
#     category = classification["categoryId"]
#     sub_category = classification["subCategory"]

#     best_model = None
#     best_score = -1

#     for model_name, model_info in models.items():
#         score = 0

#         categories = model_info.get("categories", [])
#         strengths = model_info.get("strengths", [])

#         # Category match
#         if category in categories:
#             score += 10

#         # Exact capability match
#         if sub_category in strengths:
#             score += 20

#         # Bonus rules
#         if category == "CODING":
#             if model_name == "GPT_5":
#                 score += 5
#             elif model_name == "CLAUDE_SONNET":
#                 score += 4
#             elif model_name == "DEEPSEEK_R1":
#                 score += 3

#         elif category == "MULTIMEDIA":
#             if model_name.startswith("GEMINI"):
#                 score += 5

#         elif category == "DOCUMENTS":
#             if model_name == "CLAUDE_SONNET":
#                 score += 5

#         elif category == "RESEARCH":
#             if model_name == "GROK_4":
#                 score += 5

#         elif category == "MATHEMATICS":
#             if model_name == "DEEPSEEK_R1":
#                 score += 5

#         if score > best_score:
#             best_score = score
#             best_model = model_name

#     return best_model, best_score


# # -----------------------------
# # Route Prompt
# # -----------------------------
# best_model, score = choose_best_model(
#     classification,
#     models
# )

# # -----------------------------
# # Print Result
# # -----------------------------
# print("\n========== ROUTING RESULT ==========")
# print(f"Prompt         : {user_prompt}")
# print(f"Category       : {classification['categoryId']}")
# print(f"Sub Category   : {classification['subCategory']}")
# print(f"Confidence     : {classification['confidence']}")
# print(f"Best Model     : {best_model}")
# print(f"Routing Score  : {score}")
# print("====================================")



from datetime import datetime
import time

from google.genai.errors import ClientError

from utils.loader import load_json
from services.decomposer import decompose_prompt
from services.router import choose_best_model
from services.executor import execute_task
from services.synthesizer import synthesize
from pathlib import Path

# =====================================================
# Configuration
# =====================================================

REQUESTS_PER_MINUTE = 5
REQUEST_DELAY = 60 / REQUESTS_PER_MINUTE  # 12 seconds
MAX_RETRIES = 3

# =====================================================
# Load Configurations
# =====================================================

categories = load_json("categories.json")
models = load_json("models.json")

taxonomy = {
    category["id"]: category["subCategories"]
    for category in categories["categories"]
}

# =====================================================
# User Prompt
# =====================================================

user_prompt = input("Enter your prompt:\n")

# =====================================================
# Step 1 - Decompose
# =====================================================

print("\nDecomposing prompt...\n")

decomposition = decompose_prompt(
    user_prompt,
    taxonomy
)

tasks = decomposition["tasks"]

print("=" * 80)
print("TASKS")
print("=" * 80)

for task in tasks:
    print(task)

# =====================================================
# Step 2 - Route
# =====================================================

for task in tasks:
    task["model"] = choose_best_model(
        task,
        models
    )

print("\n" + "=" * 80)
print("ROUTING")
print("=" * 80)

for task in tasks:
    print(
        f'{task["description"]}\n'
        f'  -> {task["model"]}\n'
    )

# =====================================================
# Step 3 - Execute Sequentially
# =====================================================

docs_dir = Path("Docs")
docs_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
all_saved_files: list[str] = []

results = []

print("\n" + "=" * 80)
print("EXECUTION")
print("=" * 80)

for index, task in enumerate(tasks, start=1):

    print(f"\n[{index}/{len(tasks)}]")
    print(f"Model       : {task['model']}")
    print(f"Description : {task['description']}")

    retries = 0

    while retries <= MAX_RETRIES:

        try:

            result = execute_task(
                task,
                task["model"],
                docs_dir=docs_dir,
                file_prefix=f"{timestamp}_task{task['taskId']}",
            )

            results.append(result)

            if result.get("saved_files"):
                all_saved_files.extend(result["saved_files"])
                print("✓ Files saved:")
                for saved_file in result["saved_files"]:
                    print(f"  - {saved_file}")

            print("✓ Success")

            break

        except ClientError as e:

            if "429" in str(e):

                retries += 1

                if retries > MAX_RETRIES:
                    print("❌ Maximum retries exceeded.")

                    results.append({
                        "taskId": task["taskId"],
                        "model": task["model"],
                        "response": "Failed because of rate limit."
                    })

                    break

                wait_time = REQUEST_DELAY * (2 ** retries)

                print(
                    f"⚠ Rate limit exceeded."
                    f" Waiting {wait_time:.0f} seconds..."
                )

                time.sleep(wait_time)

            else:

                print("❌ API Error")
                print(e)

                results.append({
                    "taskId": task["taskId"],
                    "model": task["model"],
                    "response": f"ERROR: {e}"
                })

                break

        except Exception as e:

            print("❌ Unexpected Error")
            print(e)

            results.append({
                "taskId": task["taskId"],
                "model": task["model"],
                "response": f"ERROR: {e}"
            })

            break

    # Wait before next request
    if index != len(tasks):

        print(f"\nWaiting {REQUEST_DELAY:.0f} seconds...\n")

        time.sleep(REQUEST_DELAY)

# =====================================================
# Step 4 - Individual Results
# =====================================================

print("\n" + "=" * 80)
print("INDIVIDUAL RESULTS")
print("=" * 80)

for result in results:

    print(f"\nModel : {result['model']}")
    print("-" * 40)
    print(result["response"])
    print("-" * 80)

# =====================================================
# Step 5 - Final Synthesis
# =====================================================

print("\nSynthesizing final response...\n")

try:

    final_answer, synthesis_files = synthesize(
        results,
        docs_dir=docs_dir,
        file_prefix=f"{timestamp}_synthesis",
        user_prompt=user_prompt,
    )
    all_saved_files.extend(synthesis_files)

    print("\n" + "=" * 80)
    print("FINAL ANSWER")
    print("=" * 80)
    print(final_answer)

    if synthesis_files:
        print("\nSynthesis files saved:")
        for saved_file in synthesis_files:
            print(f"  - {saved_file}")

    # =====================================================
    # Save response to Docs folder
    # =====================================================

    file_path = docs_dir / f"{timestamp}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Prompt\n")
        file.write("=" * 80 + "\n")
        file.write(user_prompt + "\n\n")

        file.write("Tasks\n")
        file.write("=" * 80 + "\n")
        for task in tasks:
            file.write(f"{task}\n")

        file.write("\nRouting\n")
        file.write("=" * 80 + "\n")
        for task in tasks:
            file.write(
                f"{task['description']} -> {task['model']}\n"
            )

        file.write("\nFinal Response\n")
        file.write("=" * 80 + "\n")
        file.write(final_answer)

        if all_saved_files:
            file.write("\n\nDownloaded Files\n")
            file.write("=" * 80 + "\n")
            for saved_file in all_saved_files:
                file.write(f"{saved_file}\n")

    print(f"\nResponse saved to:\n{file_path.resolve()}")

    if all_saved_files:
        print("\nAll downloaded files:")
        for saved_file in all_saved_files:
            print(f"  - {saved_file}")

except Exception as e:

    print("Failed to synthesize final answer.")
    print(e)