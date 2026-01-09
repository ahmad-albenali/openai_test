from openai import OpenAI
from google import genai
import db


def send_openai_hello():
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.1",
        input="Hello, world!",
    )
    return response


def send_gemini_hello():
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hello, world!",
    )
    return response


def main():
    # OpenAI
    openai_response = send_openai_hello()
    db.save_response(openai_response)
    print(f"OpenAI response: {openai_response.output[0].content[0].text}")

    # Gemini
    gemini_response = send_gemini_hello()
    print(f"Gemini response: {gemini_response.text}")


if __name__ == "__main__":
    main()
