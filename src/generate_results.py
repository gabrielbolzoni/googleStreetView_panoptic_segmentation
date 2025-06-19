import pandas as pd

df_geralContagem = pd.read_csv("results/resultadosContagem.csv")
df_bairroContagem = pd.read_csv("results/resultadosContagemBairro.csv")
df_geralProp = pd.read_csv("results/resultadosProp.csv")
df_bairroProp = pd.read_csv("results/resultadosPropBairro.csv")

df_geralContagem.groupby("Bairro")[["carro","pessoa"]].sum().to_csv("results/trafegoCirculacao.csv")
df_geralContagem.groupby("Bairro")[["poste","placa","poste de luz"]].sum().to_csv("results/infraUrbana.csv")

df_somatorioInstancias = df_geralContagem.drop(columns=["imagem","Bairro"]).sum(axis=0).to_frame(name='total_instancias').reset_index()
df_somatorioInstancias.columns = ['classe', 'total_instancias']
df_somatorioInstancias.sort_values(by="total_instancias",ascending=False).to_csv("listaInstancias.csv")

df_geralContagem.groupby("Bairro").sum()["moto"]