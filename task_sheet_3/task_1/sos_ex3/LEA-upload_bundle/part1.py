import pandas as pd
import matplotlib.pyplot as plt

def plot_graph(x, y):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graph')
    plt.grid(True)
    plt.show()

#BOX A
df = pd.read_csv('output_data.csv')

print(df.head())
print(df.info())
print(df.shape)
# print(sum(df['Input']),sum(df['Output_boxA']))
plot_graph(df['Input'], df['Output_boxA'])

#BOX B
# df = pd.read_csv('boxB_output.csv')

# print(df.head())
# print(df.info())
# print(df.shape)
# # print(sum(df['time']),sum(df['value']))
# plot_graph(df['time'], df['value'])
