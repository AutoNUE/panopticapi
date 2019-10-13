#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import pdb
import os, sys
import json
import glob
import numpy as np
import PIL.Image as Image

from panopticapi.utils import IdGenerator, save_json

try:
    # set up path for cityscapes scripts
    # sys.path.append('./cityscapesScripts/')
    from anue_labels import labels, id2label
except Exception:
    raise Exception("Please load Cityscapes scripts from https://github.com/mcordts/cityscapesScripts")

original_format_folder = '/home/chrizandr/idd20kII/gtFine/val/'
# folder to store panoptic PNGs
out_folder = 'output/'
# json with segmentations information
out_file = 'cityscapes_panoptic_val.json'


def panoptic_converter(original_format_folder, out_folder, out_file):
    if not os.path.isdir(out_folder):
        print("Creating folder {} for panoptic segmentation PNGs".format(out_folder))
        os.mkdir(out_folder)

    categories = []
    added_cats = []
    for idx, el in enumerate(labels):
        if el.ignoreInEval:
            continue
        if el.level3Id not in added_cats:
            # pdb.set_trace()
            categories.append({'id': el.level3Id,
                               'name': el.name,
                               'color': el.color,
                               'supercategory': el.level2IdName,
                               'isthing': 1 if el.hasInstances else 0})
            added_cats.append(el.level3Id)

    categories_dict = {cat['id']: cat for cat in categories}

    file_list = sorted(glob.glob(os.path.join(original_format_folder, '*/*_gtFine_instancelevel3Ids.png')))

    images = []
    annotations = []
    for working_idx, f in enumerate(file_list):
        if working_idx % 10 == 0:
            print(working_idx, len(file_list))

        original_format = np.array(Image.open(f))
        print("Processing file", f)
        file_name = f.split('/')[-1]
        image_id = file_name.rsplit('_', 2)[0]
        image_filename= '{}_leftImg8bit.jpg'.format(image_id)
        # pdb.set_trace()
        # image entry, id for image is its filename without extension
        images.append({"id": image_id,
                       "width": original_format.shape[1],
                       "height": original_format.shape[0],
                       "file_name": image_filename})

        pan_format = np.zeros((original_format.shape[0], original_format.shape[1], 3), dtype=np.uint8)
        id_generator = IdGenerator(categories_dict)

        idx = 0
        l = np.unique(original_format)
        segm_info = []
        for el in l:
            if el < 1000:
                semantic_id = el
                is_crowd = 1
            else:
                semantic_id = el // 1000
                is_crowd = 0
            if semantic_id not in categories_dict:
                continue
            if categories_dict[semantic_id]['isthing'] == 0:
                is_crowd = 0
            mask = original_format == el
            segment_id, color = id_generator.get_id_and_color(semantic_id)
            pan_format[mask] = color

            area = np.sum(mask) # segment area computation

            # bbox computation for a segment
            hor = np.sum(mask, axis=0)
            hor_idx = np.nonzero(hor)[0]
            x = hor_idx[0]
            width = hor_idx[-1] - x + 1
            vert = np.sum(mask, axis=1)
            vert_idx = np.nonzero(vert)[0]
            y = vert_idx[0]
            height = vert_idx[-1] - y + 1
            bbox = [x, y, width, height]

            segm_info.append({"id": int(segment_id),
                              "category_id": int(semantic_id),
                              "area": int(area),
                              "bbox": [int(x) for x in bbox],
                              "iscrowd": is_crowd})

        annotations.append({'image_id': image_id,
                            'file_name': file_name,
                            "segments_info": segm_info})

        Image.fromarray(pan_format).save(os.path.join(out_folder, file_name))

    d = {'images': images,
         'annotations': annotations,
         'categories': categories,
        }
    save_json(d, out_file)

if __name__ == "__main__":
    panoptic_converter(original_format_folder, out_folder, out_file)
