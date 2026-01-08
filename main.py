import os
from openai import OpenAI


def send_hello_world():
    
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.1",
        input="Hello, world!",
    )
    return response


def main():
    response_body = send_hello_world()
    print(response_body)


if __name__ == "__main__":
    main()
