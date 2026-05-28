# ai_gm.py - Trí não AI cho Game Master

import google.generativeai as genai
import os
import random
import json

WORLD_LORE = """
THẾ GIỚI AETERNIUM - Lãnh địa của ma thuật và kiếm đạo

LỊCH SỬ:
Aeternium là thế giới được tạo ra bởi 7 vị thần nguyên thủy. Từ hàng nghìn năm trước, 
Đế Quốc Ma Thuật Orsted từng thống trị tất cả, cho đến khi sụp đổ vì chiến tranh với 
Liên Minh Rồng. Giờ đây, thế giới chia thành nhiều vương quốc và lãnh thổ.

CÁC KHU VỰC CHÍNH:
- Làng Edenia: Làng khởi đầu bình yên, nơi người chơi bắt đầu hành trình
- Thành Phố Ironhold: Thành phố thương mại lớn nhất, đầy rẫy cơ hội và nguy hiểm
- Rừng Sâu Blackthorn: Rừng tối tăm chứa đầy quái vật và bí mật cổ đại
- Núi Dragonfang: Nơi trú ngụ của rồng, chứa kho báu huyền thoại
- Mê Cung Catacombs: Tầng ngầm vô tận dưới lòng đất, nơi những kẻ tìm kiếm sức mạnh
- Biển Stormhaven: Đại dương dữ dội với những sinh vật biển khổng lồ
- Tháp Babel: Tháp ma thuật huyền bí, mỗi tầng là một thử thách khác nhau
- Thành Cổ Ruined Citadel: Tàn tích của Đế Quốc Ma Thuật cổ đại

HỆ THỐNG PHÂN CẤP QUÁI VẬT:
F - Yếu nhất: Chuột khổng lồ, Goblin, Slime
E - Yếu: Skeleton, Orc, Troll
D - Trung bình: Ogre, Harpy, Werewolf  
C - Khá mạnh: Cyclops, Basilisk, Chimera
B - Mạnh: Lesser Dragon, Demon Knight, Ancient Golem
A - Rất mạnh: Dragon, Lich King, Demon Lord
S - Cực kỳ mạnh: Ancient Dragon, Fallen God, World-Eater
SS - Trùm Cuối: Orsted (Rồng Thần), The Void (Bóng Tối Nguyên Thủy)

PHONG CÁCH THẾ GIỚI:
- Lấy cảm hứng từ Mushoku Tensei, Berserk, Re:Zero, Overlord, Sword Art Online
- Thế giới nghiêm túc có thể chết thật sự
- Hành động có hậu quả lâu dài
- NPC có cuộc sống riêng và phản ứng thực tế
- Ma thuật dựa trên ý chí và hiểu biết
- Sức mạnh đến từ thực tập và kinh nghiệm thật
"""

SYSTEM_PROMPT = f"""
Bạn là GAME MASTER của thế giới fantasy Aeternium. Vai trò của bạn là điều hành và kể chuyện 
cho một trò chơi nhập vai dạng text, tương tự như D&D nhưng có phong cách anime fantasy.

{WORLD_LORE}

NHIỆM VỤ CỦA BẠN:
1. Mô tả hậu quả của hành động người chơi một cách sinh động, chi tiết, hấp dẫn
2. Tạo ra các tình huống ngẫu nhiên thực tế - có thể thành công, thất bại, bất ngờ
3. Mô phỏng thế giới sống động với NPC, thiên tai, sự kiện ngẫu nhiên
4. Đảm bảo mọi hành động đều có hậu quả logic
5. Giữ phong cách kể chuyện như manga/anime - kịch tính, cảm xúc, chi tiết

QUY TẮC QUAN TRỌNG:
- LUÔN trả lời bằng Tiếng Việt
- Mô tả chi tiết âm thanh, cảm giác, mùi, hình ảnh để người chơi cảm nhận thật sự
- Kết quả phải logic với chỉ số nhân vật (người yếu không thể đánh bại rồng)
- Chiến đấu phải có tỷ lệ thực tế - có thể trượt, bị phản công, có kết quả bất ngờ
- Luôn kết thúc bằng tình huống/câu hỏi để người chơi hành động tiếp
- EXP và phần thưởng phải hợp lý với độ khó hành động
- Khi người chơi làm điều gì đó nguy hiểm/ngu ngốc, hãy để hậu quả xảy ra

ĐỊNH DẠNG TRẢ LỜI:
Trả lời theo JSON với format này:
{{
  "narrative": "Mô tả sinh động về những gì xảy ra (ít nhất 3-5 câu)",
  "outcome": "success/partial/fail/critical_success/critical_fail/unexpected",
  "hp_change": số âm hoặc dương (thay đổi HP),
  "mp_change": số âm hoặc dương (thay đổi MP),
  "exp_gain": số EXP nhận được (0-500),
  "gold_change": số vàng thay đổi (âm hoặc dương),
  "location_change": "tên địa điểm mới hoặc null",
  "new_item": "tên vật phẩm nhận được hoặc null",
  "status_effect": "tên hiệu ứng hoặc null (poison/burn/freeze/stun/blind/etc)",
  "next_prompt": "Câu hỏi/tình huống tiếp theo cho người chơi",
  "hidden_condition_trigger": "tên điều kiện ẩn nếu được kích hoạt hoặc null"
}}

Chỉ trả về JSON, không có gì khác.
"""

def setup_gemini(api_key):
    """Cấu hình Gemini API"""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

async def process_action(model, character, action, game_context=""):
    """Xử lý hành động của người chơi và trả về kết quả"""
    
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
    if character.get('story_log'):
        recent_events = character['story_log'][-3:]
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
            [{"role": "user", "parts": [SYSTEM_PROMPT]},
             {"role": "model", "parts": ['{"narrative": "Tôi sẵn sàng.", "outcome": "success", "hp_change": 0, "mp_change": 0, "exp_gain": 0, "gold_change": 0, "location_change": null, "new_item": null, "status_effect": null, "next_prompt": "Hành trình bắt đầu.", "hidden_condition_trigger": null}']},
             {"role": "user", "parts": [prompt]}]
        )
        
        text = response.text.strip()
        # Làm sạch response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(text)
        return result
        
    except json.JSONDecodeError:
        # Nếu JSON lỗi, trả về kết quả mặc định
        return {
            "narrative": response.text if 'response' in locals() else "Có điều gì đó xảy ra...",
            "outcome": "success",
            "hp_change": 0,
            "mp_change": 0,
            "exp_gain": random.randint(5, 20),
            "gold_change": 0,
            "location_change": None,
            "new_item": None,
            "status_effect": None,
            "next_prompt": "Bạn sẽ làm gì tiếp theo?",
            "hidden_condition_trigger": None
        }except Exception as e:
    print("GEMINI ERROR:", repr(e))
    return {
        "narrative": f"⚠️ Game Master đang bận... hãy thử lại sau giây lát.",
            "outcome": "fail",
            "hp_change": 0,
            "mp_change": 0,
            "exp_gain": 0,
            "gold_change": 0,
            "location_change": None,
            "new_item": None,
            "status_effect": None,
            "next_prompt": "Thử lại hành động của bạn.",
            "hidden_condition_trigger": None
        }

async def generate_world_event(model, location):
    """Tạo sự kiện ngẫu nhiên trong thế giới"""
    prompt = f"""
Tạo một sự kiện ngẫu nhiên thú vị xảy ra tại {location} trong thế giới Aeternium.
Sự kiện có thể là: gặp NPC, phát hiện bí mật, thiên tai nhỏ, tin tức từ vùng khác, v.v.
Trả về JSON: {{"event": "mô tả sự kiện", "type": "npc/discovery/weather/news/danger"}}
Chỉ JSON, không gì khác.
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1] if "```json" not in text else text.split("```json")[1]
            text = text.split("```")[0].strip()
        return json.loads(text)
    except:
        return {"event": "Gió thổi nhẹ, bầu trời trong xanh. Một ngày bình yên tại " + location, "type": "weather"}

async def generate_training_result(model, character, stat, training_description):
    """Xử lý kết quả tập luyện"""
    prompt = f"""
Nhân vật {character['name']} (Level {character['level']}, {character['class']}) đang tập luyện {stat}.
Mô tả tập luyện: {training_description}
Chỉ số hiện tại: {stat} = {character['stats'].get(stat, '?')}

Tạo mô tả sinh động về buổi tập luyện và kết quả.
Trả về JSON: {{
  "narrative": "mô tả buổi tập luyện 2-3 câu",
  "stat_gain": số tăng (0.1 đến 0.5, thường là 0.1-0.2),
  "exp_gain": số EXP (10-50),
  "insight": "điều nhân vật nhận ra trong quá trình tập"
}}
Chỉ JSON.
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```json")[1].split("```")[0].strip() if "```json" in text else text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except:
        return {
            "narrative": f"{character['name']} miệt mài tập luyện {stat}. Mồ hôi chảy ướt áo nhưng ý chí không hề lung lay.",
            "stat_gain": 0.1,
            "exp_gain": 15,
            "insight": "Sức mạnh đến từ sự kiên trì."
        }
