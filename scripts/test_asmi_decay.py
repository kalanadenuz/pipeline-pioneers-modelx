from hydropulse.features.asmi import ASMICalculator
import pandas as pd
calc = ASMICalculator()
s = calc.compute_asmi(pd.Series([10, 0, 0, 50]))
print(s)
