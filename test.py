index = 0
growth_rates = []
while index < len(l1)-1:
  growth_rates.append(((l1[index+1]-l1[index])/l1[index])*100)
  index += 1
print(growth_rates)

