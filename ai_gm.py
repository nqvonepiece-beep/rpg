import os
import json
import random
import google.generativeai as genai


SYSTEM_PROMPT = """
Bạn là Game Master của một thế giới fantasy RPG tên Aeternium.

Nhiệm vụ của bạn:
- Xử lý hành động của người chơi một cách hợp lý.
- Dựa vào chỉ số nhân vật, class, trait, kỹ năng, vật phẩm và bối cảnh.
- Kết quả phải có yếu tố bất ngờ nhưng không vô lý.
- Không cho người chơi thắng quá dễ.
- Không giết nhân vật tùy tiện nếu không hợp lý.
- Luôn trả về JSON hợp lệ, không viết thêm chữ ngoài JSON.

JSON bắt buộc có dạng:
{
  "narrative": "mô tả kết quả hành động",
  "outcome": "success/fail/partial/critical",
  "hp_change": 0,
  "mp_change": 0,
  "exp_gain": 0,
  "gold_change": 0,
  "location_change": null,
  "new_item": null,
  "status_effect": null,
  "next_prompt": "gợi ý hành động tiếp theo",
  "hidden_condition_trigger": null
}
"""


def setup_gemini():
    """Khởi tạo Gemini model"""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY environment variable")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


async def process_action(model, character, action, game_context=""):
    """Xử lý hành động của người chơi bằng Gemini"""
    char_summary = f"""
THÔNG TIN NHÂN VẬT:
- Tên: {character['name']}
- Class: {character['class']}
- Trait: {character['trait']}
- Level: {character['level']}
- HP: {character['hp']}/{character['max_hp']}
- MP: {character['mp']}/{character['max_mp']}
- STR: {character['stats']['STR']} | AGI: {character['stats']['AGI']} | INT: {character['stats']['INT']}
- VIT: {character['stats']['VIT']} | WIS: {character['stats']['WIS']} | LCK: {character['stats']['LCK']}
- Kỹ năng: {', '.join(character['skills'][:10])}
- Vị trí: {character['location']}
- Vàng: {character['gold']}
- Số lần bị cận kề cái chết: {character.get('hidden_conditions', {}).get('near_death', 0)}
- Số lần giết địch: {character.get('kills', 0)}
"""

    recent_log = ""
    if character.get("story_log"):
        recent_events = character["story_log"][-3:]
        recent_log = "SỰ KIỆN GẦN ĐÂY:\n" + "\n".join(recent_events)

    prompt = f"""
{char_summary}
{recent_log}
{f"BỐI CẢNH THÊM: {game_context}" if game_context else ""}

HÀNH ĐỘNG CỦA NGƯỜI CHƠI: {action}

Hãy xử lý hành động này và trả về kết quả theo định dạng JSON đã được yêu cầu.
Nhớ rằng: kết quả phải thực tế với chỉ số nhân vật và hoàn cảnh.
Luôn có yếu tố ngẫu nhiên - đôi khi thành công, đôi khi thất bại, đôi khi bất ngờ.
"""

    try:
        response = model.generate_content(
            [
                {"role": "user", "parts": [SYSTEM_PROMPT]},
                {
                    "role": "model",
                    "parts": [
                        '{"narrative": "Tôi sẵn sàng.", "outcome": "success", "hp_change": 0, "mp_change": 0, "exp_gain": 0, "gold_change": 0, "location_change": null, "new_item": null, "status_effect": null, "next_prompt": "Hành trình bắt đầu.", "hidden_condition_trigger": null}'
                    ],
                },
                {"role": "user", "parts": [prompt]},
            ]
        )

        text = response.text.strip()

        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        return json.loads(text)

    except json.JSONDecodeError:
        print("GEMINI JSON ERROR:", response.text if "response" in locals() else "No response")
        return {
            "narrative": response.text if "response" in locals() else "Có điều gì đó xảy ra...",
            "outcome": "success",
            "hp_change": 0,
            "mp_change": 0,
            "exp_gain": random.randint(5, 20),
            "gold_change": 0,
            "location_change": None,
            "new_item": None,
            "status_effect": None,
            "next_prompt": "Bạn sẽ làm gì tiếp theo?",
            "hidden_condition_trigger": None,
        }

    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        return {
            "narrative": "⚠️ Game Master đang bận... hãy thử lại sau giây lát.",
            "outcome": "fail",
            "hp_change": 0,
            "mp_change": 0,
            "exp_gain": 0,
            "gold_change": 0,
            "location_change": None,
            "new_item": None,
            "status_effect": None,
            "next_prompt": "Thử lại hành động của bạn.",
            "hidden_condition_trigger": None,
        }


async def generate_world_event(model, location):
    """Tạo sự kiện ngẫu nhiên trong thế giới"""
    prompt = f"""
Tạo một sự kiện ngẫu nhiên thú vị xảy ra tại {location} trong thế giới Aeternium.
Sự kiện có thể là: gặp NPC, phát hiện bí mật, thiên tai nhỏ, tin tức từ vùng khác, nguy hiểm nhỏ, v.v.

Trả về JSON đúng dạng:
{{"event": "mô tả sự kiện", "type": "npc/discovery/weather/news/danger"}}

Chỉ trả về JSON, không viết thêm gì khác.
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        return json.loads(text)

    except Exception as e:
        print("WORLD EVENT ERROR:", repr(e))
        return {
            "event": "Gió thổi nhẹ, bầu trời trong xanh. Một ngày bình yên tại " + location,
            "type": "weather",
        }


async def generate_training_result(model, character, stat, training_description):
    """Xử lý kết quả tập luyện"""
    prompt = f"""
Nhân vật {character['name']} Level {character['level']}, class {character['class']} đang tập luyện {stat}.
Mô tả tập luyện: {training_description}
Chỉ số hiện tại: {stat} = {character['stats'].get(stat, '?')}

Tạo mô tả sinh động về buổi tập luyện và kết quả.

Trả về JSON đúng dạng:
{{
  "narrative": "mô tả buổi tập luyện 2-3 câu",
  "stat_gain": 0.1,
  "exp_gain": 15,
  "insight": "điều nhân vật nhận ra trong quá trình tập"
}}

Chỉ trả về JSON, không viết thêm gì khác.
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        return json.loads(text)

    except Exception as e:
        print("TRAINING ERROR:", repr(e))
        return {
            "narrative": f"{character['name']} miệt mài tập luyện {stat}. Mồ hôi chảy ướt áo nhưng ý chí không hề lung lay.",
            "stat_gain": 0.1,
            "exp_gain": 15,
            "insight": "Sức mạnh đến từ sự kiên trì.",
        }