# Setup Guide: Python Environment and Dependencies

This guide documents the steps to set up the agent-patterns project, including solutions for common Python/pip dependency issues on Ubuntu systems.

## Prerequisites

- Python 3.10+
- Ubuntu/Debian-based Linux system
- Git (for cloning the repository)

## Common Issues and Solutions

### Issue 1: System-Managed Python Environment

**Symptom:**
```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    xyz, where xyz is the package you are trying to
    install.
```

**Root Cause:**
Modern Ubuntu systems (especially 23.04+) use externally-managed Python environments. The system package manager controls Python, and pip refuses to install globally to prevent breaking system packages.

**Solution: Use `--user` Flag (Recommended)**

Install packages to your user directory:
```bash
python3 -m pip install --user mcp aiosqlite
```

**Rationale:**
- `--user` installs to `~/.local/` directory
- Does not require root/sudo
- Does not affect system Python
- Safe and non-destructive
- Survives Python version updates

**Alternative (Not Recommended): Break System Management**

```bash
python3 -m pip install --break-system-packages mcp aiosqlite
```

⚠️ **Only use this if absolutely necessary.** This disables pip's safety checks and could break system packages. With `--user`, this is never necessary.

---

### Issue 2: Missing Python Virtual Environment Support

**Symptom:**
```
Error: No module named venv
```

Or when trying to create venv:
```
The virtual environment was not created successfully because ensurepip is not available.
```

**Root Cause:**
Some minimal Python installations don't include the venv module. This is common in containerized or minimal system builds.

**Solution: Use `--user` Global Installation**

Since venv isn't available, use global `--user` installation instead:
```bash
python3 -m pip install --user mcp aiosqlite
```

**Rationale:**
- Works without venv
- Cleaner than system-wide installation
- Still isolated to user directory
- Sufficient for development

---

### Issue 3: pip Command Not Found

**Symptom:**
```
command not found: pip
command not found: pip3
```

**Root Cause:**
pip may not be available in the PATH, or Python is installed without pip.

**Solution: Use Python Module Approach**

```bash
python3 -m pip install --user mcp aiosqlite
```

Or install pip first:
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user --break-system-packages
rm get-pip.py
```

**Rationale:**
- `python3 -m pip` bypasses PATH issues
- Works reliably across systems
- Module syntax is more portable than direct command

---

## Installation Steps

### Step 1: Verify Python Version

```bash
python3 --version
```

Should be Python 3.10 or higher.

### Step 2: Install Dependencies

Install required packages to user directory:
```bash
python3 -m pip install --user mcp aiosqlite
```

**What gets installed:**
- `mcp` (1.25.0+) - Model Context Protocol for building MCP servers
- `aiosqlite` (0.20.0+) - Async SQLite database library

### Step 3: Set PYTHONPATH for Running the Server

When running the MCP server from the project root:

```bash
export PYTHONPATH=/path/to/agent-patterns/mcp-server/src
python3 -m task_manager_mcp.server
```

Or as a single command:
```bash
PYTHONPATH=/home/ywatanabe/dev/agent-patterns/mcp-server/src python3 -m task_manager_mcp.server
```

**Why PYTHONPATH?**
The MCP server module is in `mcp-server/src/task_manager_mcp/`. Python needs to know where to find it.

---

## Troubleshooting

### Checking Installation

Verify packages are installed:
```bash
python3 -m pip list | grep -E "mcp|aiosqlite"
```

Should show:
```
aiosqlite          0.20.0
mcp                1.25.0
```

### Finding User Package Location

Check where `--user` packages are installed:
```bash
python3 -m site --user-site
```

Typical output:
```
/home/username/.local/lib/python3.12/site-packages
```

### Fixing "Module Not Found" Errors

If you get `ModuleNotFoundError: No module named 'mcp'`:

1. Verify installation: `python3 -m pip list | grep mcp`
2. Check PYTHONPATH is set correctly
3. Try reinstalling: `python3 -m pip install --user --upgrade mcp`

---

## macOS Setup (Alternative)

On macOS, you can use either `--user` or virtual environments:

```bash
# Option 1: Using --user (simpler)
python3 -m pip install --user mcp aiosqlite

# Option 2: Using venv (traditional)
python3 -m venv venv
source venv/bin/activate
pip install mcp aiosqlite
```

---

## Windows Setup (WSL2)

If using Windows Subsystem for Linux (WSL2):

```bash
# Update system
sudo apt update
sudo apt install python3-pip python3-venv

# Install packages
python3 -m pip install --user mcp aiosqlite

# Set PYTHONPATH before running
set PYTHONPATH=/home/username/agent-patterns/mcp-server/src
python3 -m task_manager_mcp.server
```

---

## SDK Examples Setup

### Python Examples

```bash
cd sdk-examples/python
pip install --user -r requirements.txt
python3 with_skill.py
python3 basic_mcp.py
```

### TypeScript Examples

```bash
cd sdk-examples/typescript
npm install
npx tsx with_skill.ts
npx tsx basic_mcp.ts
```

---

## Summary of Fixes Applied to This Project

When first setting up this project, these issues were encountered and resolved:

1. **Externally-managed environment error** → Solved with `--user` flag
2. **Missing venv module** → Avoided by using `--user` installation
3. **FastMCP API incompatibility** → Updated server.py to use correct API
   - Removed `version` parameter from FastMCP initialization
   - Changed from `mcp.run()` context manager to `await mcp.run_stdio_async()`
   - Changed from `asyncio.run(main())` back to proper event loop handling

---

## Next Steps

After setting up dependencies:

1. **Start MCP Server**:
   ```bash
   PYTHONPATH=/path/to/agent-patterns/mcp-server/src python3 -m task_manager_mcp.server
   ```

2. **Register with Claude Code**:
   ```bash
   claude mcp add --transport stdio task-manager \
     -- python3 -m task_manager_mcp.server
   ```

3. **Test in Claude Code**:
   ```
   > Create a task to review the authentication PR
   > Show me all high-priority tasks
   ```

4. **Run SDK Examples**:
   - See `sdk-examples/python/` for Python integration
   - See `sdk-examples/typescript/` for TypeScript integration

---

## References

- [Python venv documentation](https://docs.python.org/3/library/venv.html)
- [PEP 668 - Externally managed environments](https://peps.python.org/pep-0668/)
- [MCP Server documentation](https://modelcontextprotocol.io/)
- [FastMCP on GitHub](https://github.com/jlowin/fastmcp)
