from openai import OpenAI

client = OpenAI()


def generate_reply(text):

    prompt = f"""
    Generate a polite business reply to this review:

    Review: {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
