#!/usr/bin/env python3

from agent.core.router import Router
from agent.llm.hybrid_router import HybridLLM

def main():
    print("============================================")
    print(" 🚀 Simple DevOps Agent Started (Hybrid AI) ")
    print("============================================")
    print(" Type commands in simple language, e.g.:")
    print("   - deploy nginx")
    print("   - rollback deployment")
    print("   - check logs for api")
    print("   - why pipeline failed")
    print("   - check cloud cost")
    print("")
    print(" Type 'exit' or 'quit' to stop.")
    print("--------------------------------------------")

    model = HybridLLM()
    router = Router(model=model)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit", "q"):
            print("\n🔚 Stopping Simple DevOps Agent. Bye!\n")
            break

        try:
            result = router.process(user_input)
            print("Agent:", result)
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

