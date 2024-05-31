import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

import numpy
#load the trained model to classify sign
from keras.models import load_model
model = load_model('model.h5')

#dictionary to label all traffic signs class.
classes = { 0:'Speed limit (20km/h)',
            1:'Speed limit (30km/h)',      
            2:'Speed limit (50km/h)',       
            3:'Speed limit (60km/h)',      
            4:'Speed limit (70km/h)',    
            5:'Speed limit (80km/h)',      
            6:'End of speed limit (80km/h)',     
            7:'Speed limit (100km/h)',    
            8:'Speed limit (120km/h)',     
            9:'No passing',   
            10:'No passing veh over 3.5 tons',     
            11:'Right-of-way at intersection',     
            12:'Priority road',    
            13:'Yield',     
            14:'Stop',       
            15:'No vehicles',       
            16:'Veh > 3.5 tons prohibited',       
            17:'No entry',       
            18:'General caution',     
            19:'Dangerous curve left',      
            20:'Dangerous curve right',   
            21:'Double curve',      
            22:'Bumpy road',     
            23:'Slippery road',       
            24:'Road narrows on the right',  
            25:'Road work',    
            26:'Traffic signals',      
            27:'Pedestrians',     
            28:'Children crossing',     
            29:'Bicycles crossing',       
            30:'Beware of ice/snow',
            31:'Wild animals crossing',      
            32:'End speed + passing limits',      
            33:'Turn right ahead',     
            34:'Turn left ahead',       
            35:'Ahead only',      
            36:'Go straight or right',      
            37:'Go straight or left',      
            38:'Keep right',     
            39:'Keep left',      
            40:'Roundabout mandatory',     
            41:'End of no passing',      
            42:'End no passing veh > 3.5 tons' }

                 
#initialise GUI
top=tk.Tk()
top.geometry('800x600')
top.title('Phân loại biển báo giao thông ')
top.configure(background='#ffffff')

label=Label(top,background='#ffffff', font=('arial',15,'bold'))
sign_image = Label(top)

def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((30,30))
    # Chuyển đổi hình ảnh thành mảng numpy
    image_array = numpy.array(image)
    # Nếu hình ảnh có 4 kênh màu, loại bỏ kênh thứ tư
    if image_array.shape[-1] == 4:
        image_array = image_array[..., :3]
    # Nếu hình ảnh chỉ có 1 kênh màu, sao chép nội dung của kênh màu để tạo thành 3 kênh màu
    elif image_array.shape[-1] == 1:
        image_array = numpy.concatenate([image_array]*3, axis=-1)
    # Mở rộng kích thước của mảng để phù hợp với yêu cầu của mô hình
    image_array = numpy.expand_dims(image_array, axis=0)
    print(image_array.shape)
    
    # Dự đoán classes
    pred_probabilities = model.predict(image_array)[0]
    pred = pred_probabilities.argmax(axis=-1)
    sign = classes[pred]
    sign_id = pred
    sign = f'{sign_id}: {classes[sign_id]}'
    print(sign)
    label.configure(foreground='#011638', text=sign)
 
   

def show_classify_button(file_path):
    classify_b=Button(top,text="Phân loại",command=lambda: classify(file_path),padx=10,pady=5)
    classify_b.configure(background='#c71b20', foreground='white',font=('arial',10,'bold'))
    classify_b.place(relx=0.79,rely=0.46)

def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass

upload=Button(top,text="Load Image",command=upload_image,padx=10,pady=5)
upload.configure(background='#c71b20', foreground='white',font=('arial',10,'bold'))

upload.pack(side=BOTTOM,pady=50)
sign_image.pack(side=BOTTOM,expand=True)
label.pack(side=BOTTOM,expand=True)
heading = Label(top, text="Phân loại biển báo giao thông",pady=10, font=('arial',20,'bold'))
heading.configure(background='#ffffff',foreground='#364156')

heading1 = Label(top, text="Bùi Lê Nhật Trường MSSV: B2005700",pady=5, font=('arial',20,'bold'))
heading1.configure(background='#ffffff',foreground='#364156')

heading.pack()
heading1.pack()

top.mainloop()