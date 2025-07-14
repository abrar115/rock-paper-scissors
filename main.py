import random
import os

HISTORY_FILE = "rps_history.txt"

def get_user_choice():
    aliases = {
        'r': 'rock',
        'p': 'paper',
        's': 'scissors',
        'rock': 'rock',
        'paper': 'paper',
        'scissors': 'scissors'
    }
    while True:
        user_input = input("Enter rock (r), paper (p), or scissors (s) (or 'quit' to exit): ").strip().lower()
        if user_input == 'quit':
            return None
        if user_input in aliases:
            return aliases[user_input]
        print("Invalid choice. Please try again.")

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user, computer):
    if user == computer:
        return "tie"
    if (user == 'rock' and computer == 'scissors') or \
       (user == 'paper' and computer == 'rock') or \
       (user == 'scissors' and computer == 'paper'):
        return "user"
    else:
        return "computer"

def save_game_result(winner, target_wins, rounds_played):
    # Save the result as "win", "loss", or "tie" along with target wins and rounds played
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{winner},{target_wins},{rounds_played}\n")

def show_game_history():
    if not os.path.exists(HISTORY_FILE):
        print("No game history found.")
        return

    with open(HISTORY_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print("No game history found.")
        return

    wins = 0
    losses = 0
    ties = 0
    rounds_list = []

    for line in lines:
        result, target, rounds = line.split(",")
        rounds_list.append(int(rounds))
        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1
        elif result == "tie":
            ties += 1

    total_games = wins + losses + ties
    print(f"\n📊 Game History Summary:")
    print(f"Total games played: {total_games}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Ties: {ties}")
    print(f"Average rounds per game: {sum(rounds_list) / total_games:.2f}")
    if wins > 0:
        best_rounds = min(rounds_list)
        print(f"🏆 Best (least rounds to win): {best_rounds}")
    print()

def play():
    print("Welcome to Rock-Paper-Scissors with game history!")

    while True:
        choice = input("Type 'play' to start a new game, 'history' to view game history, or 'quit' to exit: ").strip().lower()
        if choice == "play":
            break
        elif choice == "history":
            show_game_history()
        elif choice == "quit":
            print("Goodbye!")
            return
        else:
            print("Invalid input, please type 'play', 'history', or 'quit'.")

    while True:
        try:
            target_wins = int(input("How many wins needed to win the match? Enter a positive integer: "))
            if target_wins > 0:
                break
            else:
                print("Please enter a positive integer greater than zero.")
        except ValueError:
            print("That's not a valid number. Try again.")

    user_score = 0
    computer_score = 0
    rounds_played = 0

    while user_score < target_wins and computer_score < target_wins:
        user_choice = get_user_choice()
        if user_choice is None:
            print("Thanks for playing! Goodbye.")
            return

        computer_choice = get_computer_choice()
        print(f"You chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")

        winner = determine_winner(user_choice, computer_choice)
        rounds_played += 1

        if winner == "tie":
            print("It's a tie!")
        elif winner == "user":
            user_score += 1
            print("You win this round! 🎉")
        else:
            computer_score += 1
            print("Computer wins this round!")

        print(f"Score — You: {user_score} | Computer: {computer_score}\n")

    if user_score == target_wins:
        print(f"🎉 Congratulations! You reached {target_wins} wins and won the match!")
        save_game_result("win", target_wins, rounds_played)
    else:
        print(f"💀 The computer reached {target_wins} wins. Better luck next time!")
        save_game_result("loss", target_wins, rounds_played)

if __name__ == "__main__":
    play()
