from graph import agentic_flow
from IPython.display import Image, display

if __name__ == '__main__':
    try:
        img = Image(agentic_flow.get_graph().draw_mermaid_png())
        display(img)  # Works in Jupyter Notebook or IPython
    except Exception:
        # This requires some extra dependencies and is optional
        pass

    # Save the image to a file for viewing
    try:
        with open("output_image.png", "wb") as f:
            f.write(agentic_flow.get_graph().draw_mermaid_png())
        print("Image saved as 'output_image.png'. Open it to view the graph.")
    except Exception as e:
        print(f"Failed to save the image: {e}")