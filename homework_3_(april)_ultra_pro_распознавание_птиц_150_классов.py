# -*- coding: utf-8 -*-
"""Homework 3. (April) Ultra Pro. Распознавание птиц 150 классов

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1snhZZtUhfpc4Kb7f9VXJtk_Vqc-jz2B7

# Ultra Pro. Задача классификации на данных с kaggle
"""

# Commented out IPython magic to ensure Python compatibility.
# работа с изображениями
from tensorflow.keras.preprocessing import image
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
# модель и слои
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, GlobalMaxPooling2D, GlobalAveragePooling2D, Flatten

from keras.optimizers import Adam, Adadelta # оптимизаторы
import numpy as np # массивы для работы с сетью
import matplotlib.pyplot as plt # для вывода графиков
# %matplotlib inline

import random # случайные числа, для предпросмотра картинок
import math # нужно для округления
from google.colab import files #Для загрузки своей картинки

from PIL import Image #Отрисовка изображений

# подключем диск
from google.colab import drive
drive.mount('/content/drive')

#!rm -R /content/cars

# поставьте путь к файлу на своём диске
!cp -r "/content/drive/My Drive/AI/Birds/consolidated" "/content/sample_data"

# папка с папками картинок, рассортированных по категориям
TRAIN_PATH = '/content/sample_data/consolidated'

# размер выборки
BATCH_SIZE = 200

# ширина и высота изображения
IMG_WIDTH = 96
IMG_HEIGHT = 54

# генератор изображений
datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=5,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=0.05,
    horizontal_flip=False,
    fill_mode='nearest',
    validation_split=0.1
)

# обучающая выборка
train_generator = datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
#     color_mode='grayscale',
    shuffle=True,
    subset='training' # устанавливаем как набор для обучения
)

# проверочная выборка
validation_generator = datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
#     color_mode='grayscale',
    shuffle=True,
    subset='validation' # устанавливаем как валидационный набор
)

train_generator.class_indices

# Albatross
step = 100

for i in range(4):
    img_path = '{}/ALBATROSS/{}.jpg'.format(TRAIN_PATH, i+step)
    plt.figure(i)
    plt.imshow(image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH)))
plt.show()

# Alexandrine parakeet
for i in range(4):
    img_path = '{}/ALEXANDRINE PARAKEET/{}.jpg'.format(TRAIN_PATH, i+step)
    plt.figure(i)
    plt.imshow(image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH)))
plt.show()

# American avocet
for i in range(4):
    img_path = '{}/AMERICAN AVOCET/{}.jpg'.format(TRAIN_PATH, i+step)
    plt.figure(i)
    plt.imshow(image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH)))
plt.show()

model = Sequential()
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, GlobalMaxPooling2D, GlobalAveragePooling2D, AveragePooling2D, Flatten

model.add(Conv2D(256, (3, 3), padding='same', activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))

model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
model.add(Dropout(0.2))

model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.2))

model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
model.add(Conv2D(1024, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(512, activation='relu'))

model.add(Dense(len(train_generator.class_indices), activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0001), metrics=['accuracy'])

history = model.fit_generator(
    train_generator,
    steps_per_epoch = train_generator.samples // BATCH_SIZE,
    validation_data = validation_generator, 
    validation_steps = validation_generator.samples // BATCH_SIZE,
    epochs=60,
    verbose=1
)

plt.plot(history.history['accuracy'], 
         label='Доля верных ответов на обучающем наборе')
plt.plot(history.history['val_accuracy'], 
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

# Saving to file
model.save("birds150_classification.h5")
!ls

print(train_generator.samples // BATCH_SIZE)
print(validation_generator.samples // BATCH_SIZE)

# Trying lr=0.00001 and adding 40 epochs. And val_data 15% instead of 20%
model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.00001), metrics=['accuracy']) # loss= 'kullback_leibler_divergence'

history1 = model.fit_generator(
    train_generator,
    steps_per_epoch = train_generator.samples // BATCH_SIZE,
    validation_data = validation_generator, 
    validation_steps = validation_generator.samples // BATCH_SIZE,
    epochs=40,
    verbose=1
)

plt.plot(history1.history['accuracy'], 
         label='Доля верных ответов на обучающем наборе')
plt.plot(history1.history['val_accuracy'], 
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

# Saving to file
model.save("birds150_classification.h5")
!ls

files.download("birds150_classification.h5")

"""# Распознаем произвольные картинки из интернета"""

#Load model from file
from keras.models import load_model
files.upload()
model = load_model("birds150_classification.h5")

#Загружаем свою картинку
files.upload()
#Проверяем, что картинка загрузилась
!ls

img_path = 'tucan1.jpeg'
img = image.load_img(img_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
plt.imshow(img)
plt.show()

x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
prediction = np.argmax(model.predict(x))
print("Распознанный образ: ", prediction)
#print("Название распознанного образа: ", train_generator.class_indices.items(prediction, 0))

"""137 - Тукан, распознался правильно.  """

birds_list = list[]
birds_list = train_generator.class_indices
bird = [k for k, v in train_generator.class_indices.iteritems() if v == prediction][0]

"""# Пробуем дообучить и улучшить модель"""

files.upload()

!ls

from keras.models import load_model
model1 = load_model("birds150_classification.h5")

#добавляю 20 эпох, batch size увеличенв 2 раза (100), проверочная выборка 10% вместо 15%, шаг уменьшен в 10 раз 0.00001
#картинки перемещены с гугл диска в директорию колаба, скорость обучения увеличилась в 2 раза
model1.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.00001), metrics=['accuracy']) # loss= 'kullback_leibler_divergence'

history2 = model1.fit_generator(
    train_generator,
    steps_per_epoch = train_generator.samples // BATCH_SIZE,
    validation_data = validation_generator, 
    validation_steps = validation_generator.samples // BATCH_SIZE,
    epochs=20,
    verbose=1
)

plt.plot(history2.history['accuracy'], 
         label='Доля верных ответов на обучающем наборе')
plt.plot(history2.history['val_accuracy'], 
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

model1.save_weights("birds150_classification.h5")
files.download("birds150_classification.h5")

#точность плохо растет, усиливаем модель 
model2 = Sequential()
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, GlobalMaxPooling2D, GlobalAveragePooling2D, AveragePooling2D, Flatten

model2.add(Conv2D(256, (3, 3), padding='same', activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
model2.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
model2.add(MaxPooling2D(pool_size=(3, 3)))

model2.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
model2.add(Dropout(0.1))

model2.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
model2.add(MaxPooling2D(pool_size=(3, 3)))
model2.add(Dropout(0.2))

model2.add(Conv2D(1024, (3, 3), padding='same', activation='relu'))
model2.add(Conv2D(1024, (3, 3), padding='same', activation='relu'))
model2.add(MaxPooling2D(pool_size=(3, 3)))
model2.add(Dropout(0.3))

model2.add(Flatten())
model2.add(Dense(1024, activation='relu'))
model2.add(Dense(1024, activation='relu'))

model2.add(Dense(len(train_generator.class_indices), activation='softmax'))

model2.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0001), metrics=['accuracy'])

history3 = model2.fit_generator(
    train_generator,
    steps_per_epoch = train_generator.samples // BATCH_SIZE,
    validation_data = validation_generator, 
    validation_steps = validation_generator.samples // BATCH_SIZE,
    epochs=40,
    verbose=1
)

plt.plot(history3.history['accuracy'], 
         label='Доля верных ответов на обучающем наборе')
plt.plot(history3.history['val_accuracy'], 
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

#BATCH_SIZE = 200

model2.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.00001), metrics=['accuracy'])

history4 = model2.fit_generator(
    train_generator,
    steps_per_epoch = train_generator.samples // BATCH_SIZE,
    validation_data = validation_generator, 
    validation_steps = validation_generator.samples // BATCH_SIZE,
    epochs=20,
    verbose=1
)

plt.plot(history4.history['accuracy'], 
         label='Доля верных ответов на обучающем наборе')
plt.plot(history4.history['val_accuracy'], 
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

plt.plot(history4.history['loss'], 
         label='Ошибка на обучающем наборе')
plt.plot(history4.history['val_loss'], 
         label='Ошибка на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Ошибка')
plt.legend()
plt.show()

model2.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.00001), metrics=['accuracy'])

history5 = model2.fit_generator(
    train_generator,
    steps_per_epoch = train_generator.samples // BATCH_SIZE,
    validation_data = validation_generator, 
    validation_steps = validation_generator.samples // BATCH_SIZE,
    epochs=40,
    verbose=1
)

plt.plot(history5.history['accuracy'], 
         label='Доля верных ответов на обучающем наборе')
plt.plot(history5.history['val_accuracy'], 
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

plt.plot(history5.history['loss'], 
         label='Ошибка на обучающем наборе')
plt.plot(history5.history['val_loss'], 
         label='Ошибка на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Ошибка')
plt.legend()
plt.show()

model2.save("birds150_classification.h5")
files.download("birds150_classification.h5")

#а если еще уменьшить шаг
model2.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.000001), metrics=['accuracy'])

history6 = model2.fit_generator(
    train_generator,
    steps_per_epoch = train_generator.samples // BATCH_SIZE,
    validation_data = validation_generator, 
    validation_steps = validation_generator.samples // BATCH_SIZE,
    epochs=10,
    verbose=1
)

plt.plot(history6.history['accuracy'], 
         label='Доля верных ответов на обучающем наборе')
plt.plot(history6.history['val_accuracy'], 
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

plt.plot(history6.history['loss'], 
         label='Ошибка на обучающем наборе')
plt.plot(history6.history['val_loss'], 
         label='Ошибка на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Ошибка')
plt.legend()
plt.show()

files.upload()
img_path = 'hgoose1.jpg'
img = image.load_img(img_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
plt.imshow(img)
plt.show()

x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
prediction = np.argmax(model2.predict(x))
print("Распознанный образ: ", prediction)
#print("Название распознанного образа: ", train_generator.class_indices.items(prediction, 0))

"""не правильно"""

files.upload()
img_path = 'owl.jpg'
img = image.load_img(img_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
plt.imshow(img)
plt.show()

x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
prediction = np.argmax(model2.predict(x))
print("Распознанный образ: ", prediction)
#print("Название распознанного образа: ", train_generator.class_indices.items(prediction, 0))

"""не правильно"""

files.upload()
img_path = 'tucan.jpeg'
img = image.load_img(img_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
plt.imshow(img)
plt.show()

x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
prediction = np.argmax(model2.predict(x))
print("Распознанный образ: ", prediction)
#print("Название распознанного образа: ", train_generator.class_indices.items(prediction, 0))

"""правильно

"""