# skills_data.py - Kho kỹ năng 500+ với đầy đủ độ hiếm

import random

# Độ hiếm
RARITY_COMMON = "⚪ Thường"
RARITY_RARE = "🔵 Hiếm"
RARITY_EPIC = "🟣 Siêu Hiếm"
RARITY_LEGENDARY = "🟡 Huyền Thoại"
RARITY_HIDDEN = "❓ Ẩn"

RARITY_WEIGHTS = {
    RARITY_COMMON: 55,
    RARITY_RARE: 28,
    RARITY_EPIC: 12,
    RARITY_LEGENDARY: 4,
    RARITY_HIDDEN: 1,
}

SKILLS = {
    # ═══════════════════════════════════════
    # ⚪ KỸ NĂNG THƯỜNG (Common)
    # ═══════════════════════════════════════
    
    # --- Kiếm Thuật Cơ Bản ---
    "Chém Cơ Bản": {"rarity": RARITY_COMMON, "type": "active", "desc": "Đòn chém thông thường, nền tảng của mọi kiếm sĩ", "effect": "atk_1x", "mp": 0},
    "Tư Thế Thép": {"rarity": RARITY_COMMON, "type": "active", "desc": "Tăng phòng thủ 20% trong 1 lượt", "effect": "def_boost", "mp": 5},
    "Đòn Kép": {"rarity": RARITY_COMMON, "type": "active", "desc": "Đánh 2 lần liên tiếp, mỗi đòn 70% sát thương", "effect": "atk_double", "mp": 8},
    "Kiếm Vòng Tròn": {"rarity": RARITY_COMMON, "type": "active", "desc": "Quét kiếm vòng tròn, tấn công nhiều mục tiêu", "effect": "aoe_sweep", "mp": 10},
    "Đỡ Đòn": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Tự động giảm 10% sát thương nhận vào", "effect": "passive_def"},
    "Bước Né": {"rarity": RARITY_COMMON, "type": "passive", "desc": "+10% tỷ lệ né đòn", "effect": "passive_dodge"},
    "Nhát Kiếm Mạnh": {"rarity": RARITY_COMMON, "type": "active", "desc": "Dồn toàn lực vào một nhát, 1.5x sát thương", "effect": "atk_heavy", "mp": 12},
    "Phòng Thủ Tốt": {"rarity": RARITY_COMMON, "type": "active", "desc": "Chuyển sang tư thế phòng thủ, giảm 40% damage", "effect": "full_defense", "mp": 0},
    "Chặn Đòn": {"rarity": RARITY_COMMON, "type": "passive", "desc": "15% cơ hội chặn hoàn toàn đòn tấn công", "effect": "passive_block"},
    "Xỉa Kiếm": {"rarity": RARITY_COMMON, "type": "active", "desc": "Đòn đâm thẳng xuyên qua phòng thủ", "effect": "pierce", "mp": 8},

    # --- Cung Thuật Cơ Bản ---
    "Bắn Thẳng": {"rarity": RARITY_COMMON, "type": "active", "desc": "Mũi tên bay thẳng vào mục tiêu", "effect": "arrow_basic", "mp": 0},
    "Mắt Đại Bàng": {"rarity": RARITY_COMMON, "type": "passive", "desc": "+15% crit chance khi dùng cung", "effect": "eagle_eye"},
    "Bắn Nhanh": {"rarity": RARITY_COMMON, "type": "active", "desc": "Bắn 3 mũi tên nhanh, mỗi mũi 50% sát thương", "effect": "rapid_arrow", "mp": 10},
    "Ngắm Bắn": {"rarity": RARITY_COMMON, "type": "active", "desc": "Ngắm 1 lượt, lượt sau crit 100%", "effect": "aim", "mp": 5},
    "Bẫy Đất": {"rarity": RARITY_COMMON, "type": "active", "desc": "Đặt bẫy trên đất, bắt kẻ địch vào bẫy", "effect": "trap", "mp": 12},

    # --- Quyền Thuật Cơ Bản ---
    "Thiết Quyền": {"rarity": RARITY_COMMON, "type": "active", "desc": "Cú đấm thép cơ bản của võ tăng", "effect": "iron_fist", "mp": 5},
    "Khí Công": {"rarity": RARITY_COMMON, "type": "active", "desc": "Vận khí nội tại, hồi phục 10% MP", "effect": "meditate", "mp": 0},
    "Đá Vòng Cầu": {"rarity": RARITY_COMMON, "type": "active", "desc": "Đá cạnh vào sườn địch, gây choáng ngắn", "effect": "kick_stun", "mp": 8},
    "Ném Người": {"rarity": RARITY_COMMON, "type": "active", "desc": "Tóm và ném địch vào tường/đồng đội", "effect": "throw", "mp": 10},
    "Đỡ Tay Trần": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Tay không đỡ được đòn vũ khí, giảm 15% damage", "effect": "bare_block"},

    # --- Ẩn Thân Cơ Bản ---
    "Ẩn Thân Cơ Bản": {"rarity": RARITY_COMMON, "type": "active", "desc": "Trở nên khó nhìn thấy trong 2 lượt", "effect": "stealth_basic", "mp": 15},
    "Đâm Nhanh": {"rarity": RARITY_COMMON, "type": "active", "desc": "Đòn đâm chớp nhoáng, khó né tránh", "effect": "quick_stab", "mp": 8},
    "Thuốc Độc Cơ Bản": {"rarity": RARITY_COMMON, "type": "active", "desc": "Tẩm độc vũ khí, gây độc 3 lượt", "effect": "poison_basic", "mp": 10},
    "Chạy Trốn": {"rarity": RARITY_COMMON, "type": "active", "desc": "Thoát khỏi chiến đấu ngay lập tức", "effect": "flee", "mp": 0},
    "Móc Túi": {"rarity": RARITY_COMMON, "type": "active", "desc": "Lấy trộm vật phẩm ngẫu nhiên của địch", "effect": "pickpocket", "mp": 5},

    # --- Ma Thuật Cơ Bản ---
    "Cầu Lửa": {"rarity": RARITY_COMMON, "type": "active", "desc": "Ném quả cầu lửa nhỏ vào địch", "effect": "fireball_sm", "mp": 15},
    "Tia Nước": {"rarity": RARITY_COMMON, "type": "active", "desc": "Phóng tia nước sắc bén vào địch", "effect": "water_jet", "mp": 12},
    "Gai Đất": {"rarity": RARITY_COMMON, "type": "active", "desc": "Gai đất mọc lên từ mặt đất đâm địch", "effect": "earth_spike", "mp": 12},
    "Lưỡi Gió": {"rarity": RARITY_COMMON, "type": "active", "desc": "Lưỡi dao gió vô hình chém địch", "effect": "wind_blade", "mp": 12},
    "Khiên Ma Thuật": {"rarity": RARITY_COMMON, "type": "active", "desc": "Tạo khiên ma thuật, giảm 25% ma thuật damage", "effect": "magic_shield", "mp": 18},
    "Tia Sáng": {"rarity": RARITY_COMMON, "type": "active", "desc": "Bắn tia sáng làm mù địch tạm thời", "effect": "light_ray", "mp": 10},
    "Bóng Tối Nhỏ": {"rarity": RARITY_COMMON, "type": "active", "desc": "Bóng tối bao phủ kẻ địch, giảm tầm nhìn", "effect": "shadow_basic", "mp": 12},
    "Điện Giật Nhỏ": {"rarity": RARITY_COMMON, "type": "active", "desc": "Phóng điện nhỏ gây tê liệt ngắn", "effect": "shock_basic", "mp": 14},
    "Băng Giá Nhỏ": {"rarity": RARITY_COMMON, "type": "active", "desc": "Đóng băng một phần cơ thể địch", "effect": "freeze_basic", "mp": 14},
    "Hồi Phục Nhỏ": {"rarity": RARITY_COMMON, "type": "active", "desc": "Hồi phục 15% HP tối đa", "effect": "heal_small", "mp": 20},

    # --- Kỹ Năng Sinh Hoạt ---
    "Nấu Ăn": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Nấu ăn ngon hơn, đồ ăn hồi phục thêm 20% HP", "effect": "cooking"},
    "Rèn Kiếm Cơ Bản": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Tự sửa và rèn vũ khí cơ bản", "effect": "blacksmith_basic"},
    "Bào Chế Thuốc": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Pha chế thuốc từ thảo dược, tiết kiệm 30% vàng", "effect": "alchemy_basic"},
    "Giao Thương": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Mua bán với giá tốt hơn 15%", "effect": "merchant"},
    "Học Ngôn Ngữ": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Hiểu được ngôn ngữ cổ và các tộc người", "effect": "linguist"},
    "Cưỡi Ngựa": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Điều khiển thú cưỡi thành thạo, di chuyển 2x nhanh", "effect": "riding"},
    "Bơi Lội": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Bơi lội thành thạo, không bị penalty trong nước", "effect": "swimming"},
    "Leo Trèo": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Leo trèo giỏi, không bị penalty ở địa hình cao", "effect": "climbing"},
    "Tìm Đường": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Không bao giờ bị lạc trong rừng hay hang động", "effect": "navigation"},
    "Chăm Sóc Thú": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Thuần hóa và chăm sóc động vật", "effect": "animal_care"},

    # --- Thêm kỹ năng thường ---
    "Đòn Quét": {"rarity": RARITY_COMMON, "type": "active", "desc": "Quét hạ bộ làm địch ngã", "effect": "leg_sweep", "mp": 6},
    "Húc Vai": {"rarity": RARITY_COMMON, "type": "active", "desc": "Húc mạnh bằng vai đẩy lùi địch", "effect": "shoulder_bash", "mp": 5},
    "Khiêu Khích": {"rarity": RARITY_COMMON, "type": "active", "desc": "Khiến địch tức giận, chúng tập trung vào ngươi", "effect": "taunt", "mp": 8},
    "Tập Trung": {"rarity": RARITY_COMMON, "type": "active", "desc": "Hít thở sâu, lượt sau tăng 20% damage", "effect": "focus", "mp": 0},
    "La Hét Chiến": {"rarity": RARITY_COMMON, "type": "active", "desc": "Tiếng hét chiến đấu, tăng ATK đồng đội 10%", "effect": "war_cry", "mp": 10},
    "Cầm Máu": {"rarity": RARITY_COMMON, "type": "active", "desc": "Cầm máu vết thương, ngừng chảy máu", "effect": "bandage", "mp": 0},
    "Nhận Ra Điểm Yếu": {"rarity": RARITY_COMMON, "type": "passive", "desc": "10% cơ hội tìm điểm yếu của địch", "effect": "find_weakness"},
    "Thể Lực Tốt": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Không bị mệt mỏi sau chiến đấu dài", "effect": "endurance"},
    "Ngủ Ít": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Chỉ cần ngủ 4 tiếng là đủ phục hồi", "effect": "light_sleep"},
    "Cảm Nhận Nguy Hiểm": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Linh cảm khi nguy hiểm đến gần", "effect": "danger_sense"},
    "Kháng Độc Nhẹ": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Giảm 30% thời gian bị độc", "effect": "poison_resist_sm"},
    "Kháng Lạnh Nhẹ": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Không bị đóng băng bởi băng thuật thấp cấp", "effect": "cold_resist_sm"},
    "Máu Tốt": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Hồi 1% HP mỗi lượt tự nhiên", "effect": "regen_sm"},
    "Thần Kinh Thép": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Miễn nhiễm với sợ hãi và run rẩy cơ bản", "effect": "iron_nerves"},
    "Khéo Tay": {"rarity": RARITY_COMMON, "type": "passive", "desc": "Làm bẫy và cơ chế cơ học tốt hơn", "effect": "dexterous"},

    # ═══════════════════════════════════════
    # 🔵 KỸ NĂNG HIẾM (Rare)
    # ═══════════════════════════════════════
    
    "Kiếm Khí": {"rarity": RARITY_RARE, "type": "active", "desc": "Bắn lưỡi kiếm khí từ kiếm, tầm xa", "effect": "sword_aura", "mp": 25},
    "Nhất Đao Lưu": {"rarity": RARITY_RARE, "type": "active", "desc": "Một nhát kiếm tốc độ ánh sáng, 2.5x damage", "effect": "iai_slash", "mp": 30},
    "Vũ Bão Kiếm": {"rarity": RARITY_RARE, "type": "active", "desc": "Chém hàng trăm lần trong 1 giây", "effect": "sword_storm", "mp": 40},
    "Kiếm Phản": {"rarity": RARITY_RARE, "type": "active", "desc": "Phản lại đòn địch ngay lập tức với 150% lực", "effect": "counter_slash", "mp": 20},
    "Kiếm Đất": {"rarity": RARITY_RARE, "type": "active", "desc": "Cắm kiếm xuống đất tạo sóng chấn địa", "effect": "earth_slash", "mp": 35},
    "Kiếm Băng": {"rarity": RARITY_RARE, "type": "active", "desc": "Kiếm bọc băng, đóng băng mục tiêu khi trúng", "effect": "ice_sword", "mp": 30},
    "Kiếm Lửa": {"rarity": RARITY_RARE, "type": "active", "desc": "Kiếm bọc lửa, gây bỏng sau khi trúng", "effect": "fire_sword", "mp": 30},
    "Kiếm Sấm": {"rarity": RARITY_RARE, "type": "active", "desc": "Kiếm bọc điện, tê liệt mục tiêu", "effect": "thunder_sword", "mp": 30},
    "Bước Hư Không": {"rarity": RARITY_RARE, "type": "active", "desc": "Dịch chuyển tức thì một khoảng ngắn", "effect": "blink", "mp": 20},
    "Vũ Điệu Kiếm": {"rarity": RARITY_RARE, "type": "active", "desc": "Múa kiếm đẹp mắt nhưng cực kỳ nguy hiểm", "effect": "sword_dance", "mp": 35},

    "Đại Hỏa Cầu": {"rarity": RARITY_RARE, "type": "active", "desc": "Quả cầu lửa khổng lồ nổ tung diện rộng", "effect": "great_fireball", "mp": 40},
    "Bão Tuyết": {"rarity": RARITY_RARE, "type": "active", "desc": "Bão tuyết bao phủ vùng rộng, làm chậm địch", "effect": "blizzard", "mp": 45},
    "Sét Đánh": {"rarity": RARITY_RARE, "type": "active", "desc": "Gọi sét từ trời đánh xuống mục tiêu", "effect": "lightning_strike", "mp": 45},
    "Địa Chấn": {"rarity": RARITY_RARE, "type": "active", "desc": "Rung chuyển mặt đất, làm ngã tất cả địch", "effect": "earthquake", "mp": 50},
    "Lốc Xoáy": {"rarity": RARITY_RARE, "type": "active", "desc": "Tạo lốc xoáy hút và cuốn địch lên", "effect": "tornado", "mp": 45},
    "Trụ Băng": {"rarity": RARITY_RARE, "type": "active", "desc": "Cột băng mọc lên từ đất đóng băng địch hoàn toàn", "effect": "ice_pillar", "mp": 40},
    "Tường Lửa": {"rarity": RARITY_RARE, "type": "active", "desc": "Tạo tường lửa ngăn cách chiến trường", "effect": "fire_wall", "mp": 35},
    "Axit Loang": {"rarity": RARITY_RARE, "type": "active", "desc": "Mưa axit ăn mòn áo giáp địch", "effect": "acid_rain", "mp": 40},
    "Đại Hồi Phục": {"rarity": RARITY_RARE, "type": "active", "desc": "Hồi phục 40% HP tối đa", "effect": "heal_large", "mp": 50},
    "Hồi Phục Nhóm": {"rarity": RARITY_RARE, "type": "active", "desc": "Hồi 20% HP cho toàn bộ đồng đội", "effect": "heal_group", "mp": 60},

    "Bóng Phân Thân": {"rarity": RARITY_RARE, "type": "active", "desc": "Tạo 2 bản sao bóng tối đánh đấm địch", "effect": "shadow_clone", "mp": 45},
    "Độc Sương": {"rarity": RARITY_RARE, "type": "active", "desc": "Phun sương độc bao phủ vùng rộng", "effect": "poison_fog", "mp": 35},
    "Hút Linh Hồn": {"rarity": RARITY_RARE, "type": "active", "desc": "Hút một phần sinh lực của địch chuyển thành HP mình", "effect": "soul_drain", "mp": 30},
    "Triệu Hồi Bộ Xương": {"rarity": RARITY_RARE, "type": "active", "desc": "Triệu hồi 3 bộ xương chiến binh chiến đấu", "effect": "summon_skeleton", "mp": 50},
    "Nguyền Rủa Chậm": {"rarity": RARITY_RARE, "type": "active", "desc": "Nguyền địch, giảm 40% tốc độ trong 3 lượt", "effect": "curse_slow", "mp": 30},
    "Ảo Giác": {"rarity": RARITY_RARE, "type": "active", "desc": "Tạo ảo giác khiến địch tự đánh nhau", "effect": "illusion", "mp": 40},
    "Ẩn Thân Hoàn Hảo": {"rarity": RARITY_RARE, "type": "active", "desc": "Biến mất hoàn toàn, không thể phát hiện trong 3 lượt", "effect": "perfect_stealth", "mp": 35},
    "Thế Giới Giảm Tốc": {"rarity": RARITY_RARE, "type": "active", "desc": "Mọi thứ xung quanh chậm lại trong 2 lượt", "effect": "slow_world", "mp": 50},
    "Phân Tích Địch": {"rarity": RARITY_RARE, "type": "active", "desc": "Xem toàn bộ chỉ số và kỹ năng của địch", "effect": "analyze", "mp": 20},
    "Tăng Tốc": {"rarity": RARITY_RARE, "type": "active", "desc": "Tốc độ tăng 100% trong 2 lượt", "effect": "haste", "mp": 30},

    "Bản Năng Chiến Đấu": {"rarity": RARITY_RARE, "type": "passive", "desc": "Khi HP < 50%, tự động tăng 20% tất cả chỉ số", "effect": "battle_instinct"},
    "Bất Tử Ngắn": {"rarity": RARITY_RARE, "type": "passive", "desc": "Một lần/trận: HP không thể xuống dưới 1", "effect": "near_death_survival"},
    "Hồi Phục Nhanh": {"rarity": RARITY_RARE, "type": "passive", "desc": "Hồi 3% HP mỗi lượt", "effect": "fast_regen"},
    "Kháng Ma Thuật": {"rarity": RARITY_RARE, "type": "passive", "desc": "Giảm 30% tất cả thiệt hại ma thuật nhận vào", "effect": "magic_resist"},
    "Sát Thủ Bẩm Sinh": {"rarity": RARITY_RARE, "type": "passive", "desc": "Crit damage +50%", "effect": "born_assassin"},
    "Hào Khí": {"rarity": RARITY_RARE, "type": "passive", "desc": "Xung quanh toát ra hào khí, địch yếu hơn 10%", "effect": "aura_pressure"},
    "Nhớ Đòn": {"rarity": RARITY_RARE, "type": "passive", "desc": "Sau khi bị một chiêu, giảm 50% thiệt hại từ chiêu đó", "effect": "combat_memory"},
    "Thích Ứng": {"rarity": RARITY_RARE, "type": "passive", "desc": "Mỗi lượt tự thích nghi với môi trường chiến đấu", "effect": "adaptation"},
    "Bản Năng Động Vật": {"rarity": RARITY_RARE, "type": "passive", "desc": "Không bao giờ bị tấn công từ phía sau bất ngờ", "effect": "animal_instinct"},
    "Tâm Lý Học": {"rarity": RARITY_RARE, "type": "passive", "desc": "Đọc được ý định tiếp theo của địch, +20% né đòn", "effect": "psychology"},

    # ═══════════════════════════════════════
    # 🟣 KỸ NĂNG SIÊU HIẾM (Epic)
    # ═══════════════════════════════════════

    "Thánh Kiếm": {"rarity": RARITY_EPIC, "type": "active", "desc": "Kiếm bọc ánh sáng thánh, 3x damage với tà ác", "effect": "holy_sword", "mp": 60},
    "Siêu Tốc Liên Chém": {"rarity": RARITY_EPIC, "type": "active", "desc": "Chém 10 lần trong chớp mắt", "effect": "ultra_combo", "mp": 70},
    "Chân Không Chém": {"rarity": RARITY_EPIC, "type": "active", "desc": "Tạo chân không khi chém, sức mạnh tàn phá địa hình", "effect": "vacuum_slash", "mp": 65},
    "Thiên Kiếm": {"rarity": RARITY_EPIC, "type": "active", "desc": "Kiếm thuật đỉnh cao, gom toàn bộ khí vào một nhát", "effect": "heaven_slash", "mp": 80},
    "Kiếm Hồn": {"rarity": RARITY_EPIC, "type": "active", "desc": "Kiếm tự động chiến đấu theo ý chí chủ nhân", "effect": "sword_soul", "mp": 55},

    "Đại Lốc Lửa": {"rarity": RARITY_EPIC, "type": "active", "desc": "Lốc xoáy lửa khổng lồ thiêu rụi tất cả", "effect": "fire_tornado", "mp": 80},
    "Thiên Sét": {"rarity": RARITY_EPIC, "type": "active", "desc": "Gọi 7 tia sét đồng thời đánh xuống", "effect": "thunder_god", "mp": 85},
    "Lãnh Địa Băng": {"rarity": RARITY_EPIC, "type": "active", "desc": "Đóng băng toàn bộ chiến trường trong 2 lượt", "effect": "frozen_domain", "mp": 90},
    "Hắc Động": {"rarity": RARITY_EPIC, "type": "active", "desc": "Bóng tối nổ tung từ bên trong địch", "effect": "dark_explosion", "mp": 75},
    "Giải Phẫu Thần Thánh": {"rarity": RARITY_EPIC, "type": "active", "desc": "Hồi phục toàn bộ HP và xóa mọi debuff", "effect": "divine_heal", "mp": 100},
    "Triệu Hồi Rồng Nhỏ": {"rarity": RARITY_EPIC, "type": "active", "desc": "Triệu hồi rồng nhỏ chiến đấu cùng trong 3 lượt", "effect": "summon_dragon_sm", "mp": 90},
    "Xuyên Không Gian": {"rarity": RARITY_EPIC, "type": "active", "desc": "Dịch chuyển tức thì đến bất kỳ nơi nào trong tầm nhìn", "effect": "teleport", "mp": 50},
    "Ký Ức Cơ Thể": {"rarity": RARITY_EPIC, "type": "active", "desc": "Cơ thể tự động học và bắt chước kỹ năng địch vừa dùng", "effect": "body_memory", "mp": 40},
    "Gương Phản Chiếu": {"rarity": RARITY_EPIC, "type": "active", "desc": "Phản lại 80% mọi phép thuật nhận vào trong 1 lượt", "effect": "mirror_reflect", "mp": 60},
    "Lĩnh Vực Tử Thần": {"rarity": RARITY_EPIC, "type": "active", "desc": "Tạo vùng lĩnh vực, địch trong vùng giảm 30% mọi chỉ số", "effect": "death_domain", "mp": 80},

    "Hào Quang Bảo Vệ": {"rarity": RARITY_EPIC, "type": "active", "desc": "Tạo khiên thiêng bảo vệ đồng đội, hấp thụ 500 damage", "effect": "holy_barrier", "mp": 70},
    "Hào Khí Bá Vương": {"rarity": RARITY_EPIC, "type": "active", "desc": "Tỏa ra bá khí, địch yếu hơn 20 lần cấp độ sẽ tê liệt", "effect": "overlord_aura", "mp": 50},
    "Máu Lửa": {"rarity": RARITY_EPIC, "type": "active", "desc": "Đốt cháy bản thân, tăng 50% ATK nhưng mất 5% HP/lượt", "effect": "blood_burn", "mp": 0},
    "Nhân Vật Phụ Thuật": {"rarity": RARITY_EPIC, "type": "active", "desc": "Tạo ra người phân thân bằng xương thịt thật để đánh", "effect": "doppelganger", "mp": 85},
    "Tâm Linh Phóng Xuất": {"rarity": RARITY_EPIC, "type": "active", "desc": "Phóng linh hồn ra ngoài cơ thể, di chuyển vô hình", "effect": "astral_project", "mp": 60},

    "Đế Vương Ý Chí": {"rarity": RARITY_EPIC, "type": "passive", "desc": "Không bao giờ bị khuất phục tinh thần, miễn nhiễm CC tâm lý", "effect": "emperor_will"},
    "Thân Bất Tử": {"rarity": RARITY_EPIC, "type": "passive", "desc": "HP tối thiểu luôn là 1, không thể chết bởi đòn thường", "effect": "immortal_body"},
    "Mắt Ma Quỷ": {"rarity": RARITY_EPIC, "type": "passive", "desc": "Nhìn thấy ẩn thân, vô hình, và linh hồn", "effect": "demon_eye"},
    "Thần Tốc": {"rarity": RARITY_EPIC, "type": "passive", "desc": "Tốc độ vượt qua tầm nhìn bình thường, khó bị tấn công", "effect": "godspeed"},
    "Kẻ Ăn Kỹ Năng": {"rarity": RARITY_EPIC, "type": "passive", "desc": "Có cơ hội học kỹ năng từ địch sau khi hạ gục", "effect": "skill_eater"},
    "Thể Chất Bất Thường": {"rarity": RARITY_EPIC, "type": "passive", "desc": "HP tối đa tăng 100%, hồi phục tự nhiên 5%/lượt", "effect": "abnormal_physique"},
    "Trực Giác Chiến Đấu": {"rarity": RARITY_EPIC, "type": "passive", "desc": "Tự động né những đòn chết người với 40% cơ hội", "effect": "battle_intuition"},
    "Tâm Nhãn": {"rarity": RARITY_EPIC, "type": "passive", "desc": "Thấy được điểm yếu và luồng năng lượng của vạn vật", "effect": "mind_eye"},

    # ═══════════════════════════════════════
    # 🟡 KỸ NĂNG HUYỀN THOẠI (Legendary)
    # ═══════════════════════════════════════

    "Sword God Style: Heaven's Wrath": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Kỹ thuật tối thượng của Kiếm Thần Lưu, một nhát chứa đựng cả đời kiếm đạo. Sát thương 10x", "effect": "heaven_wrath", "mp": 150},
    "Thủy Thần Lãnh Vực": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Lãnh vực của Thủy Thần: mọi thứ trong vùng bị kiểm soát bởi nước", "effect": "water_god_domain", "mp": 200},
    "Đất Trời Sụp Đổ": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Kéo thiên thạch từ không trung xuống, hủy diệt cả vùng chiến đấu", "effect": "meteor_crash", "mp": 180},
    "Thời Gian Dừng Lại": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Dừng thời gian trong 2 lượt, chỉ mình ngươi hành động", "effect": "time_stop", "mp": 200},
    "Hắc Động Thần": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Sức mạnh hắc tối tuyệt đối, hút hết ánh sáng và sức sống xung quanh", "effect": "black_god", "mp": 200},
    "Bộc Phát Thần Lực": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Giải phóng toàn bộ giới hạn cơ thể: tất cả chỉ số x3 trong 3 lượt", "effect": "full_power_release", "mp": 100},
    "Mắt Thần Chỉ Số": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Như Rudeus: nhìn thấy và tính toán ma thuật hoàn hảo tuyệt đối", "effect": "god_eye_magic", "mp": 50},
    "Hồi Sinh": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Hồi sinh đồng đội đã chết với 50% HP", "effect": "resurrection", "mp": 250},
    "Lãnh Vực Vô Cực": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Mở ra lãnh vực: trong vùng này, ta là luật", "effect": "infinite_domain", "mp": 300},
    "Kiếm Ý Tuyệt Đỉnh": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Không cần kiếm, chỉ cần ý chí là có thể chém đứt linh hồn", "effect": "sword_will", "mp": 120},
    "Thần Vương Lãnh Vực": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Lãnh vực của thần, vật lý học bị bóp méo theo ý chí", "effect": "god_domain", "mp": 350},
    "Tuyệt Đối Phòng Thủ": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Trong 1 lượt: hoàn toàn bất khả xâm phạm", "effect": "absolute_defense", "mp": 100},
    "Ngàn Sét": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Triệu hồi ngàn tia sét đánh cùng lúc như mưa", "effect": "thousand_thunder", "mp": 250},
    "Hơi Thở Rồng Cổ Đại": {"rarity": RARITY_LEGENDARY, "type": "active", "desc": "Hơi thở của Rồng Đen Cổ Đại: thiêu rụi mọi thứ trước mắt", "effect": "ancient_dragon_breath", "mp": 200},
    "Bất Diệt": {"rarity": RARITY_LEGENDARY, "type": "passive", "desc": "Mỗi khi chết, hồi sinh với 30% HP (1 lần/ngày)", "effect": "undying"},
    "Chúa Tể Ma Thuật": {"rarity": RARITY_LEGENDARY, "type": "passive", "desc": "Mọi ma thuật của ngươi mạnh gấp đôi và chi phí MP giảm 50%", "effect": "magic_lord"},
    "Thể Xác Thần": {"rarity": RARITY_LEGENDARY, "type": "passive", "desc": "Thể xác đạt tới giới hạn thần linh: mọi vũ khí thường không làm gì được", "effect": "god_body"},
    "Vận Mệnh Anh Hùng": {"rarity": RARITY_LEGENDARY, "type": "passive", "desc": "Người được thế giới chọn: luôn có cơ hội sống khi ở tình huống tuyệt vọng", "effect": "hero_fate"},
    "Tiến Hóa": {"rarity": RARITY_LEGENDARY, "type": "passive", "desc": "Mỗi khi nguy hiểm cận kề, tự động tiến hóa để sống sót", "effect": "evolution"},
    "Nhớ Kiếp Trước": {"rarity": RARITY_LEGENDARY, "type": "passive", "desc": "Nhớ kỹ năng và tri thức từ kiếp trước: bắt đầu với 10 kỹ năng ngẫu nhiên", "effect": "past_life_memory"},

    # ═══════════════════════════════════════
    # ❓ KỸ NĂNG ẨN (Hidden - Điều kiện đặc biệt)
    # ═══════════════════════════════════════

    "Bản Năng Tử Thần": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Sống sót sau khi HP về 0. Kỹ năng ẩn: Tự động kích hoạt khi chết, có 50% cơ hội sống sót với 1 HP và tăng tất cả chỉ số 20% vĩnh viễn",
        "effect": "death_instinct",
        "unlock_condition": "near_death_3_times"
    },
    "Mắt Của Kẻ Chinh Phục": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Hạ gục 100 kẻ địch. Mắt tỏa ra áp lực, địch yếu hơn 50 cấp sẽ không dám chiến đấu",
        "effect": "conqueror_eye",
        "unlock_condition": "kills_100"
    },
    "Kiếm Đạo Chân Thật": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Dùng kiếm 500 lần trong trận. Hiểu được bản chất thật sự của kiếm thuật, mọi đòn kiếm đều như nhát kiếm đầu tiên trong đời - hoàn hảo",
        "effect": "true_sword_path",
        "unlock_condition": "sword_500_times"
    },
    "Ý Chí Quật Cường": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Thua 10 trận nhưng không bỏ cuộc. Ý chí vượt qua thể xác: khi HP = 0 vẫn có thể tiếp tục đánh thêm 2 lượt",
        "effect": "indomitable_will",
        "unlock_condition": "lose_10_times"
    },
    "Máu Quỷ Thức Tỉnh": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Dùng ma thuật tối tăm 50 lần. Máu quỷ trong người thức tỉnh, hình dạng bán quỷ: tất cả sát thương +100% nhưng không phân biệt bạn thù",
        "effect": "demon_blood_awakening",
        "unlock_condition": "dark_magic_50"
    },
    "Người Bảo Vệ": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Đỡ đòn bảo vệ đồng đội 30 lần. Tình yêu thương là sức mạnh: khi bảo vệ người khác, nhận 0 sát thương và phản lại 200%",
        "effect": "protector_spirit",
        "unlock_condition": "protect_30_times"
    },
    "Kẻ Đơn Độc": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Solo kill Boss lần đầu. Một mình chống lại tất cả: ATK/DEF +50% khi chiến đấu một mình",
        "effect": "lone_wolf",
        "unlock_condition": "solo_boss_kill"
    },
    "Rồng Thức Tỉnh": {
        "rarity": RARITY_HIDDEN,
        "type": "active",
        "desc": "🔓 Mở khóa khi: Có trait Máu Rồng + đạt Level 30. Biến thân thành Rồng Bán Thần trong 3 lượt: tất cả chỉ số x5",
        "effect": "dragon_awakening",
        "unlock_condition": "dragon_blood_lv30",
        "mp": 500
    },
    "Thuật Đọc Tâm Trí": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Giúp đỡ 20 NPC khác nhau. Tâm địa thiện lương mở ra trực giác siêu nhiên: đọc được suy nghĩ và ý định của tất cả",
        "effect": "mind_read",
        "unlock_condition": "helped_20_npcs"
    },
    "Bất Tử Thật Sự": {
        "rarity": RARITY_HIDDEN,
        "type": "passive",
        "desc": "🔓 Mở khóa khi: Đã chết và hồi sinh 3 lần. Đã qua cõi chết quá nhiều lần đến mức cái chết không còn muốn nhận: Bất tử hoàn toàn, chỉ có thể bị đánh bại chứ không chết",
        "effect": "true_immortal",
        "unlock_condition": "died_3_times"
    },
}

def get_skill_choices(num_choices=3, player_skills=None, level=1):
    """Lấy danh sách kỹ năng để người chơi chọn khi lên cấp"""
    if player_skills is None:
        player_skills = []
    
    available = {k: v for k, v in SKILLS.items() 
                 if k not in player_skills and v["rarity"] != RARITY_HIDDEN}
    
    # Cân bằng tỷ lệ theo level
    if level >= 20:
        weights = {RARITY_COMMON: 20, RARITY_RARE: 40, RARITY_EPIC: 30, RARITY_LEGENDARY: 10}
    elif level >= 10:
        weights = {RARITY_COMMON: 35, RARITY_RARE: 40, RARITY_EPIC: 20, RARITY_LEGENDARY: 5}
    else:
        weights = {RARITY_COMMON: 55, RARITY_RARE: 30, RARITY_EPIC: 12, RARITY_LEGENDARY: 3}
    
    chosen = []
    attempts = 0
    while len(chosen) < num_choices and attempts < 100:
        attempts += 1
        rarity = random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
        candidates = [k for k, v in available.items() if v["rarity"] == rarity and k not in chosen]
        if candidates:
            chosen.append(random.choice(candidates))
    
    return chosen

def get_skills_info(skill_names):
    """Lấy thông tin chi tiết của các kỹ năng"""
    result = []
    for name in skill_names:
        if name in SKILLS:
            skill = SKILLS[name]
            result.append({
                "name": name,
                "rarity": skill["rarity"],
                "type": skill["type"],
                "desc": skill["desc"],
                "mp": skill.get("mp", 0)
            })
    return result
