import json
import os
import cv2
import matplotlib.pyplot as plt


def draw_bboxes(json_file, image_folder):
    # 读取JSON文件
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 获取前10个检测结果
    results = data['result'][:100]

    for res in results:
        image_id = res['image_id']
        x, y, width, height = int(res['x']), int(res['y']), int(res['width']), int(res['height'])

        image_path = os.path.join(image_folder, f"{image_id}")

        if os.path.exists(image_path):
            # 读取图片
            image = cv2.imread(image_path)
            if image is None:
                print(f"无法读取图片: {image_path}")
                continue

            # 画框 (红色, 2像素厚度)
            cv2.rectangle(image, (int(x - width / 2), int(y - height / 2)), (int(x + width / 2), int(y + height / 2)),
                          (0, 0, 255), 2)
            output_path = f"F:/PingpangDetect/output/test_image/{image_id}"
            cv2.imwrite(output_path, image)

            # 可视化（可选）
            # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            # plt.title(image_id)
            # plt.axis('off')
            # plt.show()
        else:
            print(f"图片不存在: {image_path}")


# 使用示例
draw_bboxes("F:/PingpangDetect/submission/result.json", "F:/PingpangDetect/dataset/val/JPEGImages")