"""
情感模型测试模块
"""

import unittest
from emotionalllm.models.emotional_model import EmotionalModel


class TestEmotionalModel(unittest.TestCase):
    """
    情感模型测试类
    """
    
    def setUp(self):
        """
        测试前的准备工作
        """
        self.model = EmotionalModel()
        
    def test_initialization(self):
        """
        测试模型初始化
        """
        self.assertEqual(self.model.model_name, "base")
        self.assertEqual(self.model.emotion_threshold, 0.5)
        self.assertIsNone(self.model.model)
        self.assertIsNone(self.model.emotion_detector)
        
    def test_detect_emotion(self):
        """
        测试情感检测功能
        """
        text = "这是一个测试"
        result = self.model.detect_emotion(text)
        self.assertIsInstance(result, dict)
        self.assertIn("emotion", result)
        self.assertIn("confidence", result)
        
    def test_generate(self):
        """
        测试生成功能
        """
        prompt = "你好，请生成一个回复"
        response = self.model.generate(prompt)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        

if __name__ == "__main__":
    unittest.main() 