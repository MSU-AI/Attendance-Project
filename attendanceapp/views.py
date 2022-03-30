from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

import cv2

from .models import Person, Photo, Group
from.forms import PersonForm

from interaction.frame_analyzer import FrameAnalyzer

fa = FrameAnalyzer()


def index(request):
    return HttpResponse("Hello! Welcome to the Attendence Project website. Check out the <a href='/admin'>admin panel</a> and sign in with username 'test' and password 'test'. Or view the <a href='./app'>app frontend</a>.")


def oldapp(request):
    return render(request, "attendance-app-old.html")


def app(request):
    return render(request, "attendance-app.html")


def user_register(request, groupid):

    # TODO: Add group support!

    if request.method == 'POST':

        form = PersonForm(request.POST, request.FILES)

        if form.is_valid():

            # Get demo group:
            
            group = Group.objects.filter(name=groupid)

            if not group:

                # Create demo group:
                
                group = Group(name=groupid)
                
                group.save()

            else:

                group = group[0]

            # Get Object:

            inst = form.save(commit=False)

            img = Photo(image=form.cleaned_data.get("image"), encoded=True)

            print(img.image.path)

            # Set date and time to now:

            inst.join_date = timezone.now()
            inst.group = group

            inst.save()

            # Create a new image

            img.person = inst

            img.save()

            image = cv2.imread(img.image.path)

            fa.set_frame(image, 'BGR')

            enc = fa._get_face_encoding()

            if enc is None:
                
                # Invalid face uploaded!
                
                return HttpResponse("Invalid face uploaded!")

            print(fa.frame)
            print(enc)

            inst.encodings = enc.tolist()

            inst.save()

            return HttpResponse("Thank you for registering!")

    else:

        form = PersonForm()

        return render(request, 'demo_create.html', {'form': form})
