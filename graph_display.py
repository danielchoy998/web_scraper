import cv2
import numpy as np

def display(graph):

    png_bytes = graph.get_graph().draw_mermaid_png()
    nparr = np.frombuffer(png_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow("Graph", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






