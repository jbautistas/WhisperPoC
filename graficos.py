import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos desde el archivo CSV
data = pd.read_csv('resultados/metricas.csv')

# Convertir WER y CER a porcentajes
data['WER_percent'] = data['WER'] * 100
data['CER_percent'] = data['CER'] * 100

# Asegurar el orden de los modelos
modelos = ['tiny', 'base', 'small', 'medium', 'large']
data['modelo'] = pd.Categorical(
    data['modelo'], categories=modelos, ordered=True)

# Gráfico de barras: Tiempo promedio por modelo y dispositivo
avg_time = data.groupby(['modelo', 'device'])[
    'time_taken'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='modelo', y='time_taken', hue='device', data=avg_time)
plt.title('Tiempo Promedio por Modelo y Dispositivo')
plt.ylabel('Tiempo (segundos)')
plt.xlabel('Modelo')
plt.legend(title='Dispositivo')
plt.tight_layout()
plt.savefig('tiempo_promedio_por_modelo_dispositivo.png')
# plt.show()

# Gráfico de barras: RTF promedio por modelo y dispositivo
avg_RTF = data.groupby(['modelo', 'device'])['RTF'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='modelo', y='RTF', hue='device', data=avg_RTF)
plt.title('RTF Promedio por Modelo y Dispositivo')
plt.ylabel('Factor de Tiempo Real (RTF)')
plt.xlabel('Modelo')
plt.legend(title='Dispositivo')
plt.tight_layout()
plt.savefig('RTF_promedio_por_modelo_dispositivo.png')
# plt.show()

# Calcular y graficar el factor de aceleración (speedup)
pivot_avg_time = avg_time.pivot(
    index='modelo', columns='device', values='time_taken').reset_index()

if 'cpu' in pivot_avg_time.columns and 'cuda' in pivot_avg_time.columns:
    pivot_avg_time['speedup'] = pivot_avg_time['cpu'] / pivot_avg_time['cuda']
    plt.figure(figsize=(10, 6))
    sns.barplot(x='modelo', y='speedup', data=pivot_avg_time)
    plt.title('Factor de Aceleración (CPU/GPU) por Modelo')
    plt.ylabel('Factor de Aceleración')
    plt.xlabel('Modelo')
    plt.tight_layout()
    plt.savefig('speedup_por_modelo.png')

# Gráfico de barras: WER promedio por modelo
plt.figure(figsize=(10, 6))
sns.barplot(x='modelo', y='WER_percent', data=data,
            estimator='mean', errorbar='sd')
plt.title('WER Promedio por Modelo')
plt.ylabel('WER (%)')
plt.xlabel('Modelo')
plt.tight_layout()
plt.savefig('wer_promedio_por_modelo.png')
# plt.show()

# Gráfico de barras: CER promedio por modelo
plt.figure(figsize=(10, 6))
sns.barplot(x='modelo', y='CER_percent', data=data,
            estimator='mean', errorbar='sd')
plt.title('CER Promedio por Modelo')
plt.ylabel('CER (%)')
plt.xlabel('Modelo')
plt.tight_layout()
plt.savefig('cer_promedio_por_modelo.png')
# plt.show()

# Gráfico de caja: Distribución de WER por modelo
plt.figure(figsize=(10, 6))
sns.boxplot(x='modelo', y='WER_percent', data=data)
plt.title('Distribución de WER por Modelo')
plt.ylabel('WER (%)')
plt.xlabel('Modelo')
plt.tight_layout()
plt.savefig('wer_boxplot_por_modelo.png')
# plt.show()

# Gráfico de caja: Distribución de CER por modelo
plt.figure(figsize=(10, 6))
sns.boxplot(x='modelo', y='CER_percent', data=data)
plt.title('Distribución de CER por Modelo')
plt.ylabel('CER (%)')
plt.xlabel('Modelo')
plt.tight_layout()
plt.savefig('cer_boxplot_por_modelo.png')
# plt.show()

# Gráfico de líneas: WER por archivo de audio y modelo
plt.figure(figsize=(12, 8))
sns.lineplot(x='archivo_audio', y='WER_percent',
             hue='modelo', data=data, marker='o')
plt.title('WER por Archivo de Audio y Modelo')
plt.ylabel('WER (%)')
plt.xlabel('Archivo de Audio')
plt.xticks(rotation=90)
plt.legend(title='Modelo')
plt.tight_layout()
plt.savefig('wer_lineplot_por_audio.png')
# plt.show()

# Gráfico de líneas: CER por archivo de audio y modelo
plt.figure(figsize=(12, 8))
sns.lineplot(x='archivo_audio', y='CER_percent',
             hue='modelo', data=data, marker='o')
plt.title('CER por Archivo de Audio y Modelo')
plt.ylabel('CER (%)')
plt.xlabel('Archivo de Audio')
plt.xticks(rotation=90)
plt.legend(title='Modelo')
plt.tight_layout()
plt.savefig('cer_lineplot_por_audio.png')
# plt.show()
