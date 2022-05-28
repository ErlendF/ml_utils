from cv2 import imread, imwrite, rectangle
from os.path import join, exists
from glob import glob
from shutil import copyfile

from blur import round_blur


def get_file_name(nr, dir):
    return join(dir, "img" + str(nr+1).rjust(7, '0') + ".png")


def read_frame(filename):
    return imread(filename)


def write_faces(finished_seqs, img_dir, out_dir, blur_function=round_blur, frames=None):
    faces_by_nr = {}
    for seq in finished_seqs:
        for face in seq:
            if face["bbox"][4] in faces_by_nr:
                faces_by_nr[face["bbox"][4]].append(face["bbox"])
            else:
                faces_by_nr[face["bbox"][4]] = [face["bbox"]]

    for frame_nr, bboxes in faces_by_nr.items():
        file_name = "img" + str(frame_nr+1).rjust(7, '0') + ".png"
        out = join(out_dir, file_name)
        if frames is None:
            img = imread(join(img_dir, file_name))
        else:
            img = frames[frame_nr]
        img = blur_function(img, bboxes)
        imwrite(out, img)


def display_bboxes(finished_seqs, img_dir, out_dir, color=(0, 0, 255), frames=None):
    faces_by_nr = {}
    for seq in finished_seqs:
        for face in seq:
            if face["bbox"][4] in faces_by_nr:
                faces_by_nr[face["bbox"][4]].append(face["bbox"])
            else:
                faces_by_nr[face["bbox"][4]] = [face["bbox"]]

    for frame_nr, bboxes in faces_by_nr.items():
        file_name = "img" + str(frame_nr+1).rjust(7, '0') + ".png"
        out = join(out_dir, file_name)
        if frames is None:
            img = imread(join(img_dir, file_name))
        else:
            img = frames[frame_nr]
        for bbox in bboxes:
            rectangle(img, (int(bbox[0]), int(bbox[1])),
                      (int(bbox[2]), int(bbox[3])), color, 2)

        imwrite(out, img)


def copy_remaining_files(in_dir, out_dir):
    for filepath in sorted(glob(join(in_dir, "*.png"))):
        filename = filepath.removeprefix(in_dir).removeprefix("/")
        out_file_path = join(out_dir, filename)

        if not exists(out_file_path):
            copyfile(filepath, out_file_path)


def read_all_frames(img_dir, file_ext="png"):
    frames = []
    for filepath in sorted(glob(join(img_dir, "*.png"))):
        frames.append(imread(filepath))
    return frames
