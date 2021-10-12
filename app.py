import asyncio
import json
import signal
import sys
import uuid

import aiofiles
import aiohttp
import numpy as np
import tensorflow as tf
from aiofiles import base
from tensorflow.python.ops.metrics_impl import precision

base_url = "https://agrify.ngrok.io/"

get_images = "api/Imgsaves/GetUnproceessedImages"

update_images = "api/Imgsaves/UpdateImages"


loop = asyncio.get_event_loop()
model = tf.keras.models.load_model('model/model.h5')



def prepare_image(file):
    img = tf.keras.preprocessing.image.load_img(file, target_size=(224,224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

def predict_image(image_path):
    preprocessed_image = prepare_image(image_path)
    predictions = model.predict(preprocessed_image)
    result = predictions.argmax(axis=1)
    prediction = "None"
    if result == 0:
        prediction = "predicted : leaf_spot, {}".format(predictions[0][0])
    if result == 1:
        prediction = "predicted : common_rust, {}".format(predictions[0][1])
    if result == 2:
        prediction = "predicted : leaf_blight, {}".format(predictions[0][2])
    if result == 3:
        prediction = "predicted : healthy, {}".format(predictions[0][3])

    return prediction

async def get_json(client, url):  
    async with client.get(url) as response:
        assert response.status == 200
        return await response.read()

async def put_json(client, url, json_data):  
    async with client.put(url, json=json_data) as response:
        assert response.status == 200
        return await response.read()

async def get_image(client, url):  
    async with client.get(url) as response:
        if response.status == 200:
            filename = './model_data/{}.{}'.format(uuid.uuid1(), url.split(".")[-1])
            f = await aiofiles.open(filename, mode='wb')
            await f.write(await response.read())
            await f.close()
            return filename

async def get_reddit_top(subreddit):
    client = aiohttp.ClientSession(loop=loop)
    while True:
       
        path_append = base_url + get_images
        data1 = await get_json(client, path_append)
        j = json.loads(data1.decode('utf-8'))

        if(len(j)> 0):   

            new_data = list()
            for object in j:
                file_name = "{}api/Imgsaves/getImageFile/{}".format(base_url, object["imagpath"].split("/")[-1])  
                image_path = await get_image(client, file_name)
                if image_path is not None:
                    prediction = predict_image(image_path=image_path)
                    object["disease"] = prediction
                object["processed"] = True
                new_data.append(object)
            
            print(await put_json(client, base_url + update_images, new_data))
        await asyncio.sleep(10)

def signal_handler(signal, frame):  
    loop.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

asyncio.ensure_future(get_reddit_top('python'))  
loop.run_forever()
