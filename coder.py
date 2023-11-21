import keyboard
import pyautogui
import openai
import os
import time

openai.api_key = "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"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a python programmer trained to code what the user asks for. You may also have to explain the code or answer questions about it. At the top of each message, you will indicate if you are coding or just answering a question about the code and then that part with a <>."},
        {"role": "user", "content": "Code me something simple in python"}
    ]
)

code = response.choices[0].message['content']

index = code.find("```", 0)
index2 = code.find("```", index + 1)

print(code)
print("\n\n")
# print(index, index2)
print(code[index+9:index2-1])


# Move the mouse to (100, 100) over 2 seconds
pyautogui.moveTo(500, 100, duration=2)
pyautogui.leftClick()

# Type "Hello, World!"
keyboard.write("hello world")

# Press Enter
keyboard.press_and_release("enter")

code_state = code





