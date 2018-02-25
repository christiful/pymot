import os
import argparse
import json
import numpy as np

def parse_txt(txtfile, gt = False, video = None):
    raw = np.genfromtxt(txtfile, delimiter = ',', dtype = np.float32)
    indices = np.unique(raw[:, 0]).astype(np.int32)
    frames = []
    for nframe in indices:
        idx = np.where(raw[:, 0].astype(np.int32) == nframe)
        id_bboxes = raw[idx, 1:6]
        frame = {
                "timestamp": int(nframe),
                "num": int(nframe),
                "class": "frame" 
                }
        annotations = []
        for id_bbox in id_bboxes[0]:
            person_id, x, y, w, h = id_bbox.tolist()
            annotation = {
                        "height": h, 
                        "width": w, 
                        "id": int(person_id), 
                        "y": y, 
                        "x": x
                        }
            if gt:
                annotation["dco"] = False
            annotations.append(annotation)
        if gt:
            frame["annotations"] = annotations
        else:
            frame["hypotheses"] = annotations
        frames.append(frame)
    if video is None:
        video = ""
    json_to_write = [{
        "frames": frames,
        "class": "video",
        "filename": video
        }]
    return json_to_write

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-t', '--type', choices = ['gt', 'result'], default = 'result')
    parser.add_argument('-v', '--video')
    parser.add_argument('-o', '--output')
    parser.add_argument('-c', '--check_format', action="store_true", default=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arg()
    assert os.path.isfile(args.file), "Input file does not exist!"
    if args.output is None:
       path, _ = os.path.splitext(args.file)
       args.output = path + '.json'
       #TODO: output exists
    json_to_write = parse_txt(args.file, args.type == 'gt', args.video)
    with open(args.output, 'w') as f:
        json.dump(json_to_write, f)
        
