# Food_arranger
Food arranger program to match nutrient targets. An innovation for nutrition apps
## Example:
Foods:
Food A with nutrients (in 100 gram portion): aA = 18, bA = 16, cA = 3
Food B with nutrients (in 100 gram portion): aB = 12, bB = 6, cB = 30
Food C with nutrients (in 100 gram portion): aC = 1, bC = 1, cC = 7

Nutrient targets:
target_a = 99
target_b = 112
target_c = 369

Objective:
I want to find how much of portions of each food (A,B,C) I have to consume to match those three targets (target_a, target_b, target_c).

Solution:
A_array = [[aA,aB,aC],[bA,bB,bC],[cA,cB,cC]]
b_array = [target_a,target_b,target_c]
bounds = (0, np.inf)
result = scipy.optimize.lsq_linear(A,b,bounds = bounds) # max_iter = ... can be added for larger lists
x = result.x # list of resulting portions of each food 
predicted_values = A.dot(x) # predicted nutrient values
residuals = predicted_values - b # error for each nutrient
...

