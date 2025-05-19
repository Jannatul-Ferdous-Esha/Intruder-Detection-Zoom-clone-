from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random
import string
import base64
import os
import cv2
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
from insightface.app import FaceAnalysis
from numpy.linalg import norm
from PIL import Image
from io import BytesIO
import glob
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import base64


app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)


# Prepare known embeddings
known_embeddings = []
known_names = []


def load_known_data():
    data_dir = os.path.join(settings.BASE_DIR, 'meeting_app', 'static', 'data')

    pattern = os.path.join(data_dir, '*.jpg')
    
    # Print the pattern path to debug
    print(f"🔍 Looking for files matching: {repr(pattern)}")

    data_paths = glob.glob(pattern)
    
    print(f"🟢 Found {len(data_paths)} image(s) in {data_dir}")
    img_path = r"F:\zoom-clone-main\zoom-clone-main\meeting_app\static\data\maisha.jpg"
    img = cv2.imread(img_path)
    if img is None:
        print("❌ Couldn't read image directly.")
    else:
        print("✅ Read image directly.")

    for path in data_paths:
        print(f"➡️ Reading {path}")
        img = cv2.imread(path)
        if img is None:
            print(f"⚠️ Could not read image: {path}")
            continue
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = app.get(img_rgb)
        if faces:
            face = faces[0]
            known_embeddings.append(face['embedding'])
            known_names.append(os.path.splitext(os.path.basename(path))[0])
        else:
            print(f"⚠️ No face found in: {path}")
# def load_known_data():
#     data_paths = glob.glob('static/data/*.jpg')  # Ensure your path is correct
#     for path in data_paths:
#         img = cv2.imread(path)
#         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         faces = app.get(img_rgb)
#         if faces:
#             face = faces[0]
#             known_embeddings.append(face['embedding'])
#             known_names.append(os.path.splitext(os.path.basename(path))[0])
# def load_known_data():
#     data_paths = glob.glob('static/data/*.jpg')
#     print(f"Loading known faces from {len(data_paths)} files.")
#     for path in data_paths:
#         img = cv2.imread(path)
#         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         faces = app.get(img_rgb)
#         if faces:
#             face = faces[0]
#             known_embeddings.append(face['embedding'])
#             known_names.append(os.path.splitext(os.path.basename(path))[0])
#         else:
#             print(f"⚠️ No face found in: {path}")
load_known_data()
import uuid  # for generating unique filenames

@csrf_exempt
def process_face(request):
    if request.method == "POST":
        image_data = request.POST.get("image_data")
        if not image_data:
            return JsonResponse({"error": "No image data"}, status=400)

        try:
            # Decode base64 image
            header, encoded = image_data.split(",", 1)
            image_data = base64.b64decode(encoded)
            np_arr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Save the photo with a unique name
            filename = f"captured_{uuid.uuid4().hex}.jpg"
            save_path = os.path.join('static', 'captured_photos', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            cv2.imwrite(save_path, frame)

            # Continue with recognition
            test_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            test_faces = app.get(test_rgb)

            if not known_embeddings:
                return JsonResponse({"error": "No known embeddings loaded."}, status=500)

            if test_faces:
                test_embedding = test_faces[0]['embedding']
                similarities = [
                    np.dot(test_embedding, emb) / (norm(test_embedding) * norm(emb))
                    for emb in known_embeddings
                ]

                if similarities:
                    best_idx = int(np.argmax(similarities))
                    best_score = similarities[best_idx]

                    if best_score > 0.5:
                        name = known_names[best_idx]
                        print(f"This is {name} with score {best_score:.3f}")
                        return JsonResponse({"redirect_url": "/insider/"})

        except Exception as e:
            print("Error in processing face:", e)
            return JsonResponse({"error": "Processing failed"}, status=500)

    return JsonResponse({"redirect_url": "/intruder/"})


# @csrf_exempt
# def process_face(request):
#     if request.method == "POST":
#         image_data = request.POST.get("image_data")
#         if not image_data:
#             return JsonResponse({"error": "No image data"}, status=400)

#         try:
#             header, encoded = image_data.split(",", 1)
#             image_data = base64.b64decode(encoded)
#             np_arr = np.frombuffer(image_data, np.uint8)
#             frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
#             test_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             test_faces = app.get(test_rgb)

#             if test_faces:
#                 test_embedding = test_faces[0]['embedding']
#                 similarities = [
#                     np.dot(test_embedding, emb) / (norm(test_embedding) * norm(emb))
#                     for emb in known_embeddings
#                 ]
#                 best_idx = int(np.argmax(similarities))
#                 best_score = similarities[best_idx]

#                 if best_score > 0.5:
#                     name = known_names[best_idx]
#                     print(f"This is {name} with score {best_score:.3f}")

#                     now = datetime.now()
#                     # You can also log to a CSV or database here
#                     return JsonResponse({"redirect_url": "/insider/"})
#         except Exception as e:
#             print("Error in processing face:", e)
#             return JsonResponse({"error": "Processing failed"}, status=500)

#     print("Intruder detected")
#     return JsonResponse({"redirect_url": "/intruder/"})
# def load_known_data():
#     data_paths = glob.glob('static/data/*.jpg')
#     for path in data_paths:
#         img = cv2.imread(path)
#         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         faces = app.get(img_rgb)
#         if faces:
#             face = faces[0]
#             embedding = face['embedding']
#             name = os.path.splitext(os.path.basename(path))[0]
#             known_embeddings.append(embedding)
#             known_names.append(name)

# load_known_data()

# def process_face(request):
#     image_data = request.POST.get("image_data")
#     header, encoded = image_data.split(",", 1)
#     image_data = base64.b64decode(encoded)
#     np_arr = np.frombuffer(image_data, np.uint8)
#     frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#     # Detect faces
#     test_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     test_faces = app.get(test_rgb)

#     recognized = False
#     if test_faces:
#         test_embedding = test_faces[0]['embedding']

#         similarities = []
#         for known_embedding in known_embeddings:
#             sim = np.dot(test_embedding, known_embedding) / (norm(test_embedding) * norm(known_embedding))
#             similarities.append(sim)

#         best_match_idx = int(np.argmax(similarities))
#         best_score = similarities[best_match_idx]

#         if best_score > 0.5:  # Threshold for similarity (adjust if needed)
#             name = known_names[best_match_idx]
#             print(f"This is {name} with similarity score {round(best_score, 3)}")
#             recognized = True
#             # Log the attendance
#             now = datetime.now()
#             m_d = now.strftime("%x")
#             m_t = now.strftime("%X")
#             rows = [name, m_d, m_t]
#             # Log into CSV or database if required

#             # Redirect to insider page
#             return JsonResponse({"redirect_url": "/insider/"})
    
#     # If no match, consider as intruder
#     print("Intruder detected")
#     return JsonResponse({"redirect_url": "/intruder/"})

# def capture_video(request):
#     return render(request, 'capture_video.html')
@login_required
def capture_video(request):
    return render(request, 'capture_video.html', {'name': request.user.first_name})
@login_required
def insider(request):
    return render(request, 'dashboard.html', {'name': request.user.first_name})
@login_required
def intruder(request):
    return render(request, 'intruder.html')
@login_required
def capture_photo(request):
    return render(request, 'capture_photo.html', {'name': request.user.first_name})
@login_required
def insider_view(request):
    # Your logic for the insider view
    return render(request, 'dashboard.html',{'name': request.user.first_name})
@login_required
def intruder_view(request):
    # Your logic for the intruder view
    return render(request, 'intruder.html')
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'success': "Registration successful. Please login."})
        else:
            error_message = form.errors.as_text()
            return render(request, 'register.html', {'error': error_message})

    return render(request, 'register.html')


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/capture_photo")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.first_name})

# @login_required
# def videocall(request):
#     return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

@login_required
def videocall(request):
    room_id = request.GET.get("roomID", "")
    return render(request, 'videocall.html', {
        'name': request.user.first_name + " " + request.user.last_name,
        'roomID': room_id
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")

# @login_required
# def join_room(request):
#     if request.method == 'POST':
#         roomID = request.POST['roomID']
#         return redirect("/meeting?roomID=" + roomID)
#     return render(request, 'joinroom.html')
# @login_required
# # def join_room(request):
# #     if request.method == 'POST':
# #         roomID = request.POST['roomID']
# #         # Redirect to the actual route where your video call logic lives
# #         return redirect(reverse('videocall') + f"?roomID={roomID}")
# #     return render(request, 'joinroom.html')
# def join_room(request):
#     if request.method == 'POST':
#         roomID = request.POST['roomID']
#         return redirect(reverse('meeting') + f"?roomID={roomID}")
#     return render(request, 'joinroom.html')
@login_required
def create_meeting(request):
    # Generate a random roomID for the meeting
    roomID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Redirect to the video call page with the generated roomID
    return redirect(f'/meeting/?roomID={roomID}')

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        
        return redirect(reverse('meeting') + f'?roomID={roomID}')
    return render(request, 'joinroom.html')