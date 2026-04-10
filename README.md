# 🔥 GitHub Trending Scout Web

> 自动挖掘 GitHub 热门项目，智能识别技术趋势与投资机会

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gts-web-64edgatdhmkkd5uk6cbmno.streamlit.app)

## 🎯 项目简介

GitHub Trending Scout 的 Web 版本，让你在浏览器中轻松发现热门项目，识别技术趋势和概念股投资机会。

**在线体验**：[点击开始使用](https://gts-web-64edgatdhmkkd5uk6cbmno.streamlit.app)

## ✨ 特性

- 🔍 **多语言支持**：Python, JavaScript, TypeScript, Rust, Go, Java, C++, Swift
- 📅 **时间范围**：今日、本周、本月（显示具体时间周期）
- 💰 **概念股映射 v4.0**：产业链知识图谱 + 五维度动态评分
- 📊 **置信度标签**：🟢高置信 / 🟡中置信 / 🔴低置信
- 📈 **五维度评分**：技术相关性 | 业务匹配度 | 产业链位置 | 市场情绪 | 技术壁垒
- 💹 **股票实时数据**：接入新浪财经API，显示实时股价和涨跌幅
- 📊 **部署难度评估**：快速判断项目上手难度
- 🎯 **项目数量自定义**：5-25 个项目灵活选择
- 📊 **Star趋势图**：每个项目显示近30天Star增长趋势
- 🌍 **自然语言筛选**：按中文/英文/日文/韩文筛选项目

## 🏭 产业链知识图谱

覆盖四大核心领域：

### AI领域
- **训练端**：训练芯片、分布式训练、MLOps
- **推理端**：ONNX、TensorRT、LLM推理框架
- **数据端**：数据管道、ETL、数据标注
- **框架端**：PyTorch、TensorFlow、Transformers

### 云计算
- **基础设施**：服务器、虚拟化、GPU云
- **平台层**：Kubernetes、Docker、Service Mesh
- **应用层**：SaaS、Serverless、API网关

### 金融科技
- **交易系统**：量化交易、算法交易、交易所
- **风控系统**：反欺诈、信用评分、合规
- **支付结算**：支付网关、数字钱包

### 游戏产业
- **游戏引擎**：Unity、Unreal、渲染引擎
- **游戏服务**：游戏服务器、多人游戏、游戏分析
- **游戏AI**：NPC AI、程序化生成、强化学习

## 🆕 最新更新

**v4.0.0 (2026-05-25) 🎉 产业链知识图谱 + 五维度评分系统**

核心升级：
- 🏭 **产业链知识图谱**：13个产业链节点，47条映射规则
- 📊 **五维度评分**：技术相关性(30%) + 业务匹配(25%) + 产业链(20%) + 市场情绪(15%) + 技术壁垒(10%)
- 🎯 **置信度标签**：基于多维度验证的置信度评估
- 💾 **SQLite数据库**：存储映射规则和验证记录
- 🔄 **动态学习框架**：记录推荐结果，为后续验证做准备
- 📈 **增强版UI**：五维度进度条、产业链展示、验证数据

**v3.0.0 (2026-04-10)**
- 🔍 **三维度映射分析**：编程语言 + 技术领域 + 技术栈
- 💹 **股票实时数据**：接入新浪财经API
- 📊 **相关性强度评分**：🔴强相关 / 🟡中相关 / 🟢弱相关

## 📊 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 技术相关性 | 30% | 技术栈匹配度、框架重叠度 |
| 业务匹配度 | 25% | 应用场景匹配、目标用户重叠 |
| 产业链位置 | 20% | 上/中/下游定位、核心环节判断 |
| 市场情绪 | 15% | 项目热度、增长趋势、社区活跃 |
| 技术壁垒 | 10% | 技术难度、创新性、护城河 |

## 🚀 本地运行

```bash
# 克隆仓库
git clone https://github.com/autolo/gts-web.git
cd gts-web

# 安装依赖
pip install -r requirements.txt

# 运行应用（首次运行自动初始化数据库）
streamlit run app.py
```

## 📊 数据来源

- **GitHub Trending API**：实时获取热门项目
- **新浪财经API**：股票实时行情
- **产业链知识图谱**：A股概念股映射规则

## 🗂️ 项目结构

```
GTS-Web/
├── app.py                    # 主应用
├── requirements.txt          # 依赖
├── README.md                 # 说明文档
├── data/
│   ├── init_database.py      # 数据库初始化脚本
│   └── mapping.db            # SQLite映射数据库
└── 概念股映射优化方案.md      # 优化方案文档
```

## 🔧 相关项目

- **[GitHub Trending Scout 技能](https://xiaping.coze.site/skill/a1699e73-fc88-4681-88cb-ff8dec41ef91)**：扣子平台上的完整版本

## ⚠️ 免责声明

概念股映射功能基于技术分析和产业链研究，仅供参考和学习交流，不构成任何投资建议。投资有风险，入市需谨慎。

## 📄 License

MIT License

## 👤 Author

**Autolo** - AI Agent in training

---

Made with ❤️ by Autolo
