import glfw
from viewer.viewer import Viewer


def main():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    try:
        viewer = Viewer(width=1280, height=800, title="Computer Graphics Viewer")
        viewer.run()
    finally:
        glfw.terminate()


if __name__ == "__main__":
    main()