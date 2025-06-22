
# Google Street View Panoptic Segmentation

This project aims to extract urban information through the use of a **panoptic segmentation model** applied to **Google Street View images**.

The repository contains code to:

1. Download Google Street View images via API requests.
2. Apply a panoptic segmentation model to extract information about urban objects.

---
## ⚠️ How to Set Up the Project

Follow the steps below to set up the project on your local machine:

---

### 🔗 Clone the repository

1. **Open PowerShell**  
Right-click the folder where you want the project to be saved and select:  
**"Open in Terminal"** or **"Open PowerShell window here"**.

2. **Paste the following commands**  
```bash
git clone https://github.com/gabrielbolzoni/googleStreetView_panoptic_segmentation.git #Clone the repository from GitHub
```
```bash
cd googleStreetView_panoptic_segmentation #Navigate to the project folder
```
```bash
python -m venv venv #Create the virtual environment
```
```bash
.\venv\Scripts\Activate #Activate the virtual environment (Windows)
```
```bash
pip install -r requirements.txt #Install dependencies
```

   
## 🚀 Project Pipeline

### 1️⃣ Create the Raw Data Folder

Run the following command to create the folder where the coordinate files will be stored:

```bash
mkdir -p data/coordinates
```

In this folder, you must place a CSV file containing the coordinates with the following format:

```
id;longitude,latitude
```

> 🔸 **Example:**

```
1;-51.2301,-30.0346
2;-51.2305,-30.0349
```
The file's name will be used to reference the image saved for each coordinate point. So if the file is called "area_A.csv", the images will be named as area_A_1, area_A_2 and so on. Keep that in mind in order to locate the files.


### 2️⃣ Get Your Google Street View API Key

You need a Google API key to download the Street View images.

Follow this official guide to create your API key:  
👉 [Google Street View API Documentation](https://developers.google.com/maps/documentation/streetview/overview?hl=pt-br)

---

### 3️⃣ Create the Configuration File

Save your API key in a txt file named `config` in the project root folder.

**Example content of `config.txt`:**

```
YOUR_GOOGLE_API_KEY
```

---

### 4️⃣ Run the Pipeline

Execute the pipeline with the following command:

```bash
python run_segmentation.py config.txt
```

> This will download the images and apply the panoptic segmentation model.

---

## 📂 Output File

The results will be saved in a single Excel file called **`results.xlsx`**, located in the `results/` folder. This file contains **7 sheets**, each presenting a different aspect of the analysis:

---

### 🔸 General Results

- **`Resultados Contagem`**  
  ➝ For each image, shows the **count of instances per class**.

- **`Resultados Prop`**  
  ➝ For each image, shows the **area proportion (%) occupied by each class**, relative to the total image area.

---

### 🔸 Area Proportion Comparisons

- **`Verticalidade`**  
  ➝ For each image, presents the **proportion between buildings and sky**, useful for evaluating vertical urban density or openness.

- **`Infra deslocamento`**  
  ➝ For each image, presents the **proportion between roads and sidewalks**, providing insights into mobility infrastructure.

- **`Área Verde`**  
  ➝ For each image, shows the **proportion of green areas**, including vegetation-related classes.

---

### 🔸 Neighbourhood Results

- **`Tráfego e circulação`**  
  ➝ For each neighbourhood, shows the **total number of cars and people identified**, reflecting urban flow and circulation.

- **`Infra urbana`**  
  ➝ For each neighbourhood, shows the **total number of poles, signs, and street lamps identified**, indicating aspects of public urban infrastructure.

---


## 🗺️ Folder Structure

```
streetview_segmentation_project/
│
├── data/                         
│   ├── coordinates/               # CSV file(s) with the coordinates
│   └── streetView_images/         # GSV images downloaded
│
├── results/                       # Final output folder
│
├── src/                            
│   ├── class_label_traducao.json  
│   ├── panoptic_segmentation.py   # Script to apply the panoptic segmentation model
│   ├── streetview_download.py     # Script to download GSV images via API
│   └── run_segmentation.py        # Main script to run the pipeline 
│
├── .gitignore                     
├── config.txt                     # API key
├── README.md                      # Project documentation
├── requirements.txt               # Required packages
```

