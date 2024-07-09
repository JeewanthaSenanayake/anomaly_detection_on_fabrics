from skimage.metrics import structural_similarity as ssim
import cv2
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, Conv2DTranspose, LeakyReLU
from matplotlib.backends.backend_agg import FigureCanvasAgg

def architecture_MVTEC(input_shape=(128, 128, 1), latent_dim=100):

    parameters = dict()
    N_layers = 9
    parameters["filters"] = [32, 32, 32, 64, 64, 128, 64, 32, latent_dim]
    parameters["kernel_size"] = [4, 4, 3, 4, 3, 4, 3, 3, 8]
    parameters["strides"] = [2, 2, 1, 2, 1, 2, 1, 1, 1]
    parameters["padding"] = ["same" for _ in range(N_layers-1)] + ["valid"]

    # Input
    inputs = Input(shape=input_shape)
    x = inputs

    # Encoder
    for i in range(0, N_layers):
        x = Conv2D(
          filters=parameters["filters"][i],
          kernel_size=parameters["kernel_size"][i],
          strides=parameters["strides"][i],
          padding=parameters["padding"][i])(x)
        x = LeakyReLU(alpha=0.2)(x)

    # Decoder
    for i in reversed(range(0, N_layers)):
        x = Conv2DTranspose(
          filters=parameters["filters"][i],
          kernel_size=parameters["kernel_size"][i],
          strides=parameters["strides"][i],
          padding=parameters["padding"][i])(x)
        x = LeakyReLU(alpha=0.2)(x)

    # Output
    x = Conv2DTranspose(
      filters=input_shape[2],
      kernel_size=(3, 3),
      strides=(1, 1),
      padding="same")(x)

    outputs = x

    # Autoencoder
    autoencoder = Model(inputs, outputs, name="autoencoder")

    return autoencoder


def generate_AE(latent_dim=100, training_loss="ssim", batch_size=8):

    autoencoder = architecture_MVTEC(input_shape=(128, 128, 1), latent_dim=latent_dim)
    path_to_load_model = f"ML_Model/model_weights/carpet/"
    name = f"a_{latent_dim}_loss_{training_loss}_batch_{batch_size}.hdf5"
    path_to_load_model += name
    autoencoder.load_weights(path_to_load_model)

    return autoencoder


def reconstruct_img( img_input, autoencoder):

    img_in_size = (1024, 1024)
    img_resized_size = (512, 512)
    crop_size = (128, 128)
    step = 32

    img_input = img_input.astype("float32") / 255.0

    img_resized = cv2.resize(img_input, img_resized_size)

    img_out = np.zeros(shape=img_resized.shape)
    overlap = np.zeros(shape=img_resized.shape)

    for x in range(0 , img_resized.shape[0] - crop_size[0] + 1 , step):
        for y in range(0 , img_resized.shape[1] - crop_size[1] + 1 , step):

            x_start = x
            x_end = x_start + crop_size[0]
            y_start = y
            y_end = y + crop_size[1]
            crop = img_resized[x_start:x_end, y_start:y_end]

            X_test = []
            X_test.append(crop)
            X_test = np.array(X_test)
            X_test = np.expand_dims(X_test, axis=-1)
            img_predict = autoencoder.predict(X_test)

            img_out[(x_start+1):(x_end-1), (y_start+1):(y_end-1)] += img_predict[0, 1:-1, 1:-1, 0]
            overlap[(x_start+1):(x_end-1), (y_start+1):(y_end-1)] += np.ones(shape=crop_size)[1:-1, 1:-1]

    overlap = np.where(overlap == 0, 1, overlap)
    img_out = img_out/overlap
    img_out = cv2.resize(img_out, img_in_size)
    img_out = img_out*255

    return img_out


def create_loss_image(original_img , reconstructed_img):

    img_original = original_img.astype("float32") / 255.0
    img_predicted = reconstructed_img.astype("float32") / 255.0

    ssim_index, gradient, ssim_image = ssim(img_original[1:-1, 1:-1], img_predicted[1:-1, 1:-1], gradient=True, full=True, multichannel=False, data_range=1.0 )
    DSSIM_value = (1- ssim_index)/2

    # Create the figure and plot the SSIM image
    fig, ax = plt.subplots()
    im = ax.imshow(1 - ssim_image, vmax=1, cmap="jet")
    ax.axis('off')

    # Render the figure to a buffer
    canvas = FigureCanvasAgg(fig)
    canvas.draw()

    # Convert the figure to an image array
    width, height = fig.get_size_inches() * fig.get_dpi()
    loss_figure = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(int(height), int(width), 3)

    plt.close(fig)  # Close the figure to release memory

    return loss_figure, DSSIM_value


def detect_defects(original_image, autoencoder, normal_threshold):
    reconstructed_img = reconstruct_img(original_image, autoencoder)
    
    loss_figure, DSSIM_value = create_loss_image(original_image , reconstructed_img)
   
    if(DSSIM_value > normal_threshold):
        return loss_figure, True
    else:
        return loss_figure, False
    


# if __name__ == "__main__":

#     dataset = "carpet"
#     train_or_test = "test"
#     category = "color"
#     img_name = "009.png"

#     ## read/get original image
#     original_image = cv2.imread(f"data/{dataset}/{train_or_test}/{category}/{img_name}", 0)  
    
#     # 1) set threshold
#     normal_threshold = 0.18039123161949278

#     # 2) Create AE
#     autoencoder = generate_AE()

#     # 3) create reconstructed image    
#     loss_figure, is_defect = detect_defects(original_image, autoencoder,normal_threshold )