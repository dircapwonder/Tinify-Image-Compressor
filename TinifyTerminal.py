import tinify, os

def image_choice(option):
    img = input(f"Which image do you want to {option}?\n")
    return img
    
def num_check(number):
    try:
        num = float(input(number))
    except ValueError:
        raise SystemExit("Please enter a number.")
    
    if num <= 0:
        raise SystemExit("The number must be greater than zero!")
    
    return num

def compress(img):
    c = input("1-Convert image to the smallest type\n2-Keep the original type and compress it\n")
    if c == "1":
        source = tinify.from_file(f"{img}.jpg")
        converted = source.convert(type=["image/webp","image/png", "image/jpg"])
        extension = converted.result().extension
        converted.to_file(f"most_optimized_{img}." + extension)
    elif c == "2":
        source = tinify.from_file(f"{img}.jpg")
        source.to_file(f"optimized_{img}.jpg")
    else:
        raise SystemExit("Choice out of range!")

def resize(img):    
    w = num_check("Set your width: ")
    h = num_check("Set your heigth: ")
    source = tinify.from_file(f"{img}.jpg")
    resized = source.resize(
    method="fit",
    width=w,
    height=h
    )
    resized.to_file(f"resized_{img}.jpg")

def main():
    api_key = os.getenv("API_KEY") #$env:API_KEY="YOUR_API_KEY_HERE"
    if not api_key:
        raise ValueError("API Key not found.")
    
    tinify.key = api_key
    
    option = input("1- Compress a JPG image\n2- Resize a JPG image\n")
    if option == "1":
        compress(image_choice("optimize"))
    elif option == "2":
        resize(image_choice("resize"))
    else:
        raise SystemExit("Choice out of range!")
    
if __name__ == "__main__":
    main()




