import matplotlib.pyplot as plt
from pan_zoom import Panzoom

fig1 = plt.figure()
plt.plot([0, 1, 3, 6, 7, 4, 2, 0])
plt.show()
panzoomer = Panzoom(fig1)
print("drag-n-drop panning and mouswheel zooming awesomeness. Now: at your fingertips!")