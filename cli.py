"""Interactive CLI test tool for Shinri RAG Pipeline."""
import sys
from src.rag.pipeline import ShinriRAGPipeline


def main():
    print("=" * 75)
    print("Shinri (真理) - Mutual Fund Facts Assistant CLI")
    print("Facts-only assistant covering 5 HDFC schemes on Groww.")
    print("Type 'exit' or 'quit' to end. Type 'clear' to reset conversation memory.")
    print("=" * 75)

    pipeline = ShinriRAGPipeline()

    while True:
        try:
            user_input = input("\n[You] > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting Shinri CLI. Goodbye!")
                break
            if user_input.lower() == "clear":
                pipeline.memory.clear()
                print("Conversation history cleared.")
                continue

            result = pipeline.query(user_input)

            if result.get("rewritten_query") and result["rewritten_query"] != user_input:
                print(f"\n[Context Rewriter] -> '{result['rewritten_query']}'")

            print("\n[Shinri Response]")
            print(result["answer"])

            if result.get("retrieved_chunks"):
                print("\n[Top Retrieved Chunks]")
                for i, chunk in enumerate(result["retrieved_chunks"], 1):
                    meta = chunk["metadata"]
                    print(f"  {i}. {meta['scheme_name']} | {meta['section']} (Distance: {chunk['distance']:.4f})")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting Shinri CLI.")
            break


if __name__ == "__main__":
    main()
