# LLM-based macro regime classifier for asset allocation.
# Claude preferred (macro nuance)
from llm_client import call_llm 
 

def classify_macro(text): 
    messages = [ 
        {"role": "system", "content": "Be conservative and precise."}, 
        {"role": "user", "content": text} 
    ] 
    return call_llm(messages, temperature=0.0) 
 

if __name__ == "__main__": 
    with open("sample_inputs/fomc.txt") as f: 
        print(classify_macro(f.read())) 