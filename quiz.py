import random
import time
import json


states_and_capitals = {
    "Andhra Pradesh": "Amaravati",
    "Arunachal Pradesh": "Itanagar",
    "Assam": "Dispur",
    "Bihar": "Patna",
    "Chhattisgarh": "Raipur",
    "Goa": "Panaji",
    "Gujarat": "Gandhinagar",
    "Haryana": "Chandigarh",
    "Himachal Pradesh": "Shimla",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Madhya Pradesh": "Bhopal",
    "Maharashtra": "Mumbai",
    "Manipur": "Imphal",
    "Meghalaya": "Shillong",
    "Mizoram": "Aizawl",
    "Nagaland": "Kohima",
    "Odisha": "Bhubaneswar",
    "Punjab": "Chandigarh",
    "Rajasthan": "Jaipur",
    "Sikkim": "Gangtok",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Tripura": "Agartala",
    "Uttar Pradesh": "Lucknow",
    "Uttarakhand": "Dehradun",
    "West Bengal": "Kolkata",
}


def generate_options(correct_capital, all_capitals):
    options = random.sample(all_capitals, 2)
    options.append(correct_capital)
    random.shuffle(options)
    return options


def display_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
            print("\nLeaderboard:")
            for entry in sorted(leaderboard, key=lambda x: -x['score'])[:5]:
                print(f"{entry['name']}: {entry['score']} points, Accuracy: {entry['accuracy']:.2f}%")
    except FileNotFoundError:
        print("No leaderboard found.")

def save_to_leaderboard(name, score, accuracy):
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = []
    
    leaderboard.append({"name": name, "score": score, "accuracy": accuracy})
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file)

def get_difficulty_level(states_and_capitals):
    easy_states = ["Maharashtra", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "West Bengal"]
    medium_states = ["Goa", "Gujarat", "Haryana", "Kerala", "Odisha"]
    hard_states = ["Arunachal Pradesh", "Mizoram", "Nagaland", "Tripura", "Sikkim"]

    print("Select Difficulty Level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    choice = input("Enter the number corresponding to your choice: ").strip()

    if choice == "1":
        selected_states = {state: states_and_capitals[state] for state in easy_states if state in states_and_capitals}
    elif choice == "2":
        selected_states = {state: states_and_capitals[state] for state in medium_states if state in states_and_capitals}
    elif choice == "3":
        selected_states = {state: states_and_capitals[state] for state in hard_states if state in states_and_capitals}
    else:
        print("Invalid choice, defaulting to Easy.")
        selected_states = {state: states_and_capitals[state] for state in easy_states if state in states_and_capitals}

    return selected_states


def quiz():
    print("\nWelcome to the Indian States and Capitals Quiz!")
    print("Try to answer the questions as quickly and accurately as possible.")
    print("Top scores will be displayed on the leaderboard.\n")
    
    name = input("Enter your name: ")

    selected_states = get_difficulty_level(states_and_capitals)

    if not selected_states:
        print("No states available for the selected difficulty. Exiting quiz.")
        return

    score = 0
    num_questions = min(10, len(selected_states))  # Ensure there are enough questions
    time_limit = 10
    all_capitals = list(states_and_capitals.values())
    results = []

    selected_states_list = random.sample(list(selected_states.keys()), num_questions)

    for i, state in enumerate(selected_states_list):
        correct_capital = selected_states[state]
        options = generate_options(correct_capital, all_capitals)

        print(f"\nQuestion {i + 1}: What is the capital of {state}?")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        
        start_time = time.time()

        try:
            user_input = input(f"Enter your choice (1-3) within {time_limit} seconds: ").strip()
            elapsed_time = time.time() - start_time
            
            if elapsed_time > time_limit:
                print("Time's up! Moving to the next question.\n")
                results.append((state, correct_capital, "No answer", False))
            else:
                user_choice = int(user_input)
                user_answer = options[user_choice - 1]
                
                if user_answer.lower() == correct_capital.lower():
                    print("Correct! 🎉\n")
                    score += 1
                    results.append((state, correct_capital, user_answer, True))
                else:
                    print(f"Incorrect. The capital of {state} is {correct_capital}. 😔\n")
                    results.append((state, correct_capital, user_answer, False))
        except (ValueError, IndexError):
            print("Invalid input! Moving to the next question.\n")
            results.append((state, correct_capital, "Invalid input", False))
        
        print(f"Current Score: {score}/{i + 1}")

    print("\nQuiz Over! Here's your summary:")
    print("=" * 40)
    for result in results:
        state, correct_capital, user_answer, is_correct = result
        status = "Correct" if is_correct else "Incorrect"
        print(f"State: {state} | Your Answer: {user_answer} | Correct Answer: {correct_capital} | Result: {status}")
    print("=" * 40)

    accuracy = (score / num_questions) * 100
    print(f"\nYour final score is {score}/{num_questions}.")
    print(f"Your accuracy rate is {accuracy:.2f}%.")

    save_to_leaderboard(name, score, accuracy)

    print("\nFinal Leaderboard:")
    display_leaderboard()
    
    if score == num_questions:
        print("Amazing! You got all the answers right! 🌟")
    elif score >= num_questions // 2:
        print("Good job! You did well! 👍")
    else:
        print("Keep practicing! You'll get better! 💪")

if __name__ == "__main__":
    quiz()
