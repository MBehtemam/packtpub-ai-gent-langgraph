import os
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

llm_name = "gpt-3.5-turbo"

client = OpenAI(api_key=openai_key)

response = client.chat.completions.create(
    model=llm_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who is Nelson Mandela?"},
    ],
)


# print(response.choices[0].message.content)
# Create our own simple agent
class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        response = client.chat.completions.create(
            model=llm_name, temperature=0.0, messages=self.messages
        )
        return response.choices[0].message.content


prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

planet_mass:
e.g. planet_mass: Earth
returns the mass of a planet in the solar system

Example session:

Question: What is the combined mass of Earth and Mars?
Thought: I should find the mass of each planet using planet_mass.
Action: planet_mass: Earth
PAUSE

You will be called again with this:

Observation: Earth has a mass of 5.972 * 10^24 kg

You then output:

Answer: Earth has a mass of 5.972 * 10^24 kg

Next, call the agent again with:

Action: planet_mass: Mars
PAUSE

Observation: Mars has a mass of 0.64171 × 10^24 kg

You then output:

Answer: Mars has a mass of 0.64171 × 10^24 kg

Finally, calculate the combined mass.

Action: calculate: 5.972 + 0.64171
PAUSE

Observation: The combined mass is 6.61371 × 10^24 kg

Answer: The combined mass of Earth and Mars is 6.61371 × 10^24 kg
""".strip()


# Implement the functions actions
def calculate(what):
    return eval(what)


def planet_mass(name):
    masses = {
        "Mercury": 0.33011,
        "Venus": 4.8675,
        "Earth": 5.972,
        "Mars": 0.64171,
        "Jupiter": 1898.19,
        "Saturn": 568.34,
        "Uranus": 86.813,
        "Neptune": 102.413,
    }
    return f"{name} has a mass of {masses[name]} × 10^24 kg"


known_actions = {"calculate": calculate, "planet_mass": planet_mass}

# Create the agent
agent = Agent(system=prompt)

# response = agent("What is the mass of Earth?")
# print(response)

# response = planet_mass("Earth")
# print(response)

# next_response = f"Observation: {response}"
# print(next_response)
# response = agent(next_response)
# print(response)

# print(f"Agent Messages ---> {agent.messages}")

# ----- Complex query ---
# Complex Query
# question = "What is the combined mass of Earth and Mars and Saturn?"
# response = agent(question)
# print(response)

# next_prompt = "Observation: {}".format(planet_mass("Earth"))
# print(next_prompt)

# response = agent(next_prompt)
# print(response)
# next_prompt = "Observation: {}".format(planet_mass("Mars"))
# response = agent(next_prompt)
# print(response)
# next_prompt = "Observation: {}".format(planet_mass("Saturn"))
# response = agent(next_prompt)
# print(response)
# next_prompt = "Observation: the combined mass is {}".format(
#     calculate("5.972 + 0.64171 + 568.34")
# )
# response = agent(next_prompt)
# print(f"Final answer is {response}")

# Final Solution ---- Automate agent ----
import re
action_re = re.compile(r"^Action: (\w+): (.*)$")

#Create a query function
def query(question, max_turns=5):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            next_prompt = "Observation: {}".format(observation)
            print(next_prompt)
        else:
            return
        
# New Scenario: Calculating combined mass of Earth and Jupiter
question = "What is the combined mass of Earth and Jupiter?"
query(question)