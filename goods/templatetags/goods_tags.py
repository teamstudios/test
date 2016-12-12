from django import template

register = template.Library()


@register.inclusion_tag('good_image.html')
def show_good_image(good, width=None, height=None, css_class=None):
    """
    Render simple template with thumbnails and default image (if good image doesn't exist)
    :param good: Good object
    :param width: width of image or thumbnail
    :param height: width of image or thumbnail
    :param css_class: css class for image
    :return: dict object
    """
    if width is None:
        thumb_size = 'x' + str(height)
    elif height is None:
        thumb_size = str(width)
    else:
        thumb_size = str(width) + 'x' + str(height)
    return {'good': good, 'width': width, 'height': height, 'thumb_size': thumb_size, 'css_class': css_class}

