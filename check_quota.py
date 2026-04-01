import os
import google.generativeai as genai

# 设置你的 API Key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("--- 开始探测模型额度 ---")

# 获取所有支持生成内容的模型
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        model_name = m.name.split('/')[-1]
        try:
            model = genai.GenerativeModel(model_name)
            # 发送一个极其微小的请求来测试
            response = model.generate_content("hi", generation_config={"max_output_tokens": 1})
            print(f"✅ [可用] {model_name}")
        except Exception as e:
            if "429" in str(e):
                print(f"❌ [额度耗尽] {model_name}")
            else:
                print(f"⚠️  [其他错误] {model_name}: {str(e)[:50]}...")

print("--- 探测结束 ---")