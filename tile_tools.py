

#imports


#functions

#function that takes an SVG file and returns the width and height of the SVG
def get_svg_dimensions(svg_file):
    #open the SVG file
    with open(svg_file, 'r') as file:
        svg = file.read()
    #find the width and height of the SVG
    try:
        width = svg.split('width="')[1].split('"')[0]
        height = svg.split('height="')[1].split('"')[0]
    except: #if the SVG does not have width and height attributes, the return viewbox dimensions
        viewbox = svg.split('viewBox="')[1].split('"')[0]
        width = viewbox.split(' ')[2]
        height = viewbox.split(' ')[3]
    #return the width and height
    return width, height


#function that takes an SVG file and a rectangle position and size and returns a new SVG file cropped to that rectangle
def crop_svg(svg_file, x, y, width, height):
    #open the SVG file
    with open(svg_file, 'r') as file:
        svg = file.read()
    #find the width and height of the SVG
    width = svg.split('width="')[1].split('"')[0]
    height = svg.split('height="')[1].split('"')[0]
    #find the viewbox of the SVG
    viewbox = svg.split('viewBox="')[1].split('"')[0]
    #find the SVG path
    path = svg.split('<path d="')[1].split('</path>')[0]
    #find the SVG header
    header = svg.split('<svg')[0]
    #find the SVG footer
    footer = svg.split('</svg>')[1]
    #create the new SVG
    new_svg = header + '<svg width="' + width + '" height="' + height + '" viewBox="' + viewbox + '">' + '<path d="' + path + '"></path>' + '</svg>' + footer
    #return the new SVG
    return new_svg

#function that takes an SVG file and a rectangle position and size and returns a new SVG file cropped to that rectangle using svgpathtools
def crop_svg_svgpathtools(svg_file, x, y, width, height):
    #import svgpathtools
    import svgpathtools as spt
    # Load the SVG file
    paths, attributes = spt.svg2paths(svg_file)
    # Define the cropping rectangle (x, y, width, height)
    crop_rect = (x, y, x+width, y+height)

    # Create a new list of paths for the cropped SVG
    cropped_paths = []

    # Iterate over all paths and crop them
    for path in paths:
        cropped_path = path.crop(crop_rect)
        if cropped_path:
            cropped_paths.append(cropped_path)

    # Save the cropped SVG
    # spt.wsvg(cropped_paths, filename='cropped_svg.svg')
    return cropped_paths


#function that takes two bounding boxes and determines if the two boxes cover any of the same area. 
#box1 and box2 are lists with the format [xmin, xmax, ymin, ymax]
def boxes_overlap(box1, box2):
    #check if the boxes overlap in the x direction
    if box1[0] < box2[1] and box1[1] > box2[0]:
        #check if the boxes overlap in the y direction
        if box1[2] < box2[3] and box1[3] > box2[2]:
            return True
    return False

    
    