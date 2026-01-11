import websocket
import json
import time

def on_open(ws):
    print("✅ WebSocket Connection Opened")
    print("URL:", ws.url)
    
def on_message(ws, message):
    data = json.loads(message)
    print(f"📨 Message Type: {data.get('type', 'unknown')}")
    print(f"📊 Data Keys: {list(data.get('data', {}).keys())}")
    print(f"⏰ Timestamp: {data.get('timestamp', 'N/A')}")
    print("-" * 50)
    
    # Agar initial message aaya toh
    if data.get('type') == 'initial':
        metrics = data.get('data', {})
        print(f"💊 Total Drugs: {metrics.get('total_drugs', 0)}")
        print(f"🔥 Critical Pairs: {metrics.get('critical_risk_pairs', 0)}")
        print(f"📈 Avg Risk: {metrics.get('avg_risk_score', 0)}%")

def on_error(ws, error):
    print(f"❌ WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"🔌 WebSocket Closed: {close_status_code} - {close_msg}")

if __name__ == "__main__":
    # WebSocket URL
    ws_url = "ws://localhost:8000/ws/dashboard"
    
    print("🔗 Testing WebSocket Connection...")
    print(f"URL: {ws_url}")
    
    # WebSocket connection establish karein
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    # 30 seconds ke liye run karein aur messages receive karein
    print("\n⏳ Receiving messages for 30 seconds...")
    ws.run_forever(ping_interval=10, ping_timeout=5)
    
    
    is mn heatmap ka ek issue ha k us pr annotations show nhi ho rheen.... or charts blkul pyare nh hn.. Seaborn ka use posssible ha to wo bhi krne mn msla nh ha kaheen...jsy ek bht pyara dashboard hta ha modern colors k sth.. or in mn emojis jsy fire emoji ye bht unprofessional look de rha ha... 
    Grid wgehra js mn charts hn wo bhi achy nhi hn... Na in k colors overall app theme se match kr rhy hn... 
    
    
    # "https://www.anxietyenders.com/images/handd.jpg"
    # "https://media.istockphoto.com/id/522886451/photo/pills.jpg?s=612x612&w=0&k=20&c=BlQFnwGS7WW33AXj2TixoOqQbfB00JH-YkNB09NV9EE="