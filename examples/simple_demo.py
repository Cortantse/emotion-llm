#!/usr/bin/env python
"""
EmotionalLLM 简单示例脚本
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emotionalllm.models.emotional_model import EmotionalModel
from emotionalllm.utils.text_utils import preprocess_text, extract_keywords


def main():
    """
    主函数
    """
    print("=" * 50)
    print("EmotionalLLM 简单示例")
    print("=" * 50)
    
    # 初始化模型
    model = EmotionalModel()
    print("初始化情感模型...")
    
    # 示例输入
    sample_inputs = [
        "今天天气真好，我感到非常开心！",
        "我对这个结果感到非常失望和沮丧。",
        "这只是一个普通的测试句子，没有明显的情感。"
    ]
    
    # 处理每个示例输入
    for i, text in enumerate(sample_inputs, 1):
        print(f"\n示例 {i}: \"{text}\"")
        
        # 预处理文本
        processed_text = preprocess_text(text)
        print(f"预处理后: \"{processed_text}\"")
        
        # 提取关键词
        keywords = extract_keywords(processed_text, top_n=3)
        print(f"关键词: {', '.join(keywords)}")
        
        # 检测情感
        emotion = model.detect_emotion(text)
        print(f"检测到的情感: {emotion['emotion']} (置信度: {emotion['confidence']})")
        
        # 生成回复
        response = model.generate(text)
        print(f"模型回复: \"{response}\"")
        print("-" * 50)
    
    print("\n示例运行完成！")


if __name__ == "__main__":
    main() 