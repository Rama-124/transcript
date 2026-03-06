from collections import Counter
import os
import re

_tokenizer = None
_model = None
_load_failed = False


def _sentence_split(text):
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text.strip())
    return [p.strip() for p in parts if p.strip()]


def _fallback_summary(text, max_sentences=3):
    sentences = _sentence_split(text)
    if len(sentences) <= max_sentences:
        return text.strip()

    words = re.findall(r"[a-zA-Z']+", text.lower())
    if not words:
        return " ".join(sentences[:max_sentences])

    stop = {
        "the","a","an","and","or","but","if","then","to","of","in","on",
        "for","with","as","is","are","was","were","be","been","it","this","that",
        "at","by","from","you","your","i","we","they","he","she","them","our"
    }

    freq = Counter(w for w in words if w not in stop and len(w) > 2)

    if not freq:
        return " ".join(sentences[:max_sentences])

    scored = []
    for i, sent in enumerate(sentences):
        sent_words = re.findall(r"[a-zA-Z']+", sent.lower())
        score = sum(freq.get(w, 0) for w in sent_words)
        scored.append((score, i, sent))

    top = sorted(scored, key=lambda x: x[0], reverse=True)[:max_sentences]
    top = sorted(top, key=lambda x: x[1])
    return " ".join(s for _, _, s in top).strip()


def _load_model_once():
    global _tokenizer, _model, _load_failed

    if os.getenv("ENABLE_TRANSFORMERS_SUMMARY", "0") != "1":
        return False

    if _tokenizer and _model:
        return True

    if _load_failed:
        return False

    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        model_name = "facebook/bart-large-cnn"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        return True
    except Exception:
        _load_failed = True
        return False


def summarize_text(text):
    text = (text or "").strip()
    if not text:
        return ""

    if len(text) > 3000:
        text = text[:3000]
        last_dot = text.rfind(".")
        if last_dot != -1:
            text = text[:last_dot+1]

    if _load_model_once():
        try:
            input_text = "summarize: " + text
            inputs = _tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)

            summary_ids = _model.generate(
                inputs["input_ids"],
                max_length=120,
                min_length=40,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )

            summary = _tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            if summary.strip():
                return summary.strip()
        except Exception:
            pass

    return _fallback_summary(text)