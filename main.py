from agent import agent

def main():
    print("🧠 AI Assistant (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.invoke(user_input)
        print(f"\n🤖: {response['output']}")

if __name__ == "__main__":
    main()