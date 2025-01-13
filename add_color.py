#imports
import svgpathtools as spt
import math
#functions

#function that converts RGB color value into hexadecimal
def rgb2hex(rgb):
    """
    Converts an RGB color value to a hexadecimal color value.

    Args:
        rgb (tuple): A tuple containing the red, green, and blue values of the color.

    Returns:
        str: The hexadecimal representation of the color.
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

