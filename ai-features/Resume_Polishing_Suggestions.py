import openai
import os

# Note 1: Import the OpenAI library to interact with the API.
# Note 2: Set the API key. It's best practice to read it from environment variables.
# Example: os.environ["OPENAI_API_KEY"] = "sk-..."
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Note 3: For testing, you can temporarily paste your key here.
openai.api_key = 'your-openai-api-key-here' 

def build_system_prompt():
    """
    Note 4: This function builds the "System Prompt" which contains
    the core instructions and examples for the AI.
    """
    return """
[SYSTEM PROMPT]

👤 You are a Career Coach and an expert Resume Writer.

🎯 Your task is to take a bullet point from a user's resume and rewrite it to be more professional, powerful, and achievement-oriented.

📝 Rules you must follow:
1.  Start the sentence with a strong "Action Verb" in the past tense (e.g., "Developed," "Led," "Implemented," "Accelerated").
2.  Use the "STAR" (Situation, Task, Action, Result) or "PAR" (Problem, Action, Result) method where possible. Focus on the "Result" and quantify it with metrics/numbers if they are available in the original text.
3.  Preserve the original meaning. Do not add new information.
4.  Keep the rewrite concise.
5.  Return ONLY the polished sentence, with no pre-amble or explanation (like "Here is the rewrite:").

💡 Training Examples:
(Note 5: These "Few-shot" examples teach the AI the required quality.)
[Example 1]
Original: "I was in charge of customer support."
Polished: "Provided technical support to over 50 customers daily, resolving 95% of inquiries during the first contact."

[Example 2]
Original: "I made some social media posts."
Polished: "Managed the company's social media accounts (Facebook, Twitter), increasing audience engagement by 15% over 3 months."
---
"""

def polish_resume_sentence_v2(user_bullet_point: str) -> str:
    """
    Note 6: This is the main function you call to polish a sentence.
    (V2) Uses the modern ChatCompletion API and the detailed system prompt.
    """
    
    # Note 7: Get the system instructions (rules and examples) from the helper function.
    system_prompt = build_system_prompt()
    
    # Note 8: Prepare the user-specific part of the prompt (the original sentence).
    user_prompt = f"""
[USER INPUT]
Original: {user_bullet_point}
Polished:
"""

    try:
        # Note 9: This is the actual LLM API call using the modern Chat API.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Note 10: Specify the model to use.
            messages=[
                # Note 11: The first message is the "system" role (the rules).
                {"role": "system", "content": system_prompt},
                # Note 12: The second message is the "user" role (the sentence).
                {"role": "user", "content": user_prompt}     
            ],
            temperature=0.3,  # Note 13: Low temperature for consistent, precise results.
            max_tokens=100
        )
        
        # Note 14: Extract the clean text response from the API's reply.
        polished = response.choices[0].message['content'].strip()
        return polished

    except Exception as e:
        # Note 15: Handle any potential errors during the API call.
        print(f"An error occurred: {e}")
        return f"Error: Could not polish sentence. {e}"

# --- Note 16: This block is for testing the code when run directly ---
if __name__ == "__main__":
    
    # Note 17: Test Case 1 - A sentence from the examples.
    test_sentence_1 = "I made some social media posts."
    polished_1 = polish_resume_sentence_v2(test_sentence_1)
    
    print(f"Original: {test_sentence_1}")
    print(f"Polished: {polished_1}")
    print("-" * 20)

    # Note 18: Test Case 2 - A new, unseen sentence.
    test_sentence_2 = "I fixed some bugs in the code."
    polished_2 = polish_resume_sentence_v2(test_sentence_2)
    
    print(f"Original: {test_sentence_2}")
    print(f"Polished: {polished_2}")
    print("-" * 20)