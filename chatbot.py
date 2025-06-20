from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def chatbot():
    # Specify the model
    model_name = "microsoft/DialoGPT-medium"
    
    print("Loading the model and tokenizer...")
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print("Model and tokenizer loaded successfully!")

    # Chat loop
    chat_history_ids = None
    print("Chatbot is ready! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Encode the user's input
        input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
        
        # Append input to chat history
        chat_history_ids = (
            torch.cat([chat_history_ids, input_ids], dim=-1)
            if chat_history_ids is not None
            else input_ids
        )

        # Generate a response
        response_ids = model.generate(chat_history_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(response_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)

        # Print chatbot response
        print(f"Bot: {response}")

if __name__ == "__main__":
    chatbot()
