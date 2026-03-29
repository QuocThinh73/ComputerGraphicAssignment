import OpenGL.GL as GL
import glfw
import imgui

from imgui.integrations.glfw import GlfwRenderer
from viewer.app_state import AppState
from viewer.scene import Scene
from viewer.ui import ViewerUI


class Viewer:
    def __init__(self, width=960, height=800, title="Viewer"):
        self.width = width
        self.height = height
        self.title = title

        self.win = None
        self.mouse = (0, 0)
        self.trackball = None
        self.imgui_renderer = None

        self.state = AppState()
        self.scene = None
        self.ui = None

        self._init_window()
        self._init_opengl()
        self._init_imgui()
        self._init_app()

    def _init_window(self):
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        glfw.window_hint(glfw.DEPTH_BITS, 16)
        glfw.window_hint(glfw.DOUBLEBUFFER, True)

        self.win = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.win:
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self.win)

        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_cursor_pos_callback(self.win, self.on_mouse_move)
        glfw.set_scroll_callback(self.win, self.on_scroll)
        glfw.set_char_callback(self.win, self.on_char)

    def _init_opengl(self):
        print(
            "OpenGL",
            GL.glGetString(GL.GL_VERSION).decode(),
            "| GLSL",
            GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode(),
            "| Renderer",
            GL.glGetString(GL.GL_RENDERER).decode()
        )

        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)

    def _init_imgui(self):
        imgui.create_context()
        self.imgui_renderer = GlfwRenderer(self.win, attach_callbacks=False)

    def _init_app(self):
        self.scene = Scene(self.state)
        self.ui = ViewerUI(self.state)

    def on_key(self, win, key, scancode, action, mods):
        self.imgui_renderer.keyboard_callback(win, key, scancode, action, mods)

        io = imgui.get_io()
        if io.want_capture_keyboard:
            return

        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)
            elif key == glfw.KEY_TAB and action == glfw.PRESS:
                self.state.active_camera_idx = (self.state.active_camera_idx + 1) % len(self.state.cameras)

    def on_mouse_move(self, win, xpos, ypos):
        self.imgui_renderer.mouse_callback(win, xpos, ypos)

        io = imgui.get_io()
        if io.want_capture_mouse:
            self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
            return

        old = self.mouse
        self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
        
        active_cam = self.state.cameras[self.state.active_camera_idx]

        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT):
            active_cam.drag(old, self.mouse, glfw.get_window_size(win))

        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT):
            active_cam.pan(old, self.mouse)

    def on_scroll(self, win, dx, dy):
        self.imgui_renderer.scroll_callback(win, dx, dy)

        io = imgui.get_io()
        if io.want_capture_mouse:
            return

        active_cam = self.state.cameras[self.state.active_camera_idx]
        active_cam.zoom(dy, glfw.get_window_size(win)[1])
        
    def on_char(self, win, codepoint):
        self.imgui_renderer.char_callback(win, codepoint)

    def run(self):
        while not glfw.window_should_close(self.win):
            glfw.poll_events()

            self.imgui_renderer.process_inputs()
            imgui.new_frame()

            self.ui.draw()
            self.scene.update()

            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
            
            active_cam = self.state.cameras[self.state.active_camera_idx]
            view = active_cam.view_matrix()
            projection = active_cam.projection_matrix(win_size)

            self.scene.draw(projection, view)

            imgui.render()
            self.imgui_renderer.render(imgui.get_draw_data())

            glfw.swap_buffers(self.win)

        self.shutdown()

    def shutdown(self):
        if self.imgui_renderer is not None:
            self.imgui_renderer.shutdown()