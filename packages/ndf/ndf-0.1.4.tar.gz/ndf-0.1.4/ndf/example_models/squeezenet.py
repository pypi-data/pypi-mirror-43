import pickle
import os

from ndf.layers import Conv2D, ReLU, Concatenate, Input, MaxPooling2D, \
    AveragePooling2D, Flatten, Softmax
from ndf.model import Model


# location of this file
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def squeezenet(include_softmax=True):
    classes = 1000

    # load weights
    with open(os.path.join(
            __location__, "weights", "squeezenet_weights.pkl"), "rb") as f:
        weights = pickle.load(f)  # weights have been packed in dictionary

    def _fire(x_, filters, name="fire"):
        sq_filters, ex1_filters, ex2_filters = filters
        squeeze = Conv2D(
            sq_filters, (1, 1), padding='same', name=name + "/squeeze1x1",
            kernel_weights=weights[name + "/squeeze1x1"][0],
            bias_weights=weights[name + "/squeeze1x1"][1])(x_)
        squeeze = ReLU()(squeeze)

        expand1 = Conv2D(
            ex1_filters, (1, 1),
            padding='same', name=name + "/expand1x1",
            kernel_weights=weights[name + "/expand1x1"][0],
            bias_weights=weights[name + "/expand1x1"][1])(squeeze)
        expand1 = ReLU()(expand1)
        expand2 = Conv2D(
            ex2_filters, (3, 3),
            padding='same', name=name + "/expand3x3",
            kernel_weights=weights[name + "/expand3x3"][0],
            bias_weights=weights[name + "/expand3x3"][1])(squeeze)
        expand2 = ReLU()(expand2)
        x_ = Concatenate(axis=-1, name=name + "Concat")([expand1, expand2])

        return x_

    img_input = Input(shape=(224, 224))

    x = Conv2D(
        64, (3, 3), strides=(2, 2), padding="same", name='conv1',
        kernel_weights=weights["conv1"][0],
        bias_weights=weights["conv1"][1])(img_input)
    x = ReLU()(x)

    x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='maxpool1')(x)

    x = _fire(x, (16, 64, 64), name="fire2")
    x = _fire(x, (16, 64, 64), name="fire3")

    x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='maxpool3')(x)

    x = _fire(x, (32, 128, 128), name="fire4")
    x = _fire(x, (32, 128, 128), name="fire5")

    x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='maxpool5')(x)

    x = _fire(x, (48, 192, 192), name="fire6")
    x = _fire(x, (48, 192, 192), name="fire7")

    x = _fire(x, (64, 256, 256), name="fire8")
    x = _fire(x, (64, 256, 256), name="fire9")

    x = Conv2D(classes, (1, 1), padding='valid', name='conv10',
               kernel_weights=weights["conv10"][0],
               bias_weights=weights["conv10"][1])(x)
    x = AveragePooling2D(pool_size=(13, 13), name='avgpool10')(x)
    x = Flatten(name='flatten10')(x)
    if include_softmax:
        x = Softmax(name='softmax')(x)

    model = Model([img_input], [x])
    return model
