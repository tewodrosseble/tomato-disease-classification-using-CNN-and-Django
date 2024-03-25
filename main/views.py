from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image
import io
import os
from django.http import HttpResponse

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')


def index(request):
    return render(request, 'main/index.html')

MODEL_PATH = 'model/tomato_model.h5'
if os.path.exists(MODEL_PATH):
    # Load the model
    model = tf.keras.models.load_model(MODEL_PATH)
else:
    print(f"Model file not found at {MODEL_PATH}")

model = None
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")


class_mapping = {
    1: 'Pepper__bell___healthy',
    2: 'Tomato__Target_Spot',
    3: 'Potato___healthy',
    4: 'Tomato_Late_blight',
    5: 'Tomato__Tomato_YellowLeaf__Curl_Virus',
    6: 'Tomato_Septoria_leaf_spot',
    7: 'Tomato_Bacterial_spot',
    8: 'Tomato__Tomato_mosaic_virus',
    9: 'PlantVillage',
    10: 'Tomato_Early_blight',
    11: 'Potato___Early_blight',
    12: 'Pepper__bell___Bacterial_spot',
    13: 'Tomato_healthy',
    14: 'Potato___Late_blight',
    15: 'Tomato_Leaf_Mold',
    16: 'Tomato_Spider_mites_Two_spotted_spider_mite'
}

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        # Get the uploaded image from the request
        uploaded_image = request.FILES['image']

        if model is not None:
            try:
                # Open and resize the image to 100x100 pixels
                image = Image.open(uploaded_image)
                image = image.resize((100, 100))

                # Convert the resized image to a NumPy array
                image = np.array(image)

                # Preprocess the image using ResNet50 preprocessing
                image = preprocess_input(image)

                # Perform inference on the preprocessed image
                predictions = model.predict(np.expand_dims(image, axis=0))

                # Get the predicted class index
                predicted_class_index = np.argmax(predictions, axis=1)[0]

                # Get the class name based on the predicted index
                predicted_class_name = class_mapping.get(predicted_class_index, 'Unknown')

                response_message = f'Predicted class: {predicted_class_name}'
                context = {'predicted_class': predicted_class_name}

                # Return the response as plain text
                # return HttpResponse(response_message)
                return render(request, 'main/predicted.html', context)
            except Exception as e:
                print(f"Error during prediction: {e}")
                context = {'error_message': 'Prediction failed.'}
                return render(request, 'prediction_result.html', context)
        else:
            context = {'error_message': 'Model not loaded.'}
            return render(request, 'prediction_result.html', context)
    else:
        return HttpResponse('Invalid request method')
        


# @csrf_exempt  # For demonstration purposes; consider CSRF protection in production
# def predict(request):
#     if request.method == 'POST':
#         # Get the uploaded image from the request
#         uploaded_image = request.FILES['image']

#         if model is not None:
#             try:
#                 # Preprocess the image using ResNet50 preprocessing
#                 image = Image.open(uploaded_image)
#                 image = image.resize((100, 100))  # Resize to match ResNet50 input size
#                 image = np.array(image)
#                 image = preprocess_input(image)

#                 # Perform inference on the preprocessed image
#                 predictions = model.predict(np.expand_dims(image, axis=0))

#                 # Process and return the prediction results
#                 predicted_class = np.argmax(predictions, axis=1)[0]  # Assuming classification
#                 return JsonResponse({'predicted_class': str(predicted_class)})
#             except Exception as e:
#                 print(f"Error during prediction: {e}")
#                 return JsonResponse({'error': 'Prediction failed.'})
#         else:
#             return JsonResponse({'error': 'Model not loaded.'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})

# @csrf_exempt  # For demonstration purposes; consider CSRF protection in production
# def predict(request):
#     if request.method == 'POST':
#         # Get the uploaded image from the request
#         uploaded_image = request.FILES['image']
        
#         # Load the pre-trained model
#         # model = tf.keras.models.load_model('../model/tomato_model.h5')
     

#         BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#         model_path = os.path.join(BASE_DIR, 'model', 'tomato_model.h5')
#         if os.path.exists(model_path):
#             model = tf.keras.models.load_model(model_path)
#         else:
#             print(f"Model file not found at {model_path}")
        
#         # Preprocess the image using ResNet50 preprocessing
#         image = Image.open(uploaded_image)
#         image = image.resize((224, 224))  # Resize to match ResNet50 input size
#         image = np.array(image)
#         image = preprocess_input(image)
    
#         predictions = model.predict(np.expand_dims(image, axis=0))
        
#         # Process and return the prediction results
#         predicted_class = np.argmax(predictions, axis=1)[0]  # Assuming classification
        
#         return JsonResponse({'predicted_class': str(predicted_class)})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})
