from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from PIL import Image, ImageDraw
import random

def website_screenshot(url, output_filename, width=375, height=812):
    # Set up the Selenium WebDriver for Chrome
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    
    browser.set_window_size(width, height)

    # Navigate to the URL
    browser.get(url)
    
    # Save the screenshot to the specified file
    browser.save_screenshot(output_filename)
    
    # Close the browser
    browser.quit()

    # Crop the screenshot based on the color
    cropped_filename = "Cropped_" + output_filename
    crop_to_color(output_filename, cropped_filename, (186, 197, 200))

def crop_to_color(input_filename, output_filename, target_color, tolerance=3):
    image = Image.open(input_filename)
    pixels = image.load()

    width, height = image.size
    top, bottom = height, 0

    # Identifying top and bottom boundaries
    for x in range(width):
        for y in range(220, height-350):
            r, g, b = pixels[x, y][:3]
            if all(abs(c - tc) <= tolerance for c, tc in zip((r, g, b), target_color)):
                top = min(top, y) - 0.01
                bottom = max(bottom, y) + 0.5
                break  # Once the target color is found, move to the next column

    if top < bottom:  # Ensure there is something to crop
        # Crop the top part of the image
        top_part = image.crop((0, 0, width, top))
        # Crop the bottom part of the image
        bottom_part = image.crop((0, bottom, width, height))

        # Create a new image to combine the two parts
        new_height = top_part.height + bottom_part.height
        combined_image = Image.new('RGB', (width, new_height))

        # Paste the top and bottom parts onto the combined image
        combined_image.paste(top_part, (0, 0))
        combined_image.paste(bottom_part, (0, top_part.height))

        combined_image.save(output_filename)
    else:
        print("No matching color found within tolerance.")
    
    image = combined_image
    radius = 20
    width, height = image.size
    
    # Crop out the top 110 pixels and the bottom 250 pixels
    image = image.crop((0, 115, width, height - 255))
    
    image.save(output_filename)



# # Example usage
# url = "https://www.reddit.com/r/AmItheAsshole/comments/1biqbup/aita_for_blowing_up_on_my_husbands_friend_after/"
# output_filename = "Capture_" + str(random.randint(0,10000)) + ".png"
# website_screenshot(url, output_filename)
