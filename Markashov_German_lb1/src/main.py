import matplotlib.pyplot as plt

data = []
with open("data.csv", "r") as file:
    header = file.readline().strip()
    string = file.readline().strip()
    while(string):
        data.append(string)
        string = file.readline().strip()

print(f"{data=}")

n_values = []
ops_values = []
time_values = []

for line in data:
    parts = line.split(',')
    n_values.append(int(parts[0]))
    ops_values.append(int(parts[1]))
    time_values.append(float(parts[2]))

even_n = [n for i, n in enumerate(n_values) if n % 2 == 0]
even_ops = [ops for i, ops in enumerate(ops_values) if n_values[i] % 2 == 0]
odd_n = [n for i, n in enumerate(n_values) if n % 2 != 0]
odd_ops = [ops for i, ops in enumerate(ops_values) if n_values[i] % 2 != 0]

fig, ax = plt.subplots(figsize=(12, 8))
fig.suptitle('Анализ квадрирования квадрата', fontsize=16)

ax.plot(odd_n, odd_ops, 'ro-', linewidth=2, markersize=8)
ax.set_xlabel('Размер квадрата (n) - нечетные')
ax.set_ylabel('Количество операций')
ax.set_title('Операции для нечетных n')
ax.grid(True)
ax.set_yscale('log')

for i, n in enumerate(odd_n):
    ax.annotate(f'{odd_ops[i]}', (n, odd_ops[i]), 
                textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('square_packing_analysis.png', dpi=150)