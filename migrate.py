import base64
import os
from PIL import Image
import requests

from lxml.html import fromstring, tostring

import mjson

BASE_EXPORT_PATH = '../../personal/export'
EXPORT_BLOG_PATH = os.path.join(BASE_EXPORT_PATH, 'news')
EXPORT_IMAGES_PATH = os.path.join(BASE_EXPORT_PATH, 'image-repository')
EXPORT_VIDEOS_PATH = os.path.join(BASE_EXPORT_PATH, 'video-repository')

ASSET_IMG_PATH = 'assets/img'
ASSET_VID_PATH = 'assets/video'

POSTS_PATH = '_posts'


IMG_UID_TO_PATH = {}
RENAMED_IMAGES = {}


def import_image(data, filename, dest_path):
    if isinstance(data, dict):
        im_data = data
    else:
        im_data = mjson.loads(data.replace('type://', ''))['data']

    im_bdata = base64.b64decode(im_data['data'])

    if '.' not in filename:
        RENAMED_IMAGES[filename] = filename + '.' + im_data['content_type'].split('/')[-1]
        filename = RENAMED_IMAGES[filename]
    elif filename.split('.')[-1] in ('mov', 'mp4'):  # this is a moving that we have screenshot for
        RENAMED_IMAGES[filename] = filename.rsplit('.')[0] + '.' + im_data['content_type'].split('/')[-1]
        filename = RENAMED_IMAGES[filename]

    new_filepath = os.path.join(dest_path, filename)
    if os.path.exists(new_filepath):
        return new_filepath

    with open(new_filepath, 'wb') as fi:
        fi.write(im_bdata)

    for name, size in [('large', (768, 768)), ('medium', (400, 400))]:
        pim = Image.open(new_filepath)
        pim.thumbnail(size, Image.ANTIALIAS)
        thumb_filepath = f"{new_filepath.rsplit('.')[0]}_{name}.{new_filepath.rsplit('.')[-1]}"
        pim.save(thumb_filepath)
    return new_filepath


def import_images(path):
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        with open(filepath) as fi:
            data = mjson.loads(fi.read())

        if data['portal_type'] not in ('Image', 'Video'):
            continue

        fdata = data['data']
        if fdata.get('image'):
            IMG_UID_TO_PATH[data['uid']] = import_image(
                fdata['image'], filename, ASSET_IMG_PATH)
        elif 'plone.app.contenttypes.behaviors.leadimage.ILeadImage' in fdata:
            # look in behavior for image...
            lead = fdata['plone.app.contenttypes.behaviors.leadimage.ILeadImage']
            imdata = mjson.loads(lead['image'])['data']
            IMG_UID_TO_PATH[data['uid']] = import_image(
                imdata, filename, ASSET_IMG_PATH)


def rename_image_attr(el, attrib='src'):
    src = el.attrib[attrib]
    size = 'full'
    if 'resolveuid' in src:
        part = src.split('/resolveuid/')[-1]
        if '@@images/image' in part:
            size = part.split('/')[-1]
        uid = part.split('/@@images')[0]
        if uid in IMG_UID_TO_PATH:
            src = '/' + IMG_UID_TO_PATH[uid]
    else:
        src = src.replace(
            'http://nohost/Plone/image-repository',
            '/assets/img'
        ).replace(
            'http://nohost/Plone/video-repository',
            '/assets/img'
        ).replace('/image-repository/', '/assets/img/')
        if '@@images/image' in src:
            size = src.split('/')[-1]
        src = src.split('/@@images')[0]
        filename = src.split('/')[-1]
        if filename in RENAMED_IMAGES:
            src = '/'.join(src.split('/')[:-1]) + '/' + RENAMED_IMAGES[filename]
    if size != 'full':
        src = f"{src.rsplit('.')[0]}_{size}.{src.rsplit('.')[-1]}"
    el.attrib[attrib] = src


def import_blog(filename, data):
    if data['state'] != 'published':
        print(f'skipping {filename}')
        return
    if data['portal_type'] != 'News Item':
        print(f'skipping {filename}')
        return
    fdata = data['data']
    try:
        dublin = fdata['plone.app.dexterity.behaviors.metadata.IDublinCore']
    except KeyError:
        print(f'skipping {filename}')
        return

    layout = fdata['rendered_layout']
    dom = fromstring(layout)

    for im in dom.cssselect('img'):
        rename_image_attr(im, 'src')

    for vid in dom.cssselect('video'):
        rename_image_attr(vid, 'poster')
        vid.attrib['controls'] = 'all'
    for source in dom.cssselect('video source'):
        source.attrib['src'] = source.attrib['src'].replace(
            'http://nohost/Plone/video-repository',
            '/assets/video'
        ).split('@@download')[0]

    for el in dom.cssselect(','.join([
        '[class*="mosaic-plone.app.standardtiles.keywords-tile"]',
        '[class*="mosaic-IDublinCore-title-tile"]',
        '[class*="mosaic-IDublinCore-effective-tile"]',
    ])):
        parent = el.getparent()
        parent.remove(el)

    for anchor in dom.cssselect('a'):
        anchor.attrib['href'] = anchor.attrib['href'].replace(
            'http://nohost/Plone', '')

    layout = tostring(dom.cssselect('[data-panel="content"]')[0])

    effective = dublin['effective']
    tags = dublin['subjects']
    title = dublin['title']
    description = dublin['description']
    new_filepath = os.path.join(POSTS_PATH, '{}-{}.html'.format(
        effective.strftime('%Y-%m-%d'),
        filename))
    output = f'''---
layout: post
title:  "{title}"
date:   {effective.strftime('%Y-%m-%d %H:%M:%S')}
categories: {' '.join(tags)}
description: {description}
---
{layout.decode('utf8')}
'''
    with open(new_filepath, 'w') as fi:
        fi.write(output)


def import_blogs(path):
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            continue
        with open(filepath) as fi:
            data = mjson.loads(fi.read())
        import_blog(filename, data)


def import_videos(path):
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        with open(filepath) as fi:
            data = mjson.loads(fi.read())

        if data['portal_type'] != 'Video':
            continue

        new_filepath = os.path.join(ASSET_VID_PATH, filename)
        if os.path.exists(new_filepath):
            continue

        url = 'https://www.nathanvangheem.com/video-repository/' + filename
        print(f'Downloading {url}')
        resp = requests.get(url)
        with open(new_filepath, 'wb') as fi:
            fi.write(resp.content)


if __name__ == '__main__':
    import_images(EXPORT_IMAGES_PATH)
    import_images(EXPORT_VIDEOS_PATH)
    import_videos(EXPORT_VIDEOS_PATH)
    import_blogs(EXPORT_BLOG_PATH)
