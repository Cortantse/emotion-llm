"""
文本处理工具函数
"""

def preprocess_text(text):
    """
    对输入文本进行预处理
    
    参数:
        text (str): 输入文本
        
    返回:
        str: 预处理后的文本
    """
    # 移除多余空格
    text = " ".join(text.split())
    # 转换为小写
    text = text.lower()
    return text


def extract_keywords(text, top_n=5):
    """
    从文本中提取关键词
    
    参数:
        text (str): 输入文本
        top_n (int): 返回的关键词数量
        
    返回:
        list: 关键词列表
    """
    # 实际实现会使用NLP技术提取关键词
    # 这里只是一个简单示例
    words = text.split()
    # 按词长度排序并取前 top_n 个
    keywords = sorted(set(words), key=len, reverse=True)[:top_n]
    return keywords


def sentiment_score_to_emotion(score):
    """
    将情感分数转换为情感标签
    
    参数:
        score (float): 情感分数，范围[-1, 1]
        
    返回:
        str: 情感标签
    """
    if score >= 0.5:
        return "positive"
    elif score <= -0.5:
        return "negative"
    else:
        return "neutral" 