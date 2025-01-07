#imports
import svgpathtools as spt
import math
#functions

#function that takes an SVG file and returns the width and height of the SVG
#add comments and docstring
def get_svg_dimensions(svg_file):
    """
    Takes an SVG file and returns the width and height of the SVG.

    Args:
        svg_file (str): The path to the SVG file.

    Returns:
        tuple: A tuple containing the width and height of the SVG as strings.
    """
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

def rect2path(rect):
    """
    Converts a rectangle to an SVG path.

    Args:
        rect (tuple): A tuple containing the x, y, width, and height of the rectangle.

    Returns:
        spt.Path: An SVG path representing the rectangle.
    """
    coords = [(rect[0], rect[1]), (rect[0], rect[1]+rect[3]), (rect[0]+rect[2], rect[1]+rect[3]),
              (rect[0]+rect[2], rect[1])]
    lines = []
    for i, point in enumerate(coords):
        lines.append(spt.Line(complex(*coords[i-1]), complex(*point)))
    return spt.Path(*lines)

def poly2path(poly):
    # TODO: use spt.polygon() instead
    pass

def path2attr(rect_path):
    """
    Converts an SVG path to a dictionary of attributes.
    Args: 
        rect_path (spt.Path): An SVG path representing a rectangle.
    Returns:
        dict: A dictionary of attributes for the SVG path."""
    new_att = {}
    new_att['d'] = rect_path.d()
    new_att['fill'] = 'none'
    new_att['stroke'] = 'red'
    return new_att

def visualize_crop(file, crop_rect):
    """
    Visualizes a crop rectangle on an SVG file.
    Args:
        file (str): The path to the SVG file.
        crop_rect (tuple): A tuple containing the x, y, width, and height of the crop rectangle.
    Returns:
        str: The path to the SVG file with the crop rectangle visualized.
    """
    crop_path = rect2path(crop_rect)
    new_attr = path2attr(crop_path)
    #rebuild SVG with red box
    paths, attributes, svg_attributes = spt.svg2paths2(file)
    paths.append(crop_path)
    attributes.append(new_attr)
    spt.wsvg(paths, attributes=attributes, svg_attributes=svg_attributes, filename='test_crop_rect.svg')
    return 'test_crop_rect.svg'


#function that takes two bounding boxes and determines if the two boxes cover any of the same area. 
#box1 and box2 are lists with the format [xmin, xmax, ymin, ymax]
def boxes_overlap(box1, box2):
    """
    Determines if two bounding boxes overlap.
    Args:
        box1 (list): A list containing the x-min, x-max, y-min, and y-max of the first bounding box.
        box2 (list): A list containing the x-min, x-max, y-min, and y-max of the second bounding box.
    Returns:
        bool: True if the bounding boxes overlap, False otherwise.
        """
    #check if the boxes overlap in the x direction
    if box1[0] < box2[1] and box1[1] > box2[0]:
        #check if the boxes overlap in the y direction
        if box1[2] < box2[3] and box1[3] > box2[2]:
            return True
    return False

    
def dim_str2num(s):
    """
    Converts a string representing a dimension to a number.
    Args:
        s (str): A string representing a dimension.
    Returns:
        tuple: A tuple containing the dimension as a number and the unit as a string.
        """
    try:
        float(s)
        return float(s), None
    except ValueError:
        return float(s[:-2]), s[-2:]

def dim_num2str(dim, unit):
    """
    Converts a number and unit to a string.
    Args:
        dim (float): The dimension as a number.
        unit (str): The unit as a string.  Can be 'cm', 'in', 'mm', or 'px'.
    Returns:
        str: A string representing the dimension."""
    if unit == None:
        return "{}".format(math.floor(dim))
    if unit in ['cm', 'in', 'mm']:
        return "{}{}".format(dim, unit)
    if unit == "px":
        return "{}{}".format(math.floor(dim), unit)
    else:
        print("invalid input for unit argument")

#resize SVG height and width to match cropped size
def crop_svg_attr(svg_attributes, croppath):
    """
    Resizes the height and width of an SVG to match the cropped size.
    Args:
        svg_attributes (dict): A dictionary of attributes for the SVG.
        croppath (spt.Path): An SVG path representing the crop rectangle.
    Returns:
        dict: A dictionary of attributes for the resized SVG.
    """
    #height and width dimensions are recognized as cm, mm, in, em, ex, pt, pc, and px
    cbbox = croppath.bbox() #[xmin, xmax, ymin, ymax]
    orig_vbox = [float(x) for x in svg_attributes['viewBox'].split(' ')] #[xmin, ymin, xmax, ymax]
    orig_height, height_unit = dim_str2num(svg_attributes['height'])
    orig_width, width_unit = dim_str2num(svg_attributes['width'])
    new_height = orig_height*((cbbox[3]-cbbox[2])/(orig_vbox[3]-orig_vbox[1]))
    new_width = orig_width*((cbbox[1]-cbbox[0])/(orig_vbox[2]-orig_vbox[0]))
    #new_viewbox = '{} {} {} {}'.format(cbbox[0], cbbox[2], cbbox[1], cbbox[3])
    new_viewbox = '{} {} {} {}'.format(cbbox[0], cbbox[2], cbbox[1] - cbbox[0], cbbox[3] - cbbox[2])
    new_svg_attributes = svg_attributes.copy()
    new_svg_attributes['viewBox'] = new_viewbox
    new_svg_attributes['height'] = dim_num2str(new_height, height_unit)
    new_svg_attributes['width'] = dim_num2str(new_width, width_unit)
    return new_svg_attributes
    


def crop_svg(file, croppath):
    """
    Crops an SVG file to a specified path.
    Args:
        file (str): The path to the SVG file.
        croppath (spt.Path): An SVG path representing the crop rectangle.
    Returns:
        tuple: A tuple containing the cropped paths, attributes, and SVG attributes.
    """
    #returns list of paths, attributes, and svg_attributes from the original file cropped to within the croppath
    paths, attributes, svg_attributes = spt.svg2paths2(file)
    tol = 0.0002
    cropped_paths = []
    cropped_attributes = []
    new_svg_attributes = crop_svg_attr(svg_attributes, croppath)
    for path, attrib in zip(paths, attributes):
        if boxes_overlap(croppath.bbox(), path.bbox()):
            if path.is_contained_by(croppath):
                cropped_paths.append(path)
                cropped_attributes.append(attrib)
            else:
                intersections = path.intersect(croppath)
                #(list[tuple[float, Curve, float]]): list of intersections, each
                #in the format ((T1, seg1, t1), (T2, seg2, t2)), where
                #self.point(T1) == seg1.point(t1) == seg2.point(t2) == other_curve.point(T2)
                if not intersections:
                    print("path {} is found to overlap but not intersect or be contained by croppath".format(path))
                intersection_points = sorted([x[0][0] for x in intersections])
                start_points = [x+tol for x in intersection_points]
                start_points.insert(0, 0)
                end_points = [x-tol for x in intersection_points]
                end_points.append(1)
                brokenpath = []
                brokenpath_failures = 0
                for start, stop in zip(start_points, end_points):
                    try:
                        brokenpath.append(path.cropped(start, stop))
                    except:
                        brokenpath_failures += 1
                for broken in brokenpath:
                    if broken.is_contained_by(croppath):
                        cropped_paths.append(broken)
                        broken_attr = attrib
                        broken_attr['d'] = broken.d()
                        cropped_attributes.append(broken_attr)
    if brokenpath_failures:
        print("intersecting paths failed to resolve {}/{} times".format(brokenpath_failures, len(brokenpath)))
    return cropped_paths, cropped_attributes, new_svg_attributes  

   