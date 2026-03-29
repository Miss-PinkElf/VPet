import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from ...schemas.events import (
    DevEventRequest,
    DevEventResponse,
    DevScenarioListResponse,
    DevSequenceDispatchResponse,
    DevSequenceRequest,
)
from ...services.app_services import AppServices
from ..dependencies import get_services

router = APIRouter()

REPO_ROOT = Path(__file__).resolve().parents[4]
QUICK_TEST_CATALOG_PATH = REPO_ROOT / '.explore' / 'desktop-pet-vpet-body-bridge' / 'quick-tests.json'

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
      .page-link {
        display: inline-flex;
        margin-bottom: 16px;
        color: #2e6bcf;
        text-decoration: none;
        font-size: 14px;
        font-weight: 600;
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
      .sequence-panel {
        margin-top: 24px;
        padding: 16px;
        border-radius: 16px;
        background: #fff6ea;
      }
      .sequence-panel h2 {
        margin: 0 0 12px;
        font-size: 16px;
      }
      .sequence-panel p {
        margin: 0 0 12px;
        font-size: 13px;
        line-height: 1.5;
        color: #5d4a27;
      }
      .sequence-panel textarea {
        min-height: 180px;
      }
      .sequence-panel button {
        align-self: auto;
        background: linear-gradient(135deg, #f0a037, #df6d35);
      }
    </style>
  </head>
  <body>
    <main>
      <a class="page-link" href="/dev/quick-test">打开 Quick Test JSON 页面</a>
      <h1>桌宠后端测试页</h1>
      <p>这个页面只用于联调。选择一种高层事件并发送，前端应按事件类型更新对话气泡、动作或窗口位置。第一阶段默认使用显式 `window.move`；`move.intent` 只保留运行时 legacy 兼容，不再作为联调主入口。</p>
      <form id="control-form">
        <label>
          事件类型
          <select id="event-type">
            <option value="bubble.show">bubble.show</option>
            <option value="emotion.set">emotion.set</option>
            <option value="motion.play">motion.play</option>
            <option value="mode.switch">mode.switch</option>
            <option value="window.move">window.move</option>
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
        <p class="scenario-note">这些组合场景现在由后端 sequence/scenario 层负责调度，前端页面只触发预设场景，不再自己保存步骤与延迟。</p>
        <div class="scenario-actions" id="scenario-actions"></div>
      </section>
      <section class="sequence-panel">
        <h2>自定义 Sequence</h2>
        <p>这里继续用于更长链路联调。`delay_ms` 表示该步执行前的等待时间；`wait_for` 可让该步在真正落稳后再进入下一步。当前最实用的门控是 `event_applied`、`move_complete` 和 `motion_complete`。当一条 sequence 里出现两次 `bubble.show` 这类重复事件时，优先看状态里的 `last_event_id / last_sequence_name / last_step_index`。</p>
        <textarea id="sequence-editor">{
  "name": "think-speak-move-touch-speak-recover",
  "steps": [
    {
      "event": {
        "type": "mode.switch",
        "mode": "thinking"
      },
      "wait_for": "event_applied"
    },
    {
      "event": {
        "type": "bubble.show",
        "text": "我先想一下这件事。",
        "duration_ms": 4000,
        "expression": "thinking",
        "graph": "think"
      },
      "wait_for": "event_applied"
    },
    {
      "event": {
        "type": "window.move",
        "dx": 80,
        "dy": -20,
        "style": "smart"
      },
      "wait_for": "move_complete",
      "wait_timeout_ms": 5000,
      "settle_ms": 120
    },
    {
      "event": {
        "type": "motion.play",
        "motion": "touch_head",
        "priority": 55
      },
      "wait_for": "motion_complete",
      "wait_timeout_ms": 6000,
      "settle_ms": 120
    },
    {
      "event": {
        "type": "bubble.show",
        "text": "想好了，我继续说给你听。",
        "duration_ms": 5000,
        "expression": "thinking",
        "graph": "think"
      },
      "wait_for": "event_applied"
    },
    {
      "event": {
        "type": "mode.switch",
        "mode": "normal"
      }
    }
  ]
}</textarea>
        <button type="button" id="run-sequence">Run Sequence</button>
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
      const fieldDx = document.getElementById('field-dx');
      const fieldDy = document.getElementById('field-dy');
      const scenarioActions = document.getElementById('scenario-actions');
      const sequenceEditor = document.getElementById('sequence-editor');
      const runSequenceButton = document.getElementById('run-sequence');

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

      const renderScenarioButtons = (scenarios) => {
        scenarioActions.replaceChildren();
        scenarios.forEach((scenario) => {
          const button = document.createElement('button');
          button.type = 'button';
          button.dataset.scenario = scenario.scenario_id;
          button.title = scenario.description;
          button.textContent = scenario.title;
          button.addEventListener('click', async () => {
            try {
              await runScenario(scenario.scenario_id);
            } catch (error) {
              status.textContent = error.message || '组合场景发送失败';
            }
          });
          scenarioActions.appendChild(button);
        });
      };

      const runScenario = async (scenarioKey) => {
        status.textContent = `发送组合场景：${scenarioKey}`;
        const response = await fetch(`/api/dev/scenarios/${scenarioKey}`, {
          method: 'POST',
        });
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || '组合场景发送失败');
        }
        await wait(350);
        await refreshState();
        status.textContent = `组合场景已下发：${result.sequence_name}`;
      };

      const loadScenarios = async () => {
        const response = await fetch('/api/dev/scenarios');
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || '组合场景加载失败');
        }
        renderScenarioButtons(result.scenarios || []);
      };

      const runSequence = async () => {
        let payload;
        try {
          payload = JSON.parse(sequenceEditor.value);
        } catch (error) {
          throw new Error('sequence JSON 解析失败');
        }

        const response = await fetch('/api/dev/sequences', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || 'sequence 发送失败');
        }
        await wait(350);
        await refreshState();
        status.textContent = `sequence 已下发：${result.sequence_name}`;
      };

      eventTypeSelect.addEventListener('change', syncVisibleFields);
      syncVisibleFields();
      loadScenarios().catch((error) => {
        status.textContent = error.message || '组合场景加载失败';
      });
      refreshState();
      window.setInterval(refreshState, 1500);
      runSequenceButton.addEventListener('click', async () => {
        try {
          await runSequence();
        } catch (error) {
          status.textContent = error.message || 'sequence 发送失败';
        }
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

QUICK_TEST_PAGE_HTML = """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>桌宠 Quick Test</title>
    <style>
      body {
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f4f7fb;
        color: #18223f;
      }
      main {
        max-width: 860px;
        margin: 40px auto;
        padding: 24px;
        border-radius: 20px;
        background: #ffffff;
        box-shadow: 0 18px 42px rgba(24, 34, 63, 0.12);
      }
      h1 {
        margin: 0 0 12px;
        font-size: 24px;
      }
      p {
        margin: 0 0 16px;
        line-height: 1.6;
      }
      a {
        color: #2e6bcf;
        text-decoration: none;
        font-weight: 600;
      }
      textarea {
        width: 100%;
        min-height: 260px;
        padding: 14px;
        border: 1px solid #c8d6eb;
        border-radius: 14px;
        font: inherit;
        box-sizing: border-box;
        resize: vertical;
      }
      .toolbar {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 16px;
      }
      button {
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
      .test-panel,
      .result-panel,
      .state-panel {
        margin-top: 24px;
        padding: 16px;
        border-radius: 16px;
      }
      .test-panel {
        background: #f6fbf5;
      }
      .result-panel {
        background: #fff6ea;
      }
      .state-panel {
        background: #eef4ff;
      }
      .test-list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 12px;
      }
      .test-card {
        border: 1px solid #d8e4f8;
        border-radius: 14px;
        padding: 14px;
        background: white;
        cursor: pointer;
      }
      .test-card.selected {
        border-color: #4d9cff;
        box-shadow: 0 0 0 3px rgba(77, 156, 255, 0.18);
      }
      .test-card h2 {
        margin: 0 0 8px;
        font-size: 16px;
      }
      .test-card p {
        margin: 0 0 12px;
        font-size: 13px;
        color: #4d607e;
      }
      .test-meta {
        margin-bottom: 12px;
        font-size: 12px;
        color: #667b9d;
      }
      .test-result-summary {
        margin: 0 0 12px;
        font-size: 12px;
        color: #35506f;
      }
      pre {
        margin: 0;
        white-space: pre-wrap;
        word-break: break-word;
        font-size: 13px;
        line-height: 1.5;
      }
      #status {
        min-height: 24px;
        margin-top: 16px;
        font-size: 14px;
      }
      .result-editor-panel {
        margin-top: 24px;
        padding: 16px;
        border-radius: 16px;
        background: #f7f3ff;
      }
      .result-editor-panel h2 {
        margin: 0 0 12px;
        font-size: 16px;
      }
      .result-editor-grid {
        display: grid;
        grid-template-columns: 180px 1fr;
        gap: 12px;
      }
      .result-editor-panel label {
        display: flex;
        flex-direction: column;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
      }
      .result-editor-panel select,
      .result-editor-panel textarea {
        width: 100%;
        padding: 12px;
        border: 1px solid #c8d6eb;
        border-radius: 12px;
        font: inherit;
        box-sizing: border-box;
      }
      .result-editor-panel textarea {
        min-height: 150px;
        resize: vertical;
      }
      .result-editor-actions {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
        margin-top: 12px;
      }
      .result-editor-actions button {
        min-width: 132px;
      }
      #selected-test-name,
      #selected-test-meta {
        margin: 0 0 8px;
      }
    </style>
  </head>
  <body>
    <main>
      <a href="/dev/control">返回完整联调页</a>
      <h1>桌宠 Quick Test</h1>
      <p>这个页面比 `/dev/control` 更轻，只做一件事：读取一份包含多个测试项的 JSON，然后点击其中一个直接发送。`payload` 里如果是单事件就走 `/api/dev/messages`，如果包含 `steps` 就走 `/api/dev/sequences`。</p>
      <textarea id="catalog-editor">{
  "tests": [
    {
      "id": "move-right",
      "title": "右移 120",
      "description": "验证显式位移是否稳定。",
      "payload": {
        "type": "window.move",
        "dx": 120,
        "dy": 0
      }
    },
    {
      "id": "touch-head",
      "title": "摸头动作",
      "description": "验证单独动作入口。",
      "payload": {
        "type": "motion.play",
        "motion": "touch_head",
        "priority": 50
      }
    },
    {
      "id": "thinking-walk-speak",
      "title": "思考后移动并说话",
      "description": "验证 4 步 sequence。",
      "payload": {
        "name": "thinking-walk-speak-normal",
        "steps": [
          {
            "event": {
              "type": "mode.switch",
              "mode": "thinking"
            }
          },
          {
            "event": {
              "type": "window.move",
              "dx": 90,
              "dy": -20,
              "style": "smart"
            },
            "wait_for": "move_complete",
            "wait_timeout_ms": 5000,
            "settle_ms": 120
          },
          {
            "event": {
              "type": "bubble.show",
              "text": "我先想一下，再边移动边回答。",
              "duration_ms": 5000,
              "graph": "think"
            }
          },
          {
            "event": {
              "type": "mode.switch",
              "mode": "normal"
            }
          }
        ]
      }
    }
  ]
}</textarea>
      <div class="toolbar">
        <button type="button" id="load-file">Load File</button>
        <button type="button" id="save-file">Save File</button>
        <button type="button" id="load-tests">Load Tests</button>
        <button type="button" id="refresh-state">Refresh State</button>
      </div>
      <p id="status"></p>
      <section class="test-panel">
        <h2>可执行测试</h2>
        <div class="test-list" id="test-list"></div>
      </section>
      <section class="result-editor-panel">
        <h2>测试结果</h2>
        <p id="selected-test-name">尚未选择测试项。</p>
        <p id="selected-test-meta"></p>
        <div class="result-editor-grid">
          <label>
            结果状态
            <select id="result-status">
              <option value="untested">未测试</option>
              <option value="pass">通过</option>
              <option value="fail">失败</option>
              <option value="mixed">部分通过</option>
            </select>
          </label>
          <label>
            结果说明
            <textarea id="result-note" placeholder="记录你在这次测试里看到的现象、体感或问题..."></textarea>
          </label>
        </div>
        <div class="result-editor-actions">
          <button type="button" id="reload-result">Reload Result</button>
          <button type="button" id="save-result">Save Result</button>
        </div>
      </section>
      <section class="result-panel">
        <h2>最近一次发送结果</h2>
        <pre id="last-result">等待发送...</pre>
      </section>
      <section class="state-panel">
        <h2>最新状态回传</h2>
        <pre id="latest-state">等待 VPet 回传状态...</pre>
      </section>
    </main>
    <script>
      const catalogEditor = document.getElementById('catalog-editor');
      const loadFileButton = document.getElementById('load-file');
      const saveFileButton = document.getElementById('save-file');
      const loadTestsButton = document.getElementById('load-tests');
      const refreshStateButton = document.getElementById('refresh-state');
      const testList = document.getElementById('test-list');
      const status = document.getElementById('status');
      const lastResult = document.getElementById('last-result');
      const latestState = document.getElementById('latest-state');
      const selectedTestName = document.getElementById('selected-test-name');
      const selectedTestMeta = document.getElementById('selected-test-meta');
      const resultStatus = document.getElementById('result-status');
      const resultNote = document.getElementById('result-note');
      const reloadResultButton = document.getElementById('reload-result');
      const saveResultButton = document.getElementById('save-result');

      let currentCatalog = null;
      let selectedTestIndex = null;

      const wait = (milliseconds) =>
        new Promise((resolve) => window.setTimeout(resolve, milliseconds));

      const normalizeCatalog = (parsed) => {
        if (Array.isArray(parsed)) {
          return { tests: parsed };
        }
        if (parsed && typeof parsed === 'object' && Array.isArray(parsed.tests)) {
          return parsed;
        }
        throw new Error('JSON 需要是数组，或包含 tests 数组。');
      };

      const normalizeTests = (parsed) => {
        return normalizeCatalog(parsed).tests;
      };

      const getPayload = (test) => {
        if (test && typeof test === 'object' && test.payload && typeof test.payload === 'object') {
          return test.payload;
        }
        throw new Error('每个测试项都需要 payload。');
      };

      const isSequencePayload = (payload) =>
        Array.isArray(payload?.steps);

      const fetchCatalog = async () => {
        const response = await fetch('/api/dev/quick-test/catalog');
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || '测试目录读取失败');
        }
        const normalized = normalizeCatalog(result.catalog);
        currentCatalog = normalized;
        catalogEditor.value = JSON.stringify(normalized, null, 2);
        return normalized;
      };

      const persistCatalog = async (catalog) => {
        const response = await fetch('/api/dev/quick-test/catalog', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(catalog),
        });
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || '测试目录保存失败');
        }
        const normalized = normalizeCatalog(result.catalog);
        currentCatalog = normalized;
        catalogEditor.value = JSON.stringify(normalized, null, 2);
        return normalized;
      };

      const saveCatalog = async () => {
        let parsed;
        try {
          parsed = JSON.parse(catalogEditor.value);
        } catch (error) {
          throw new Error('JSON 解析失败，无法保存');
        }
        return persistCatalog(normalizeCatalog(parsed));
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

      const sendPayload = async (payload) => {
        const endpoint = isSequencePayload(payload) ? '/api/dev/sequences' : '/api/dev/messages';
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || '发送失败');
        }
        return { endpoint, result };
      };

      const executeTest = async (test, index) => {
        const payload = getPayload(test);
        const label = test.title || test.id || `test-${index + 1}`;
        selectTest(index);
        status.textContent = `发送中：${label}`;
        const { endpoint, result } = await sendPayload(payload);
        lastResult.textContent = JSON.stringify({ endpoint, result, payload }, null, 2);
        await wait(350);
        await refreshState();
        status.textContent = `已发送：${label}`;
      };

      const renderTests = (tests) => {
        testList.replaceChildren();
        tests.forEach((test, index) => {
          const payload = getPayload(test);
          const card = document.createElement('article');
          card.className = 'test-card';
          if (index === selectedTestIndex) {
            card.classList.add('selected');
          }
          card.addEventListener('click', () => {
            selectTest(index);
          });

          const title = document.createElement('h2');
          title.textContent = test.title || test.id || `test-${index + 1}`;
          card.appendChild(title);

          if (test.description) {
            const description = document.createElement('p');
            description.textContent = test.description;
            card.appendChild(description);
          }

          const meta = document.createElement('div');
          meta.className = 'test-meta';
          meta.textContent = isSequencePayload(payload)
            ? `sequence · ${payload.steps.length} steps`
            : `event · ${payload.type || 'unknown'}`;
          card.appendChild(meta);

          const resultSummary = document.createElement('p');
          resultSummary.className = 'test-result-summary';
          if (test.result) {
            const updatedAt = test.result.updated_at ? ` · ${test.result.updated_at}` : '';
            resultSummary.textContent = `结果：${test.result.status || 'untested'}${updatedAt}`;
          } else {
            resultSummary.textContent = '结果：未记录';
          }
          card.appendChild(resultSummary);

          const button = document.createElement('button');
          button.type = 'button';
          button.textContent = 'Run';
          button.addEventListener('click', async (event) => {
            event.stopPropagation();
            try {
              await executeTest(test, index);
            } catch (error) {
              status.textContent = error.message || '发送失败';
            }
          });
          card.appendChild(button);

          testList.appendChild(card);
        });
      };

      const loadTests = () => {
        let parsed;
        try {
          parsed = JSON.parse(catalogEditor.value);
        } catch (error) {
          throw new Error('JSON 解析失败');
        }
        const catalog = normalizeCatalog(parsed);
        currentCatalog = catalog;
        const tests = catalog.tests;
        if (tests.length === 0) {
          throw new Error('没有可执行测试项');
        }
        renderTests(tests);
        status.textContent = `已加载 ${tests.length} 个测试项`;
        if (selectedTestIndex === null) {
          selectTest(0);
        } else if (selectedTestIndex < tests.length) {
          selectTest(selectedTestIndex);
        }
      };

      const fillResultEditor = (test) => {
        const result = test.result || {};
        selectedTestName.textContent = `当前测试：${test.title || test.id || '未命名测试'}`;
        selectedTestMeta.textContent = test.goal
          ? `目标：${test.goal}`
          : (test.description || '');
        resultStatus.value = result.status || 'untested';
        resultNote.value = result.note || '';
      };

      const selectTest = (index) => {
        if (!currentCatalog || !Array.isArray(currentCatalog.tests) || index < 0 || index >= currentCatalog.tests.length) {
          return;
        }
        selectedTestIndex = index;
        fillResultEditor(currentCatalog.tests[index]);
        renderTests(currentCatalog.tests);
      };

      const saveSelectedResult = async () => {
        if (!currentCatalog || selectedTestIndex === null || !currentCatalog.tests[selectedTestIndex]) {
          throw new Error('请先选择一个测试项');
        }

        const test = currentCatalog.tests[selectedTestIndex];
        test.result = {
          status: resultStatus.value,
          note: resultNote.value.trim(),
          updated_at: new Date().toISOString(),
        };

        const savedCatalog = await persistCatalog(currentCatalog);
        renderTests(savedCatalog.tests);
        selectTest(Math.min(selectedTestIndex, savedCatalog.tests.length - 1));
      };

      const reloadSelectedResult = () => {
        if (!currentCatalog || selectedTestIndex === null || !currentCatalog.tests[selectedTestIndex]) {
          throw new Error('请先选择一个测试项');
        }
        fillResultEditor(currentCatalog.tests[selectedTestIndex]);
      };

      loadTestsButton.addEventListener('click', () => {
        try {
          loadTests();
        } catch (error) {
          status.textContent = error.message || '测试项加载失败';
        }
      });

      refreshStateButton.addEventListener('click', () => {
        refreshState().catch((error) => {
          status.textContent = error.message || '状态拉取失败';
        });
      });

      loadFileButton.addEventListener('click', async () => {
        try {
          const catalog = await fetchCatalog();
          renderTests(normalizeTests(catalog));
          status.textContent = '已从 quick-tests.json 读取测试目录';
        } catch (error) {
          status.textContent = error.message || '测试目录读取失败';
        }
      });

      saveFileButton.addEventListener('click', async () => {
        try {
          await saveCatalog();
          status.textContent = '已保存到 quick-tests.json';
        } catch (error) {
          status.textContent = error.message || '测试目录保存失败';
        }
      });

      reloadResultButton.addEventListener('click', () => {
        try {
          reloadSelectedResult();
          status.textContent = '已重新载入当前测试结果';
        } catch (error) {
          status.textContent = error.message || '结果读取失败';
        }
      });

      saveResultButton.addEventListener('click', async () => {
        try {
          await saveSelectedResult();
          status.textContent = '已保存当前测试结果到 quick-tests.json';
        } catch (error) {
          status.textContent = error.message || '结果保存失败';
        }
      });

      fetchCatalog()
        .then((catalog) => {
          renderTests(catalog.tests);
          if (catalog.tests.length > 0) {
            selectTest(0);
          }
          status.textContent = '已从 quick-tests.json 读取测试目录';
        })
        .catch((error) => {
          status.textContent = (error.message || '测试目录读取失败') + '，已保留当前编辑器内容';
          loadTests();
        });

      refreshState();
      window.setInterval(refreshState, 1500);
    </script>
  </body>
</html>
"""


def _default_quick_test_catalog() -> dict[str, Any]:
    return {
        'tests': [
            {
                'id': 'move-right',
                'title': '右移 120',
                'description': '验证显式位移是否稳定。',
                'payload': {
                    'type': 'window.move',
                    'dx': 120,
                    'dy': 0,
                },
            },
            {
                'id': 'touch-head',
                'title': '摸头动作',
                'description': '验证单独动作入口。',
                'payload': {
                    'type': 'motion.play',
                    'motion': 'touch_head',
                    'priority': 50,
                },
            },
            {
                'id': 'thinking-walk-speak',
                'title': '思考后移动并说话',
                'description': '验证 4 步 sequence。',
                'payload': {
                    'name': 'thinking-walk-speak-normal',
                    'steps': [
                        {
                            'event': {
                                'type': 'mode.switch',
                                'mode': 'thinking',
                            },
                            'wait_for': 'event_applied',
                        },
                        {
                            'event': {
                                'type': 'window.move',
                                'dx': 90,
                                'dy': -20,
                                'style': 'smart',
                            },
                            'wait_for': 'move_complete',
                            'wait_timeout_ms': 5000,
                            'settle_ms': 120,
                        },
                        {
                            'event': {
                                'type': 'bubble.show',
                                'text': '我先想一下，再边移动边回答。',
                                'duration_ms': 5000,
                                'graph': 'think',
                            },
                        },
                        {
                            'event': {
                                'type': 'mode.switch',
                                'mode': 'normal',
                            },
                        },
                    ],
                },
            },
            {
                'id': 'think-speak-move-touch-speak-recover',
                'title': '思考 -> 说话 -> 移动 -> 摸头 -> 再说话 -> 恢复',
                'description': '验证更长的 6 步 sequence，并观察重复 bubble.show 的关联字段。',
                'payload': {
                    'name': 'think-speak-move-touch-speak-recover',
                    'steps': [
                        {
                            'event': {
                                'type': 'mode.switch',
                                'mode': 'thinking',
                            },
                            'wait_for': 'event_applied',
                        },
                        {
                            'event': {
                                'type': 'bubble.show',
                                'text': '我先想一下这件事。',
                                'duration_ms': 4000,
                                'expression': 'thinking',
                                'graph': 'think',
                            },
                            'wait_for': 'event_applied',
                        },
                        {
                            'event': {
                                'type': 'window.move',
                                'dx': 80,
                                'dy': -20,
                                'style': 'smart',
                            },
                            'wait_for': 'move_complete',
                            'wait_timeout_ms': 5000,
                            'settle_ms': 120,
                        },
                        {
                            'event': {
                                'type': 'motion.play',
                                'motion': 'touch_head',
                                'priority': 55,
                            },
                            'wait_for': 'motion_complete',
                            'wait_timeout_ms': 6000,
                            'settle_ms': 120,
                        },
                        {
                            'event': {
                                'type': 'bubble.show',
                                'text': '想好了，我继续说给你听。',
                                'duration_ms': 5000,
                                'expression': 'thinking',
                                'graph': 'think',
                            },
                            'wait_for': 'event_applied',
                        },
                        {
                            'event': {
                                'type': 'mode.switch',
                                'mode': 'normal',
                            },
                        },
                    ],
                },
            },
        ],
    }


def _read_quick_test_catalog() -> dict[str, Any] | list[Any]:
    if not QUICK_TEST_CATALOG_PATH.exists():
        catalog = _default_quick_test_catalog()
        QUICK_TEST_CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        QUICK_TEST_CATALOG_PATH.write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        return catalog

    try:
        return json.loads(QUICK_TEST_CATALOG_PATH.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f'quick-tests.json 解析失败: {exc.msg}') from exc


def _write_quick_test_catalog(catalog: dict[str, Any] | list[Any]) -> dict[str, Any] | list[Any]:
    QUICK_TEST_CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUICK_TEST_CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    return catalog


@router.get('/dev/control', response_class=HTMLResponse)
async def dev_control_page() -> HTMLResponse:
    return HTMLResponse(CONTROL_PAGE_HTML)


@router.get('/dev/quick-test', response_class=HTMLResponse)
async def dev_quick_test_page() -> HTMLResponse:
    return HTMLResponse(QUICK_TEST_PAGE_HTML)


@router.get('/api/dev/quick-test/catalog')
async def get_quick_test_catalog() -> JSONResponse:
    return JSONResponse(content={'status': 'ok', 'catalog': _read_quick_test_catalog()})


@router.put('/api/dev/quick-test/catalog')
async def update_quick_test_catalog(catalog: dict[str, Any] | list[Any] = Body(...)) -> JSONResponse:
    return JSONResponse(content={'status': 'ok', 'catalog': _write_quick_test_catalog(catalog)})


@router.post('/api/dev/messages', response_model=DevEventResponse)
async def send_dev_message(
    request: DevEventRequest,
    services: AppServices = Depends(get_services),
) -> DevEventResponse:
    event = services.behavior_policy_engine.build_manual_event(request)
    await services.event_bus.publish(event)
    return DevEventResponse(status='ok', event=event)


@router.get('/api/dev/scenarios', response_model=DevScenarioListResponse)
async def list_dev_scenarios(
    services: AppServices = Depends(get_services),
) -> DevScenarioListResponse:
    return DevScenarioListResponse(status='ok', scenarios=services.dev_sequence_orchestrator.list_scenarios())


@router.post('/api/dev/scenarios/{scenario_id}', response_model=DevSequenceDispatchResponse)
async def trigger_dev_scenario(
    scenario_id: str,
    services: AppServices = Depends(get_services),
) -> DevSequenceDispatchResponse:
    return await services.dev_sequence_orchestrator.dispatch_scenario(scenario_id)


@router.post('/api/dev/sequences', response_model=DevSequenceDispatchResponse)
async def trigger_dev_sequence(
    request: DevSequenceRequest,
    services: AppServices = Depends(get_services),
) -> DevSequenceDispatchResponse:
    return await services.dev_sequence_orchestrator.dispatch_sequence(request)
