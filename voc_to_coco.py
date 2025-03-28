import os
import json
import xml.etree.ElementTree as ET

# 输入文件路径
txt_file = "F:/PingpangDetect/dataset/train/train_list.txt"
output_json_path = "F:/PingpangDetect/dataset/train/annotations_coco.json"
voc_root = "F:/PingpangDetect/dataset/train/"

# COCO JSON 结构
coco_data = {
    "images": [],
    "annotations": [],
    "categories": []
}

# 记录类别信息
category_dict = {}
image_id = 1
annotation_id = 1

# 读取 .txt 文件
with open(txt_file, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) != 2:
            continue

        image_path, xml_path = parts
        xml_full_path = os.path.join(voc_root, xml_path)

        # 解析 XML
        tree = ET.parse(xml_full_path)
        root = tree.getroot()

        filename = root.find("filename").text
        width = int(root.find("size/width").text)
        height = int(root.find("size/height").text)

        # 添加图片信息
        coco_data["images"].append({
            "id": image_id,
            "file_name": filename,
            "width": width,
            "height": height
        })

        # 解析标注框
        for obj in root.findall("object"):
            category_name = obj.find("name").text

            # 生成类别 ID
            if category_name not in category_dict:
                category_dict[category_name] = len(category_dict) + 1
                coco_data["categories"].append({
                    "id": category_dict[category_name],
                    "name": category_name,
                    "supercategory": "object"
                })

            category_id = category_dict[category_name]

            # 解析 bbox
            bndbox = obj.find("bndbox")
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)

            width = xmax - xmin
            height = ymax - ymin
            area = width * height

            # 添加 annotation
            coco_data["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": [xmin, ymin, width, height],
                "area": area,
                "iscrowd": 0
            })

            annotation_id += 1

        image_id += 1

# 保存为 JSON
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(coco_data, f, indent=4, ensure_ascii=False)

print(f"转换完成！COCO JSON 已保存至: {output_json_path}")
