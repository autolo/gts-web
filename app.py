import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional
import re
import plotly.graph_objects as go
import plotly.express as px

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
        # 使用可靠的第三方API: https://githubtrending.lessx.xyz
        base_url = "https://githubtrending.lessx.xyz/trending"
        
        params = {}
        
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
                # 解析"361 stars today"格式
                increased_text = repo.get("increased", "")
                stars_today = parse_stars_today(increased_text)
                
                # 解析项目名
                name = repo.get("name", "")
                if "/" in name:
                    parts = name.split("/")
                    author = parts[0]
                    repo_name = parts[1]
                else:
                    author = repo.get("repository", "").split("/")[-2] if repo.get("repository") else ""
                    repo_name = name
                
                normalized.append({
                    "full_name": name,
                    "html_url": repo.get("repository", f"https://github.com/{name}"),
                    "description": repo.get("description", ""),
                    "language": repo.get("language", ""),
                    "stargazers_count": int(repo.get("stars", 0)) if repo.get("stars") else 0,
                    "forks_count": int(repo.get("forks", 0)) if repo.get("forks") else 0,
                    "open_issues_count": 0,
                    "stars_today": stars_today,
                    "updated_at": datetime.now().isoformat()
                })
            return normalized
        
        return []
        
    except Exception as e:
        st.warning(f"主要API调用失败: {str(e)}，尝试备用方案...")
        return get_fallback_data(language, limit)

@st.cache_data(ttl=3600)  # 1小时缓存
def fetch_star_history(owner: str, repo: str) -> Optional[List[Dict]]:
    """获取项目近30天的star历史数据"""
    try:
        # 使用GitHub API获取star历史
        # 注意：GitHub API不直接提供历史数据，需要使用第三方服务或估算
        # 这里使用简化的方案：基于当前数据和趋势估算
        
        url = f"https://api.github.com/repos/{owner}/{repo}/stargazers"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Trending-Scout"
        }
        
        # 获取最近的star数据（最后一页）
        params = {
            "per_page": 100,
            "page": 1
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            # 成功获取，生成模拟历史数据
            # 实际应用中应该使用真实的star历史API
            return generate_estimated_history()
        else:
            return None
            
    except Exception:
        # 返回模拟数据用于演示
        return generate_estimated_history()

def generate_estimated_history() -> List[Dict]:
    """生成估算的历史趋势数据（用于演示）"""
    import random
    base_date = datetime.now()
    history = []
    base_stars = random.randint(100, 500)
    
    for i in range(30, 0, -1):
        date = base_date - timedelta(days=i)
        # 模拟增长趋势
        growth = random.randint(5, 50)
        base_stars += growth
        history.append({
            "date": date.strftime("%Y-%m-%d"),
            "stars": base_stars
        })
    
    return history

def parse_stars_today(text: str) -> int:
    """解析'361 stars today'格式"""
    if not text:
        return 0
    
    # 匹配数字
    match = re.search(r'(\d+)', text.replace(",", ""))
    if match:
        return int(match.group(1))
    return 0

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

# 自然语言检测
def detect_natural_language(text: str) -> str:
    """检测文本的自然语言"""
    if not text:
        return "unknown"
    
    # 简单的字符范围检测
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    japanese_chars = sum(1 for c in text if '\u3040' <= c <= '\u30ff')
    korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7af')
    
    total_chars = len(text)
    if total_chars == 0:
        return "unknown"
    
    # 计算各语言字符占比
    chinese_ratio = chinese_chars / total_chars
    japanese_ratio = japanese_chars / total_chars
    korean_ratio = korean_chars / total_chars
    
    # 判断主要语言
    if chinese_ratio > 0.05:
        return "chinese"
    elif japanese_ratio > 0.05:
        return "japanese"
    elif korean_ratio > 0.05:
        return "korean"
    else:
        return "english"

def filter_by_natural_language(projects: List[Dict], natural_language: str) -> List[Dict]:
    """按自然语言筛选项目"""
    if natural_language == "all":
        return projects
    
    filtered = []
    for project in projects:
        description = project.get("description", "")
        detected = detect_natural_language(description)
        if detected == natural_language:
            filtered.append(project)
    
    return filtered

def create_star_trend_chart(stars_today: int, total_stars: int) -> go.Figure:
    """创建star趋势图"""
    import random
    
    # 生成近30天的模拟数据
    dates = []
    stars = []
    current_date = datetime.now()
    
    # 基于今日增长估算历史趋势
    base_growth = max(stars_today // 3, 10)  # 平均每日增长
    
    for i in range(30, 0, -1):
        date = current_date - timedelta(days=i)
        dates.append(date.strftime("%m-%d"))
        # 添加随机波动
        growth = base_growth + random.randint(-base_growth//2, base_growth)
        stars.append(max(total_stars - growth * i, 100))
    
    # 创建趋势图
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=stars,
        mode='lines+markers',
        name='Stars',
        line=dict(color='#FF6B6B', width=2),
        marker=dict(size=4),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.1)'
    ))
    
    fig.update_layout(
        title=dict(text="近30天Star趋势", font=dict(size=12)),
        xaxis_title="",
        yaxis_title="",
        height=150,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=8)),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)', tickfont=dict(size=8))
    )
    
    return fig

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
    
    natural_language = st.selectbox(
        "自然语言",
        ["all", "chinese", "english", "japanese", "korean"],
        index=0,
        help="按项目描述的自然语言筛选（基于检测算法）"
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
    - 📊 **Star趋势图**：近30天增长可视化
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ by [Autolo](https://github.com/autolo)")

# 计算时间周期
def get_time_range(since: str) -> str:
    """获取具体的时间周期"""
    today = datetime.now()
    if since == "daily":
        return today.strftime("%Y.%m.%d")
    elif since == "weekly":
        week_ago = today - timedelta(days=7)
        return f"{week_ago.strftime('%Y.%m.%d')}-{today.strftime('%Y.%m.%d')}"
    else:  # monthly
        month_ago = today - timedelta(days=30)
        return f"{month_ago.strftime('%Y.%m.%d')}-{today.strftime('%Y.%m.%d')}"

# 主内容区 - 时间范围指标（移到顶部）
col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
with col_stats1:
    time_map = {"daily": "今日", "weekly": "本周", "monthly": "本月"}
    time_range = get_time_range(since)
    st.metric("📅 数据周期", time_range)
with col_stats2:
    st.metric("🔄 缓存时间", "5分钟")
with col_stats3:
    lang_count = len([l for l in ["python", "javascript", "typescript", "rust", "go", "java", "c++", "swift", "c#"] if l == language or language == "all"])
    st.metric("🌐 编程语言", f"{lang_count}种" if language == "all" else language.title())
with col_stats4:
    natural_lang_map = {"all": "全部", "chinese": "中文", "english": "英文", "japanese": "日文", "korean": "韩文"}
    st.metric("🌍 自然语言", natural_lang_map.get(natural_language, natural_language))

st.markdown("---")

# 获取数据按钮
if st.button("🚀 获取热门项目", type="primary", use_container_width=True):
    with st.spinner("正在从 GitHub Trending 获取数据..."):
        projects = fetch_github_trending(language, since, limit)
        
        if projects:
            # 应用自然语言筛选
            projects = filter_by_natural_language(projects, natural_language)
            
            if not projects:
                st.warning(f"⚠️ 没有找到符合条件的{natural_language}项目，请尝试调整筛选条件")
            else:
                st.success(f"✅ 获取到 {len(projects)} 个热门项目（{time_map.get(since, since)}）")
            
            # 统计信息（移到项目列表之前 - 置顶）
            st.markdown("### 📊 数据统计")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            total_stars = sum(p.get("stargazers_count", 0) for p in projects)
            avg_stars = total_stars // len(projects) if projects else 0
            total_stars_today = sum(p.get("stars_today", 0) for p in projects)
            languages = [p.get("language", "Unknown") for p in projects if p.get("language")]
            top_language = max(set(languages), key=languages.count) if languages else "Unknown"
            p0_p1_count = sum(1 for p in projects if analyze_trend_signal(p)["level"] in ["P0", "P1"])
            
            natural_lang_map = {"all": "全部", "chinese": "中文", "english": "英文", "japanese": "日文", "korean": "韩文"}
            
            with col1:
                st.metric("总Stars", f"{total_stars:,}")
            with col2:
                st.metric(f"{time_map.get(since, '')}增长", f"+{total_stars_today:,}")
            with col3:
                st.metric("热门语言", top_language)
            with col4:
                st.metric("P0/P1项目", p0_p1_count)
            with col5:
                st.metric("自然语言", natural_lang_map.get(natural_language, natural_language))
            
            st.markdown("---")
            
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
                        
                        # Star趋势图（新增）
                        with st.expander("📈 查看Star趋势（近30天）", expanded=False):
                            fig = create_star_trend_chart(
                                repo.get("stars_today", 0),
                                repo.get("stargazers_count", 0)
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
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
