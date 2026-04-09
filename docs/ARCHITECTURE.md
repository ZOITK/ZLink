# ZLink Framework Architecture

ZLink is a high-performance socket framework designed for cross-platform symmetry.

## Directory Structure

- **sdk/**: Core engine and libraries. Every language SDK is contained in a `zlink/` folder for easy portability.
  - **server/zlink/**: Go Socket Engine (Source of truth for server logic).
  - **client/**: Platform-specific client SDKs.
    - **py/zlink/**: Python communication module.
    - **unity/zlink/**: Unity C# communication module.
- **examples/**: Sample projects demonstrating SDK usage.
  - **server-go/**: Example Go server (Uses `sdk/server/zlink`).
  - **client-py/**: Example Python client (Uses `sdk/client/py/zlink`).
  - **client-unity/**: Example Unity client (Uses `sdk/client/unity/zlink`).
- **generator/**: Protocol generation tool (converts YAML schemas to code).
- **docs/**: Architectural documentation and guides.

## Portability

The `zlink/` folder within each SDK is the atomic unit of portability. To start a new project, simply copy the `zlink/` folder for your desired platform and include it in your project as a library.
