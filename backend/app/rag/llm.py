from typing import Optional


class DeepSeekLLM:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI
            from app.core.config import settings
            self._client = OpenAI(
                api_key=settings.deepseek_api_key,
                base_url=settings.deepseek_api_base,
            )
        return self._client

    def chat(
        self,
        question: str,
        context: str,
        user_context: str = "",
        history: Optional[list[dict]] = None,
    ) -> dict:
        from openai import OpenAIError
        from app.core.config import settings

        system_prompt = f"""你是一个高考志愿填报智能助手。请基于以下提供的参考信息回答问题。

如果参考信息中有相关依据，请基于依据回答，并在回答中引用相关来源。
如果参考信息不足以回答问题，请诚实告知。

用户个人信息：
{user_context}

参考信息：
{context}
"""
        messages = [{"role": "system", "content": system_prompt}]

        if history:
            for msg in history[-6:]:
                messages.append(msg)

        messages.append({"role": "user", "content": question})

        try:
            response = self.client.chat.completions.create(
                model=settings.deepseek_model,
                messages=messages,
                temperature=0.5,
                max_tokens=2048,
            )
            return {
                "answer": response.choices[0].message.content,
            }
        except OpenAIError as e:
            return {
                "answer": f"DeepSeek API 调用失败：{str(e)}。请检查 API Key 是否正确配置。",
            }
