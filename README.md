# 🛒 商城后端系统

基于 FastAPI + SQLAlchemy + MySQL 的电商后台 API 项目，支持用户认证、商品管理、多级分类、订单处理和库存流水跟踪。

---

## 📌 项目简介

本项目是一个完整的 Python Web 后端应用，实现了以下核心功能：

- 用户注册、登录、JWT 身份认证
- 商品增删改查，支持按分类筛选
- 多级分类树形结构（无限级嵌套）
- 订单创建，自动扣减库存，记录出库流水
- 手动入库/出库，支持通过条形码自动创建商品
- 完整的库存变动流水记录
- 使用 Alembic 进行数据库迁移管理

项目代码分层清晰，采用 `models`、`schemas`、`routers` 分离架构，适合学习 FastAPI + SQLAlchemy 的实战项目。

---

## 🛠️ 技术栈

| 类别 | 技术 |
| :--- | :--- |
| 语言 | Python 3.10+ |
| 框架 | FastAPI |
| ORM | SQLAlchemy 2.0 |
| 数据库 | MySQL / SQLite（开发可用 SQLite） |
| 迁移工具 | Alembic |
| 认证 | JWT（python-jose） + bcrypt（passlib） |
| 文档 | Swagger UI（自动生成） |

## 📁 项目结构

```
web/
├── main.py                         # 应用入口
├── alembic/                        # 数据库迁移目录
├── app/
│   ├── database.py                 # 数据库连接
│   ├── core/                       # 认证工具
│   ├── models/                     # 数据表模型
│   ├── schemas/                    # Pydantic 校验模型
│   └── routers/                    # 路由层（业务逻辑）
├── requirements.txt                # 项目依赖
└── .gitignore                      # Git 忽略文件
```

## 🚀 本地运行

### 环境要求
- Python 3.10+
- MySQL（可选，使用 SQLite 时无需安装）

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/Lazzy-A/web-.git
cd web-

# 2. 创建虚拟环境
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 修改数据库配置（如使用 MySQL，编辑 app/database.py）
# 默认使用 SQLite，无需额外配置

# 5. 执行数据库迁移（首次运行）
alembic upgrade head

# 6. 启动服务
fastapi dev main.py
```
📚 API 文档
启动服务后，Swagger 自动生成：

用户模块：/users/register、/users/login、/users/me

商品模块：/products/（支持分页、筛选）、/products/{id}

分类模块：/categories/、/categories/tree（树形结构）

订单模块：/orders/（下单自动扣库存）、/orders/{id}/status

库存模块：/inventory/in（入库）、/inventory/out（出库）、/inventory/logs（流水查询）

所有受保护接口需在 Swagger 右上角点击 Authorize，输入 JWT Token。

🧪 核心业务流程演示
入库流程（支持自动创建商品）
发送 POST /inventory/in，带上 barcode、quantity

如果商品存在 → 直接增加库存

如果商品不存在 → 需要提供 tradename 和 price，系统自动创建商品再入库

下单扣库存流程
发送 POST /orders/，带上 product_id、quantity

系统检查库存是否充足

扣减库存，创建订单，记录出库流水

📝 数据库迁移（Alembic）
bash
# 修改模型后生成迁移脚本
alembic revision --autogenerate -m "修改描述"

# 执行迁移
alembic upgrade head

# 回滚
alembic downgrade -1

🤝 贡献
本项目为个人学习项目，欢迎 Fork 或提出 Issue。

📬 联系方式
GitHub：@Lazzy-A

Email：2032433425@qq.com
