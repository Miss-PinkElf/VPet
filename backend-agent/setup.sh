#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv"
REQUIREMENTS_PATH="$SCRIPT_DIR/requirements.txt"

echo "========================================"
echo "  Backend 环境初始化脚本 (推荐 Python 3.11，最低 3.9)"
echo "========================================"

check_python_version() {
    local cmd="$1"
    "$cmd" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1
}

get_python_version() {
    local cmd="$1"
    "$cmd" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")' 2>/dev/null
}

if [ -d "$VENV_PATH" ]; then
    echo "[INFO] 虚拟环境已存在: $VENV_PATH"
else
    echo "[STEP 1] 检查 Python 环境..."
    
    PYTHON_CMD=""
    PYTHON_SOURCE=""

    if command -v python3.11 >/dev/null 2>&1 && check_python_version "python3.11"; then
        PYTHON_CMD="python3.11"
        PYTHON_SOURCE="system"
    elif command -v pyenv >/dev/null 2>&1; then
        PYENV_311_VERSION="$(pyenv versions --bare 2>/dev/null | awk '/^3\.11(\.|$)/ { print; exit }')"
        if [ -n "$PYENV_311_VERSION" ]; then
            PYENV_ROOT="$(pyenv root)"
            PYENV_311_BIN="$PYENV_ROOT/versions/$PYENV_311_VERSION/bin/python"
            if [ -x "$PYENV_311_BIN" ] && check_python_version "$PYENV_311_BIN"; then
                PYTHON_CMD="$PYENV_311_BIN"
                PYTHON_SOURCE="pyenv:$PYENV_311_VERSION"
            fi
        fi
    fi

    if [ -z "$PYTHON_CMD" ] && command -v python3 >/dev/null 2>&1 && check_python_version "python3"; then
        PYTHON_CMD="python3"
        PYTHON_SOURCE="system"
    fi

    if [ -z "$PYTHON_CMD" ] && command -v python >/dev/null 2>&1 && check_python_version "python"; then
        PYTHON_CMD="python"
        PYTHON_SOURCE="system"
    fi

    if [ -n "$PYTHON_CMD" ]; then
        PY_VER="$(get_python_version "$PYTHON_CMD")"
        echo "[OK] 使用 Python: $PY_VER ($PYTHON_SOURCE)"
        if [[ "$PY_VER" != 3.11.* ]]; then
            echo "[WARN] 当前不是 Python 3.11，继续使用兼容版本创建虚拟环境"
        fi
    fi

    if [ -z "$PYTHON_CMD" ]; then
        echo "[ERROR] 未找到可用的 Python（需要 >= 3.9）"
        echo "Mac: brew install python@3.11"
        echo "Mac (pyenv): pyenv install 3.11.11"
        echo "Ubuntu: sudo apt install python3.11 python3.11-venv"
        exit 1
    fi

    echo "[STEP 2] 创建虚拟环境..."
    $PYTHON_CMD -m venv "$VENV_PATH"
    echo "[OK] 虚拟环境创建成功"
fi

BIN_PATH="$VENV_PATH/bin"
ACTIVATE_SH="$BIN_PATH/activate"

echo "[STEP 3] 检查激活脚本..."
if [ -f "$ACTIVATE_SH" ]; then
    echo "[OK] 激活脚本已就绪"
    echo "  - activate (Bash/Zsh)"
else
    echo "[WARN] 缺少激活脚本"
fi

echo "[STEP 4] 安装依赖..."
source "$ACTIVATE_SH"

if [ -f "$REQUIREMENTS_PATH" ]; then
    pip install -r "$REQUIREMENTS_PATH"
    echo "[OK] 依赖安装完成"
else
    echo "[WARN] requirements.txt 不存在，跳过依赖安装"
fi

echo ""
echo "========================================"
echo "  初始化完成！"
echo "========================================"
echo ""
echo "后续使用请运行:"
echo "  source .venv/bin/activate"
echo "  ./run-dev.sh"
echo ""
