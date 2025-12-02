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
df = pd.read_csv('task_sheet_3/sos_ex3/LEA-upload_bundle/output_data.csv')

print(df.head())
print(df.info())
print(df.shape)
# print(sum(df['Input']),sum(df['Output_boxA']))
plot_graph(df['Input'], df['Output_boxA'])

#BOX B
df = pd.read_csv('/home/kamran-ali/H-BRS/Semester/Self_organizing_system/Assignments/Self_Organizing_System/boxB_output.csv')

print(df.head())
print(df.info())
print(df.shape)
# print(sum(df['time']),sum(df['value']))
plot_graph(df['time'], df['value'])
