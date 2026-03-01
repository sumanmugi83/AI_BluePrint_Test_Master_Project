import sys
import json
import ollama

def generate_test_cases(user_story, model='llama3.2'):
    """
    Generates test cases from a user story using Ollama.
    Returns: JSON object (dict)
    """
    if not user_story:
        return {"error": "User story cannot be empty"}

    system_prompt = """
    You are a Senior QA Manual Tester. Your output must be strict valid JSON only. 
    No markdown, no explanatory text, no code fences.
    
    Structure your response exactly like this:
    {
      "test_cases": [
        {
          "id": "TC_001",
          "title": "Short title",
          "preconditions": "Preconditions here",
          "steps": ["Step 1", "Step 2"],
          "expected_result": "Expected result",
          "type": "Positive" 
        }
      ],
      "summary": "Brief summary"
    }
    """

    user_prompt = f"""
    Analyze the following User Story and generate comprehensive test cases (Positive, Negative, and Edge Cases).
    
    User Story: "{user_story}"
    """

    try:
        response = ollama.generate(
            model=model,
            system=system_prompt,
            prompt=user_prompt,
            format='json', # Enforce JSON mode if supported by model/library, else relies on prompt
            stream=False
        )
        
        response_text = response['response']
        
        # Attempt to parse JSON
        try:
            data = json.loads(response_text)
            return data
        except json.JSONDecodeError:
            # Fallback: aggressive cleaning if model included markdown fences
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Allow running as a standalone script: python generate_test_cases.py "Story..."
    if len(sys.argv) > 1:
        story = " ".join(sys.argv[1:])
        result = generate_test_cases(story)
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({"error": "No user story provided as argument"}))
