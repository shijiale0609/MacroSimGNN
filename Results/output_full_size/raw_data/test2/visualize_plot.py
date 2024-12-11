import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns


#plt.figure(figsize=(6,6))
#targets = np.load("train_targets.npy")
#print(targets.shape)
#predictions = np.load("train_predictions.npy")
#print(predictions.shape)
#plt.scatter(-np.log(targets), -np.log(predictions))
#x = np.linspace(0,int(max(max(-np.log(targets)), max(-np.log(predictions))))+1)
#plt.plot(x,x, c='red')
#plt.xlabel("True GED/((|G1|+|G2|)/2)")
#plt.ylabel("Predicted GED/((|G1|+|G2|)/2)")
#plt.savefig("train_result_x_y.png")

#plt.figure(figsize=(6,6))
#plt.hist(-np.log(targets),alpha=0.5, label="targets")
#plt.hist(-np.log(predictions), alpha=0.5, label="predictions")
#plt.legend()
#plt.savefig("train_result_hist.png")
#print("R2 score:", r2_score(-np.log(targets), -np.log(predictions)))
#print("MSE error:",mean_squared_error(-np.log(targets), -np.log(predictions)))

plt.figure(figsize=(6,6))
targets = np.load("targets.npy")
print(targets.shape)
predictions = np.load("predictions.npy")
print(predictions.shape)
sns.jointplot(x = -np.log(targets), y = -np.log(predictions))
x = np.linspace(0,int(max(max(-np.log(targets)), max(-np.log(predictions))))+1)
plt.plot(x,x, c='red')
plt.xlabel("True GED/((|G1|+|G2|)/2)")
plt.ylabel("Predicted GED/((|G1|+|G2|)/2)")
plt.savefig("train_result_x_y_joint.png")

print("R2 score:", r2_score(-np.log(targets), -np.log(predictions)))
print("MSE error:",mean_squared_error(-np.log(targets), -np.log(predictions)))
print(targets)
print(predictions)
