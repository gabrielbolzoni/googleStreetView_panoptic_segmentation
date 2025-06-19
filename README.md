
# Google Street View Panoptic Segmentation

This project aims to extract urban information through the use of a **panoptic segmentation model** applied to **Google Street View images**.

The repository contains code to:

1. Download Google Street View images via API requests.
2. Apply a panoptic segmentation model to extract information about urban objects.

---

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

---

### 2️⃣ Get Your Google Street View API Key

You need a Google API key to download the Street View images.

Follow this official guide to create your API key:  
👉 [Google Street View API Documentation](https://developers.google.com/maps/documentation/streetview/overview?hl=pt-br)

---

### 3️⃣ Create the Configuration File

Save your API key in a text file named `config.txt` in the project root folder.

**Example content of `config.txt`:**

```
YOUR_GOOGLE_API_KEY
```

---

### 4️⃣ Install Dependencies

Install all required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Run the Pipeline

Execute the pipeline with the following command:

```bash
python init.py
```

> This will download the images and apply the panoptic segmentation model.

---

## 📂 Output Files

The results will be saved in the `results/` folder, including the following CSV files:

- **`resultadosContagem.csv`**  
  ➝ Contains, for each image, the **count of instances per class**.

- **`resultadosProp.csv`**  
  ➝ Contains, for each image, the **area proportion (%) occupied by each class** relative to the total image area.

---

## 🗺️ Folder Structure

```
streetview_segmentation_project/
│
├── data/
│   └── coordinates/       # Folder for input CSV with coordinates
│
├── results/                # Folder with output CSV files
│
├── config.txt              # File with your Google API key
├── requirements.txt        # Python dependencies
├── init.py                 # Main script to run the pipeline
│
└── README.md               # Project documentation
```

---

## 📑 License

This project is licensed under the MIT License.

---
