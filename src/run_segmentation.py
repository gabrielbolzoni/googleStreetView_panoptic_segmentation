import sys
import os
from src.streetview_downloader import import_coordinates,get_streetview_images
from src.panoptic_segmentation import generate_results

# -------------------- Execução principal via terminal --------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python run_segmentation.py <caminho_do_arquivo_api_key>")
        sys.exit(1)

    caminho_api_key = sys.argv[1]

    with open(caminho_api_key, 'r') as f:
        api_key = f.read().strip()
    
    os.makedirs("/results")
    coords_dict = import_coordinates("data/coordinates")
    get_streetview_images(coords_dict, api_key)
    generate_results("data/streetView_images")

    