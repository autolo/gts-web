import streamlit as st
import requests
import json
from datetime import datetime
import time
from typing import Dict, List, Optional

# 页面配置
st.set_page_config(
    page_title="GitHub Trending Scout",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 缓存配置
@st.cache_data(ttl=300)  # 5分钟缓存
def fetch_github_trending(language: str, since: str, limit: int) -> List[Dict]:
    """获取GitHub热门项目 - 使用第三方Trending API"""
    try:
        # 方法1: 使用第三方 GitHub Trending API
        # API文档: https://github.com/huchenme/github-trending-api
        
        base_url = "https://github-trending-api.now.sh/repositories"
        
        params = {
            "limit": min(limit, 25)  # API限制最多25条
        }
        
        if language != "all":
            params["language"] = language
        
        # since参数: daily, weekly, monthly
        if since in ["daily", "weekly", "monthly"]:
            params["since"] = since
        
        headers = {
            "User-Agent": "GitHub-Trending-Scout",
            "Accept": "application/json"
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data and isinstance(data, list):
            # 标准化数据格式
            normalized = []
            for repo in data[:limit]:
                normalized.append({
                    "full_name": repo.get("author", "") + "/" + repo.get("name", ""),
                    "html_url": "https://github.com/" + repo.get("author", "") + "/" + repo.get("name", ""),
                    "description": repo.get("description", ""),
                    "language": repo.get("language", ""),
                    "stargazers_count": repo.get("stars", 0),
                    "forks_count": repo.get("forks", 0),
                    "open_issues_count": repo.get("currentPeriodStars", 0),  # 用当前周期stars代替
                    "stars_today": repo.get("starsSince", repo.get("currentPeriodStars", 0)),
                    "updated_at": datetime.now().isoformat()
                })
            return normalized
        
        return []
        
    except Exception as e:
        st.warning(f"主要API调用失败，尝试备用方案: {str(e)}")
        return fetch_from_backup_api(language, since, limit)

@st.cache_data(ttl=300)
def fetch_from_backup_api(language: str, since: str, limit: int) -> List[Dict]:
    """备用API - 使用另一个数据源"""
    try:
        # 备用API: https://api.oioweb.cn/api/github/trending
        base_url = "https://api.oioweb.cn/api/github/trending"
        
        params = {}
        if language != "all":
            params["language"] = language
        if since in ["daily", "weekly", "monthly"]:
            params["since"] = since
        
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == 200 and "result" in data:
            normalized = []
            for repo in data["result"][:limit]:
                # 解析项目名（格式：author/name）
                name_parts = repo.get("repository", "").split("/")
                author = name_parts[0] if len(name_parts) > 0 else ""
                name = name_parts[1] if len(name_parts) > 1 else ""
                
                normalized.append({
                    "full_name": f"{author}/{name}",
                    "html_url": repo.get("url", f"https://github.com/{author}/{name}"),
                    "description": repo.get("description", ""),
                    "language": repo.get("language", ""),
                    "stargazers_count": repo.get("stars", 0),
                    "forks_count": repo.get("forks", 0),
                    "open_issues_count": 0,
                    "stars_today": repo.get("starsSince", 0),
                    "updated_at": datetime.now().isoformat()
                })
            return normalized
        
        return []
        
    except Exception as e:
        st.warning(f"备用API也失败，使用本地缓存数据")
        return get_fallback_data(language, limit)

def get_fallback_data(language: str, limit: int) -> List[Dict]:
    """最终备用：本地数据"""
    fallback_projects = [
        {
            "full_name": "modelscope/swift",
            "html_url": "https://github.com/modelscope/swift",
            "description": "ModelScope Swift: 魔搭社区官方提供的模型微调、推理框架",
            "language": "Python",
            "stargazers_count": 8500,
            "forks_count": 1200,
            "open_issues_count": 45,
            "stars_today": 150,
            "updated_at": "2026-04-10T00:00:00Z"
        },
        {
            "full_name": "microsoft/semantic-kernel",
            "html_url": "https://github.com/microsoft/semantic-kernel",
            "description": "Semantic Kernel: 微软官方AI开发框架，支持多语言AI应用开发",
            "language": "C#",
            "stargazers_count": 22000,
            "forks_count": 3400,
            "open_issues_count": 120,
            "stars_today": 89,
            "updated_at": "2026-04-10T00:00:00Z"
        },
        {
            "full_name": "langchain-ai/langchain",
            "html_url": "https://github.com/langchain-ai/langchain",
            "description": "LangChain: 构建LLM应用的开发框架，支持链式调用和工具集成",
            "language": "Python",
            "stargazers_count": 95000,
            "forks_count": 15000,
            "open_issues_count": 450,
            "stars_today": 320,
            "updated_at": "2026-04-10T00:00:00Z"
        },
        {
            "full_name": "denoland/deno",
            "html_url": "https://github.com/denoland/deno",
            "description": "Deno: 现代JavaScript和TypeScript运行时",
            "language": "Rust",
            "stargazers_count": 98000,
            "forks_count": 5400,
            "open_issues_count": 890,
            "stars_today": 78,
            "updated_at": "2026-04-10T00:00:00Z"
        },
        {
            "full_name": "vercel/next.js",
            "html_url": "https://github.com/vercel/next.js",
            "description": "Next.js: React框架，支持SSR、SSG、ISR等多种渲染模式",
            "language": "JavaScript",
            "stargazers_count": 125000,
            "forks_count": 26700,
            "open_issues_count": 1200,
            "stars_today": 450,
            "updated_at": "2026-04-10T00:00:00Z"
        }
    ]
    
    if language != "all":
        fallback_projects = [p for p in fallback_projects if p["language"].lower() == language.lower()]
    
    return fallback_projects[:limit]

# 概念股映射（增强版）
CONCEPT_STOCK_MAP = {
    "Python": {
        "stocks": ["东方财富", "同花顺", "恒生电子"],
        "reason": "Python是AI/数据科学首选语言，金融科技、量化交易核心"
    },
    "JavaScript": {
        "stocks": ["科大讯飞", "寒武纪", "海光信息"],
        "reason": "前端框架生态，AI应用层开发"
    },
    "TypeScript": {
        "stocks": ["科大讯飞", "寒武纪", "海光信息"],
        "reason": "企业级应用开发，AI工具链建设"
    },
    "Rust": {
        "stocks": ["中科曙光", "浪潮信息", "紫光股份"],
        "reason": "高性能计算，系统级开发，国产化替代"
    },
    "Go": {
        "stocks": ["中科曙光", "浪潮信息", "紫光股份"],
        "reason": "云原生、微服务架构，基础设施软件"
    },
    "Java": {
        "stocks": ["东方财富", "恒生电子", "金证股份"],
        "reason": "企业级应用，金融系统核心"
    },
    "C++": {
        "stocks": ["中科曙光", "浪潮信息", "寒武纪"],
        "reason": "高性能计算，AI推理引擎，游戏引擎"
    },
    "Swift": {
        "stocks": ["立讯精密", "歌尔股份", "蓝思科技"],
        "reason": "iOS生态，消费电子产业链"
    },
    "C#": {
        "stocks": ["科大讯飞", "用友网络", "金山办公"],
        "reason": "企业软件，办公自动化，AI应用"
    },
    "Unknown": {
        "stocks": ["待分析"],
        "reason": "暂无映射数据"
    }
}

# 趋势信号分析
def analyze_trend_signal(repo: Dict) -> Dict:
    """分析项目趋势信号"""
    stars = repo.get("stargazers_count", 0)
    stars_today = repo.get("stars_today", 0)
    forks = repo.get("forks_count", 0)
    
    # 计算信号强度
    signal_score = 0
    signals = []
    
    # 今日Star增长信号（更重要）
    if stars_today > 500:
        signal_score += 3
        signals.append(f"🔥 今日暴涨（+{stars_today} stars）")
    elif stars_today > 100:
        signal_score += 2
        signals.append(f"⭐ 今日热门（+{stars_today} stars）")
    elif stars_today > 50:
        signal_score += 1
        signals.append(f"📈 持续增长（+{stars_today} stars）")
    
    # 总Star规模
    if stars > 50000:
        signal_score += 2
        signals.append("🏆 明星项目（50K+ stars）")
    elif stars > 10000:
        signal_score += 1
        signals.append("⭐ 成熟项目（10K+ stars）")
    
    # Fork活跃度
    if forks > 1000:
        signal_score += 1
        signals.append("💪 高度活跃（1K+ forks）")
    
    # 信号等级
    if signal_score >= 6:
        level = "P0"
        level_desc = "🔥 紧急关注"
    elif signal_score >= 4:
        level = "P1"
        level_desc = "⭐ 重点跟踪"
    elif signal_score >= 2:
        level = "P2"
        level_desc = "👀 持续观察"
    else:
        level = "P3"
        level_desc = "📝 一般关注"
    
    return {
        "score": signal_score,
        "level": level,
        "level_desc": level_desc,
        "signals": signals,
        "stars_today": stars_today
    }

# 部署难度评估
def assess_difficulty(repo: Dict) -> Dict:
    """评估部署难度"""
    language = repo.get("language", "Unknown")
    description = repo.get("description", "").lower()
    
    difficulty = 1  # 1-5星
    factors = []
    
    # 语言难度
    lang_difficulty = {
        "Python": 1,
        "JavaScript": 1,
        "TypeScript": 2,
        "Go": 2,
        "Rust": 4,
        "C++": 4,
        "Java": 2,
        "Swift": 3,
        "C#": 2,
        "Unknown": 2
    }
    difficulty = lang_difficulty.get(language, 2)
    
    # 检查关键词
    if "docker" in description or "kubernetes" in description:
        factors.append("🐳 容器化部署")
    if "api" in description or "server" in description:
        factors.append("🖥️ 需要服务器")
    if "gpu" in description or "cuda" in description:
        factors.append("🎮 需要GPU")
        difficulty = min(difficulty + 1, 5)
    if "model" in description or "ai" in description or "llm" in description:
        factors.append("🤖 AI模型")
    
    stars = difficulty * "⭐"
    
    return {
        "level": difficulty,
        "stars": stars,
        "factors": factors
    }

# 主界面
st.title("🔥 GitHub Trending Scout")
st.markdown("**自动挖掘GitHub热门项目，智能识别技术趋势与投资机会**")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 配置")
    
    language = st.selectbox(
        "编程语言",
        ["all", "python", "javascript", "typescript", "rust", "go", "java", "c++", "swift", "c#"],
        index=0
    )
    
    since = st.selectbox(
        "时间范围",
        ["daily", "weekly", "monthly"],
        index=0,
        help="daily=今日热门, weekly=本周热门, monthly=本月热门"
    )
    
    limit = st.slider("项目数量", 5, 25, 10)
    
    st.markdown("---")
    
    # 显示模式
    view_mode = st.radio(
        "显示模式",
        ["卡片视图", "表格视图"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📊 功能说明")
    st.markdown("""
    - 🔍 **热门项目发现**：实时获取GitHub Trending
    - 📈 **趋势信号分析**：P0/P1/P2分级
    - 💰 **概念股映射**：技术趋势→A股映射
    - 🚀 **部署评估**：快速判断上手难度
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ by [Autolo](https://github.com/autolo)")

# 主内容区
col_stats1, col_stats2, col_stats3 = st.columns(3)
with col_stats1:
    time_map = {"daily": "今日", "weekly": "本周", "monthly": "本月"}
    st.metric("📅 时间范围", time_map.get(since, since))
with col_stats2:
    st.metric("🔄 缓存时间", "5分钟")
with col_stats3:
    lang_count = len([l for l in ["python", "javascript", "typescript", "rust", "go", "java", "c++", "swift", "c#"] if l == language or language == "all"])
    st.metric("🌐 支持语言", f"{lang_count}种" if language == "all" else language.title())

st.markdown("---")

# 获取数据按钮
if st.button("🚀 获取热门项目", type="primary", use_container_width=True):
    with st.spinner("正在从 GitHub Trending 获取数据..."):
        projects = fetch_github_trending(language, since, limit)
        
        if projects:
            st.success(f"✅ 获取到 {len(projects)} 个热门项目（{time_map.get(since, since)}）")
            
            # 表格视图
            if view_mode == "表格视图":
                table_data = []
                for i, repo in enumerate(projects, 1):
                    trend = analyze_trend_signal(repo)
                    difficulty = assess_difficulty(repo)
                    stock_info = CONCEPT_STOCK_MAP.get(repo.get("language", "Unknown"), CONCEPT_STOCK_MAP["Unknown"])
                    
                    stars_today = repo.get("stars_today", 0)
                    stars_today_str = f"+{stars_today}" if stars_today > 0 else "-"
                    
                    table_data.append({
                        "排名": i,
                        "项目名称": f"[{repo['full_name']}]({repo['html_url']})",
                        "语言": repo.get("language", "-"),
                        "总Stars": f"{repo['stargazers_count']:,}",
                        "今日增长": stars_today_str,
                        "趋势": trend["level"],
                        "概念股": stock_info["stocks"][0]
                    })
                
                st.dataframe(
                    table_data,
                    use_container_width=True,
                    hide_index=True
                )
            
            # 卡片视图
            else:
                for i, repo in enumerate(projects, 1):
                    trend = analyze_trend_signal(repo)
                    difficulty = assess_difficulty(repo)
                    stock_info = CONCEPT_STOCK_MAP.get(repo.get("language", "Unknown"), CONCEPT_STOCK_MAP["Unknown"])
                    
                    with st.container():
                        # 项目标题行
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"### {i}. [{repo['full_name']}]({repo['html_url']})")
                            st.markdown(f"📝 {repo.get('description', '暂无描述')[:150]}...")
                        
                        with col2:
                            stars_today = repo.get("stars_today", 0)
                            st.metric("趋势信号", trend["level_desc"], f"+{stars_today} stars")
                        
                        with col3:
                            st.metric("部署难度", difficulty["stars"])
                        
                        # 详细信息行
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            tags = []
                            if repo.get('language'):
                                tags.append(f"🖥️ {repo['language']}")
                            tags.append(f"⭐ {repo['stargazers_count']:,}")
                            tags.append(f"🍴 {repo['forks_count']:,}")
                            st.markdown(" | ".join(tags))
                        
                        with col2:
                            st.markdown(f"💰 **概念股**: {', '.join(stock_info['stocks'])}")
                            st.markdown(f"📋 *{stock_info['reason']}*")
                        
                        with col3:
                            for signal in trend["signals"][:2]:  # 只显示前2个信号
                                st.markdown(signal)
                        
                        st.markdown("---")
            
            # 统计信息
            st.markdown("### 📊 数据统计")
            col1, col2, col3, col4 = st.columns(4)
            
            total_stars = sum(p.get("stargazers_count", 0) for p in projects)
            avg_stars = total_stars // len(projects) if projects else 0
            total_stars_today = sum(p.get("stars_today", 0) for p in projects)
            languages = [p.get("language", "Unknown") for p in projects if p.get("language")]
            top_language = max(set(languages), key=languages.count) if languages else "Unknown"
            p0_p1_count = sum(1 for p in projects if analyze_trend_signal(p)["level"] in ["P0", "P1"])
            
            with col1:
                st.metric("总Stars", f"{total_stars:,}")
            with col2:
                st.metric(f"{time_map.get(since, '')}增长", f"+{total_stars_today:,}")
            with col3:
                st.metric("热门语言", top_language)
            with col4:
                st.metric("P0/P1项目", p0_p1_count)
        else:
            st.error("获取数据失败，请稍后重试")

# 底部信息
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94A3B8;'>
    💡 <b>提示</b>：点击项目名称可跳转到GitHub页面 | 
    数据来源：GitHub Trending API | 
    概念股映射仅供参考，不构成投资建议
</div>
""", unsafe_allow_html=True)
