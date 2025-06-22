import torch
from transformers import OneFormerProcessor, OneFormerForUniversalSegmentation
from PIL import Image
from collections import defaultdict
import numpy as np
from collections import Counter
import json
import os
import pandas as pd

# Carregar o modelo e o processador
processor = OneFormerProcessor.from_pretrained("shi-labs/oneformer_ade20k_swin_large")
model = OneFormerForUniversalSegmentation.from_pretrained("shi-labs/oneformer_ade20k_swin_large")

def generate_results(streetView_images_folder):
    proporcoes_list = []
    contagens_list = []

    for filename in os.listdir(streetView_images_folder):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        caminho_imagem = os.path.join(streetView_images_folder, filename)
        image = Image.open(caminho_imagem).convert("RGB")

        panoptic_inputs = processor(images=image, task_inputs=["panoptic"], return_tensors="pt")
        with torch.no_grad():
            panoptic_outputs = model(**panoptic_inputs)

        panoptic_result = processor.post_process_panoptic_segmentation(
            panoptic_outputs, target_sizes=[image.size[::-1]]
        )[0]

        proporcao_por_classe, contagem_por_classe, prop_veg = calculate_image_metrics(panoptic_result)

        # Dict para proporções
        proporcao_row = {label_id: proporcao for label_id, proporcao in proporcao_por_classe.items()}
        proporcao_row["proporcao_vegetacao"] = prop_veg
        proporcao_row["imagem"] = filename
        proporcoes_list.append(proporcao_row)

        # Dict para contagens
        contagem_row = {label_id: contagem for label_id, contagem in contagem_por_classe.items()}
        contagem_row["imagem"] = filename
        contagens_list.append(contagem_row)

    # Criar os DataFrames e definir "imagem" como índice
    df_proporcoes = pd.DataFrame(proporcoes_list).set_index("imagem").fillna(0)
    df_contagens = pd.DataFrame(contagens_list).set_index("imagem").fillna(0)
    
    return export_results(df_proporcoes,df_contagens)

def calculate_image_metrics(panoptic_segmentation):
    mask = panoptic_segmentation["segmentation"].numpy()
    segments_info = [seg for seg in panoptic_segmentation["segments_info"] if seg["score"] >= 0.8]
    area_por_classe = defaultdict(int)
    total_pixels = mask.size
    for segment in segments_info:
        segment_id = segment["id"]
        label_id = segment["label_id"]
        area_segmento = np.sum(mask == segment_id)
        area_por_classe[label_id] += area_segmento
    proporcao_por_classe = {label: area / total_pixels for label, area in area_por_classe.items()}
    contagem_por_classe = Counter([segment["label_id"] for segment in segments_info])
    areaVerde_ids = [4,9,17,72] #árvore,grama,planta,palmeira
    proporcao_vegetacao = sum(proporcao_por_classe.get(id, 0) for id in areaVerde_ids)

    return proporcao_por_classe,contagem_por_classe,proporcao_vegetacao

def export_results(df_proporcoes,df_contagens):
    df_proporcoes["Bairro"] = df_proporcoes.index.str.split("_").str[0]
    df_contagens["Bairro"] = df_contagens.index.str.split("_").str[0]

    with open("src/class_label_traducao.json", "r", encoding="utf-8") as f:
        id_traducao = json.load(f)

    label_traducao_int = {int(k): v for k, v in id_traducao.items()}
    # Output final de proporções
    df_prop_completo = df_proporcoes.rename(columns=label_traducao_int) #.to_csv('results/resultadosProp.csv')
    verticalidade = df_prop_completo.groupby("Bairro")[["predio", "ceu"]].mean().reset_index()
    infraDesloc = df_prop_completo.groupby("Bairro")[["estrada", "calçada"]].mean().reset_index()
    areaVerde = df_prop_completo.groupby("Bairro")[["árvore", "grama", "planta", "palmeira"]].mean().reset_index()
    
    # Output final de contagens
    df_contagem_completo = df_contagens.rename(columns=label_traducao_int) #.to_csv('results/resultadosContagem.csv')
    trafegoCirculacao = df_contagem_completo.groupby("Bairro")[["carro", "pessoa"]].sum().reset_index()
    infraUrbana = df_contagem_completo.groupby("Bairro")[["poste", "placa", "poste de luz"]].sum().reset_index()

    with pd.ExcelWriter('results/results.xlsx', engine='xlsxwriter') as writer:
        df_contagem_completo.to_excel(writer, sheet_name='Resultados Contagem', index=False)
        df_prop_completo.to_excel(writer, sheet_name='Resultados Prop', index=False)
        verticalidade.to_excel(writer, sheet_name='Verticalidade', index=False)
        infraDesloc.to_excel(writer, sheet_name='Infra deslocamento', index=False)
        areaVerde.to_excel(writer, sheet_name='Área Verde', index=False)
        trafegoCirculacao.to_excel(writer, sheet_name='Tráfego e circulação', index=False)
        infraUrbana.to_excel(writer, sheet_name='Infra urbana', index=False)
    return 



