# prompts.py

FIVE_YEAR_OLD_PROMPT = "Explain {topic} in {domain} to me like I am a 5 year old."

UNDERGRAD_PROMPT = "Explain {topic} in {domain} to me like I am an undergrad student. Provide a simple explanation, 2 use cases, and 2 advantages and disadvantages if they exist. Example #1: Explain linear regressoin in maths to me like I am an undergrad student. Provide a simple explanation, 2 use cases, and 2 advantages and disadvantages if they exist. Response: **Linear Regression:**\n\nLinear regression is a statistical method used to establish a linear relationship between a dependent variable (y) and one or more independent variables (x). The goal is to create a linear equation that best predicts the value of y based on the values of x.\n\n**Simple Explanation:**\n\nImagine you're trying to predict the price of a house based on its size. You collect data on the size and price of several houses. Linear regression helps you find the best-fitting line that describes the relationship between size and price. This line can then be used to predict the price of a new house based on its size.\n\n**Use Cases:**\n\n1. **Predicting Stock Prices:** A financial analyst uses linear regression to analyze the relationship between a company's stock price and its revenue. By finding the best-fitting line, the analyst can predict future stock prices based on expected revenue.\n2. **Predicting Student Grades:** A teacher uses linear regression to analyze the relationship between a student's study hours and their exam grades. By finding the best-fitting line, the teacher can predict a student's grade based on their study hours.\n\n**Advantages:**\n\n1. **Easy to Interpret:** Linear regression provides a simple and easy-to-understand equation that describes the relationship between variables.\n2. **Wide Range of Applications:** Linear regression can be applied to a wide range of fields, including economics, finance, social sciences, and more.\n\n**Disadvantages:**\n\n1. **Assumes Linearity:** Linear regression assumes that the relationship between variables is linear, which may not always be the case. Non-linear relationships can lead to inaccurate predictions.\n2. **Sensitive to Outliers:** Linear regression can be sensitive to outliers in the data, which can affect the accuracy of the predictions.\n\n"

EXPERT_PROMPT = "Explain {topic} and its process in {domain} to me like I am a subject matter expert. Provide a detailed explanation with step-by-step procedure in 8 steps. Drop starting and closing remarks."

FIVE_YEAR_OLD_IMAGE_PROMPT = "Create a simple, colorful illustration explaining {topic} in {domain} for a 5-year-old child. Use basic shapes, friendly imagery, and minimal text. The image should be easy to understand and visually appealing to young children. Do not use any arrows or labels just focus on the visuals."

UNDERGRAD_IMAGE_PROMPT = "Design a diagram or infographic explaining {topic} in {domain} suitable for an undergraduate student. Include key concepts, processes, and relevant data visualizations. Do not use any arrows or labels."

EXPERT_IMAGE_PROMPT = "Generate a detailed visualization of {topic} in {domain} for an expert audience. Use the image of term instead of using the word. Eg: use the image of sun instead of writing sun and pointing an arrow to it."

def get_prompt(level, topic, domain):
    if level == "5 year old":
        return FIVE_YEAR_OLD_PROMPT.format(topic=topic, domain=domain)
    elif level == "undergrad student":
        return UNDERGRAD_PROMPT.format(topic=topic, domain=domain)
    elif level == "Subject Matter Expert":
        return EXPERT_PROMPT.format(topic=topic, domain=domain)
    else:
        raise ValueError("Invalid level specified")

def get_image_prompt(level, topic, domain):
    if level == "5 year old":
        return FIVE_YEAR_OLD_IMAGE_PROMPT.format(topic=topic, domain=domain)
    elif level == "undergrad student":
        return UNDERGRAD_IMAGE_PROMPT.format(topic=topic, domain=domain)
    elif level == "Subject Matter Expert":
        return EXPERT_IMAGE_PROMPT.format(topic=topic, domain=domain)
    else:
        raise ValueError("Invalid level specified")
