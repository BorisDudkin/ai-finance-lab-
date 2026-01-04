import json 
from llm_client import call_llm 
 

def generate_signals(text): 
    messages = [ 
        {"role": "system", "content": "Return valid JSON only."}, 
        {"role": "user", "content": f""" 
From the text below, generate allocation signals. 
 

JSON schema: 
{{ 
  "equities": "overweight|neutral|underweight", 
  "rates": "long|neutral|short", 
  "credit": "tighten|neutral|widen", 
  "confidence": 0-1 
}} 
 

TEXT: 
{text} 
"""} 
    ] 
    return json.loads(call_llm(messages)) 