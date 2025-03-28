import os
import json
import xml.etree.ElementTree as ET

def create_pascal_voc(filename, width, height, objects, save_path):
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "zdy"
    ET.SubElement(annotation, "filename").text = filename
    ET.SubElement(annotation, "path").text = save_path
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(annotation, "segmented").text = "0"
    for obj in objects:
        obj_elem = ET.SubElement(annotation, "object")
        ET.SubElement(obj_elem, "name").text = obj["name"]
        ET.SubElement(obj_elem, "pose").text = "Unspecified"
        ET.SubElement(obj_elem, "truncated").text = "0"
        ET.SubElement(obj_elem, "difficult").text = "0"
        bndbox = ET.SubElement(obj_elem, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(obj["xmin"])
        ET.SubElement(bndbox, "ymin").text = str(obj["ymin"])
        ET.SubElement(bndbox, "xmax").text = str(obj["xmax"])
        ET.SubElement(bndbox, "ymax").text = str(obj["ymax"])
    tree = ET.ElementTree(annotation)
    tree.write(save_path)

def convert_annotations(json_file, image_dir, output_img_dir, output_ann_dir, game_name, img_width=1920, img_height=1080, box_size=32):
    with open(json_file, 'r') as f:
        annotations = json.load(f)

    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_ann_dir, exist_ok=True)

    for frame_id, data in annotations.items():
        x, y = data["ball_position"]["x"], data["ball_position"]["y"]
        if x == -1 or y == -1:
            continue
        xmin = max(0, x - box_size // 2)
        ymin = max(0, y - box_size // 2)
        xmax = min(img_width, x + box_size // 2)
        ymax = min(img_height, y + box_size // 2)
        objects = [{"name": "pinpang", "xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax}]
        original_filename = f"frame_{int(frame_id):06d}.png"
        new_filename = f"{game_name}_{original_filename}"
        xml_filename = os.path.join(output_ann_dir, f"{game_name}_frame_{int(frame_id):06d}.xml")
        img_src_path = os.path.join(image_dir, original_filename)
        img_dest_path = os.path.join(output_img_dir, new_filename)
        create_pascal_voc(new_filename, img_width, img_height, objects, xml_filename)
        if os.path.exists(img_src_path):
            os.rename(img_src_path, img_dest_path)

def process_directory(train_dir):
    output_img_dir = os.path.join(train_dir, "JPEGImages")
    output_ann_dir = os.path.join(train_dir, "Annotations")
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_ann_dir, exist_ok=True)
    for game_folder in os.listdir(train_dir):
        game_path = os.path.join(train_dir, game_folder)
        if os.path.isdir(game_path) and game_folder.startswith("game_"):
            json_file = os.path.join(game_path, "annotations.json")
            image_dir = os.path.join(game_path, "frames")
            if os.path.exists(json_file) and os.path.exists(image_dir):
                print(f"Processing {game_folder}...")
                convert_annotations(json_file, image_dir, output_img_dir, output_ann_dir, game_folder)
    print(f"All games processed! Images and annotations saved in {output_img_dir} and {output_ann_dir}.")

train_directory = "F:/PingpangDetect/dataset/val"
process_directory(train_directory)