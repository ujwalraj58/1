from langchain_rag import get_answer
from voice import speak, listen

def main():
    print("🟢 Voice Chatbot Started")
    print("Type 'exit' at any time to quit.")
    
    while True:
        mode = input("\n🎙️ Do you want to [speak] or [type] your question? ").strip().lower()

        if mode == "exit":
            print("👋 Exiting...")
            break

        if mode == "speak":
            question = listen()
            if question.startswith("Sorry,"):
                print("❌ Could not understand your voice. Try again.")
            continue

            print(f"📝 You said: {question}")

            if "exit" in question.lower():
                break

        answer = get_answer(question)
        print("🤖 Answer:", answer)
        speak(answer)

        elif mode == "type":
            question = input("⌨️ Enter your question: ").strip()

            if question.lower() == "exit":
                break

            answer = get_answer(question)
            print("🤖 Answer:", answer)

        else:
            print("❌ Invalid input. Please type 'speak' or 'type'.")

if __name__ == "__main__":
    main()
