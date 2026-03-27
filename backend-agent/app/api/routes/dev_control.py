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
      .state-panel {
        margin-top: 24px;
        padding: 16px;
        border-radius: 16px;
        background: #eef4ff;
      }
      .state-panel h2 {
        margin: 0 0 12px;
        font-size: 16px;
      }
      #latest-state {
        margin: 0;
        white-space: pre-wrap;
        word-break: break-word;
        font-size: 13px;
        line-height: 1.5;
      }
      .scenario-panel {
        margin-top: 24px;
        padding: 16px;
        border-radius: 16px;
        background: #f6fbf5;
      }
      .scenario-panel h2 {
        margin: 0 0 12px;
        font-size: 16px;
      }
      .scenario-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
      }
      .scenario-actions button {
        align-self: auto;
        min-width: 0;
        padding: 0 16px;
        background: linear-gradient(135deg, #4fc28a, #3d96d2);
      }
      .scenario-note {
        margin: 0 0 12px;
        font-size: 13px;
        line-height: 1.5;
        color: #36506f;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>桌宠后端测试页</h1>
      <p>这个页面只用于联调。选择一种高层事件并发送，前端应按事件类型更新对话气泡、动作或窗口位置。第一阶段默认使用显式 `window.move`，`move.intent` 只保留 legacy 兼容验证。</p>
      <form id="control-form">
        <label>
          事件类型
          <select id="event-type">
            <option value="bubble.show">bubble.show</option>
            <option value="emotion.set">emotion.set</option>
            <option value="motion.play">motion.play</option>
            <option value="mode.switch">mode.switch</option>
            <option value="window.move">window.move</option>
            <option value="move.intent">move.intent (legacy)</option>
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

        <div class="grid">
          <label id="field-bubble-motion" class="hidden">
            bubble.motion（`touch_head / touch_body / pinch / thinking` 走原生编排）
            <select id="bubble-motion">
              <option value="">无</option>
              <option value="touch_body">touch_body</option>
              <option value="touch_head">touch_head</option>
              <option value="pinch">pinch</option>
              <option value="thinking">thinking</option>
              <option value="idle">idle</option>
            </select>
          </label>

          <label id="field-graph" class="hidden">
            graph
            <select id="graph">
              <option value="">无</option>
              <option value="think">think</option>
              <option value="pinch">pinch</option>
            </select>
          </label>
        </div>

        <label id="field-emotion" class="hidden">
          emotion
          <select id="emotion">
            <option value="">无</option>
            <option value="shy">shy</option>
            <option value="think">think</option>
            <option value="thinking">thinking</option>
            <option value="pinch">pinch</option>
          </select>
        </label>

        <label id="field-motion" class="hidden">
          motion
          <select id="motion">
            <option value="">请选择</option>
            <option value="idle">idle</option>
            <option value="move">move</option>
            <option value="normal">normal</option>
            <option value="touch_head">touch_head</option>
            <option value="touch_body">touch_body</option>
            <option value="sleep">sleep</option>
            <option value="raised">raised</option>
            <option value="state_one">state_one</option>
            <option value="pinch">pinch</option>
            <option value="thinking">thinking</option>
          </select>
        </label>

        <label id="field-mode" class="hidden">
          mode
          <select id="mode">
            <option value="">请选择</option>
            <option value="normal">normal</option>
            <option value="thinking">thinking</option>
          </select>
        </label>

        <label id="field-intent" class="hidden">
          intent（legacy）
          <select id="intent">
            <option value="">请选择</option>
            <option value="dock_left">dock_left</option>
            <option value="dock_right">dock_right</option>
            <option value="dock_top">dock_top</option>
            <option value="dock_bottom">dock_bottom</option>
          </select>
        </label>

        <div class="grid">
          <label id="field-dx" class="hidden">
            dx（逻辑位移）
            <input id="dx" type="number" step="10" value="120" />
          </label>

          <label id="field-dy" class="hidden">
            dy（逻辑位移）
            <input id="dy" type="number" step="10" value="0" />
          </label>
        </div>

        <button type="submit">Send</button>
      </form>
      <p id="status"></p>
      <section class="scenario-panel">
        <h2>组合场景</h2>
        <p class="scenario-note">用于继续验证 `window.move` 和说话/动作的组合体感。这里默认只组合显式 `window.move`，不再把 intent 当主路径。</p>
        <div class="scenario-actions">
          <button type="button" data-scenario="move-then-bubble">move -> bubble</button>
          <button type="button" data-scenario="bubble-then-move">bubble -> move</button>
          <button type="button" data-scenario="move-then-motion">move -> motion</button>
          <button type="button" data-scenario="move-then-bubble-touch">move -> bubble.touch</button>
        </div>
      </section>
      <section class="state-panel">
        <h2>最新状态回传</h2>
        <pre id="latest-state">等待 VPet 回传状态...</pre>
      </section>
    </main>
    <script>
      const form = document.getElementById('control-form');
      const eventTypeSelect = document.getElementById('event-type');
      const textInput = document.getElementById('text');
      const durationInput = document.getElementById('duration-ms');
      const emotionInput = document.getElementById('emotion');
      const motionInput = document.getElementById('motion');
      const bubbleMotionInput = document.getElementById('bubble-motion');
      const graphInput = document.getElementById('graph');
      const priorityInput = document.getElementById('priority');
      const modeInput = document.getElementById('mode');
      const intentInput = document.getElementById('intent');
      const dxInput = document.getElementById('dx');
      const dyInput = document.getElementById('dy');
      const status = document.getElementById('status');
      const latestState = document.getElementById('latest-state');
      const fieldText = document.getElementById('field-text');
      const fieldDuration = document.getElementById('field-duration');
      const fieldEmotion = document.getElementById('field-emotion');
      const fieldMotion = document.getElementById('field-motion');
      const fieldBubbleMotion = document.getElementById('field-bubble-motion');
      const fieldGraph = document.getElementById('field-graph');
      const fieldPriority = document.getElementById('field-priority');
      const fieldMode = document.getElementById('field-mode');
      const fieldIntent = document.getElementById('field-intent');
      const fieldDx = document.getElementById('field-dx');
      const fieldDy = document.getElementById('field-dy');
      const scenarioButtons = Array.from(document.querySelectorAll('[data-scenario]'));

      const wait = (milliseconds) =>
        new Promise((resolve) => window.setTimeout(resolve, milliseconds));

      const syncVisibleFields = () => {
        const nextType = eventTypeSelect.value;
        fieldText.classList.toggle('hidden', nextType !== 'bubble.show');
        fieldDuration.classList.toggle('hidden', nextType !== 'bubble.show');
        fieldBubbleMotion.classList.toggle('hidden', nextType !== 'bubble.show');
        fieldEmotion.classList.toggle('hidden', !(nextType === 'bubble.show' || nextType === 'emotion.set'));
        fieldMotion.classList.toggle('hidden', nextType !== 'motion.play');
        fieldGraph.classList.toggle('hidden', !(nextType === 'bubble.show' || nextType === 'emotion.set'));
        fieldPriority.classList.toggle('hidden', nextType !== 'motion.play');
        fieldMode.classList.toggle('hidden', nextType !== 'mode.switch');
        fieldDx.classList.toggle('hidden', nextType !== 'window.move');
        fieldDy.classList.toggle('hidden', nextType !== 'window.move');
        fieldIntent.classList.toggle('hidden', nextType !== 'move.intent');
      };

      const renderState = (state) => {
        if (!state) {
          latestState.textContent = '后端已启动，但还没收到 VPet 插件状态。';
          return;
        }

        latestState.textContent = JSON.stringify(state, null, 2);
      };

      const refreshState = async () => {
        try {
          const response = await fetch('/api/dev/state');
          const result = await response.json();
          if (!response.ok) {
            throw new Error(result.detail || '状态拉取失败');
          }
          renderState(result.state || null);
        } catch (error) {
          latestState.textContent = error.message || '状态拉取失败';
        }
      };

      const sendEvent = async (payload) => {
        const response = await fetch('/api/dev/messages', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || '发送失败');
        }
        return result;
      };

      const scenarioPayloads = {
        'move-then-bubble': [
          { type: 'window.move', dx: 120, dy: -20 },
          { type: 'bubble.show', text: '我先挪一下再说。', duration_ms: 5000, expression: 'thinking', graph: 'think' },
        ],
        'bubble-then-move': [
          { type: 'bubble.show', text: '我边说边换位置。', duration_ms: 5000, motion: 'touch_body', expression: 'shy' },
          { type: 'window.move', dx: -120, dy: 20 },
        ],
        'move-then-motion': [
          { type: 'window.move', dx: 140, dy: 0 },
          { type: 'motion.play', motion: 'touch_head', priority: 50 },
        ],
        'move-then-bubble-touch': [
          { type: 'window.move', dx: -120, dy: 0 },
          { type: 'bubble.show', text: 'move then touch bubble', duration_ms: 5000, motion: 'touch_body', expression: 'shy' },
        ],
      };

      const scenarioGapMs = {
        'move-then-bubble': 450,
        'bubble-then-move': 280,
        'move-then-motion': 280,
        'move-then-bubble-touch': 450,
      };

      const runScenario = async (scenarioKey) => {
        const steps = scenarioPayloads[scenarioKey];
        if (!steps) {
          throw new Error('未知组合场景');
        }

        status.textContent = `发送组合场景：${scenarioKey}`;
        const gapMs = scenarioGapMs[scenarioKey] || 280;
        for (let index = 0; index < steps.length; index += 1) {
          await sendEvent(steps[index]);
          if (index < steps.length - 1) {
            await wait(gapMs);
          }
        }
        await wait(350);
        await refreshState();
        status.textContent = `组合场景完成：${scenarioKey}`;
      };

      eventTypeSelect.addEventListener('change', syncVisibleFields);
      syncVisibleFields();
      refreshState();
      window.setInterval(refreshState, 1500);
      scenarioButtons.forEach((button) => {
        button.addEventListener('click', async () => {
          try {
            await runScenario(button.dataset.scenario);
          } catch (error) {
            status.textContent = error.message || '组合场景发送失败';
          }
        });
      });

      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        status.textContent = '发送中...';

        try {
          const payload = {
            type: eventTypeSelect.value,
            text: textInput.value,
            duration_ms: Number(durationInput.value),
            emotion: emotionInput.value,
            motion: eventTypeSelect.value === 'bubble.show' ? bubbleMotionInput.value : motionInput.value,
            expression: eventTypeSelect.value === 'bubble.show' ? emotionInput.value : '',
            graph: graphInput.value,
            priority: Number(priorityInput.value),
            mode: modeInput.value,
            intent: intentInput.value,
            dx: Number(dxInput.value),
            dy: Number(dyInput.value),
          };

          const result = await sendEvent(payload);

          status.textContent = `已推送：${result.event.type}`;
          textInput.value = '';
          refreshState();
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
