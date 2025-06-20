from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from textblob import TextBlob

class AdvancedChatbot:
    def __init__(self):
        # Load the DialoGPT model and tokenizer
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.chat_history_ids = None

    def analyze_sentiment(self, user_input):
        # Analyze sentiment of the user input
        blob = TextBlob(user_input)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            return "positive"
        elif sentiment < 0:
            return "negative"
        else:
            return "neutral"
        
    def get_response(self, user_input):
        # Analyze sentiment and generate an appropriate response
        sentiment = self.analyze_sentiment(user_input)
        response_prefix = self.generate_sentiment_response(sentiment)

        # Add sentiment-based prefix to the user input
        user_input_with_sentiment = f"{response_prefix} {user_input}"

        # Tokenize and generate a response from the model
        new_user_input_ids = self.tokenizer.encode(user_input_with_sentiment + self.tokenizer.eos_token, return_tensors='pt')

        # Maintain context history for conversation
        if self.chat_history_ids is not None:
            bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
        else:
            bot_input_ids = new_user_input_ids

        bot_output = self.model.generate(bot_input_ids, max_length=1000, pad_token_id=self.tokenizer.eos_token_id, do_sample=True, top_k=50, top_p=0.95, temperature=0.7)

        # Update chat history
        self.chat_history_ids = bot_output

        # Decode and return the response
        bot_response = self.tokenizer.decode(bot_output[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return bot_response

    def generate_sentiment_response(self, sentiment):
        # Generate response based on sentiment
        if sentiment == "positive":
            return "I'm glad you're feeling good! 😊"
        elif sentiment == "negative":
            return "I'm sorry to hear you're feeling down. 😟"
        else:
            return "I see you're feeling neutral. 😐"

def chat():
    # Initialize the chatbot
    chatbot = AdvancedChatbot()

    print("Chatbot is ready! Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            bot_response = chatbot.get_response(user_input)
            print("Bot:", bot_response)

if __name__ == "__main__":
    chat()
