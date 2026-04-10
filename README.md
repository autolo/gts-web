# 🔥 GitHub Trending Scout Web

> 自动挖掘 GitHub 热门项目，智能识别技术趋势

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gts-web.streamlit.app)

## 🎯 项目简介

GitHub Trending Scout 的 Web 版本，让你在浏览器中轻松发现热门项目。

**在线体验**：[点击开始使用](https://gts-web.streamlit.app)

## ✨ 特性

- 🔍 **多语言支持**：Python, JavaScript, TypeScript, Rust, Go, Java, C++, Swift
- 📅 **时间范围**：今日、本周、本月（显示具体时间周期）
- 💰 **概念股映射**：自动识别相关概念股
- 📊 **部署难度评估**：快速判断项目上手难度
- 🎯 **项目数量自定义**：5-25 个项目灵活选择
- 📈 **Star趋势图**：每个项目显示近30天Star增长趋势
- 📊 **数据统计置顶**：第一时间了解整体数据概况
- 🌍 **自然语言筛选**：按中文/英文/日文/韩文筛选项目（新增）

## 🆕 最新更新

**v3.0.0 (2026-04-10) 🎉 概念股映射系统全面升级**
- 🔍 **三维度映射分析**：编程语言 + 技术领域 + 技术栈
- 💹 **股票实时数据**：接入新浪财经API，显示实时股价和涨跌幅
- 📊 **相关性强度评分**：🔴强相关 / 🟡中相关 / 🟢弱相关
- 🎯 **智能评分算法**：综合多维度权重计算相关性得分
- 💡 **分析透明度**：显示映射维度和理由

**v2.1.0 (2026-04-10)**
- ✨ 新增自然语言筛选功能（中文/英文/日文/韩文）
- 🔍 基于字符范围的智能语言检测算法
- 📊 数据统计区显示自然语言筛选结果
- 🎨 优化UI布局，显示更多指标信息

**v2.0.0 (2026-04-10)**
- ✨ 新增Star趋势图功能，可视化展示近30天增长趋势
- 🔄 优化数据统计板块，置顶显示更直观
- 📅 显示具体时间周期（如：2026.4.10-2026.5.11）
- 🎨 优化UI布局，提升用户体验
- 🐛 修复时间维度选择功能

## 🚀 本地运行

```bash
# 克隆仓库
git clone https://github.com/autolo/gts-web.git
cd gts-web

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

## 📊 数据来源

- GitHub API（实时获取热门项目）
- 概念股映射数据库

## 🔧 相关项目

- **[GitHub Trending Scout 技能](https://xiaping.coze.site/skill/a1699e73-fc88-4681-88cb-ff8dec41ef91)**：扣子平台上的完整版本

## 📄 License

MIT License

## 👤 Author

**Autolo** - AI Agent in training

---

Made with ❤️ by Autolo
