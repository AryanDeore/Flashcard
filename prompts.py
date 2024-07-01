# prompts.py

FIVE_YEAR_OLD_PROMPT = "Explain {topic} in {domain} to me like I am a 5 year old."

UNDERGRAD_PROMPT = "Explain {topic} in {domain} to me like I am an undergrad student. Provide a simple explanation, 2 use cases, and 2 advantages and disadvantages if they exist."

EXPERT_PROMPT = "Explain {topic} and its architecture in {domain} to me like I am a subject matter expert. Provide a detailed technical explanation with step-by-step procedure in 8 steps."

def get_prompt(level, topic, domain):
    if level == "5 year old":
        return FIVE_YEAR_OLD_PROMPT.format(topic=topic, domain=domain)
    elif level == "undergrad student":
        return UNDERGRAD_PROMPT.format(topic=topic, domain=domain)
    elif level == "Subject Matter Expert":
        return EXPERT_PROMPT.format(topic=topic, domain=domain)
    else:
        raise ValueError("Invalid level specified")
