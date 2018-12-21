# GLSLInclude
A simple Python script to support `#include` keyword in GLSL shaders

Just write your shader file with `#include` statement(s) and name of the module next to it. Then run this script. It will swap the `#include` statements with respective modules.
## How to Use

Module Shader File: **fog.glsl**
```glsl
vec4 CalculateFogPosition(mat4 ligthSpace)
{
    return lightSpace * model * vec4(position, 1.0f);
}
```

Shader File: **shadow.glsl**
```glsl
#version 330 core
layout (location = 0) in vec3 position;

uniform mat4 model;
uniform mat4 lightSpace;

// module file extension is not needed
#include fog 

void main()
{
    gl_Position = CalculateFogPosition(lightSpace)
}
```

Run the script with Python 3.

```shell
python3 reproduce_shaders.py
```
You can also specify paths for base, module and output folders. Default values are, `./` `./util` and `./output` respectively.

```shell
python3 reproduce_shaders.py --base=base_path --module=module_path --output=output_path
```

The final produced shadowVS.glsl will be following.

Shader File: **output/shadow.glsl**
```glsl
#version 330 core
layout (location = 0) in vec3 position;

uniform mat4 model;
uniform mat4 lightSpace;

vec4 CalculateFogPosition(mat4 ligthSpace)
{
    return lightSpace * model * vec4(position, 1.0f);
}

void main()
{
    gl_Position = CalculateFogPosition(lightSpace)
}
```
