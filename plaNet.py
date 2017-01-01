# plaNet.py
# Adapting VGG's convolutional neural network to classify images of planets.
# Based on tutorials and lessons by Jeremy Howard.

from utils.utils import *

path = 'data/'
vgg = Vgg16()
model = vgg.model

def get_bn_da_layers(p):
    return [
        MaxPooling2D(input_shape=conv_layers[-1].output_shape[1:]),
        Flatten(),
        Dropout(p),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(p),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(p),
        Dense(9, activation='softmax')
        ]

p = 0.8

# Grab all of VGG's convolutional layers.
last_conv_idx = [i for i,l in enumerate(model.layers) if type(l) is Convolution2D][-1]
conv_layers = model.layers[:last_conv_idx+1]
conv_model = Sequential(conv_layers)

# Load training and validation data.
batches = get_batches(path+'train')
val_batches = get_batches(path+'valid', shuffle=False)
val_classes = val_batches.classes
trn_classes = batches.classes
val_labels = onehot(val_classes)
trn_labels = onehot(trn_classes)

# Calculate the values of the last convolutional layer in VGG.
conv_feat = conv_model.predict_generator(batches, batches.nb_sample)
conv_val_feat = conv_model.predict_generator(val_batches, val_batches.nb_sample)

# Use data augmentation to increase available data.
gen_t = image.ImageDataGenerator(rotation_range=15, height_shift_range=0.05, 
                shear_range=0.1, channel_shift_range=20, width_shift_range=0.1)
da_batches = get_batches(path+'train', gen_t, shuffle=False)

# Re-calculate convolutional model output with the newly augmented dataset.
da_conv_feat = conv_model.predict_generator(da_batches, da_batches.nb_sample*5)

# Combine augmented features and original features.
da_conv_feat = np.concatenate([da_conv_feat, conv_feat])
# Account for increased batch size.
da_trn_labels = np.concatenate([trn_labels]*6)

bn_model = Sequential(get_bn_da_layers(p))
bn_model.compile(Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
# Train the model on the augmented data.
bn_model.fit(da_conv_feat, da_trn_labels, nb_epoch=1, validation_data=(conv_val_feat, val_labels))

# Decrease learning rate.
bn_model.optimizer.lr=0.01

# Run a few more epochs.
bn_model.fit(da_conv_feat, da_trn_labels, nb_epoch=4, validation_data=(conv_val_feat, val_labels))

# Decrease learning rate even more.
bn_model.optimizer.lr=0.0001

# Run a few more epochs.
bn_model.fit(da_conv_feat, da_trn_labels, nb_epoch=4, validation_data=(conv_val_feat, val_labels))

# Save weights.
bn_model.save_weights(path+'models/da_conv.h5')