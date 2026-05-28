# ⚔️ Fantasy RPG Discord Bot - Aeternium

Bot Discord nhập vai fantasy với AI Game Master tự động!

## 📋 Danh Sách Lệnh

| Lệnh | Mô Tả |
|------|--------|
| `!create` | Tạo nhân vật mới |
| `!profile` hoặc `!p` | Xem thông số nhân vật |
| `!do [hành động]` | Làm bất cứ điều gì! |
| `!train [stat] [mô tả]` | Tập luyện nâng chỉ số |
| `!rest` | Nghỉ ngơi hồi phục |
| `!skills` | Xem kỹ năng |
| `!chooseskill` | Chọn kỹ năng mới (cần Skill Point) |
| `!statup [stat]` | Nâng chỉ số (cần Stat Point) |
| `!inventory` | Xem túi đồ |
| `!world` | Xem thông tin thế giới |
| `!leaderboard` | Bảng xếp hạng |

## 🚀 Cách Deploy lên Railway

1. Tạo tài khoản tại railway.app
2. New Project → Deploy from GitHub repo
3. Upload code lên GitHub
4. Thêm biến môi trường:
   - DISCORD_TOKEN = token của bot Discord
   - GEMINI_API_KEY = API key của Google Gemini
5. Deploy!

## ⚙️ Biến Môi Trường Cần Thiết

DISCORD_TOKEN=token_discord_của_bạn
GEMINI_API_KEY=api_key_gemini_của_bạn
