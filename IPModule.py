from Dnn import predict
import numpy as np
import cv2
from forex_python.converter import CurrencyRates

image = cv2.imread("IMG_1906.JPG")


# Function that returns circles within the input image
# Works through turning the input image to greyscale and blurring it
# Then using Hough to get the coins
def findCoins(img, showCoins=False):
    scaling = 800.0/max(img.shape[0:2])
    img_gray = cv2.resize(img, None, fx=scaling, fy=scaling)
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.blur(img_gray, (5, 5))
    coins = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT,
                             1.2, 70, param2=35, minRadius=20, maxRadius=100)
    if coins is not None:
        coins = (np.round(coins[0, :]) / scaling).astype("int")
    return coins


# Adaptively correcting brightness Through 3 functions


# Calculates the Min and Max precentiles of the given image
def compute(img, min_percentile, max_percentile):
    max_percentile_pixel = np.percentile(img, max_percentile)
    min_percentile_pixel = np.percentile(img, min_percentile)

    return max_percentile_pixel, min_percentile_pixel

# The core funtion for Brightness


def aug(src):
    # Checks if the brightness is more than 130
    if get_lightness(src) > 130:
        print("The brightness of the picture is sufficient, no enhancement")
    max_percentile_pixel, min_percentile_pixel = compute(src, 1, 99)

    # Remove values ​​outside the quantile range
    src[src >= max_percentile_pixel] = max_percentile_pixel
    src[src <= min_percentile_pixel] = min_percentile_pixel

    # Stretch the quantile range from 0 to 255. 255*0.1 and 255*0.9 are taken here because pixel values ​​may overflow, so it is best not to set it to 0 to 255.
    out = np.zeros(src.shape, src.dtype)
    cv2.normalize(src, out, 255*0.1, 255*0.9, cv2.NORM_MINMAX)

    return out
# Fn gets the brightness of the image


def get_lightness(src):
    # Calculate brightness
    hsv_image = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    lightness = hsv_image[:, :, 2].mean()

    return lightness


def detectImage(image, currency):
    # Enhancing the Image Brightness
    image = aug(image)

    # Detecting the coins within the image
    coins = findCoins(image)

    coinsValues = []
    if coins is not None:

        # Getting the biggest coin radius
        maxRadius = np.amax(coins, 0)[2]
        # loop over coordinates and radii of the circles
        for ix, (x, y, r) in enumerate(coins):
            # Cutting the coin out of the image
            coin = image[y-maxRadius:y+maxRadius, x-maxRadius:x+maxRadius]
            # Check for zeroes if so continue
            if coin.shape[0] == 0 or coin.shape[1] == 0:
                continue
            # Resizing the coin image to send it to prediction
            coin = cv2.resize(coin, (150, 150))
            # Creating a blurred mask to add to the coin
            coinTemp = cv2.GaussianBlur(coin, (0, 0), 3)
            # Adding the mask with the coin to sharpen the image
            coin = cv2.addWeighted(coin, 2, coinTemp, -0.5, 0, coinTemp)

            # try recognition of coinValue type and add result to list
            coinValue = predict(coin)
            coinsValues.append(coinValue)

            # draw contour and results in the output image
            if (coinValue):
                cv2.circle(image, (x, y), r, (0, 255, 0), 2)
                cv2.putText(image, coinValue[:-1],
                            (x - 40, y), cv2.FONT_HERSHEY_PLAIN,
                            5, (0, 0, 255), thickness=5, lineType=cv2.LINE_AA)
        Currencies = {
            "Euro": 0,
            "Cents": 0,
            "Pounds": 0,
            "Piasters": 0
        }
    # Calculating the coins total values
        for i in coinsValues:
            if(i[:-1] == "1eg"):
                Currencies["Pounds"] += 1
            elif(i[:-1] == "50p"):
                Currencies["Piasters"] += 50
            elif(i[:-1] == "25p"):
                Currencies["Piasters"] += 25
            elif(i[:-1] == "1e"):
                Currencies["Euro"] += 1
            elif(i[:-1] == "2e"):
                Currencies["Euro"] += 2
            elif(i[:-1] == "1c"):
                Currencies["Cents"] += 1
            elif(i[:-1] == "2c"):
                Currencies["Cents"] += 2
            elif(i[:-1] == "5c"):
                Currencies["Cents"] += 5
            elif(i[:-1] == "10c"):
                Currencies["Cents"] += 10
            elif(i[:-1] == "20c"):
                Currencies["Cents"] += 20
            elif(i[:-1] == "50c"):
                Currencies["Cents"] += 50
        while(Currencies["Cents"] >= 100):
            Currencies["Euro"] += 1
            Currencies["Cents"] -= 100
        while(Currencies["Piasters"] >= 100):
            Currencies["Pounds"] += 1
            Currencies["Piasters"] -= 100

    # save output for retriveing in front end to terminate program
    cv2.imwrite("static/upload/image.jpg", image)

    c = CurrencyRates()
    OutEuro = 0.0
    OutPounds = 0.0
    if currency:
        # Conver Euros to any currency
        OutEuro = float(
            Currencies["Euro"]+Currencies["Cents"]/100)*float(c.get_rate('EUR', currency))
        egtocurrency = {
            'EUR': 18.5,
            'USD': 15.6,
            'GBP': 20.6
        }
        OutPounds = float(Currencies["Pounds"] +
                          Currencies["Piasters"]/100)/egtocurrency[currency]
    print(type(OutEuro))
    print(type(OutPounds))
    return Currencies, (float(OutEuro)+float(OutPounds))
