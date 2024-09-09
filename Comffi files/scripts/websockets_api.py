import io
from PIL import Image
import random
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

def load_prompt(user_prompt, steps, workflow_file = ''):

    #load workflow from json
    workflow_file_name = "workflow_api_flux_dev.json"
    if workflow_file == 'Y':
        workflow_file_name = "workflow_api_flux_dev_lora.json"
    elif workflow_file == 'T':
        workflow_file_name = "workflow_api_lora_Tami.json"

    with open(workflow_file_name, "r", encoding="utf-8") as f:
        workflow_data = f.read()

    prompt = json.loads(workflow_data)
    #set the text prompt for our positive CLIPTextEncode
    prompt["6"]["inputs"]["text"] = user_prompt

    #set the steps value
    prompt["17"]["inputs"]["steps"] = steps
    #set the seed for our KSampler node
    prompt["25"]["inputs"]["noise_seed"] =  random.randint(1,4294967294)

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    
        # Get images as byte data
    images = get_images(ws, prompt)
    
    processed_images = {}  # Dictionary to store processed image objects

    # Process images into PIL Image objects
    for node_id in images:
        processed_images[node_id] = []  # Initialize list for each node_id
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))  # Load image from bytes

            # Save image to BytesIO object
            image_byte_array = io.BytesIO()
            image.save(image_byte_array, format='PNG')
            image_byte_array.seek(0)  # Move cursor to the beginning of the BytesIO object

            # Append the BytesIO object to the list for this node_id
            processed_images[node_id].append(image_byte_array)

    return processed_images

#Commented out code to display the output images:


