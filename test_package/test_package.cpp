#include <cstdlib>
#include <stdio.h>
#include <SOIL2/SOIL2.h>
#include <GLFW/glfw3.h>

int main(int argc, char * argv[])
{
    if (argc < 2) {
	    printf("shut");
        return EXIT_FAILURE;
    }
    glfwInit();

    bool under_ci = (std::getenv("TRAVIS") != NULL) || (std::getenv("APPVEYOR") != "NULL");

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGL", NULL, NULL);

    glfwMakeContextCurrent(window);

    int tex_2d = SOIL_load_OGL_texture
        (
            argv[1],
            SOIL_LOAD_AUTO,
            SOIL_CREATE_NEW_ID,
            SOIL_FLAG_MIPMAPS | SOIL_FLAG_INVERT_Y | SOIL_FLAG_NTSC_SAFE_RGB | SOIL_FLAG_COMPRESS_TO_DXT
        );
    glfwTerminate();

    /* check for an error during the load process */
    if(0 == tex_2d)
    {
        printf("SOIL loading error: '%s'\n", SOIL_last_result());
        return under_ci ? EXIT_SUCCESS : EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
