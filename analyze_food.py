import base64
from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(api_key="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")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_food_image(image_path):
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What food is in this photo? Estimate calories and ingredients."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content


# Example use:
if __name__ == "__main__":
    path = "example_food.jpg"  # replace with your test image path
    result = analyze_food_image(path)
    print(result)
