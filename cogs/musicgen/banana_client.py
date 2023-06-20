import base64
import datetime
import json
import tempfile
import banana_dev as banana
import os

from cogs.musicgen.helpers import slugify

api_key = os.getenv("BANANA_API_KEY")
model_key = os.getenv("BANANA_MODEL_KEY")

def decode_audio(audio):
  # Remove the "b'" and the "'" at the end of the string
  raw = audio[2:-1]
  audio = base64.b64decode(bytes(raw, 'utf-8'))
  return audio

def generate_musicgen(prompt: str, duration = 8 ):

  model_inputs = {
    "prompt": prompt,
    "duration": duration
  }

  results = banana.run(api_key, model_key, model_inputs)

  if results.get('message') != "success":
    raise Exception('API ERROR: ' + str(results))

  outputs = results.get('modelOutputs')[0].get('outputs')

  uuid = results.get('id')

  audio = decode_audio(outputs[0].get('audio'))

  # Create folder of date if not exists YYYY-MM-DD
  date = datetime.now().strftime("%Y-%m-%d")
  folder = f"music_generations/{date}"
  if not os.path.exists(folder):
    os.makedirs(folder)

  fileNB = len(os.listdir(folder))
  filename = uuid + '-'+ slugify(prompt).replace('_', '-') + f"-{fileNB}.mp3"
  filename = filename[:200]
  
  path = os.path.join(folder, filename)

  with open(path, "wb") as f:
    f.write(audio)

  return path, filename

if __name__ == "__main__":
  # prompt = "drum and bass beat with intense percussions"
  # duration = 8
  # outputs = generate_musicgen(prompt, duration)

  # with open("outputs.json", "w") as f:
  #   f.write(json.dumps(outputs, indent=2))

  with open("results.json", "r") as f:
    outputs = json.loads(f.read())

  outputs = outputs.get('modelOutputs')[0].get('outputs')
  # print(outputs)
  
  for i, res in enumerate(outputs):
    raw = res.get("audio")[2:-1]
    print(raw[:10], raw[-10:])
    save_audio(bytes(raw, 'utf-8'), f"{i}")

      