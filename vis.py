import cv2
import numpy as np

dirty_map = [[]]#[
#        [197, 342, 350, 364, 374, 392, 398, 403, 583, 585, 681],
#        [379, 394, 408, 464, 472, 491, 521],
#        [20, 313, 628, 646],
#        [5, 509, 578, 626]]
del_map = []#[373, 378, 433, 479, 529, 614, 666, 239, 42, 243, 246, 306,
#         23, 24, 41, 50, 112, 95, 51, 142, 149, 195, 196, 80, 81, 125, 145]
id_map = {}
for l in dirty_map:
    for num in l:
        id_map[num] = l[0]

#cap = cv2.VideoCapture('../surv_03271038_03271040.avi')
cap = cv2.VideoCapture('/home/pfy/data/MOTchallenge/MOT16-11.mp4')
ret, frame = cap.read()
h,w, _ = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/pfy/data/tmp.avi',fourcc, 20.0, (w, h))

raw = np.genfromtxt('gt_new.txt', delimiter=',', dtype = np.float32)
nframe = 1
ids = np.unique(raw[:, 1])
id_colors = {i: tuple(np.random.randint(0, 256, (3))) for i in ids}  
while(cap.isOpened()):
    print nframe
    if not ret:
        break
    # if nframe < 1080:
    #     ret, frame = cap.read()
    #     nframe += 1
    #     continue
    idx = np.where(raw[:, 0] == nframe)
    id_bboxes = raw[idx, 1:6]
    frame_ids = []
    for id_bbox in id_bboxes[0]:
        person_id, x, y, w, h = id_bbox
        if person_id in del_map:
            continue
        if person_id in id_map:
            person_id = id_map[person_id]
            if person_id in frame_ids:
                continue
        frame_ids.append(person_id)
        color = id_colors[person_id]
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, str(int(person_id)), (x,y), cv2.FONT_HERSHEY_DUPLEX, 0.6, color)
    out.write(frame)
    #cv2.imshow('frame', frame)
    #cv2.waitKey(5)
    nframe += 1
    ret, frame = cap.read()
