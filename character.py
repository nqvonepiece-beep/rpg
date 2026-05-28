
CLASSES = {
    "⚔️ Chiến Binh": {
        "desc": "Bậc thầy cận chiến, dũng mãnh và kiên cường như thép",
        "stats": {"STR": 8, "AGI": 5, "INT": 2, "VIT": 8, "WIS": 2, "LCK": 3},
        "hp_mult": 1.6, "mp_mult": 0.7,
        "skills": ["Chém Cơ Bản", "Tư Thế Thép"]
    },
    "🗡️ Thích Khách": {
        "desc": "Bóng tối chuyển động, một nhát là chí mạng",
        "stats": {"STR": 5, "AGI": 9, "INT": 4, "VIT": 5, "WIS": 3, "LCK": 6},
        "hp_mult": 1.1, "mp_mult": 1.0,
        "skills": ["Đâm Nhanh", "Ẩn Thân Cơ Bản"]
    },
    "🔥 Pháp Sư": {
        "desc": "Kẻ điều khiển nguyên tố, sức mạnh hủy diệt từ xa",
        "stats": {"STR": 2, "AGI": 4, "INT": 10, "VIT": 3, "WIS": 8, "LCK": 3},
        "hp_mult": 0.8, "mp_mult": 2.0,
        "skills": ["Cầu Lửa", "Khiên Ma Thuật"]
    },
    "🏹 Cung Thủ": {
        "desc": "Mắt đại bàng, tay thần, không bao giờ trượt mục tiêu",
        "stats": {"STR": 5, "AGI": 8, "INT": 4, "VIT": 5, "WIS": 4, "LCK": 6},
        "hp_mult": 1.1, "mp_mult": 0.9,
        "skills": ["Bắn Thẳng", "Mắt Đại Bàng"]
    },
    "🛡️ Hiệp Sĩ Thánh": {
        "desc": "Ánh sáng và thép, bảo vệ đồng đội đến hơi thở cuối cùng",
        "stats": {"STR": 6, "AGI": 4, "INT": 5, "VIT": 9, "WIS": 6, "LCK": 2},
        "hp_mult": 1.8, "mp_mult": 1.2,
        "skills": ["Thánh Kiếm", "Hào Quang Bảo Vệ"]
    },
    "☠️ Tử Linh Sĩ": {
        "desc": "Điều khiển linh hồn người chết, bóng tối là sức mạnh",
        "stats": {"STR": 3, "AGI": 4, "INT": 9, "VIT": 5, "WIS": 7, "LCK": 2},
        "hp_mult": 1.0, "mp_mult": 1.8,
        "skills": ["Triệu Hồn", "Hút Sinh Lực"]
    },
    "🌿 Druids": {
        "desc": "Một với thiên nhiên, chữa lành và phá hủy bằng sức mạnh đất trời",
        "stats": {"STR": 4, "AGI": 5, "INT": 7, "VIT": 6, "WIS": 8, "LCK": 4},
        "hp_mult": 1.2, "mp_mult": 1.5,
        "skills": ["Chữa Lành Thiên Nhiên", "Gai Độc"]
    },
    "👊 Võ Tăng": {
        "desc": "Thân xác là vũ khí, mỗi cú đấm phá núi rời sông",
        "stats": {"STR": 7, "AGI": 7, "INT": 3, "VIT": 7, "WIS": 4, "LCK": 4},
        "hp_mult": 1.4, "mp_mult": 0.9,
        "skills": ["Thiết Quyền", "Khí Công"]
    },
    "🎵 Nhạc Sĩ Chiến": {
        "desc": "Âm nhạc là phép thuật, tiếng đàn có thể giết người",
        "stats": {"STR": 3, "AGI": 6, "INT": 7, "VIT": 4, "WIS": 7, "LCK": 7},
        "hp_mult": 1.0, "mp_mult": 1.6,
        "skills": ["Khúc Chiến Ca", "Âm Ba Hủy Diệt"]
    },
    "🐉 Rồng Kỵ Sĩ": {
        "desc": "Được rồng cổ đại chọn, mang trong mình máu của long tộc",
        "stats": {"STR": 7, "AGI": 6, "INT": 6, "VIT": 7, "WIS": 5, "LCK": 4},
        "hp_mult": 1.5, "mp_mult": 1.3,
        "skills": ["Hơi Thở Rồng", "Vảy Rồng"]
    },
    "🌑 Tà Thuật Sư": {
        "desc": "Bán linh hồn cho bóng tối, đổi lấy sức mạnh vô hạn",
        "stats": {"STR": 4, "AGI": 5, "INT": 10, "VIT": 4, "WIS": 5, "LCK": 1},
        "hp_mult": 0.9, "mp_mult": 2.2,
        "skills": ["Nguyền Rủa", "Hấp Thụ Ma Lực"]
    },
    "⚡ Kiếm Thánh": {
        "desc": "Đỉnh cao của kiếm đạo, mỗi nhát kiếm chứa đựng ý chí",
        "stats": {"STR": 9, "AGI": 8, "INT": 5, "VIT": 6, "WIS": 5, "LCK": 5},
        "hp_mult": 1.4, "mp_mult": 1.1,
        "skills": ["Kiếm Khí", "Nhất Đao Lưu"]
    }
}

TRAITS = {
    "Dũng Cảm": {"desc": "Không bao giờ lùi bước, +10% ATK khi HP < 30%", "effect": "brave"},
    "Tinh Ranh": {"desc": "Luôn tìm điểm yếu, +15% crit chance", "effect": "cunning"},
    "Thông Thái": {"desc": "Học nhanh hơn người, +20% EXP nhận được", "effect": "wise"},
    "May Mắn": {"desc": "Số trời chiều, tăng drop rate và crit", "effect": "lucky"},
    "Bị Nguyền": {"desc": "Mang lời nguyền cổ đại, ẩn giấu sức mạnh khủng khiếp", "effect": "cursed"},
    "Thiên Tài": {"desc": "Sinh ra đã khác người, tất cả skill học 2x nhanh", "effect": "gifted"},
    "Kiên Cường": {"desc": "Không bao giờ chết đứng, +30% HP tối đa", "effect": "resilient"},
    "Hắc Ám": {"desc": "Thân với bóng tối, skill bóng tối +20% sức mạnh", "effect": "dark_affinity"},
    "Thánh Thiện": {"desc": "Được thần phù hộ, skill ánh sáng +20% sức mạnh", "effect": "holy"},
    "Kẻ Sống Sót": {"desc": "Đã qua cõi chết, miễn nhiễm với instant kill", "effect": "survivor"},
    "Máu Rồng": {"desc": "Có giọt máu rồng trong huyết mạch, sức mạnh nguyên thủy", "effect": "dragon_blood"},
    "Vô Danh": {"desc": "Không ai biết tên ngươi, nhưng số phận đã chọn ngươi", "effect": "unknown"}
}

def create_new_character(name, class_name, trait_name):
    cls = CLASSES[class_name]
    base_stats = cls["stats"]
    
    max_hp = int((100 + base_stats["VIT"] * 10) * cls["hp_mult"])
    max_mp = int((50 + base_stats["WIS"] * 8) * cls["mp_mult"])
    
    # Trait bonuses
    if trait_name == "Kiên Cường":
        max_hp = int(max_hp * 1.3)
    
    character = {
        "name": name,
        "class": class_name,
        "trait": trait_name,
        "level": 1,
        "exp": 0,
        "exp_next": 100,
        "skill_points": 0,
        "stat_points": 0,
        "hp": max_hp,
        "max_hp": max_hp,
        "mp": max_mp,
        "max_mp": max_mp,
        "stats": {
            "STR": base_stats["STR"],
            "AGI": base_stats["AGI"],
            "INT": base_stats["INT"],
            "VIT": base_stats["VIT"],
            "WIS": base_stats["WIS"],
            "LCK": base_stats["LCK"]
        },
        "skills": cls["skills"],
        "inventory": ["Bánh Mì x3", "Thuốc Máu Nhỏ x2"],
        "gold": 50,
        "location": "Làng Khởi Đầu - Edenia",
        "story_log": [],
        "training_log": {},
        "kills": 0,
        "quests_done": 0,
        "titles": [],
        "hidden_conditions": {
            "battles_won": 0,
            "near_death": 0,
            "dark_magic_used": 0,
            "helped_others": 0,
            "solo_boss_kill": 0,
        }
    }
    
    # Gifted trait bonus
    if trait_name == "Thiên Tài":
        for stat in character["stats"]:
            character["stats"][stat] += 2
    
    return character

def get_character_stats_text(char):
    """Tạo text hiển thị stats nhân vật"""
    hp_bar = make_bar(char["hp"], char["max_hp"], 15)
    mp_bar = make_bar(char["mp"], char["max_mp"], 15)
    exp_bar = make_bar(char["exp"], char["exp_next"], 15)
    
    stats = char["stats"]
    text = f"""
╔══════════════════════════════════╗
║  {char['name'][:20]:<20}  ║
╠══════════════════════════════════╣
║  Class: {char['class']:<24}║
║  Trait: {char['trait']:<24}║
║  Level: {char['level']:<3}  |  Vàng: {char['gold']} 💰      ║
║  Vị trí: {char['location'][:23]:<23}║
╠══════════════════════════════════╣
║  ❤️  HP: {char['hp']}/{char['max_hp']}
║  {hp_bar}
║  💙 MP: {char['mp']}/{char['max_mp']}
║  {mp_bar}
║  ⭐ EXP: {char['exp']}/{char['exp_next']}
║  {exp_bar}
╠══════════════════════════════════╣
║  💪 STR: {stats['STR']:<4} | 🏃 AGI: {stats['AGI']:<4}    ║
║  🧠 INT: {stats['INT']:<4} | 🛡️ VIT: {stats['VIT']:<4}    ║
║  📖 WIS: {stats['WIS']:<4} | 🍀 LCK: {stats['LCK']:<4}    ║
╠══════════════════════════════════╣
║  DEF: {calc_def(stats):<5} | MDEF: {calc_mdef(stats):<5}        ║
║  ATK: {calc_atk(stats):<5} | MATK: {calc_matk(stats):<5}        ║
║  CRIT: {calc_crit(stats):<4}% | SPD: {calc_spd(stats):<5}       ║
╠══════════════════════════════════╣
║  🎯 Kills: {char['kills']:<5} | 📜 Quest: {char['quests_done']:<3}   ║
║  🎓 Skill Points: {char.get('skill_points', 0):<3}               ║
║  📊 Stat Points: {char.get('stat_points', 0):<4}               ║
╚══════════════════════════════════╝
"""
    return text

def calc_atk(stats): return stats["STR"] * 3 + stats["AGI"]
def calc_matk(stats): return stats["INT"] * 3 + stats["WIS"]
def calc_def(stats): return stats["VIT"] * 2 + stats["STR"] // 2
def calc_mdef(stats): return stats["WIS"] * 2 + stats["INT"] // 2
def calc_crit(stats): return min(50, stats["LCK"] * 2 + stats["AGI"] // 3)
def calc_spd(stats): return stats["AGI"] * 2 + stats["LCK"] // 2

def make_bar(current, maximum, length=15):
    if maximum == 0: return "░" * length
    filled = int((current / maximum) * length)
    return "█" * filled + "░" * (length - filled)

def calc_exp_for_level(level):
    return int(100 * (level ** 1.5))

def level_up(char):
    """Xử lý khi nhân vật lên cấp"""
    messages = []
    while char["exp"] >= char["exp_next"]:
        char["exp"] -= char["exp_next"]
        char["level"] += 1
        char["exp_next"] = calc_exp_for_level(char["level"])
        char["stat_points"] = char.get("stat_points", 0) + 5
        char["skill_points"] = char.get("skill_points", 0) + 1
        
        # HP/MP tăng khi lên cấp
        hp_gain = char["stats"]["VIT"] * 3 + 10
        mp_gain = char["stats"]["WIS"] * 2 + 5
        char["max_hp"] += hp_gain
        char["max_mp"] += mp_gain
        char["hp"] = min(char["hp"] + hp_gain, char["max_hp"])
        char["mp"] = min(char["mp"] + mp_gain, char["max_mp"])
        
        messages.append(
            f"🎉 **{char['name']} lên Level {char['level']}!**\n"
            f"❤️ +{hp_gain} HP tối đa | 💙 +{mp_gain} MP tối đa\n"
            f"📊 +5 Stat Points | 🎓 +1 Skill Point\n"
            f"Dùng `!statup` để phân bổ chỉ số và `!chooseskill` để chọn kỹ năng!"
        )
    return messages
