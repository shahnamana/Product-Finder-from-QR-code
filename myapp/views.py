from django.shortcuts import render
# from django.shortcuts import render_to_response
import folium
from django.conf import settings
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, resolve
from django.views import generic
from qrcode_project_final.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL


import os
import numpy as np
import qrcode



def show_details(request, num = 1):
    # print("The num value is ", num)
    product_database = list(ProductDet.objects.values())
    image_list = ProductDet
    # print("The image l")
    # print("\n\n\n\n\n ", image_list, "\n\n\n\n\n\n\n")
    finallist = []
    for i in product_database:
        if i['product_id'] == num:
            finallist.append(i)
    finallist = finallist[0]
    image_url = settings.MEDIA_ROOT+"\\"+finallist['product_image']
    # print("the value in product image is ", image_url)
    # print("Final List is ", finallist)
    address_database = list(Address.objects.values())
    # print()
    final_list = []
    # print("\n\n\n\n\n\n\n\n\n\n\n\n", type(address_database))
    # for i in address_database:
    #     print(i, "\n\n\n\n")
    for i in address_database:
        if i['product_det_id'] == num:
            final_list.append(i)
    google_maps_url = 'https://maps.google.com/?q='
    # https://maps.google.com/?q=<lat>,<lng>
    for i in final_list:
        lat_long = [float(i['latitude']), float(i['longitude'])]
        # print(lat_long)
        m = folium.Map(lat_long, zoom_start=12, height = 306, width = 506.5)
        icon = folium.Icon(color='red')
        folium.Marker(location=lat_long, icon=icon).add_to(m)
        m = m._repr_html_()
        i['gmaps'] = google_maps_url + str(i['latitude']) + ',' + str(i['longitude'])
        i['map'] = m

    # print("the final list is \n", final_list,"\n\n\n\n\n")
    context = {'address_fields':final_list, "product_details":finallist, 'image_url':image_list, 'media_url': MEDIA_URL}

    return render(request,'index.html',context=context)


def generate_qr_main(product_id):
    #the site address should be in data variable
    data = 'http://127.0.0.1:8000/show/'+str(product_id)
    # instantiate QRCode object
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    # add data to the QR code
    qr.add_data(data)
    # compile the data into a QR code array
    qr.make()
    # print the image shape
    # print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
    # transfer the array into an actual image
    img = qr.make_image(fill_color="black", back_color="white")
    # save it to a file
    path = settings.MEDIA_ROOT
    image_path = path+ r"\qrcodes"+ "\\"+str(product_id)+".png"
    # print("The img list is ", image_path)
    # print("\n\nThe final path is ", image_path, "\n\n\n\n\n")
    img.save(image_path)
    image_path = image_path.split(r'media',1)[1]
    image_path = "\\media"+image_path
    return image_path

def dynamic_articles_view(request):
    # context['object_list'] = article.objects.filter(title__icontains=request.GET.get('search'))
    # a= request.POST.get('search')
    # print("The a is ",a)
    # url_to_go = 'http://127.0.0.1:8000/show/'+str(a)
    # return
    search_query = request.GET.get('search_box', None)
    return show_details(request, int(a))


def qr_code_generate_func(request):
    if request.method == 'POST':
        product_id = request.POST['productId']
        # print("The entered value is ", product_id)
        path = settings.MEDIA_ROOT
        img_list = os.listdir(path + "/qrcodes"+"/")
        img_list = [i[:-4] for i in img_list]
        img_list_int = [int(i) for i in img_list]
        if product_id in img_list_int:
            path_to_qr_image = "\\media\\qrcodes\\"+str(product_id)+".png"
        else:
            path_to_qr_image = generate_qr_main(product_id)

        context = {'path_to_qr_image':path_to_qr_image}
        return render(request, 'qrcode_display.html', context=context)

    form = {}
    return render(request, 'qrcode_generator_form.html',context=form)


def all_products(request):
    product_database = list(ProductDet.objects.values())

    return render(request, 'all_products.html', context={'product_database':product_database, 'media_url': MEDIA_URL, 'len_db':[i for i in range(len(product_database))]} )


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
