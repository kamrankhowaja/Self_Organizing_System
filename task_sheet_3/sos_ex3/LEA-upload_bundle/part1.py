import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_graph(x, y):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graph')
    plt.grid(True)
    plt.show()


df = pd.read_csv('task_sheet_3/sos_ex3/LEA-upload_bundle/output_data.csv')

print(df.head())
print(df.info())
print(df.shape)
print(sum(df['Input']),sum(df['Output_boxA']))
plot_graph(df['Input'], df['Output_boxA'])


