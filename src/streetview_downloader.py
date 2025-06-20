import requests
import os
import pandas as pd
from pathlib import Path


# -------------------- Função para importar coordenadas --------------------
def import_coordinates(mainFolder_path: str):
    coodinates_dict = {}
    mainFolder = Path(mainFolder_path)

    for file in mainFolder.glob("*.csv"):
        df = pd.read_csv(file)
        neighborhood_name = file.stem
        coordinates_list = df[["longitude", "latitude"]].values.tolist()
        coodinates_dict[neighborhood_name] = coordinates_list
    return coodinates_dict

# -------------------- Função para baixar imagens --------------------
def get_streetview_images(coordinates_dict, api_key, fov=90, pitch=0):
    output_folder = "data/streetView_images"
    os.makedirs(output_folder, exist_ok=True)

    for bairro, pontos in coordinates_dict.items():
        for idx, (lng, lat) in enumerate(pontos):
            output_path = os.path.join(output_folder, f"{bairro}_{idx}.jpg")

            url_image = (
                f"https://maps.googleapis.com/maps/api/streetview"
                f"?size=640x640"
                f"&location={lat},{lng}"
                f"&fov={fov}"
                f"&pitch={pitch}"
                f"&key={api_key}"
            )
            response = requests.get(url_image)

            if response.status_code == 200:
                with open(output_path, 'wb') as file:
                    file.write(response.content)
                print(f"Imagem salva em: {output_path}")
            else:
                print(f"Erro ao baixar imagem ({bairro} - {idx}): {response.status_code}")


