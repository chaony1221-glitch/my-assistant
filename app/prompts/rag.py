def build_rag_prompt(
    question: str, 
    context: str,
) -> str:
    return f"""
用户问题：{question}

RAG工具返回：
{context}

请根据RAG工具结果，用自然语言简洁回答用户，不要使用“根据资料显示”“根据提供的资料”“参考资料中提到”等开头。
直接回答用户问题。
"""
