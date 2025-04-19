# 开发指南

## 开发环境设置

### 系统要求
- Windows/Linux/macOS
- C++编译器（支持C++11）
- Python 3.x
- CMake 3.10+

### 依赖安装

#### Python依赖
```bash
pip install -r requirements.txt
```

#### C++依赖
- 无外部依赖

## 构建项目

### C++部分
```bash
mkdir build
cd build
cmake ..
make
```

### Python部分
无需特殊构建步骤

## 代码风格

### C++代码风格
- 遵循Google C++ Style Guide
- 使用4空格缩进
- 使用C++11特性

### Python代码风格
- 遵循PEP 8
- 使用4空格缩进
- 使用类型注解

## 测试
运行测试：
```bash
python -m pytest test/
```

## 提交代码
1. 创建新的分支
2. 编写代码和测试
3. 运行测试
4. 提交Pull Request

## 版本控制
- 使用语义化版本号
- 主版本号.次版本号.修订号
- 重大更新时增加主版本号 