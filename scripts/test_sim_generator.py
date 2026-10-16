from hydropulse.data.synthetic_generator import KelaniDataGenerator
g = KelaniDataGenerator()
df = g.generate_time_series(start_date='2024-01-01', end_date='2024-01-10')
print(df.shape)
