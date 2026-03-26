from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from ...schemas.events import DevEventRequest, DevEventResponse
from ...services.app_services import AppServices
from ..dependencies import get_services

router = APIRouter()

CONTROL_PAGE_HTML = """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>桌宠后端测试页</title>
    <style>
      body {
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f4f7fb;
        color: #18223f;
      }
      main {
        max-width: 520px;
        margin: 48px auto;
        padding: 24px;
        border-radius: 20px;
        background: #ffffff;
        box-shadow: 0 18px 42px rgba(24, 34, 63, 0.12);
      }
      h1 {
        margin-top: 0;
        font-size: 24px;
      }
      form {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      label {
        display: flex;
        flex-direction: column;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
      }
      textarea, input, select {
        min-height: 140px;
        padding: 14px;
        border: 1px solid #c8d6eb;
        border-radius: 14px;
        font: inherit;
        box-sizing: border-box;
      }
      input, select {
        min-height: 44px;
      }
      textarea {
        resize: vertical;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
      }
      .hidden {
        display: none;
      }
      button {
        align-self: flex-end;
        min-width: 120px;
        height: 42px;
        border: none;
        border-radius: 999px;
        background: linear-gradient(135deg, #4dd8ff, #79b8ff);
        color: white;
        font: inherit;
        font-weight: 600;
        cursor: pointer;
      }
      #status {
        min-height: 24px;
        font-size: 14px;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>桌宠后端测试页</h1>
      <p>这个页面只用于联调。选择一种高层事件并发送，前端应按事件类型更新对话气泡、状态或动作意图。</p>
      <form id="control-form">
        <label>
          事件类型
          <select id="event-type">
            <option value="bubble.show">bubble.show</option>
            <option value="emotion.set">emotion.set</option>
            <option value="motion.play">motion.play</option>
            <option value="mode.switch">mode.switch</option>
            <option value="move.intent">move.intent</option>
          </select>
        </label>

        <label id="field-text">
          气泡文本
          <textarea id="text" placeholder="输入要推送给前端桌宠的消息..."></textarea>
        </label>

        <div class="grid">
          <label id="field-duration">
            持续时间（ms）
            <input id="duration-ms" type="number" min="1000" max="20000" value="5000" />
          </label>

          <label id="field-priority" class="hidden">
            优先级
            <input id="priority" type="number" min="0" max="100" value="50" />
          </label>
        </div>

        <label id="field-emotion" class="hidden">
          emotion
          <input id="emotion" type="text" placeholder="例如 curious / shy / angry" />
        </label>

        <label id="field-motion" class="hidden">
          motion
          <input id="motion" type="text" placeholder="例如 wave_slow / idle_breath" />
        </label>

        <label id="field-mode" class="hidden">
          mode
          <input id="mode" type="text" placeholder="例如 quiet_companion / companion" />
        </label>

        <label id="field-intent" class="hidden">
          intent
          <input id="intent" type="text" placeholder="例如 dock_right / follow_cursor" />
        </label>

        <button type="submit">Send</button>
      </form>
      <p id="status"></p>
    </main>
    <script>
      const form = document.getElementById('control-form');
      const eventTypeSelect = document.getElementById('event-type');
      const textInput = document.getElementById('text');
      const durationInput = document.getElementById('duration-ms');
      const emotionInput = document.getElementById('emotion');
      const motionInput = document.getElementById('motion');
      const priorityInput = document.getElementById('priority');
      const modeInput = document.getElementById('mode');
      const intentInput = document.getElementById('intent');
      const status = document.getElementById('status');
      const fieldText = document.getElementById('field-text');
      const fieldDuration = document.getElementById('field-duration');
      const fieldEmotion = document.getElementById('field-emotion');
      const fieldMotion = document.getElementById('field-motion');
      const fieldPriority = document.getElementById('field-priority');
      const fieldMode = document.getElementById('field-mode');
      const fieldIntent = document.getElementById('field-intent');

      const syncVisibleFields = () => {
        const nextType = eventTypeSelect.value;
        fieldText.classList.toggle('hidden', nextType !== 'bubble.show');
        fieldDuration.classList.toggle('hidden', nextType !== 'bubble.show');
        fieldEmotion.classList.toggle('hidden', nextType !== 'emotion.set');
        fieldMotion.classList.toggle('hidden', nextType !== 'motion.play');
        fieldPriority.classList.toggle('hidden', nextType !== 'motion.play');
        fieldMode.classList.toggle('hidden', nextType !== 'mode.switch');
        fieldIntent.classList.toggle('hidden', nextType !== 'move.intent');
      };

      eventTypeSelect.addEventListener('change', syncVisibleFields);
      syncVisibleFields();

      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        status.textContent = '发送中...';

        try {
          const payload = {
            type: eventTypeSelect.value,
            text: textInput.value,
            duration_ms: Number(durationInput.value),
            emotion: emotionInput.value,
            motion: motionInput.value,
            priority: Number(priorityInput.value),
            mode: modeInput.value,
            intent: intentInput.value,
          };

          const response = await fetch('/api/dev/messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });

          const result = await response.json();
          if (!response.ok) {
            throw new Error(result.detail || '发送失败');
          }

          status.textContent = `已推送：${result.event.type}`;
          textInput.value = '';
        } catch (error) {
          status.textContent = error.message || '发送失败';
        }
      });
    </script>
  </body>
</html>
"""


@router.get('/dev/control', response_class=HTMLResponse)
async def dev_control_page() -> HTMLResponse:
    return HTMLResponse(CONTROL_PAGE_HTML)


@router.post('/api/dev/messages', response_model=DevEventResponse)
async def send_dev_message(
    request: DevEventRequest,
    services: AppServices = Depends(get_services),
) -> DevEventResponse:
    event = services.behavior_policy_engine.build_manual_event(request)
    await services.event_bus.publish(event)
    return DevEventResponse(status='ok', event=event)
