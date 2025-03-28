## 模型的最终效果可以在"test_image"文件夹中查看~  
## 数据集说明  
数据集文件过大无法上传至此处  
数据集可从 [AI Studio](https://aistudio.baidu.com/datasetdetail/321138) 下载。  
下载后，需将数据整理为以下结构：  
dataset  
├── train  
│ ├── JPEGImages # 训练集图片  
│ │ ├── img_name.png  
│ │ ├── ...  
│ ├── Annotations # 训练集标注（XML格式）  
│ │ ├── img_name.xml  
│ │ ├── ...  
│ ├── train_annotations_coco.json # COCO 格式标注（推理用）  
│ ├── train_list.txt # 训练/评估标注文件  
│ ├── labels.txt  
│ ├── game_1  
│ │ ├── frames  
│ │ ├── annotations.json  
│ │ ├── ...  
│ ├── ...  
├── val  
│ ├── JPEGImages # 验证集图片  
│ │ ├── img_name.png  
│ │ ├── ...  
│ ├── Annotations # 验证集标注（XML格式）  
│ │ ├── img_name.xml  
│ │ ├── ...  
│ ├── val_annotations_coco.json # COCO 格式标注（推理用）  
│ ├── val_list.txt # 训练/评估标注文件  
│ ├── labels.txt  
│ ├── game_1  
│ │ ├── frames  
│ │ ├── annotations.json  
│ │ ├── ...  
│ ├── ...  
