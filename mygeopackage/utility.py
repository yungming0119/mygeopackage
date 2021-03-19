"""Utility module."""

def rgb_to_hex(color):
    """Helper function for converting RGB color to hex code

    Args:
        color (list): List of R,G,B value

    Returns:
        str: Hex code for the RGB value
    """
    r,g,b = color
    #print('%02x%02x%02x' % (r,g,b))
    return '#%02x%02x%02x' % (r,g,b)